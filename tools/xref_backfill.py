#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
xref_backfill.py — 交叉引用回填生成器 (Phase 2 / Xref)

对交叉引用不足的章，注入「## 相关章节（交叉引用）」小节，
链接来源按优先级取（均指向真实存在的章，去重）：
  1. DAG 前置依赖 deps[T]      -> 标签「前置基础」
  2. DAG 后续依赖 preds[T]      -> 标签「后续依赖」
  3. 编号相邻章 T±1 / T±2       -> 标签「相邻主题」
  4. 同 part 兄弟章             -> 标签「同模块」
每条链接附一句话诚实理由（关系由 DAG/编号决定，非注水）。

链接格式：`` `Book/partXX/chYY.md` ``（机器可检，crossref_audit 计数）。
插入位置：章末「## 自测练习」之前；若该小节已存在或引用已≥阈值则跳过（幂等，不注水）。

用法：
  python tools/xref_backfill.py --all          # 全部章（自动跳过已达标）
  python tools/xref_backfill.py Book/partXX/chYY.md [..]   # 指定章
  python tools/xref_backfill.py --list-low      # 列出引用<3的章
"""
import re
import os
import sys
import json
import shutil
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "Book"
LP = ROOT / "tools" / "learning_path.json"

CROSSREF_RE = re.compile(r"(?:⟶\s*|→\s*)(Book/[^\s\)\]>。，；：、）(（]+)")
FILE_LINK_RE = re.compile(r"`?(Book/[A-Za-z0-9_/.\-]+\.md)`?")
SEC_HDR = "## 相关章节（交叉引用）"
EXERCISE_HDR = "## 自测练习（Exercises）"
THRESHOLD = 3


def load_dag():
    d = json.load(open(LP, encoding="utf-8"))
    edges = d["edges"]
    deps, preds = {}, {}
    for e in edges:
        deps.setdefault(e["from"], []).append(e["to"])
        preds.setdefault(e["to"], []).append(e["from"])
    return deps, preds


def chapter_meta():
    """返回 {num: {path, title}}，num 为 2 位字符串。"""
    meta = {}
    for part in sorted(BOOK.iterdir()):
        if not part.is_dir():
            continue
        for ch in sorted(part.glob("ch*.md")):
            m = re.match(r"ch(\d+)_", ch.name)
            if not m:
                continue
            num = f"{int(m.group(1)):02d}"
            title = ""
            for line in ch.read_text(encoding="utf-8").splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    break
            meta[num] = {"path": ch, "title": title, "part": part.name}
    return meta


def count_refs(text):
    refs = set(FILE_LINK_RE.findall(text)) | set(CROSSREF_RE.findall(text))
    real = [r.strip("`").replace("\\", "/") for r in refs
            if re.search(r"ch\d+_", r) and (ROOT / r.strip("`").replace("\\", "/")).exists()]
    return real


def rel_path(p):
    return p.relative_to(ROOT).as_posix()


def build_section(target_num, meta, deps, preds, existing_nums=None):
    """返回 (section_text, link_count)。existing_nums: 章内已链接的章号集合(排除冗余)。"""
    seen = set()
    picked = []  # (label, num)
    if existing_nums is None:
        existing_nums = set()

    def add(label, num):
        if num == target_num or num in seen or num in existing_nums:
            return False
        if num not in meta:
            return False
        if not meta[num]["path"].exists():
            return False
        seen.add(num)
        picked.append((label, num))
        return True

    # 1) 前置依赖
    for n in sorted(deps.get(target_num, []), key=lambda x: int(x)):
        if len([p for p in picked if p[0] == "前置基础"]) >= 2:
            break
        add("前置基础", n)
    # 2) 后续依赖
    for n in sorted(preds.get(target_num, []), key=lambda x: int(x)):
        if len([p for p in picked if p[0] == "后续依赖"]) >= 2:
            break
        add("后续依赖", n)
    # 3) 相邻章
    t = int(target_num)
    for off in (-1, 1, -2, 2):
        add("相邻主题", f"{t+off:02d}")
    # 4) 同 part 兄弟
    tp = meta[target_num]["part"]
    for num, info in sorted(meta.items(), key=lambda kv: int(kv[0])):
        if info["part"] == tp and num != target_num:
            if add("同模块", num):
                break

    if not picked:
        return None, 0

    lines = [SEC_HDR, ""]
    for label, num in picked:
        info = meta[num]
        link = f"`{rel_path(info['path'])}`"
        if label == "前置基础":
            reason = "学习本章前建议先掌握的前置基础"
        elif label == "后续依赖":
            reason = "本章为其前置，建议后续延伸阅读"
        elif label == "相邻主题":
            reason = "编号相邻、主题接续"
        else:
            reason = "同模块下的其他主题"
        lines.append(f"- **{label}**：{link}（{info['title']}）—— {reason}。")
    lines.append("")
    return "\n".join(lines), len(picked)


def backfill(path: Path, meta, deps, preds, dry=False):
    text = path.read_text(encoding="utf-8")
    # 幂等：已有专节则跳过
    if SEC_HDR in text:
        return "skip-section"
    cur_refs = count_refs(text)
    if len(cur_refs) >= THRESHOLD:
        return "skip-threshold"
    num = re.match(r"ch(\d+)_", path.name).group(1)
    num = f"{int(num):02d}"
    if num not in meta:
        return "skip-nometa"
    exist_nums = set()
    for r in cur_refs:
        m = re.search(r"ch(\d+)_", r)
        if m:
            exist_nums.add(f"{int(m.group(1)):02d}")
    section, n = build_section(num, meta, deps, preds, existing_nums=exist_nums)
    if not section:
        return "skip-empty"
    if not dry:
        if not path.with_suffix(".md.bak").exists():
            shutil.copy(path, path.with_suffix(".md.bak"))
        if EXERCISE_HDR in text:
            text = text.replace(EXERCISE_HDR, section + "\n" + EXERCISE_HDR, 1)
        else:
            text = text.rstrip() + "\n\n" + section + "\n"
        path.write_text(text, encoding="utf-8")
    return f"ok:{n}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list-low", action="store_true")
    ap.add_argument("--dry", action="store_true", help="只打印不写入")
    args = ap.parse_args()

    deps, preds = load_dag()
    meta = chapter_meta()

    if args.list_low:
        low = []
        for num, info in meta.items():
            c = len(count_refs(info["path"].read_text(encoding="utf-8")))
            if c < THRESHOLD:
                low.append((c, num, info["path"]))
        low.sort()
        print(f"引用<{THRESHOLD}的章: {len(low)}")
        for c, num, p in low:
            print(f"  {c:>2}  {rel_path(p)}")
        return

    if args.paths:
        targets = [Path(p if Path(p).is_absolute() else ROOT / p) for p in args.paths]
    elif args.all:
        targets = [info["path"] for info in meta.values()]
    else:
        print("需指定 --all 或 章路径，或 --list-low"); sys.exit(2)

    ok = skip = empty = 0
    for p in targets:
        r = backfill(p, meta, deps, preds, dry=args.dry)
        if r.startswith("ok"):
            ok += 1
            if args.dry:
                print(f"[dry+]{r} {rel_path(p)}")
        elif r.startswith("skip"):
            skip += 1
        else:
            empty += 1
    print(f"回填完成: ok={ok} skip={skip} empty={empty}")


if __name__ == "__main__":
    main()
