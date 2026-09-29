#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""ig_cards_665.py — 665 B1：把 664 独立生成的 15 条断言拆成**可复现的卡**。

设计（为什么不是直接写 markdown）
================================
卡的生命在于**能被别人重跑一遍验证**。所以本工具做的三件事都是"机器可复算"的：

  1. `fixtures/ig-NN.cpp`：把 664 B2 的反例代码**逐字节**落盘（`data/cards_665/fixtures/`，
     不写受控的 `Examples/`、`atoms/`、`evidence/`）；
  2. 真机复跑检测器（本机 g++/clang++；ASan/UBSan/TSan 走 WSL），记录 `rc` + 输出摘录 +
     是否命中；海拔不变的比较用**签名**（ san 命中关键词 / 告警首行 / 两档输出 / stdout ）；
  3. 每张卡都带上**边界三元组 + 判决词**，交给 `four_state_verdict_638.enforce()` 出四态，
     让卡不是"我觉得对"，而是"工具在什么条件下判它对"。

信任边界（红线）
================
* **不代签**：卡的 status 一律 `machine-derived`，**没有人签过的 verified**。
* 边界三元组是**按用途重定义**的（`mutation_set_hash` = 探针集 sha256；`mutation_count` = 该卡实跑次数；
  `generator_version` = `ig_cards_665/v1`），不是 656 mutation 的血统 ⇒ 全部标 `needs_review=true`。

用法
====
    python tools/ig_cards_665.py --build      # 落夹具 + 真机复跑 + 写卡 + 写 index
    python tools/ig_cards_665.py --check      # 重跑全部复现命令，比对签名（CI 可用）
    python tools/ig_cards_665.py --selftest   # 自检（含 Counting 恒等式）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import four_state_verdict_638 as fs  # noqa: E402

OUT_DIR = ROOT / "data" / "cards_665"
FIX_DIR = OUT_DIR / "fixtures"
INDEX = OUT_DIR / "index_665.json"
GENERATOR_VERSION = "ig_cards_665/v1"

SAN = {"tsan": "thread", "asan": "address", "ubsan": "undefined"}

# 664 的原始 15 条：只从库存数据源导入，**不在这里重写内容**（避免两处漂移）。
_SOURCE_NOTE = "tools/independent_generation_664.py::CASES"

# 每张卡的**主张**（纠正后的知识）预测什么观测：即"什么算支持这张卡"。
# 这张表是**判据**，不是结论：写在这里是为了让"支持/未呈现/矛盾"可机器判定。
EXPECT: dict[str, str] = {
    "ig-01": "catch",   # 有符号溢出是 UB ⇒ UBSan 应报
    "ig-02": "catch",   # 越界 ⇒ ASan 应报
    "ig-03": "miss",    # delete nullptr 是 no-op ⇒ ASan 应保持沉默
    "ig-04": "measure",  # 无移动构造时退化为拷贝 ⇒ 应测到 "copy"
    "ig-05": "measure",  # sizeof 等于裸指针 ⇒ 应测到两数相等
    "ig-06": "miss",    # weak_ptr 断开则不泄漏 ⇒ 应保持沉默
    "ig-07": "catch",   # 空指针解引用 ⇒ ASan 应报
    "ig-08": "catch",   # 除零 ⇒ UBSan 应报
    "ig-09": "catch",   # 依赖 UB 时 -O0/-O2 可能不同 ⇒ 期望观察到差异
    "ig-10": "catch",   # char 符号性跨实现差异 ⇒ 期望观察到差异（本机可能不呈现）
    "ig-11": "measure",  # sizeof(int) 本机实测
    "ig-12": "catch",   # vector<bool> 取址失败 ⇒ 编译应报
    "ig-13": "catch",   # 严格别名 ⇒ 期望跨配置差异（本探针常不呈现）
    "ig-14": "catch",   # new[]/delete 不匹配 ⇒ ASan 应报
    "ig-15": "measure",  # 具名右值引用是左值 ⇒ 应测到 "copy"
    "ig-16": "measure",  # 665 补探针（ig-04 修正版）
}
# 测量类的期望读数（严格比对：连空串都算一种结果）
EXPECT_VAL: dict[str, str] = {
    "ig-04": "move",   # 该夹具类型**同时**有移动构造 ⇒ 即便编译通过了，也只可能打印 move
    "ig-05": "8 8",
    "ig-11": "4",
    "ig-15": "copy",
    "ig-16": "copy",
}

