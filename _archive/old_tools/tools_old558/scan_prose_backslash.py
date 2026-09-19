# 扫描 Book/ 散文中（代码块外、行内代码外）的反斜杠转义序列。
# 这类序列进入 pandoc→xelatex 管线会变成 Undefined control sequence。
# 用法: python tools/scan_prose_backslash.py [--fix]
#   无参数: 仅报告
#   --fix  : 把含转义序列的文本片段改为行内代码（保守：只处理整段中文引号内/行内的代码片段）
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = ROOT / "Book"

# 常见 C 转义序列（LaTeX 中不存在的命令）
ESC = r"\\[ntr0abefv'\"\\]"

def strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)

def scan():
    hits = []
    for fp in BOOK.rglob("*.md"):
        if "_legacy" in fp.parts:
            continue
        text = fp.read_text(encoding="utf-8")
        lines = text.split("\n")
        in_fence = False
        for i, line in enumerate(lines, 1):
            stripped = line.lstrip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            # 跳过表格分隔行、HTML 注释
            if stripped.startswith("<!--") or stripped.startswith("|"):
                pass  # 仍检查，但表格里的代码也常出问题
            visible = strip_inline_code(line)
            for m in re.finditer(ESC, visible):
                hits.append((fp.relative_to(ROOT), i, line.strip()))
                break
    return hits

if __name__ == "__main__":
    hits = scan()
    for rel, ln, line in hits:
        print(f"{rel}:{ln}: {line[:120]}")
    print(f"\n共 {len(hits)} 处散文转义序列")
    sys.exit(1 if hits else 0)
