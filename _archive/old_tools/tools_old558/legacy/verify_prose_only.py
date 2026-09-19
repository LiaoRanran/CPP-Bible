#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P0-15 安全网：逐文件比对 HEAD 与工作区所有「正常」代码围栏是否逐字节一致。

设计前提：本波次是「纯 prose 插入」，只在章内新增一个 ## ㉒ 段（仅 prose + 引用 bullet），
绝不允许改动任何 ```...``` 围栏。此脚本提取每个 ch*.md 的围栏序列（有序），
比对 HEAD 版与当前工作区版的「正常围栏」（lang + 内容）是否完全相同。

对「畸形围栏」（内容以 markdown 标题 `#{1,6} ` 开头，通常是前序未闭合 ``` 造成的配对错位）
做容错：HEAD 与 WORK 各自剔除畸形围栏后再比对。这类围栏是仓库既有问题，
插入 prose 只会平移其被吞掉的文本，不会改动真实代码，故不判为违规（仅作 WARNING 提示）。
任何「正常围栏」内容不一致 = 触犯红线，报错退出（exit 1）。

用法：
  python tools/verify_prose_only.py
  python tools/verify_prose_only.py --json out.json
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOOK = REPO / "Book"

FENCE_RE = re.compile(r"```([^\n`]*)\n(.*?)```", re.DOTALL)
HEADING_RE = re.compile(r"(?m)^#{1,6} ")


def fences_of(text: str):
    """返回有序围栏列表 [(lang, content), ...]，content 去掉末尾换行统一。"""
    out = []
    for m in FENCE_RE.finditer(text):
        lang = m.group(1).strip()
        content = m.group(2).replace("\r\n", "\n").rstrip("\n")
        out.append((lang, content))
    return out


def is_malformed(fence):
    """畸形围栏：内容以 markdown 标题开头（前序未闭合 ``` 造成的配对错位）。"""
    lang, content = fence
    stripped = content.lstrip()
    return bool(HEADING_RE.match(stripped))


def read_head(path: Path) -> str:
    rel = path.relative_to(REPO).as_posix()
    try:
        return subprocess.run(
            ["git", "show", f"HEAD:{rel}"],
            cwd=REPO, capture_output=True, text=True, check=True,
        ).stdout
    except subprocess.CalledProcessError:
        return ""  # 未跟踪（不应发生）


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="输出 JSON 报告路径")
    args = ap.parse_args()

    files = sorted(BOOK.rglob("ch*.md"))
    problems = []
    warnings = []
    checked = 0
    for f in files:
        head_text = read_head(f)
        if head_text is None:
            continue
        work_text = f.read_text(encoding="utf-8")
        checked += 1

        h_all = fences_of(head_text)
        w_all = fences_of(work_text)
        h_clean = [x for x in h_all if not is_malformed(x)]
        w_clean = [x for x in w_all if not is_malformed(x)]

        h_mal = len(h_all) - len(h_clean)
        w_mal = len(w_all) - len(w_clean)
        if h_mal or w_mal:
            warnings.append({
                "file": str(f.relative_to(REPO)),
                "head_malformed": h_mal,
                "work_malformed": w_mal,
            })

        if h_clean != w_clean:
            info = {
                "file": str(f.relative_to(REPO)),
                "head_clean": len(h_clean),
                "work_clean": len(w_clean),
            }
            for i, (a, b) in enumerate(zip(h_clean, w_clean)):
                if a != b:
                    info["first_diff_index"] = i
                    info["head_lang"] = a[0]
                    info["work_lang"] = b[0]
                    info["head_head"] = a[1][:80]
                    info["work_head"] = b[1][:80]
                    break
            problems.append(info)

    if args.json:
        Path(args.json).write_text(
            json.dumps({"checked": checked, "problems": problems,
                        "warnings": warnings}, ensure_ascii=False, indent=2),
            encoding="utf-8", newline="\n")

    print(f"[verify_prose_only] checked={checked} problems={len(problems)} "
          f"malformed-fence-warnings={len(warnings)}")
    for w in warnings:
        print(f"  WARN(malformed fence, pre-existing): {w['file']} "
              f"head_mal={w['head_malformed']} work_mal={w['work_malformed']}")
    if problems:
        for p in problems:
            print(f"  REDLINE VIOLATION: {p['file']} "
                  f"(head_clean={p.get('head_clean')} work_clean={p.get('work_clean')} "
                  f"first_diff={p.get('first_diff_index')})")
        sys.exit(1)
    print("OK: 所有正常代码围栏与 HEAD 逐字节一致（纯 prose 插入合规）")
    sys.exit(0)


if __name__ == "__main__":
    main()