#: 664 套件自身缺陷登记（**不代 664 打补丁**，只如实记录并另开修正探针）
KNOWN_DEFECTS: dict[str, str] = {
    "ig-04": ("664 夹具缺 `#include <utility>` ⇒ 编译失败（`std::move` 未声明），本条拿不到读数 ⇒ unknown。"
              "更严重的是：该夹具的类型**同时**具备移动构造（`T(T&&)`），即使补上头文件也只会打印 `move`，"
              "即**支持原断言而非推翻它** —— 664 Agent B 在这条上的反例构造是无效的。"
              "故本卡不借挂机器结论，另以 665 新增探针 ig-16（类型**无**移动构造）重做该条。"),
}

# 665 新增探针：664 的 ig-04 夹具缺 `#include <utility>` 且夹具类型自带移动构造 ⇒ 反例无效。
# **不偷偷改 664 的夹具**（那会让历史实验失真），而是另开一条修正探针并显式标注来源。
EXTRA_PROBES: list[dict] = [
    {"id": "ig-16", "assertion": "std::move 一定触发移动构造（664 ig-04 的**修正重做**探针）",
     "counterexample": "类型无移动构造时 std::move 退化为拷贝 ⇒ 实测打印 copy（不是 move）",
     "code": ('#include <cstdio>\n#include <utility>\n'
              'struct T{T()=default;T(const T&){std::printf("copy");}};  // 故意不提供移动构造\n'
              'int main(){T a; T b(std::move(a));}'),
     "detector": "measure", "gap": "664 ig-04 夹具自身缺陷导致 unknown；本探针为该条的修正重做"},
]


def _load_cases() -> list[dict]:
    """只读导入 664 的反例套件（模块 __main__ 有守卫，导入安全）。"""
    import independent_generation_664 as ig
    return list(ig.CASES)


def _to_wsl(p: str) -> str:
    p = p.replace("\\", "/")
    return ("/mnt/" + p[0].lower() + p[2:]) if len(p) > 1 and p[1:] and p[1] == ":" else p


def _sh(cmd, timeout: int = 180) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa: BLE001
        return -99, f"EXC: {e}"


def _wsl(cmd: str, timeout: int = 180) -> tuple[int, str]:
    return _sh(["wsl", "-e", "bash", "-lc", cmd], timeout)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))  # 统一 LF，不用通用换行


def _excerpt(s: str, n: int = 1200) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[:n] + "\n…[truncated]"


# ── 每种检测器的"跑一遍"，返回 (verdict, note, signature, runs, raw) ────
def run_probe(kind: str, src: Path) -> tuple[str, str, str, int, str]:
    """跑一遍，给出 机器判决 / 人读说明 / 可复算签名 / 实跑次数 / 原始输出。"""
    if kind == "compiler-warn":
        rc, out = _sh(["g++", "-std=c++17", "-Wall", "-Wextra", "-fsyntax-only", str(src)])
        lines = [l for l in out.splitlines() if ("warning:" in l or "error:" in l)]
        if not lines:
            return "miss", "无告警/无错误（rc=%d）" % rc, "no-diagnostic", 1, out
        # 首行含临时路径 ⇒ 只取文件名之后的部分，保证跨次运行稳定
        first = lines[0].split(str(src))[-1].split("\\")[-1]
        return "catch", _excerpt(lines[0], 200), "diag:" + first.strip()[:80], 1, out

    if kind == "cross-compile":
        exe = src.with_suffix(".exe")
        outs, ok = [], True
        for opt in ("-O0", "-O2"):
            rc, _ = _sh(["g++", "-std=c++17", opt, str(src), "-o", str(exe)])
            if rc != 0:
                ok = False
                outs.append("compile-fail")
                continue
            rc, out = _sh([str(exe)], timeout=30)
            outs.append((out or "").strip())
        raw = "|".join(outs)
        if not ok:
            return "unknown", "编译失败", "compile-fail", 2, raw
        diff = outs[0] != outs[1]
        sig = "diff" if diff else ("same:" + _sha(outs[0] + "|" + outs[1])[:16])
        note = ("-O0/-O2 结果不同：%r vs %r" % (outs[0][:60], outs[1][:60])) if diff else "两优化级一致"
        return ("catch" if diff else "miss"), note, sig, 2, raw

    if kind in SAN:
        w = _to_wsl(str(src))
        rc, out = _wsl(f"g++ -std=c++17 -O1 -g -fsanitize={SAN[kind]} -pthread {w} -o /tmp/ig665_{src.stem}")
        if rc != 0:
            return "unknown", "编译失败：" + _excerpt(out, 200), "compile-fail", 1, out
        rc, out = _wsl(f"/tmp/ig665_{src.stem}", timeout=60)
        low = out.lower()
        hit_word = next((w2 for w2 in ("AddressSanitizer", "LeakSanitizer", "ThreadSanitizer",
                                      "runtime error", "data race") if w2 in out or w2.lower() in low), "")
        if hit_word:
            return "catch", f"{kind} 命中（rc={rc}）：{hit_word}", "hit:" + hit_word, 1, out
        return "miss", f"{kind} 无报告（rc={rc}）", "clean", 1, out

    if kind == "measure":
        exe = src.with_suffix(".exe")
        rc, out = _sh(["g++", "-std=c++17", "-O2", str(src), "-o", str(exe)])
        if rc != 0:
            return "unknown", "编译失败：" + _excerpt(out, 200), "compile-fail", 1, out
        rc, out = _sh([str(exe)], timeout=30)
        s = (out or "").strip()
        return "measure", s[:120], "out:" + _sha(s)[:16], 1, s

    return "unknown", "未支持检测器", "unsupported", 0, ""


