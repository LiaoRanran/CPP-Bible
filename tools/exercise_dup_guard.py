#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exercise_dup_guard.py — 习题"题库串章"防回归门禁（确定性，零依赖）

问题背景
--------
早期审计发现：通用模板题库（`max_safe` / `std::integral` 概念题 / `constexpr fact`
/ 泛型 `max`）被整体克隆进大量无关章节的"自测练习"，仅套一层薄主题包装，
既稀释章节技术核心、又制造跨章重复。本工具在 CI 中**确定性**地捕获这一类回归：

  提取每章"自测练习"小节内的 ```cpp 块 → 归一化（去注释/预处理指令/折叠空白）
  → 哈希 → 若同一归一化块出现在 **>=2 个不同章节**，判为"题库串章"克隆并 BLOCK。

为何确定性而非 LLM：克隆是"相同代码片段出现在多章"，哈希碰撞即可精确捕获，
无模糊判定、无 flake。与 verify_exercises.py（仅编译练习块）互补：
verify_exercises 保证"能编译"，本工具保证"不被克隆复用"。

归一化策略
----------
- 去 `/* */` 与 `//` 注释
- 去 `#` 开头的预处理行（`#include`/`#pragma`/`#define` 等， clones 常共享 include）
- 折叠所有空白为单空格
仅对归一化后长度 >= MIN_LEN 的块参与比对，避免 `return 0;` 等平凡碰撞。

退出码
------
- 0：无跨章克隆（或仅章内重复）
- 1：发现跨章克隆（阻断 CI）

用法
----
  python3 tools/exercise_dup_guard.py                 # 全量扫描 Book/
  python3 tools/exercise_dup_guard.py --json out.json # 输出 JSON 报告
"""
import re, os, sys, json, hashlib, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "Book")

# 优先锚定规范的"自测练习 / Exercises"小节（147 章通用）；
# 仅当缺省时才回退到含"习题/练习"的附录/内化小节，避免误抓"思考题/源码阅读路线"。
SEC_KEYS_PRIMARY = ["自测练习", "Exercises"]
SEC_KEYS_SECONDARY = ["习题", "练习"]
MIN_LEN = 100  # 归一化后最小长度，低于此视为平凡块不参与比对


def _norm(src: str) -> str:
    s = re.sub(r"/\*.*?\*/", "", src, flags=re.S)   # 块注释
    s = re.sub(r"//[^\n]*", "", s)                  # 行注释
    s = re.sub(r"^\s*#.*$", "", s, flags=re.M)      # 预处理行
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _section_bounds(text: str):
    """返回 (start_idx, end_idx) 文本区间：第一个练习小节的起始，到其所在
    `## ` 级别的下一个同级/更高一级标题之前（或文件尾）。"""
    heads = list(re.finditer(r"^(#{1,6})\s.*$", text, re.M))
    if not heads:
        return None
    # 先按主关键词（自测练习/Exercises）锚定，回退到次关键词
    start = None
    for keys in (SEC_KEYS_PRIMARY, SEC_KEYS_SECONDARY):
        for h in heads:
            if any(k in h.group(0) for k in keys):
                start = h
                break
        if start is not None:
            break
    if start is None:
        return None
    level = len(start.group(1))  # 该练习标题的 # 级数
    end = len(text)
    for h in heads:
        if h.start() <= start.start():
            continue
        # 下一个同级或更高级标题即为小节边界
        if len(h.group(1)) <= level:
            end = h.start()
            break
    return (start.start(), end)


def extract_exercise_cpp(md_path: str):
    text = open(md_path, encoding="utf-8").read()
    bounds = _section_bounds(text)
    if bounds is None:
        return []
    sec = text[bounds[0]:bounds[1]]
    blocks = re.findall(r"```cpp(.*?)```", sec, re.S)
    out = []
    for b in blocks:
        n = _norm(b)
        if len(n) >= MIN_LEN:
            out.append((n, hashlib.sha1(n.encode()).hexdigest()[:12]))
    return out


def scan():
    by_hash = {}
    for dp, _, fs in os.walk(BOOK):
        for f in fs:
            if not re.match(r"ch\d+_.*\.md$", f):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, ROOT)
            for n, h in extract_exercise_cpp(p):
                by_hash.setdefault(h, {"norm": n, "chapters": []})
                if rel not in by_hash[h]["chapters"]:
                    by_hash[h]["chapters"].append(rel)
    # 仅保留跨章（>=2 不同章节）且非章内重复
    cross = {h: v for h, v in by_hash.items() if len(v["chapters"]) >= 2}
    return by_hash, cross


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="写出 JSON 报告路径")
    args = ap.parse_args()

    by_hash, cross = scan()

    print(f"=== 习题串章门禁: 扫描归一化块 {len(by_hash)} 个 ===")
    if not cross:
        print("OK: 未发现跨章克隆的练习代码块。")
        if args.json:
            with open(args.json, "w", encoding="utf-8") as f:
                json.dump({"cross_chapter_dups": {}}, f, ensure_ascii=False, indent=2)
        return 0

    print(f"BLOCK: 发现 {len(cross)} 个跨章克隆块：")
    report = {}
    for h, v in sorted(cross.items(), key=lambda kv: -len(kv[1]["chapters"])):
        chs = sorted(v["chapters"])
        report[h] = {"chapters": chs, "sample": v["norm"][:160]}
        print(f"  hash={h} 章节数={len(chs)}: {chs}")
        print(f"    样例: {v['norm'][:160]}")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"cross_chapter_dups": report}, f, ensure_ascii=False, indent=2)
    print("\n判定：存在跨章克隆 → 阻断（exit 1）。请改写被克隆的练习为各章自有主题。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
