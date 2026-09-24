"""632 C2 · human 90 填充执行工具（纯标准库，默认 --dry-run）。

把「人」的裁决（data/autoimmune_human_decisions_632.jsonl）写入对应 atom 卡 frontmatter：
- 定位 `claim_structured:` 下 `  - id: prop-N` 块，设置 `object:` / `signed_by:` 字段；
- `signed_by` 走 v0.2 签名壳（`v0.2:<value>`），**不落私钥**——机器永不代签（§零.3），
  真实签名由持钥人在册者完成；
- **默认 --dry-run**：只打印 diff，不写盘；
- --apply 前必须自证 631 工具 --check 全绿（铁律 #3），否则拒绝写盘（fail-closed）。

铁律：纯标准库、新工具必有 --check、至少 5 例单测。
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
DECISIONS = REPO_ROOT / "data" / "autoimmune_human_decisions_632.jsonl"
GATE_SCRIPT = HERE / "run_631_gate.py"


def load_decisions(path: Path = DECISIONS) -> list[dict]:
    out = []
    if not Path(path).is_file():
        return out
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def _signed_by_shell(value: str) -> str:
    """signed_by 走 v0.2 壳；不落私钥（机器永不代签）。"""
    v = str(value).strip()
    return v if v.startswith("v0.2:") else f"v0.2:{v}"


def apply_decision(card_text: str, prop_id: str, field: str, value: str) -> str:
    """在 card_text 的 `claim_structured` 中定位 `- id: prop_id` 块，设置 field。"""
    lines = card_text.split("\n")
    out: list[str] = []
    i, n = 0, len(lines)
    in_block = False
    block_indent = ""
    done = False
    while i < n:
        ln = lines[i]
        m = re.match(r"^(\s*)-\s+id:\s*(\S+)\s*$", ln)
        if m:
            if in_block and not done:
                out.append(f"{block_indent}  {field}: {_value(field, value)}")
                done = True
            in_block = (m.group(2) == prop_id)
            block_indent = m.group(1)
            out.append(ln)
            i += 1
            continue
        if in_block:
            fm = re.match(rf"^(\s*){re.escape(field)}:\s*(.*)$", ln)
            if fm and len(fm.group(1)) >= 2:
                out.append(f"{fm.group(1)}{field}: {_value(field, value)}")
                done = True
                i += 1
                continue
            if ln.strip() != "" and (len(ln) - len(ln.lstrip())) < len(block_indent) + 2:
                if not done:
                    out.append(f"{block_indent}  {field}: {_value(field, value)}")
                    done = True
                in_block = False
        out.append(ln)
        i += 1
    if in_block and not done:
        out.append(f"{block_indent}  {field}: {_value(field, value)}")
    return "\n".join(out)


def _value(field: str, value: str) -> str:
    return _signed_by_shell(value) if field == "signed_by" else str(value)


def render_diff(card_rel: str, old: str, new: str) -> str:
    d = difflib.unified_diff(
        old.splitlines(), new.splitlines(),
        fromfile=f"a/{card_rel}", tofile=f"b/{card_rel}", lineterm="")
    return "\n".join(d)


def apply_decisions(decisions: list[dict], root: Path = REPO_ROOT, dry_run: bool = True) -> list[str]:
    """返回 diff 列表；dry_run=True 不写盘，False 写盘。"""
    diffs: list[str] = []
    for d in decisions:
        rel = d.get("card_rel") or f"atoms/{d.get('card_id','').lower().replace('atom-','')}"
        p = root / rel
        if not p.is_file():
            diffs.append(f"!! 跳过（卡不存在）: {rel}")
            continue
        old = p.read_text(encoding="utf-8")
        new = apply_decision(old, d.get("prop_id", ""), d.get("field", ""), d.get("value", ""))
        diffs.append(render_diff(rel, old, new))
        if not dry_run:
            p.write_text(new, encoding="utf-8")
    return diffs


def self_proof_passed() -> bool:
    """铁律 #3：--apply 前自证 631 门禁全绿。"""
    if not GATE_SCRIPT.is_file():
        print("!! 未找到 631 门禁脚本 tools/run_631_gate.py，拒绝 --apply（fail-closed）")
        return False
    r = subprocess.run([sys.executable, str(GATE_SCRIPT)], capture_output=True, text=True)
    if r.returncode != 0:
        print("!! 631 门禁未全绿，拒绝 --apply：")
        print(r.stdout[-800:] + r.stderr[-800:])
        return False
    return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="632 C2 human 90 填充执行（默认 dry-run）")
    ap.add_argument("--check", action="store_true", help="只读：打印决策数与样例，exit 0")
    ap.add_argument("--dry-run", action="store_true", help="只打印 diff，不写盘（默认）")
    ap.add_argument("--apply", action="store_true", help="写盘；须先自证 631 门禁全绿")
    ap.add_argument("--decisions", default=str(DECISIONS))
    args = ap.parse_args(argv)
    decisions = load_decisions(args.decisions)
    if args.check:
        print(f"632 C2 --check OK：待执行决策 {len(decisions)} 条")
        for d in decisions[:3]:
            print(f"  样例 {d.get('card_rel')} {d.get('prop_id')} "
                  f"[{d.get('field')}] = {d.get('value')}")
        return 0
    if args.apply:
        if not self_proof_passed():
            return 1
        diffs = apply_decisions(decisions, dry_run=False)
        print(f"已应用 {len(decisions)} 条决策（已自证 631 门禁全绿）")
        for dd in diffs[:3]:
            print(dd)
        return 0
    # 默认 dry-run
    diffs = apply_decisions(decisions, dry_run=True)
    print(f"[dry-run] 以下 {len(decisions)} 条决策将写入（--apply 才落盘，且须自证 631 门禁全绿）：")
    for dd in diffs:
        print(dd)
        print("-" * 40)
    return 0


if __name__ == "__main__":
    sys.exit(main())