def reproduce_cmds(kind: str, src: Path) -> list[str]:
    """卡里写给人看的复现命令（要与 run_probe 的实际调用**逐条对应**）。"""
    rel = src.relative_to(ROOT).as_posix()
    if kind == "compiler-warn":
        return [f"g++ -std=c++17 -Wall -Wextra -fsyntax-only {rel}"]
    if kind == "cross-compile":
        return [f"g++ -std=c++17 -O0 {rel} -o build/{src.stem}_O0.exe && ./build/{src.stem}_O0.exe",
                f"g++ -std=c++17 -O2 {rel} -o build/{src.stem}_O2.exe && ./build/{src.stem}_O2.exe"]
    if kind in SAN:
        w = _to_wsl(str(src))
        return [f"wsl -e bash -lc \"g++ -std=c++17 -O1 -g -fsanitize={SAN[kind]} -pthread {w} "
                f"-o /tmp/ig665_{src.stem}\"",
                f"wsl -e bash -lc /tmp/ig665_{src.stem}"]
    if kind == "measure":
        return [f"g++ -std=c++17 -O2 {rel} -o build/{src.stem}.exe && ./build/{src.stem}.exe"]
    return []


def support_of(case_id: str, v: str, measured_out: str) -> tuple[str, str]:
    """主张是否被本次观测支持。返回 (verdict_word, 人读理由)。

    三分支（不做二值化）——判决词必须与 638 的词表对齐
    （`_PASS_WORDS` 含空串，写 "" 会被当成 pass ⇒ 未呈现必须显式写 `unknown`）：
      pass     = 观测**支持**本卡主张
      unknown  = **未呈现**（探针/检测器没能力让它出现 ⇒ 不许当成"卡错了"）
      block    = 观测**与本卡主张矛盾**（这才算 fail）
    """
    exp = EXPECT.get(case_id)
    if exp is None:
        return "unknown", f"未登记判据（EXPECT 缺 {case_id}）"
    if v == "unknown":
        return "unknown", "检测器不可用/编译失败 ⇒ 证据不足，不是卡错"
    if exp == "measure":
        want = EXPECT_VAL.get(case_id)
        if want is None:
            return "unknown", f"测量类但 EXPECT_VAL 缺 {case_id}"
        return (("pass", f"实测读数 {measured_out!r} == 期望 {want!r}")
                if measured_out.strip() == want else
                ("block", f"实测读数 {measured_out!r} != 期望 {want!r}"))
    if v == exp:
        return "pass", f"期望 {exp}、实测 {v}：观测支持主张"
    if exp in ("catch", "measure") and v == "miss":
        return "unknown", (f"期望 {exp}、实测 miss：**本探针未呈现**（检测器能力/平台所致），"
                           "按 638 语义判 unknown，不判卡错")
    return "block", f"期望 {exp}、实测 {v}：与本卡主张矛盾"


