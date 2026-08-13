#!/usr/bin/env python3
"""C2: Mermaid 图表审计。

两级校验：
  A. 静态结构校验（无浏览器，快）：
     - 首行须是合法图表类型（flowchart/graph/classDiagram/sequenceDiagram/
       stateDiagram[-v2]/erDiagram/timeline/gantt/pie/mindmap/journey...）
     - 方括号 []、圆括号 ()、花括号 {}、竖线 || 成对
     - 双引号 " 成对
     - flowchart/graph 至少含一条边（-->, ---, -.->, ==>）
  B. 真实渲染校验（可选，--render）：调用 mmdc 逐块渲染为 svg，
     捕获 mermaid 解析器的真实报错。

用法：
  python tools/mermaid_audit.py            # 仅静态校验
  python tools/mermaid_audit.py --render    # 追加 mmdc 真实渲染

退出码：0 = 全通过；非 0 = 有块失败。
"""
from __future__ import annotations
import re
import sys
import subprocess
import tempfile
from pathlib import Path

# Windows 控制台默认 GBK，打印 ✅/❌ 等非 GBK 字符会抛 UnicodeEncodeError 致进程异常退出。
# 统一把 stdout 设为 utf-8（Linux 上本就是 utf-8，属幂等）；encoding 失败则降级不致命。
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
except Exception:  # noqa
    pass  # 安全忽略: stdout 编码重配置不可用则忽略(仅影响显示)

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "Book"
MMDC = "C:/Users/ASUS/AppData/Roaming/npm/mmdc.cmd"

VALID_HEADERS = (
    "flowchart", "graph", "classDiagram", "sequenceDiagram",
    "stateDiagram-v2", "stateDiagram", "erDiagram", "timeline",
    "gantt", "pie", "mindmap", "journey", "quadrantChart",
    "xychart-beta", "gitGraph", "requirementDiagram", "C4Context",
)

BLOCK_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)


def extract_blocks():
    blocks = []
    for md in sorted(BOOK.rglob("ch*.md")):
        if "_legacy" in str(md):
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for i, m in enumerate(BLOCK_RE.finditer(text)):
            body = m.group(1)
            line_no = text[: m.start()].count("\n") + 1
            blocks.append({
                "file": str(md.relative_to(ROOT)),
                "idx": i,
                "line": line_no,
                "body": body,
            })
    return blocks


def _strip_directive(body: str) -> str:
    """剥离 mermaid 指令块：首行 '---' 与闭合 '---' 之间为 theme:/classDef 等配置，
    属合法 mermaid 语法，不应当作『非法图表类型首行』。"""
    lines = body.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i + 1:])
    return body


def _strip_quotes(s: str) -> str:
    """去掉双引号字符串内部内容，使节点标签里的字面括号/引号不参与配对统计。"""
    return re.sub(r'"[^"]*"', '""', s)


def static_check(b) -> list[str]:
    errs = []
    body = b["body"]
    diag = _strip_directive(body)          # 忽略合法指令块（--- theme/classDef ---）
    lines = [ln for ln in diag.splitlines() if ln.strip()]
    if not lines:
        return ["空 mermaid 块（指令块后无图表体）"]
    header = lines[0].strip()
    if not any(header.startswith(h) for h in VALID_HEADERS):
        errs.append(f"非法图表类型首行: '{header[:40]}'")
    # 括号/引号配对：先剥离引号内字面文本，避免 A["[x]"] 等合法标签被误判
    bare = _strip_quotes(diag)
    for op, cl, name in [("[", "]", "方括号"), ("(", ")", "圆括号"),
                          ("{", "}", "花括号")]:
        if bare.count(op) != bare.count(cl):
            errs.append(f"{name}不配对: {op}={bare.count(op)} {cl}={bare.count(cl)}")
    if diag.count('"') % 2 != 0:
        errs.append(f'双引号不成对: 共 {diag.count(chr(34))} 个')
    # flowchart/graph 至少一条边
    if header.startswith(("flowchart", "graph")):
        if not re.search(r"--+>|--+|-\.->|==+>|-\.-", diag):
            errs.append("flowchart/graph 无任何连线（边）")
    return errs


