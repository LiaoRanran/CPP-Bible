#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
align_part01.py — 将 part01 历史章节对齐到 v3 约定（机械部分）：
  1. 立场分层标签规范化：[平台·Itanium ABI] -> [平台]；[实现·CFront] -> [实现] 等。
  2. 末尾「## 附录...」提升为 ⑳ 练习题+思考题+源码阅读路线（内化，无独立"推荐阅读"节）。
  3. 不改动任何史实正文，仅调整标题与标签格式。
用法：
  python tools/align_part01.py --root <CPP-Bible> --apply
"""
import argparse, re, pathlib, shutil

LABELS = ['标准', '实现', '平台', '经验']

def fix_stance(text: str) -> str:
    for lb in LABELS:
        # [平台·Itanium ABI] / [实现：CFront] / [经验:x] -> [平台] / [实现] ...
        text = re.sub(r'\[' + lb + r'[·：:][^\]]*\]', '[' + lb + ']', text)
    return text

def align_file(path: pathlib.Path, apply: bool):
    lines = path.read_text(encoding='utf-8').splitlines()
    out = []
    promoted = 0
    for ln in lines:
        # 立场标签规范化（整行文本）
        new = fix_stance(ln)
        # 末尾附录提升为 ⑳
        m = re.match(r'^##\s*附录.*$', new)
        if m:
            new = '## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立"推荐阅读"节）'
            promoted += 1
        out.append(new)
    if apply:
        bak = path.with_suffix(path.suffix + '.bak')
        if not bak.exists():
            shutil.copy2(path, bak)
        path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    return promoted

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    files = sorted(root.glob('Book/part01_history/ch*.md'))
    total = 0
    for p in files:
        n = align_file(p, apply=args.apply)
        total += n
        print(f"  {p.name}: 提升附录->{n and '⑳' or '—'}")
    print("MODE:", "APPLY" if args.apply else "DRY-RUN", "| promoted:", total)

if __name__ == '__main__':
    main()