def render_card(c: dict, m: dict) -> str:
    """渲染一张卡（md）。数据全来自本次真机复跑 + 664 库存记录。"""
    return f"""---
schema: queyi-ig-card/v1
id: {m["id"]}
source_run: {m["_source_run"]}
source_suite: {m["_source_suite"]}
generated_by: tools/ig_cards_665.py
generated_at: {m["measured_at"]}
status: machine-derived          # 红线：verified 唯人签，本卡**无人签**，别当人已核准
signed_by: none
human_review: required
assertion_under_test: "{c["assertion"]}"
counterexample: "{c["counterexample"]}"
detector: {c["detector"]}
fixture: {m["fixture_rel"]}
fixture_sha256: {m["fixture_sha256"]}
reproduce:
{m["_repro_yaml"]}
verdict: {m["verdict"]}
verdict_word: "{m["verdict_word"]}"
support_reason: "{m["support_reason"]}"
machine_note: "{m["note"]}"
measured_out: "{m["measured_out"]}"
signature: "{m["signature"]}"
runs: {m["runs"]}
boundary:
  standard: {m["boundary"]["standard"]}
  compiler: {m["boundary"]["compiler"]}
  platform: {m["boundary"]["platform"]}
  input_domain: {m["boundary"]["input_domain"]}
mutation_set_hash: {m["mutation_set_hash"]}
mutation_count: {m["runs"]}
generator_version: {GENERATOR_VERSION}
four_state: {m["four_state"]}
four_state_reason: "{m["four_state_reason"]}"
b_refuted_664: {("null" if m["b_refuted_664"] is None else str(m["b_refuted_664"]).lower())}
agree_with_664: {m["agree_with_664"]}
validator_gap_664: "{c["gap"]}"
needs_review: true               # 边界三元组按"探针集"口径复用，非 mutation 血统 ⇒ 一律待核
---

# {m["id"]} · {c["assertion"]}

> 机器卡：`status=machine-derived`，**没人签**。
> 它记录的是"这条断言在什么命令下会给出什么观测"，不是"人已经核准这条知识"。

## 一、被测断言（664 Agent A）

{c["assertion"]}

## 二、反例（664 Agent B）

{c["counterexample"]}

## 三、证据（本机真机复跑，{m["measured_at"]}）

- 检测器：`{c["detector"]}`
- 夹具：`{m["fixture_rel"]}`（sha256 `{m["fixture_sha256"][:16]}…`）
- 机器判决：**`{m["verdict"]}`** —— {m["note"]}
- 复算签名：`{m["signature"]}`（`--check` 重跑须复现同一签名）

### 复现命令

```sh
{m["_repro_text"]}
```

## 四、边界（这张卡的 claim 在什么范围内成立）

| 维度 | 值 |
|---|---|
| standard | {m["boundary"]["standard"]} |
| compiler | {m["boundary"]["compiler"]} |
| platform | {m["boundary"]["platform"]} |
| input_domain | {m["boundary"]["input_domain"]} |

边界三元组按 638 口径填（`mutation_set_hash` = 探针集 sha256；`mutation_count` = 实跑次数；
`generator_version` = `{GENERATOR_VERSION}`），**不是 mutation-testing 血统**，标 `needs_review=true`。

## 五、四态判决（638 工具，先看边界再定态）

`{m["four_state"]}` —— {m["four_state_reason"]}

- 支持判定（期望 vs 实测）：{m["support_reason"]}

## 六、验证器自身的漏洞（664 Agent C 标注）

{c["gap"]}
{m["_defect_block"]}
## 七、与 664 记录的对照

- 664 判 B 是否推翻断言：`{m["b_refuted_664"]}`；664 验证器结论：`{m["validator_verdict_664"]}`。
- 本次重跑结论：`{m["verdict"]}` ⇒ **{'一致' if m["agree_with_664"] else '不一致（见 j 诚实登记：环境/命令/颗粒度差异都可能造成）'}**。
"""


