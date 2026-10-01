#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""external_anchor_fetch_672j.py — 672j W5：外部锚定的**数据获取与机械抽取**。

做什么
======
1. 抓 `https://raw.githubusercontent.com/isocpp/CppCoreGuidelines/master/CppCoreGuidelines.md`
   （唯一实测可取的外部源；cppref/SO 均 403 —— 见预注册 §source_availability）；
2. **机械抽取**"Example, bad" 紧随的 ```cpp 代码块 + 所属规则编号（不改写代码）；
3. 落 `data/external_anchor/guideline_raw_extract_672j.json`（候选池，含 URL、抓取时间、
   文档 sha256、每条代码的 sha256）——**这一步不判决、不筛质量**；
4. `--assemble` 把候选池按预注册规则组装成数据集（前 N 条、去重、映射检测器）。

用法
====
    python tools/external_anchor_fetch_672j.py --fetch      # 抓取 + 抽取（写候选池）
    python tools/external_anchor_fetch_672j.py --assemble   # 组装 dataset（写 external_anchor_672j.json）
    python tools/external_anchor_fetch_672j.py --selftest   # 自检（不联网）
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANCHOR_DIR = ROOT / "data" / "external_anchor"
POOL = ANCHOR_DIR / "guideline_raw_extract_672j.json"
DATASET = ANCHOR_DIR / "external_anchor_672j.json"
SRC_URL = "https://raw.githubusercontent.com/isocpp/CppCoreGuidelines/master/CppCoreGuidelines.md"
UA = {"User-Agent": "Mozilla/5.0 (compatible; queyi-anchor/1.0)"}

N_VERBATIM_TARGET = 35
N_RECONSTRUCTED_TARGET = 15

#: 规则编号（如 ES.20 / R.11 / CP.2 / SL.7 / I.11 / F.43 …）
RULE_RE = re.compile(r"^#{2,5} <a name=\"?([^\">]+)\"?></a>\s*([A-Z]{1,3}\.[0-9]+)\s*:?\s*(.*)$")
RULE_RE2 = re.compile(r"^#{2,5}\s*([A-Z]{1,3}\.[0-9]+)\s*:?\s*(.*)$")
BAD_RE = re.compile(r"(example,?\s*bad|bad\s+example|\bbad\b\s*[:：]|消极|反面)", re.I)


def sha256(txt: str) -> str:
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()


def fetch_md() -> tuple[str, dict]:
    req = urllib.request.Request(SRC_URL, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
    md = raw.decode("utf-8", errors="replace")
    meta = {"url": SRC_URL, "fetched_at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    return md, meta


def extract_bad_examples(md: str) -> list[dict]:
    """机械抽取：规则编号 + bad 标记 + 紧随其后的 ```cpp 块。"""
    lines = md.splitlines()
    cur_rule, cur_title = None, ""
    out: list[dict] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = RULE_RE.match(ln) or RULE_RE2.match(ln)
        if m:
            cur_rule, cur_title = m.group(2), m.group(3).strip()[:90]
        if BAD_RE.search(ln):
            # 两种代码块形态都要支持：```cpp 围栏（最多 6 行内）与 4 空格缩进块
            j, fence = i + 1, None
            while j < len(lines) and j <= i + 6:
                if lines[j].strip().startswith("```"):
                    fence = j
                    break
                if re.match(r"^(    |\t)\S", lines[j]):
                    break
                if lines[j].strip():
                    break
                j += 1
            code = ""
            end = i
            if fence is not None and re.match(r"^```(cpp|c\+\+)\s*$", lines[fence].strip()):
                k, body = fence + 1, []
                while k < len(lines) and not lines[k].strip().startswith("```"):
                    body.append(lines[k])
                    k += 1
                code, end = "\n".join(body).strip(), k
            else:
                # 缩进块：找最近的一条缩进行（允许中间隔一行说明文字）
                k = i + 1
                while k < len(lines) and k <= i + 8 and not re.match(r"^(    |\t)\S", lines[k]):
                    k += 1
                if k <= i + 8 and k < len(lines):
                    body2 = []
                    while k < len(lines) and (not lines[k].strip()
                                              or re.match(r"^(    |\t)", lines[k])):
                        t = lines[k]
                        body2.append(t[4:] if t.startswith("    ") else
                                     (t[1:] if t.startswith("\t") else ""))
                        k += 1
                    code, end = "\n".join(body2).strip(), k - 1
            if 25 <= len(code) <= 1500:
                out.append({
                    "rule_id": cur_rule or "N/A",
                    "rule_title": cur_title,
                    "anchor_line": i + 1,
                    "code": code,
                    "code_sha256": sha256(code),
                    "verbatim": True,
                })
                i = end
                continue
        i += 1
    # 去重（同代码只留首条）
    seen, uniq = set(), []
    for s in out:
        if s["code_sha256"] in seen:
            continue
        seen.add(s["code_sha256"])
        uniq.append(s)
    return uniq


def detect_mapping(code: str) -> tuple[list[str], str]:
    """机械映射（预注册口径）：含 <thread> → tsan；有 main → asan+ubsan 双跑；否则 → compiler-warn。"""
    if re.search(r"#include\s*<thread>", code) or re.search(r"\bstd::thread\b", code):
        return ["tsan"], "含 <thread> ⇒ TSan"
    if re.search(r"\bint\s+main\s*\(", code):
        return ["asan", "ubsan"], "含 main ⇒ ASan+UBSan 双跑（任一报出即 catch）"
    return ["compiler-warn"], "片段（无 main）⇒ -fsyntax-only 告警判据"


def assemble(pool: dict, n_verbatim: int = N_VERBATIM_TARGET,
             max_scan: int = 200) -> dict:
    """组装 subset A：**按文档顺序**取前 n 条「唯一规则 + 加统一 harness 后可编译」的候选。

    机械性说明（防挑樱桃）：
      * 顺序 = 文档顺序（不是按"能不能检出"挑）；
      * 唯一性 = 同一规则只取一条；
      * harness = 统一 prelude（标准头 + `using namespace std;`，**不改片段主体**）——
        这是对预注册的一次**方法补充**：原样可编译率只有 11/60，不补 harness 分母会小到失去意义；
        补法统一施加于所有 subset A 样本，且逐条记录 `harness` 字段。
    """
    import subprocess
    import tempfile

    cands = pool["candidates"]
    picked: list[dict] = []
    skipped_uncompilable: list[str] = []
    rules_seen: set[str] = set()
    scanned = 0
    for c in cands:
        if c["rule_id"] in ("N/A",) or c["rule_id"] in rules_seen:
            continue                     # 同一规则只取一条（防单一规则的例子刷屏）
        rules_seen.add(c["rule_id"])
        scanned += 1
        ok = False
        with tempfile.TemporaryDirectory(prefix="w5asm_") as d:
            p = Path(d) / "s.cpp"
            p.write_text(PRELUDE + c["code"], encoding="utf-8")
            try:
                r = subprocess.run(["g++", "-std=c++17", "-fsyntax-only", "-Wall",
                                    "-Wextra", str(p)], capture_output=True, text=True,
                                   timeout=60)
                ok = r.returncode == 0
            except Exception:  # noqa: BLE001
                ok = False
        if not ok:
            skipped_uncompilable.append(c["rule_id"])
            if scanned >= max_scan:
                break
            continue
        dets, why = detect_mapping(c["code"])
        picked.append({
            "id": f"g-{len(picked) + 1:02d}",
            "subset": "guideline_bad_verbatim",
            "label": "guideline_violation",
            "rule_id": c["rule_id"], "rule_title": c["rule_title"],
            "source_url": SRC_URL, "source_doc_sha256": pool["source"]["sha256"],
            "code_sha256": c["code_sha256"], "verbatim": True,
            "harness": "prelude_v1（统一加标准头 + using namespace std；片段主体不改）",
            "expected_detectors": dets, "detector_note": why,
            "code": c["code"],
        })
        if len(picked) >= n_verbatim:
            break
    return {"picked": picked, "rules": [p["rule_id"] for p in picked],
            "scanned": scanned, "skipped_uncompilable": skipped_uncompilable}


#: 统一 harness（subset A 专用；不改片段主体，只补标准头与 using）
PRELUDE = ("#include <cstdio>\n#include <cstdlib>\n#include <cstring>\n#include <string>\n"
           "#include <vector>\n#include <map>\n#include <memory>\n#include <thread>\n"
           "#include <mutex>\n#include <algorithm>\n#include <iostream>\n"
           "using namespace std;\n")


def _reconstructed() -> list[dict]:
    """公开 UB 类别重建（verified_source=false；类别出处逐条注明）。"""
    base = [
        ("u-01", "有符号整数溢出", "cppreference『未定义行为』：signed integer overflow",
         "ubsan", "#include <cstdio>\nint main(){int a=2147483647;int b=a+1;std::printf(\"%d\\n\",b);return 0;}\n"),
        ("u-02", "左移负/超宽", "cppreference『未定义行为』：shift exponent negative",
         "ubsan", "#include <cstdio>\nint main(){int n=-1;int x=1<<n;std::printf(\"%d\\n\",x);return 0;}\n"),
        ("u-03", "除零（运行期）", "cppreference『未定义行为』：division by zero",
         "ubsan", "#include <cstdio>\nint main(int c,char**){int z=c-1;int y=7/z;std::printf(\"%d\\n\",y);return 0;}\n"),
        ("u-04", "空指针解引用", "cppreference『未定义行为』：null pointer dereference",
         "ubsan", "#include <cstdio>\nint main(){int* p=nullptr;*p=3;std::printf(\"%d\\n\",*p);return 0;}\n"),
        ("u-05", "越界读栈数组", "cppreference『未定义行为』：out-of-bounds access",
         "asan", "#include <cstdio>\nint main(){int a[3]={1,2,3};int s=0;for(int i=0;i<5;++i)s+=a[i];std::printf(\"%d\\n\",s);return 0;}\n"),
        ("u-06", "释放后使用", "cppreference『未定义行为』：use after free",
         "asan", "#include <cstdlib>\n#include <cstdio>\nint main(){int* p=(int*)std::malloc(4);std::free(p);*p=4;std::printf(\"%d\\n\",*p);return 0;}\n"),
        ("u-07", "双重释放", "cppreference『未定义行为』：double free",
         "asan", "#include <cstdlib>\nint main(){void* p=std::malloc(8);std::free(p);std::free(p);return 0;}\n"),
        ("u-08", "new[]/delete 不配对", "C++ Core Guidelines R.11（显式 new/delete 的配对）",
         "asan", "#include <cstdio>\nint main(){int* a=new int[4];a[1]=2;std::printf(\"%d\\n\",a[1]);delete a;return 0;}\n"),
        ("u-09", "对齐违规", "cppreference『未定义行为』：misaligned access",
         "ubsan", "#include <cstdio>\n#include <cstdint>\nint main(){char b[8]={0};int* p=(int*)(b+1);*p=7;std::printf(\"%d\\n\",*p);return 0;}\n"),
        ("u-10", "严格别名违规", "C++ Core Guidelines ES.42 / 别名词条",
         "ubsan", "#include <cstdio>\nint main(){int x=1;float* f=(float*)&x;*f=2.0f;std::printf(\"%d\\n\",x);return 0;}\n"),
        ("u-11", "数据竞争", "cppreference『未定义行为』：data race",
         "tsan", "#include <thread>\n#include <cstdio>\nint g=0;\nint main(){std::thread a([]{for(int i=0;i<100000;++i)++g;}),b([]{for(int i=0;i<100000;++i)++g;});a.join();b.join();std::printf(\"%d\\n\",g);return 0;}\n"),
        ("u-12", "泄漏", "C++ Core Guidelines R.11（资源必须释放）",
         "asan", "#include <cstdio>\nint main(){int* p=new int[8];p[0]=1;std::printf(\"%d\\n\",p[0]);return 0;}\n"),
        ("u-13", "未初始化读", "cppreference『未定义行为』：indeterminate value",
         "warn", "#include <cstdio>\nint main(){int x;std::printf(\"%d\\n\",x);return 0;}\n"),
        ("u-14", "printf 格式不匹配", "C++ Core Guidelines / POSIX printf 契约",
         "warn", "#include <cstdio>\nint main(){double d=1.0;std::printf(\"%d\\n\",d);return 0;}\n"),
        ("u-15", "有返回值路径缺失", "C++ Core Guidelines F.44",
         "warn", "#include <cstdio>\nint f(int x){if(x>0)return x;}\nint main(){std::printf(\"%d\\n\",f(2));return 0;}\n"),
    ]
    out = []
    for sid, desc, cite, det, code in base:
        dets = ["compiler-warn"] if det == "warn" else [det]
        out.append({
            "id": f"{sid}", "subset": "ub_reconstructed", "label": "ub_reconstructed",
            "rule_id": None, "rule_title": desc, "source_url": None,
            "verbatim": False, "verified_source": False, "citation": cite,
            "code_sha256": sha256(code), "expected_detectors": dets,
            "detector_note": f"类别 → {dets[0]}" + ("（-fsyntax-only）" if det == "warn" else ""),
            "code": code,
        })
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="672j W5：外部锚定数据获取/组装")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--assemble", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    ANCHOR_DIR.mkdir(parents=True, exist_ok=True)
    if a.fetch:
        md, meta = fetch_md()
        cands = extract_bad_examples(md)
        POOL.write_text(json.dumps({"schema": "queyi-anchor-pool/672j",
                                    "source": meta, "n_candidates": len(cands),
                                    "candidates": cands},
                                   ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")
        print(f"[anchor-fetch] 抓取 {meta['bytes']}B sha256={meta['sha256'][:12]}；"
              f"抽取候选 {len(cands)} 条 → {POOL.name}")
    if a.assemble:
        if not POOL.is_file():
            print("[anchor-fetch] 缺候选池，先 --fetch", file=sys.stderr)
            return 1
        pool = json.loads(POOL.read_text(encoding="utf-8"))
        asm = assemble(pool)
        samples = asm["picked"] + _reconstructed()
        doc = {
            "schema": "queyi-external-anchor/672j",
            "generated_by": "tools/external_anchor_fetch_672j.py",
            "generated_at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prereg": "data/experiments/prereg_672j.json",
            "source": pool["source"],
            "extraction": "机械抽取：规则编号 + 'Example, bad' + 紧随 ```cpp；同规则只取一条；不改写",
            "counts": {"total": len(samples),
                       "guideline_bad_verbatim": len(asm["picked"]),
                       "ub_reconstructed": len(samples) - len(asm["picked"])},
            "rules_covered": asm["rules"],
            "harness": {"subset_a": "prelude_v1（统一标准头 + using namespace std；片段主体不改）",
                        "why": "原样可编译率 11/60 ⇒ 不补 harness 分母失去意义；补法统一施加、逐条记录",
                        "deviation_from_prereg": "预注册未写 harness ⇒ 作为方法补充登记（不改假设/阈值/抽样顺序）"},
            "compilability_filter": {"scanned_unique_rules": asm.get("scanned"),
                                     "skipped_uncompilable_rules": asm.get("skipped_uncompilable"),
                                     "rule": "文档顺序扫描；同一规则只取一条；加 harness 后 -fsyntax-only 编译失败 ⇒ 跳过并登记（预注册『编译不可行 ⇒ 排除』条款）"},
            "caliber": "两部分目标类不同（准则违规 vs UB）⇒ 率必须分列；verbatim 部分可凭 code_sha256 复核",
            "samples": samples,
        }
        DATASET.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8", newline="\n")
        print(f"[anchor-assemble] 数据集 {len(samples)} 条"
              f"（verbatim {len(asm['picked'])} + 重建 {len(samples) - len(asm['picked'])}）"
              f" → {DATASET.name}")
    return 0


def selftest() -> int:
    ok = 0
    md = ("### <a name=\"Res-expr\"></a>ES.20: Always initialize an object\n\n"
          "##### Example, bad\n\n```cpp\nint x;\nstd::printf(\"%d\", x);\n```\n\n"
          "### <a name=\"Rr-newdelete\"></a>R.11: Avoid calling new and delete explicitly\n\n"
          "##### Example, bad\n\n```cpp\nauto w = new Widget{};\ndelete w;\n```\n")
    got = extract_bad_examples(md)
    assert len(got) == 2, got
    assert got[0]["rule_id"] == "ES.20" and "int x;" in got[0]["code"]
    assert got[1]["rule_id"] == "R.11"
    ok += 3
    # 去重：同代码块只留一条
    md2 = md + md
    assert len(extract_bad_examples(md2)) == 2
    ok += 1
    # 机械映射
    assert detect_mapping("#include <thread>\nint main(){}")[0] == ["tsan"]
    assert detect_mapping("int main(){return 0;}")[0] == ["asan", "ubsan"]
    assert detect_mapping("void f(){}")[0] == ["compiler-warn"]
    ok += 3
    # 重建池：15 条、id 唯一、都有 cite 与 detector
    rec = _reconstructed()
    assert len(rec) == N_RECONSTRUCTED_TARGET == 15
    assert len({r["id"] for r in rec}) == 15
    assert all(r["citation"] and r["expected_detectors"] for r in rec)
    assert all(r["verbatim"] is False and r["verified_source"] is False for r in rec)
    ok += 4
    print(f"[anchor-fetch-selftest] {ok} 项通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
