#!/usr/bin/env python3
"""mermaid_lint.py - zero-dependency mermaid syntax linter for the CPP-Bible book.

Goals
-----
1. Extract every ```mermaid fence from Book/**/*.md (backtick-count aware, so
   4-backtick separators in prose never fool the parser).
2. Validate each block against a self-contained, type-aware rule set covering
   the diagram kinds actually used in this book:
     flowchart / graph, classDiagram, sequenceDiagram, stateDiagram(-v2), timeline.
3. Emit a JSON report (per-block PASS/FAIL + line-numbered reasons) and exit
   non-zero if any block fails — suitable as a CI quality gate.

This linter is intentionally dependency-free (pure Python) so it runs in CI
without Node/mermaid. It was bootstrapped against the real `mermaid.parse()`
output (run locally via tools/_mermaid_groundtruth.mjs) so the rule tables
target the actual error classes present in the corpus.

Usage
-----
    python tools/mermaid_lint.py                 # lint Book/, print summary
    python tools/mermaid_lint.py --json rep.json # also write JSON
    python tools/mermaid_lint.py --check         # exit 1 if any FAIL
    python tools/mermaid_lint.py --root path     # override scan root
"""
import argparse
import json
import os
import re
import sys

# --------------------------------------------------------------------------
# Fence extraction (backtick-count aware)
# --------------------------------------------------------------------------
FENCE_RE = re.compile(r'^(?P<indent> *)(?P<ticks>`{3,})(?P<info>.*)$')

OPEN_INFO_OK = ("mermaid",)  # info string must start with this