def render_check(b) -> str | None:
    """用 mmdc 真实渲染，返回错误文本或 None。"""
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "d.mmd"
        out = Path(td) / "d.svg"
        src.write_text(b["body"], encoding="utf-8")
        try:
            r = subprocess.run(
                [MMDC, "-i", str(src), "-o", str(out), "-q"],
                capture_output=True, text=True, timeout=120,
                encoding="utf-8", errors="replace",
            )
        except subprocess.TimeoutExpired:
            return "渲染超时(>120s)"
        except FileNotFoundError:
            return "MMDC_NOT_FOUND"
        if r.returncode != 0 or not out.exists():
            msg = (r.stderr or r.stdout or "").strip().splitlines()
            tail = " / ".join(msg[-3:]) if msg else f"exit={r.returncode}"
            return tail[:300]
    return None


def parse_check_node() -> tuple[int, str]:
    """调用 tools/mermaid_parse_check.mjs 用 mermaid 官方 parser 真实解析。
    返回 (exit_code, 输出尾部)。"""
    node = "C:/Users/ASUS/.workbuddy/binaries/node/versions/22.22.2/node.exe"
    script = ROOT / "tools" / "mermaid_parse_check.mjs"
    try:
        r = subprocess.run([node, str(script)], capture_output=True,
                           text=True, timeout=300, cwd=str(ROOT),
                           encoding="utf-8", errors="replace")
    except Exception as e:  # noqa
        return 2, f"调用失败: {e}"
    out = (r.stdout + r.stderr).strip()
    return r.returncode, out


def main() -> int:
    do_render = "--render" in sys.argv
    do_parse = "--parse" in sys.argv
    blocks = extract_blocks()
    mode = "仅静态结构校验"
    if do_parse:
        mode = "静态 + mermaid.parse 官方解析"
    elif do_render:
        mode = "静态 + mmdc 真实渲染"
    print("=" * 64)
    print(f"C2 Mermaid 审计：{len(blocks)} 个图块，来自 "
          f"{len({b['file'] for b in blocks})} 个文件")
    print(f"模式：{mode}")
    print("=" * 64)

    fails = []
    # 静态
    for b in blocks:
        errs = static_check(b)
        if errs:
            fails.append((b, "STATIC", errs))

    if do_render:
        mmdc_missing = False
        n = len(blocks)
        for j, b in enumerate(blocks, 1):
            print(f"\r  渲染 {j}/{n} ...", end="", flush=True)
            err = render_check(b)
            if err == "MMDC_NOT_FOUND":
                mmdc_missing = True
                break
            if err:
                fails.append((b, "RENDER", [err]))
        print()
        if mmdc_missing:
            print("⚠️  未找到 mmdc，跳过渲染校验（静态结果仍有效）")

    # mermaid.parse 官方解析
    parse_rc = 0
    if do_parse:
        parse_rc, parse_out = parse_check_node()
        tail = parse_out.splitlines()[-1] if parse_out else ""
        print(f"\n[mermaid.parse] {tail}")
        if parse_rc != 0:
            for ln in parse_out.splitlines():
                s = ln.strip()
                if s.startswith("x "):
                    # mjs 输出格式：x <相对路径>:<行号>  <错误信息>
                    rest = s[2:].strip()
                    if ":" in rest:
                        loc, msg = rest.split(":", 1)
                        fails.append(({"file": loc.strip(), "line": 0, "idx": 0},
                                      "PARSE", [msg.strip()]))
                    else:
                        fails.append(({"file": "", "line": 0, "idx": 0},
                                      "PARSE", [rest]))

    if not fails and parse_rc == 0:
        suffix = "静态校验"
        if do_parse:
            suffix = "静态 + mermaid.parse 官方解析"
        elif do_render:
            suffix = "（含真实渲染）"
        print(f"\n✅ 全部 {len(blocks)} 个 Mermaid 图块通过{suffix}。")
        return 0

    print(f"\n❌ {len(fails)} 个图块有问题：")
    for b, kind, errs in fails:
        print(f"  [{kind}] {b['file']}:{b['line']} (第{b['idx']+1}块)")
        for e in errs:
            print(f"        - {e}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