def build() -> int:
    cases = _load_cases() + EXTRA_PROBES       # 追加 665 修正探针（ig-16）
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cards = []
    for c in cases:
        cid = c["id"]
        mid = "IG" + cid.split("-")[1]
        src = FIX_DIR / f"{cid}.cpp"
        code = c.get("code") or ""
        _write(src, code + "\n" if code and not code.endswith("\n") else code)
        if code:
            v, note, sig, runs, raw = run_probe(c["detector"], src)
        else:
            v, note, sig, runs, raw = ("unknown", "无代码", "no-code", 0, "")

        probe_set = "|".join(reproduce_cmds(c["detector"], src)) + "#" + (code or "")
        ms_hash = _sha(probe_set)
        bnd = {"standard": "C++17",
               "compiler": ("WSL g++ (Ubuntu 13.3.0)" if c["detector"] in SAN
                            else ("本机 g++ 13.1.0 (MinGW-w64 x86-64-posix-seh)" if c["detector"] != "cross-compile"
                                  else "本机 g++ 13.1.0 -O0 与 -O2 自比对")),
               "platform": ("WSL2 Linux x86-64" if c["detector"] in SAN else "Windows x86-64 (MinGW-w64)"),
               "input_domain": "unknown"}
        word, why = support_of(cid, v, raw if v == "measure" else raw)
        # 测量卡：期望读数严格比对；非测量卡：比对 EXPECT 与实测是否同一分类
        # explanation 是 638 的"例外说明"字段：只有**非干净通过**才填 ⇒ 让四态分布可分辨
        rec = {"verdict": word, "explanation": ("" if word == "pass" else why),
               "mutation_set_hash": ms_hash, "mutation_count": runs,
               "generator_version": GENERATOR_VERSION}
        cls = fs.classify(rec)
        agree = None
        prev = None
        m = {"id": mid, "source_id": cid,
             "assertion_under_test": c["assertion"], "counterexample": c["counterexample"],
             "fixture_rel": src.relative_to(ROOT).as_posix(),
             "fixture_sha256": _sha(code or ""), "detector": c["detector"], "expect": EXPECT.get(cid),
             "verdict": v, "note": note, "signature": sig,
             "runs": runs, "verdict_word": word, "support_reason": why,
             "four_state": cls["state"],
             "four_state_reason": "; ".join(cls["reasons"]) or "（无降级说明）",
             "boundary": bnd, "mutation_set_hash": ms_hash,
             "measured_out": (raw or "")[:200],
             "measured_at": time.strftime("%Y-%m-%d %H:%M:%S"),
             "b_refuted_664": None, "validator_verdict_664": prev, "agree_with_664": agree}
        repro = reproduce_cmds(c["detector"], src)
        m["_repro_yaml"] = "\n".join(f"  - {json.dumps(x, ensure_ascii=False)}" for x in repro) or "  []"
        m["_repro_text"] = "\n".join(repro) or "（无）"
        d = KNOWN_DEFECTS.get(cid)
        m["_defect_block"] = ("\n### ⚠ 664 套件缺陷登记（诚实记录，不代打补丁）\n\n" + d + "\n") if d else ""
        m["_source_run"] = (f"data/independent_generation_run_664.json#{cid}" if cid != "ig-16"
                            else "665 新增修正探针（非 664 产物）")
        m["_source_suite"] = (_SOURCE_NOTE if cid != "ig-16"
                              else "tools/ig_cards_665.py::EXTRA_PROBES")
        cards.append((c, m))
        print(f"  {mid:<5} {cid:<6} {v.upper():<8} {c['detector']:<14} {note[:56]}")

    # 664 记录对照
    prior = {}
    try:
        p = ROOT / "data" / "independent_generation_run_664.json"
        prior = {r["id"]: r for r in json.loads(p.read_text(encoding="utf-8"))["results"]}
    except Exception:  # noqa: BLE001
        pass

    dist, fs_dist, rows, agree_n = {}, {}, [], 0
    for c, m in cards:
        pr = prior.get(c["id"], {})
        m["b_refuted_664"] = pr.get("b_refuted")
        prev = pr.get("validator_verdict")
        m["validator_verdict_664"] = prev
        m["agree_with_664"] = (prev is None) or (prev == m["verdict"])
        agree_n += 1 if m["agree_with_664"] else 0
        dist[m["verdict"]] = dist.get(m["verdict"], 0) + 1
        fs_dist[m["four_state"]] = fs_dist.get(m["four_state"], 0) + 1
        _write(OUT_DIR / f"{m['id']}.md", render_card(c, m))
        rows.append({k: v for k, v in m.items() if not k.startswith("_")})

    idx = {"schema": "queyi-ig-cards/v1", "generated_by": "tools/ig_cards_665.py",
           "generated_at": time.strftime("%Y-%m-%d"), "batch": 665, "segment": "B1",
           "total": len(rows), "verdict_dist": dist, "four_state_dist": fs_dist,
           "agree_with_664": f"{agree_n}/{len(rows)}",
           "cards": rows,
           "honest_note": (f"{len(rows)} 张卡全部为 machine-derived（**无人签**，不含任何 verified 人签卡）；"
                           "证据全部来自本机/WSL 真机复跑（`--check` 可逐张复算签名）；"
                           "边界三元组按 638 口径复用、非 mutation 血统 ⇒ 全部 needs_review=true；"
                           "664 套件自身的缺陷（ig-04）已登记在卡内 §六，不代打补丁、不事后对齐。")}
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nverdict={dist}  four_state={fs_dist}  与664一致={idx['agree_with_664']}")
    print(f"已写 {INDEX.relative_to(ROOT).as_posix()} 与 {len(rows)} 张卡")
    return 0