def extract_blocks(root):
    """Yield dicts: {rel, abs, open_line, close_line, type, body, lines}."""
    blocks = []
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, os.path.dirname(root.rstrip("/"))).replace("\\", "/")
            # rel is relative to the parent of root; normalize to Book/...
            try:
                with open(full, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except OSError:
                continue
            lines = text.splitlines(keepends=False)
            # find opens
            i = 0
            n = len(lines)
            while i < n:
                m = FENCE_RE.match(lines[i])
                if m and m.group("info").strip().split()[0:1] and \
                        m.group("info").strip().split()[0] == "mermaid":
                    ticks = len(m.group("ticks"))
                    # search matching close: same tick count, no info
                    j = i + 1
                    close = None
                    while j < n:
                        cm = FENCE_RE.match(lines[j])
                        if cm and len(cm.group("ticks")) == ticks and cm.group("info").strip() == "":
                            close = j
                            break
                        j += 1
                    if close is None:
                        blocks.append({
                            "rel": rel, "abs": full, "open_line": i + 1,
                            "close_line": None, "type": "UNKNOWN",
                            "body": "\n".join(lines[i + 1:]),
                            "lines": lines[i + 1:], "unclosed": True,
                        })
                        break
                    body = lines[i + 1:close]
                    blocks.append({
                        "rel": rel, "abs": full, "open_line": i + 1,
                        "close_line": close + 1,
                        "type": detect_type(body), "body": "\n".join(body),
                        "lines": body, "unclosed": False,
                    })
                    i = close + 1
                    continue
                i += 1
    return blocks


def detect_type(lines):
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("%%") or s.startswith("//"):
            continue
        if re.match(r"^(flowchart|graph)\b", s, re.I):
            return "flowchart"
        if re.match(r"^classDiagram\b", s, re.I):
            return "classDiagram"
        if re.match(r"^sequenceDiagram\b", s, re.I):
            return "sequenceDiagram"
        if re.match(r"^stateDiagram(-v2)?\b", s, re.I):
            return "stateDiagram"
        if re.match(r"^timeline\b", s, re.I):
            return "timeline"
        # first meaningful token
        return "UNKNOWN:" + (s.split()[0] if s.split() else "?")
    return "EMPTY"


# --------------------------------------------------------------------------
# Rule helpers
# --------------------------------------------------------------------------
ARROW_TOKENS = (
    "-->", "---", "==>", "->>", "--x", "--o", "-.->", "-.->>",
    "==>",  # alias
)
# valid flowchart arrow cores (between nodes)
FLOWCHART_ARROW = re.compile(
    r"(-->|---|==>|->>|--x|--o|-\.->|-\.->>|==\||-\.|\.->)")
SEQUENCE_ARROW = re.compile(r"(->>|->|-->|-\.->|==>|=>)")


def strip_label(line):
    """Remove trailing comments (%% ...) for analysis."""
    # mermaid supports %% comments
    return re.sub(r"%%.*$", "", line).rstrip()


# --------------------------------------------------------------------------
# Per-type validators: append (lineno, code, msg) into errors
# --------------------------------------------------------------------------
def check_flowchart(lines, errors):
    header_ok = False
    subgraph_stack = []
    in_classdef = False
    for idx, raw in enumerate(lines, start=1):
        line = strip_label(raw)
        s = line.strip()
        if not s:
            continue
        if s.startswith("%%") or s.startswith("//"):
            continue
        # direction header
        if re.match(r"^(flowchart|graph)\b", s, re.I):
            if not re.match(r"^(flowchart|graph)\s+(TB|TD|BT|LR|RL|NW|NE|SW|SE)\b", s, re.I):
                errors.append((idx, "FLOW_HEADER",
                               f"invalid flowchart/graph header: {s!r} "
                               f"(need a direction token TB/TD/BT/LR/RL)"))
            else:
                header_ok = True
            # also check trailing junk like 'flowchart TD A-->B' (header must be its own line)
            rest = re.sub(r"^(flowchart|graph)\s+\w+\s*", "", s, flags=re.I).strip()
            if rest:
                errors.append((idx, "FLOW_HEADER_INLINE",
                               f"graph header line carries extra content {rest!r}; "
                               f"put edges on their own lines"))
            continue
        # subgraph
        if re.match(r"^subgraph\b", s, re.I):
            if re.match(r"^subgraph\s+\w+\s*\[.*\]$", s) or \
               re.match(r"^subgraph\s+\w+\s*$", s) or \
               re.match(r"^subgraph\s+\[.*\]$", s):
                subgraph_stack.append(idx)
            else:
                errors.append((idx, "SUBGRAPH_SYNTAX",
                               f"subgraph header malformed: {s!r} "
                               f"(use `subgraph id [label]` or `subgraph [label]`)"))
                subgraph_stack.append(idx)
            continue
        if s == "end":
            if subgraph_stack:
                subgraph_stack.pop()
            else:
                errors.append((idx, "END_ORPHAN", "stray `end` with no open subgraph"))
            continue
        # classDef / class / style / click / linkStyle / direction
        if re.match(r"^(classDef|class\s|style\s|click\s|linkStyle|direction|default\s)", s, re.I):
            continue
        # relation/edge line: contains an arrow somewhere
        if FLOWCHART_ARROW.search(s):
            # rough balance check on brackets used in node labels
            _check_bracket_balance(idx, s, errors)
            # require a target node after the arrow (catches B-->, B--> dangling)
            m = FLOWCHART_ARROW.search(s)
            after = s[m.end():]
            after_clean = re.sub(r'\|[^|]*\|', '', after)        # drop inline labels
            after_clean = re.sub(r'\s+(class|style)\s+\S+.*$', '', after_clean)
            after_clean = re.sub(r'^[\s>\-]+$', '', after_clean.strip())  # drop dangling arrow residue
            if after_clean == '':
                errors.append((idx, "EDGE_NO_TARGET", "edge arrow has no target node"))
            continue
        # node declaration line: `A[..]` or `A(..)` or `A{..}` possibly with &
        if re.match(r"^[\w]+\s*([\[\(\{].*[\]\)\}])?\s*(&\s*[\w]+\s*[\[\(\{].*[\]\)\}])*\s*$", s) and \
                not s.startswith(("note", "click", "style", "class", "subgraph")):
            _check_bracket_balance(idx, s, errors)
            continue
        # lines beginning with & (continuation)
        if s.startswith("&"):
            continue
        # note blocks
        if s.startswith("note") or s.startswith(":::"):
            continue
        # otherwise: suspicious line that is neither edge nor node decl
        errors.append((idx, "FLOW_UNPARSED",
                       f"line not recognized as valid flowchart statement: {s!r}"))
    if subgraph_stack:
        for o in subgraph_stack:
            errors.append((o, "SUBGRAPH_UNCLOSED", "subgraph opened here has no matching `end`"))


def _check_bracket_balance(idx, s, errors):
    # Only node-shape brackets [ ] ( ) { } matter. C++ template angles < > are
    # legitimate label text (e.g. pair<key,value>) and must NOT be balanced.
    pairs = {']': '[', ')': '(', '}': '{'}
    opens = []
    in_str = False
    for ch in s:
        if ch in "\"'" and not in_str:
            in_str = ch
        elif ch == in_str:
            in_str = False
        elif in_str:
            continue
        elif ch in "[({":
            opens.append(ch)
        elif ch in pairs:
            if not opens or opens[-1] != pairs[ch]:
                errors.append((idx, "BRACKET_MISMATCH",
                               f"unbalanced bracket near {ch!r} in: {s!r}"))
                return
            opens.pop()
    if opens:
        errors.append((idx, "BRACKET_UNCLOSED",
                       f"unclosed bracket(s) {opens} in: {s!r}"))


def check_classdiagram(lines, errors):
    for idx, raw in enumerate(lines, start=1):
        line = strip_label(raw)
        s = line.strip()
        if not s or s.startswith("%%"):
            continue
        if re.match(r"^classDiagram\b", s, re.I):
            continue
        # directives
        if re.match(r"^(direction|class\s|relation\s|hide|show|namespace|title|note\s|style\s|link\s|callback\s)", s, re.I):
            continue
        # class / abstract class / class Name { ... } or class Name
        if re.match(r"^(class|abstract\s+class|interface|enum|annotation)\b", s):
            # either `class A` or `class A {` ... tracked by brace? keep simple
            if not re.match(r"^(class|abstract\s+class|interface|enum|annotation)\s+\w+(\s*<\s*[\w,\s]+\s*>)?\s*(\{)?\s*$", s):
                errors.append((idx, "CLASS_DECL", f"class declaration malformed: {s!r}"))
            continue
        # relation: A <|-- B, A *-- B, A o-- B, A --> B, A ..> B, A -- B, etc.
        RELOP = re.compile(r"(<\|\-\-|\-\->|\*\-\-|o\-\-|\.\.>|==>|\-\-|\.\.|<\||x\-\-|o\.\.|<\.\-|-\.-)")
        if RELOP.search(s) and re.search(r"\w", s):
            m = RELOP.search(s)
            lhs = s[:m.start()].strip()
            rhs = s[m.end():].strip()
            rhs = re.sub(r'^:\s*.*$', '', rhs).strip()              # drop trailing : label
            rhs = re.sub(r'\s+(class|style)\s+\S+.*$', '', rhs).strip()
            if not lhs:
                errors.append((idx, "RELATION_NO_LHS", f"relation missing left endpoint: {s!r}"))
            elif not rhs:
                errors.append((idx, "RELATION_NO_RHS", f"relation missing right endpoint: {s!r}"))
            continue
        # member lines inside a class body: visibility-prefixed, type name,
        # name : desc, method()/field[], or CJK member text.
        if (re.match(r"^[\+\-\#\~]", s)
                or re.match(r"^<<.*>>$", s)
                or re.match(r"^[A-Za-z_]\w*(\s*<[^>]*>)?\s+\w+\s*[;=]?$", s)
                or re.match(r"^[A-Za-z_]\w*\s*:\s*.+$", s)
                or re.match(r"^[A-Za-z_]\w*\s*[\(\[]", s)
                or re.match(r"^[一-鿿]", s)
                or re.match(r"^[A-Za-z_一-鿿]", s)
                or s in ("}",)):
            continue
        errors.append((idx, "CLASS_UNPARSED", f"line not recognized as classDiagram syntax: {s!r}"))


def check_sequence(lines, errors):
    block_stack = []
    for idx, raw in enumerate(lines, start=1):
        line = strip_label(raw)
        s = line.strip()
        if not s or s.startswith("%%"):
            continue
        if re.match(r"^sequenceDiagram\b", s, re.I):
            continue
        if re.match(r"^(participant|actor|box|title|autonumber|Note\s|legend|end|opt|alt|else|loop|par|break|critical|group|rect|activate|deactivate|create|destroy|return)\b", s, re.I):
            kw = re.match(r"^(opt|alt|else|loop|par|break|critical|group|box|rect)\b", s, re.I)
            if kw and re.match(r"^(opt|alt|else|loop|par|break|critical|group)\b", s, re.I):
                block_stack.append((kw.group(1), idx))
            elif s == "end":
                if block_stack:
                    block_stack.pop()
                else:
                    errors.append((idx, "SEQ_END_ORPHAN", "stray `end`"))
            continue
        # message line: A->>B: label  or A->B
        if SEQUENCE_ARROW.search(s):
            if not re.match(r"^[\w\s\.\-]+\s*(->>|->|-->|-\.->|==>|=>)\s*[\w\s\.\-]+(:.*)?$", s):
                errors.append((idx, "SEQ_MSG", f"message line malformed: {s!r}"))
            continue
        errors.append((idx, "SEQ_UNPARSED", f"line not recognized as sequenceDiagram syntax: {s!r}"))
    if block_stack:
        for kw, o in block_stack:
            errors.append((o, "SEQ_BLOCK_UNCLOSED", f"`{kw}` block not closed with `end`"))


def check_state(lines, errors):
    for idx, raw in enumerate(lines, start=1):
        line = strip_label(raw)
        s = line.strip()
        if not s or s.startswith("%%"):
            continue
        if re.match(r"^stateDiagram(-v2)?\b", s, re.I):
            continue
        # valid stateDiagram line forms:
        if re.match(r"^\[\*\]\s*$", s):                       # initial pseudo-state alone
            continue
        if re.match(r"^\[\*\]\s*-->\s*.+$", s):               # initial transition
            _check_bracket_balance(idx, s, errors)
            continue
        if re.match(r".+\s*-->\s*\[\*\](\s*:.*)?\s*$", s):    # final transition (opt label)
            _check_bracket_balance(idx, s, errors)
            continue
        if re.match(r"^(state|note|title|direction|classDef|class\s|style\s)\b", s, re.I):
            continue
        if re.match(r"^\w+\s*(:.*)?$", s):                   # "StateName" or "StateName : desc"
            continue
        if re.match(r"^\w+\s*-->\s*\w+(\s*:.*)?$", s):       # transition with optional label
            _check_bracket_balance(idx, s, errors)
            continue
        errors.append((idx, "STATE_UNPARSED", f"line not recognized as stateDiagram syntax: {s!r}"))


def check_timeline(lines, errors):
    seen_section = False
    for idx, raw in enumerate(lines, start=1):
        line = strip_label(raw)
        s = line.strip()
        if not s or s.startswith("%%"):
            continue
        if re.match(r"^timeline\b", s, re.I):
            continue
        if re.match(r"^title\b", s, re.I):
            continue
        if re.match(r"^section\b", s, re.I):
            seen_section = True
            continue
        # entry:  "label : text" or "label : event1 : event2"
        if re.match(r"^[^:]+:.*$", s):
            continue
        errors.append((idx, "TIMELINE_UNPARSED", f"timeline entry malformed (need `topic : event`): {s!r}"))


VALIDATORS = {
    "flowchart": check_flowchart,
    "classDiagram": check_classdiagram,
    "sequenceDiagram": check_sequence,
    "stateDiagram": check_state,
    "timeline": check_timeline,
}


def lint_block(block):
    errors = []
    if block.get("unclosed"):
        errors.append((block["open_line"], "UNCLOSED_FENCE",
                       "mermaid fence opened but never closed"))
        return errors
    if block["type"] == "EMPTY" or block["type"].startswith("EMPTY"):
        errors.append((block["open_line"], "EMPTY_BLOCK", "empty mermaid block"))
        return errors
    fn = VALIDATORS.get(block["type"])
    if fn is None:
        errors.append((block["open_line"], "TYPE_UNKNOWN",
                       f"diagram type not supported by linter: {block['type']!r}"))
        return errors
    fn(block["lines"], errors)
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="scan root (default: <repo>/Book)")
    ap.add_argument("--json", default=None, help="write JSON report here")
    ap.add_argument("--check", action="store_true", help="exit 1 if any FAIL")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    root = args.root or os.path.join(repo, "Book")
    if not os.path.isdir(root):
        print(f"ERROR: root not a dir: {root}", file=sys.stderr)
        sys.exit(2)

    blocks = extract_blocks(root)
    results = []
    fail = 0
    by_type = {}
    for b in blocks:
        errs = lint_block(b)
        ok = len(errs) == 0
        if not ok:
            fail += 1
        by_type[b["type"]] = by_type.get(b["type"], 0) + 1
        results.append({
            "rel": b["rel"], "open_line": b["open_line"],
            "type": b["type"], "ok": ok,
            "errors": [{"line": ln, "code": c, "msg": m} for (ln, c, m) in errs],
        })

    report = {
        "total": len(blocks),
        "failed": fail,
        "passed": len(blocks) - fail,
        "by_type": dict(sorted(by_type.items(), key=lambda x: -x[1])),
        "blocks": results,
    }
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    # console summary
    print(f"mermaid blocks: {len(blocks)} | passed: {len(blocks)-fail} | failed: {fail}")
    print("by type:", json.dumps(report["by_type"], ensure_ascii=False))
    for r in results:
        if not r["ok"]:
            print(f"  FAIL {r['rel']}:{r['open_line']} [{r['type']}]")
            for e in r["errors"]:
                print(f"      L{e['line']} {e['code']}: {e['msg']}")
    if args.check and fail:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