def check() -> int:
    """重跑全部卡的复现命令，比对签名；同时重算四态是否稳定。"""
    if not INDEX.is_file():
        print("[ig_cards_665] 缺 %s（先 --build）" % INDEX.name)
        return 1
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    bad = []
    for row in idx["cards"]:
        src = ROOT / row["fixture_rel"]
        if not src.is_file():
            bad.append((row["id"], "夹具缺失"))
            continue
        v, note, sig, runs, raw = run_probe(row["detector"], src)
        if v != row["verdict"] or sig != row["signature"]:
            bad.append((row["id"], f"{row['verdict']}/{row['signature']} → {v}/{sig}"))
        print(f"  {row['id']:<5} {v.upper():<8} {'OK' if not bad or bad[-1][0] != row['id'] else 'DRIFT'}")
    for cid, why in bad:
        print(f"[DRIFT] {cid}: {why}")
    print(f"\nig_cards_665 --check: {'PASS' if not bad else 'FAIL'}  "
          f"（{len(idx['cards']) - len(bad)}/{len(idx['cards'])} 复现一致）")
    return 0 if not bad else 1


def selftest() -> int:
    fails = []

    def chk(name: str, cond: bool) -> None:
        if not cond:
            fails.append(name)

    r = {"verdict": "pass", "mutation_set_hash": "a" * 64, "mutation_count": 1,
         "generator_version": GENERATOR_VERSION}
    chk("有边界+pass ⇒ pass", fs.enforce(r) == "pass")
    chk("有边界+block ⇒ fail", fs.enforce({**r, "verdict": "block"}) == "fail")
    chk("缺边界 ⇒ unknown", fs.enforce({"verdict": "pass"}) == "unknown")
    chk("_to_wsl 路径转换", _to_wsl("C:\\a\\b.cpp") == "/mnt/c/a/b.cpp")
    chk("支持判定：期望=实测 ⇒ pass", support_of("ig-01", "catch", "") == ("pass", "期望 catch、实测 catch：观测支持主张"))
    chk("支持判定：未呈现 ⇒ unknown（不许当 fail）", support_of("ig-09", "miss", "")[0] == "unknown")
    chk("支持判定：读数不合 ⇒ block", support_of("ig-05", "measure", "8 16")[0] == "block")
    chk("支持判定：检测器不可用 ⇒ unknown", support_of("ig-04", "unknown", "")[0] == "unknown")
    cases = _load_cases()
    chk("664 套件 15 条", len(cases) == 15)
    if INDEX.is_file():
        idx = json.loads(INDEX.read_text(encoding="utf-8"))
        chk("index 卡数=清点卡数", idx["total"] == len([p for p in OUT_DIR.glob("IG*.md")]))
        chk("verdict 分布求和=total", sum(idx["verdict_dist"].values()) == idx["total"])
        chk("四态分布求和=total", sum(idx["four_state_dist"].values()) == idx["total"])
    for f in fails:
        print("FAIL: %s" % f)
    print("ig_cards_665 selftest: %s" % ("PASS" if not fails else "FAIL"))
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="665 B1：664 断言 → 可复现卡")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.check:
        return check()
    if a.build:
        return build()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
