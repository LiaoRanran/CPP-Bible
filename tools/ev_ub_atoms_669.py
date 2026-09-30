#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""ev_ub_atoms_669.py — 669 P0-2：给 668 的 5 张机器卡补**独立证据卡**（EV-*-669）。

病（668 §5.2 诚实登记，本批实跑复核）
====================================
668 把 5 张新卡（ATOM-UB-WRAP/OOB/NULLDEREF/DIVZERO-001、ATOM-MEM-NEWARR-001）的机器证据
**内联**在卡面 `evidence_668:` 里，没有独立的 `evidence/**/EV-*.md`。后果有三条，全部实跑复现：
  ① `tests/test_prop_graph.py` 3 条红：命题的锚来源集合变成 `{evidence, none}`，而判据要求
     **只有** `evidence`（`by_anchor_source["none"] == 0` 亦随之破）；
  ② `gate_engine` 的 `OBSERVATION-NEEDS-ARTIFACT`（block）：observation 命题缺"机器闭环支撑"；
  ③ **30 条 gate block**（6 条规则 × 5 张卡），不是"只有 3 条测试红"。

治法（本工具）
==============
把 `data/cards_665/index_665.json` 里**已经跑过**的检测器记录落成正式证据卡，一件不多一件不少：

* **工件** = 用**本机编译器**对**同一夹具**做 `-S` 的汇编产物（新增 `Examples/atoms/_atom_*_669.asm`，
  sha256 现算现写）。断言用**跨编译器实测过**的结构指纹（见 `ASSERT_NOTE`）。
* **记录** = 由本工具读 index 生成**探针夹具**（`data/cards_669/probe_*_669.cpp`，`std::puts` 一行），
  探针把记录**打印出来** ⇒ replay 的 run_match 走"编译器构建的可执行文件"，
  **不引入 python/shell 依赖**（CI 与本机都能跑），且数值**一律从 index 读出**（不手打）。
* **边缘** = 卡面显式写清本卡**不**重跑检测器（`reproduce` 给出 665 的原法：WSL + sanitizer），
  并把 `expected_sanitizer` 声明好 ⇒ 在**有 libasan/libubsan 的环境（CI Linux）**上，
  replay 的 sanitizer 校验会**真的重跑检测器**（那是第二份独立测量，不是豁免）。

红线
====
* **不代签**：证据卡 `status: machine-derived`；原子卡的 `verified_by` 只写 `machine:*`（无 human:*）。
* **不改** index_665.json / 夹具 / 664·665 产物 / 既有 56 张证据卡；只**新增**卡、探针与工件。
* 数字一律脚本现算；`--check` 可复核卡面记录与事实源是否漂移。

用法
====
    python tools/ev_ub_atoms_669.py --build     # 生成探针 + 汇编工件 + 5 张证据卡
    python tools/ev_ub_atoms_669.py --check     # 漂移复核（夹具 sha / 工件 sha / 记录一致性）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

INDEX = ROOT / "data" / "cards_665" / "index_665.json"
PROBE_DIR = ROOT / "data" / "cards_669"
GENERATOR_VERSION = "ev_ub_atoms_669/v1"

#: 每张卡：原子卡 → 665 记录 → 证据卡 → 工件/探针/断言
#: `artifact_assert` 的选择依据（**实测**，不是猜）：同一夹具在
#: MinGW GCC 15.3（`C:/Qt/Tools/mingw1530_64`）与 WSL Linux GCC 13.3 下各编译一次，
#: 只保留**两边都成立**的结构指纹 ⇒ 跨编译器分支（CI）也真的能校验。
CARDS: list[dict] = [
    {
        "atom": "ATOM-UB-WRAP-001",
        "atom_path": "atoms/ub/ATOM-UB-WRAP-001.md",
        "src_id": "ig-01",
        "ev_id": "EV-UB-WRAP-669",
        "ev_rel": "evidence/ub/EV-UB-WRAP-669.md",
        "artifact": "Examples/atoms/_atom_ub_wrap_669.asm",
        "probe": "data/cards_669/probe_ub_wrap_669.cpp",
        "assert": [{"kind": "contains", "text": "mov\\teax, 1"}],
        "asm_obs": ("整段 UB 体被优化器**折叠成常量返回**：`main` 里只有 `mov eax, 1` + `ret`，"
                    "连 `x += 1` 的 `add` 和 `x < 0` 的比较都消失了（MinGW 15.3 与 Linux 13.3 同形）。"),
        "san": "ub",
        "san_flag": "undefined",
    },
    {
        "atom": "ATOM-UB-OOB-001",
        "atom_path": "atoms/ub/ATOM-UB-OOB-001.md",
        "src_id": "ig-02",
        "ev_id": "EV-UB-OOB-669",
        "ev_rel": "evidence/ub/EV-UB-OOB-669.md",
        "artifact": "Examples/atoms/_atom_ub_oob_669.asm",
        "probe": "data/cards_669/probe_ub_oob_669.cpp",
        "assert": [{"kind": "contains", "text": "mov\\teax, 1"}],
        "asm_obs": ("越界写在 -O2 下**整条消失**（数组、索引、写入全被消掉，只剩 `mov eax, 1`）——"
                    "这正是「越界是 UB ⇒ 优化器可假定不发生」的机器形态；"
                    "也解释了为什么它**不保证崩**（运行期实测见卡面 §2）。"),
        "san": "address",
        "san_flag": "address",
    },
    {
        "atom": "ATOM-UB-NULLDEREF-001",
        "atom_path": "atoms/ub/ATOM-UB-NULLDEREF-001.md",
        "src_id": "ig-07",
        "ev_id": "EV-UB-NULLDEREF-669",
        "ev_rel": "evidence/ub/EV-UB-NULLDEREF-669.md",
        "artifact": "Examples/atoms/_atom_ub_nullderef_669.asm",
        "probe": "data/cards_669/probe_ub_nullderef_669.cpp",
        "assert": [{"kind": "contains_any", "texts": ["mov\\tDWORD PTR ds:0, 0", "ud2"]}],
        "asm_obs": ("`main` 里是**对地址 0 的真实写入**（`mov DWORD PTR ds:0, 0`）后接 `ud2`"
                    "（不可达标记）——编译器没有把空指针解引用「优化掉」，"
                    "而是照 UB 的语义生成了会崩的代码（两平台同形）。"),
        "san": "address",
        "san_flag": "address",
    },
    {
        "atom": "ATOM-UB-DIVZERO-001",
        "atom_path": "atoms/ub/ATOM-UB-DIVZERO-001.md",
        "src_id": "ig-08",
        "ev_id": "EV-UB-DIVZERO-669",
        "ev_rel": "evidence/ub/EV-UB-DIVZERO-669.md",
        "artifact": "Examples/atoms/_atom_ub_divzero_669.asm",
        "probe": "data/cards_669/probe_ub_divzero_669.cpp",
        "assert": [{"kind": "contains", "text": "idiv"}],
        "asm_obs": ("`volatile` 让被除数/除数必须真的从内存读（`mov` 两次）⇒ 除法指令 `idiv` 真实存在、"
                    "**不会被折叠**；两平台同形。这条与 ig-01/02 的「整段消失」形成对照："
                    "同是 UB，能不能被优化器吃掉取决于它是否可证。"),
        "san": "ub",
        "san_flag": "undefined",
    },
    {
        "atom": "ATOM-MEM-NEWARR-001",
        "atom_path": "atoms/mem/ATOM-MEM-NEWARR-001.md",
        "src_id": "ig-14",
        "ev_id": "EV-MEM-NEWARR-669",
        "ev_rel": "evidence/mem/EV-MEM-NEWARR-669.md",
        "artifact": "Examples/atoms/_atom_mem_newarr_669.asm",
        "probe": "data/cards_669/probe_mem_newarr_669.cpp",
        "assert": [{"kind": "contains_any", "texts": ["_Zna", "_ZdlPv"]}],
        "asm_obs": ("`new int[4]` → `operator new[]`（`_Zna…`），`delete p` → `operator delete(void*)`"
                    "（`_ZdlPv…`）——**两个函数族不同**就是「配对不匹配」的机器指纹；"
                    "拼写随平台变（MinGW `_Znay`/`_ZdlPvy`、Linux `_Znam@PLT`/`_ZdlPvm@PLT`），"
                    "故断言取族名子串 `_Zna` / `_ZdlPv`。"),
        "san": "address",
        "san_flag": "address",
    },
]

ASSERT_NOTE = ("断言依据（实测）：同一夹具在 MinGW GCC 15.3 与 WSL Linux GCC 13.3 下各 `-O2 -S` "
               "编译一次，只保留两边都成立的指纹 ⇒ 跨编译器分支（CI）也是真校验。")


def _sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _load_index() -> dict[str, dict]:
    idx = json.loads(INDEX.read_text(encoding="utf-8"))
    return {c["source_id"]: c for c in idx["cards"]}


def _record_line(card: dict, row: dict, file_sha: str) -> str:
    """探针要打印的**一行记录**（数值全部现算/现读：index_665.json + 夹具文件字节，不手打）。"""
    return (f"{card['ev_id']} rec=index_665/{card['src_id']} detector={row['detector']} "
            f"verdict={row['verdict']} sig={row['signature']} "
            f"fixture_file_sha={file_sha} index_fixture_sha={row['fixture_sha256']} "
            f"measured_at={row['measured_at'].replace(' ', 'T')}")


def _probe_source(line: str) -> str:
    return (
        "// 669 P0-2 · 记录复算探针（**由 tools/ev_ub_atoms_669.py 从 data/cards_665/index_665.json 生成**，勿手改）\n"
        "// 作用：把 665 的检测器记录变成**编译器可构建**的一行输出 ⇒ replay 的 run_match 可在任何平台复核\n"
        "// （记录漂移 ⇒ 本探针输出与卡面 actual.run_* 不一致 ⇒ refute）。检测器**复跑**见卡面 reproduce。\n"
        "#include <cstdio>\n"
        "int main() {\n"
        f'    std::puts("{line}");\n'
        "    return 0;\n"
        "}\n"
    )


def _compile_artifact(src_rel: str, out_rel: str) -> None:
    from toolchain import resolve_gpp
    out = ROOT / out_rel
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [resolve_gpp(), "-std=c++17", "-O2", "-S", "-masm=intel", src_rel, "-o", out_rel]
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                       errors="replace", timeout=300)
    if r.returncode != 0:
        raise SystemExit(f"[ev669] 工件编译失败 rc={r.returncode}：{(r.stderr or '')[:300]}")


def _to_wsl(rel: str) -> str:
    """仓库相对路径 → WSL 视角的 /mnt/<盘>/… 路径。"""
    p = (ROOT / rel).as_posix()
    return "/mnt/" + p[0].lower() + p[2:] if len(p) > 1 and p[1] == ":" else p


def _run(cmd: list[str], timeout: int = 300, cwd: Path | None = None) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, errors="replace",
                           timeout=timeout, cwd=str(cwd or ROOT))
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except (OSError, subprocess.TimeoutExpired) as exc:
        return -99, f"EXC: {type(exc).__name__}: {exc}"


def _detector_shell(row: dict, flag: str) -> str:
    """665 原法（WSL + sanitizer）的检测器命令；产物落 /tmp，不碰仓库。"""
    w = _to_wsl(row["fixture_rel"])
    tag = row["source_id"]
    return (f"g++ -std=c++17 -O1 -g -fsanitize={flag} -pthread {w} -o /tmp/ev669_{tag}"
            f" && /tmp/ev669_{tag}")


def reprobe() -> int:
    """**本机真机复跑**：WSL 检测器日志 + Windows 探针输出 → 两份留痕（各平台一份）。

    为什么必须做（不是可选装饰）：`EV-MATRIX-UNBACKED` 要求"多编译器声明要有多平台留痕"，
    而"留痕"必须是**可核对的文件**。本函数把两平台各跑一次并把原始输出**落盘进仓库**：
      · `Examples/atoms/_atom_*_669.out`     —— WSL 侧：检测器（ubsan/asan）原始输出
      · `Examples/atoms/_atom_*_669.win.out` —— Windows 侧：记录探针在 MinGW 下的输出
    两份都含头部（命令/夹具文件 sha/rc/签名核对结论），是"当时真的跑过"的载体。
    """
    from toolchain import resolve_gpp
    idx = _load_index()
    from datetime import datetime
    stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    bad: list[str] = []
    for card in CARDS:
        row = idx[card["src_id"]]
        fx = ROOT / row["fixture_rel"]
        file_sha = _sha_file(fx)
        line = _record_line(card, row, file_sha)
        tag = card["ev_id"].lower().replace("-", "_")
        # ① WSL 侧：检测器真跑
        sh = _detector_shell(row, card["san_flag"])
        rc, out = _run(["wsl", "-e", "bash", "-lc", sh], timeout=300)
        sig_ok = row["signature"].split(":", 1)[-1].lower() in out.lower()
        log_a = ROOT / "Examples" / "atoms" / f"_atom_{tag.split('_', 1)[1]}.out"
        log_a.write_text(
            f"# 669 P0-2 · 检测器复跑留痕（**WSL 侧**）—— {card['ev_id']}\n"
            f"# 夹具：{row['fixture_rel']}（文件 sha256 {file_sha}）\n"
            f"# 命令：wsl -e bash -lc \"{sh}\"\n"
            f"# 时间：{stamp}   rc={rc}   期望签名：{row['signature']}   "
            f"命中：{'是' if sig_ok else '否'}\n"
            f"# 说明：本文件是 **真机复跑** 的原始输出（不是转录）；检测器需 libasan/libubsan，"
            f"故只能在 WSL 侧跑（MinGW 无该运行库）。\n"
            f"---\n{out}\n", encoding="utf-8", newline="\n")
        if not sig_ok:
            bad.append(f"{card['ev_id']}: WSL 复跑未命中签名 {row['signature']!r}")
        # ② Windows 侧：记录探针真跑（同一条 record 行必须在另一平台复现）
        exe = ROOT / "build" / f"_ev669_probe_{card['src_id']}.exe"
        exe.parent.mkdir(exist_ok=True)
        rc2, out2 = _run([resolve_gpp(), "-std=c++17", "-O2", card["probe"], "-o",
                          str(exe.relative_to(ROOT)).replace("\\", "/")])
        if rc2 == 0:
            rc2, out2 = _run([str(exe)])
        win_ok = line in out2
        log_b = ROOT / "Examples" / "atoms" / f"_atom_{tag.split('_', 1)[1]}.win.out"
        log_b.write_text(
            f"# 669 P0-2 · 记录探针留痕（**Windows/MinGW 侧**）—— {card['ev_id']}\n"
            f"# 探针：{card['probe']}   夹具：{row['fixture_rel']}   时间：{stamp}\n"
            f"# 命令：g++ -std=c++17 -O2 {card['probe']} -o build/_ev669_probe_{card['src_id']}.exe"
            f" && build/_ev669_probe_{card['src_id']}.exe\n"
            f"# rc={rc2}   记录行复现：{'是' if win_ok else '否'}\n"
            f"---\n{out2}\n", encoding="utf-8", newline="\n")
        if not win_ok:
            bad.append(f"{card['ev_id']}: Windows 侧探针输出与记录不符")
        print(f"  {card['ev_id']:<22} WSL 检测器={'OK' if sig_ok else 'DRIFT'}  "
              f"Win 探针={'OK' if win_ok else 'DRIFT'}")
    for b in bad:
        print(f"[DRIFT] {b}")
    print(f"[ev669] reprobe: {'PASS' if not bad else 'FAIL'}（{len(CARDS) - len(bad)}/{len(CARDS)} 双平台留痕一致）")
    return 0 if not bad else 1


def _render_card(card: dict, row: dict, sha: str, toolchain: str, line: str,
                 file_sha: str) -> str:
    a = card["assert"][0]
    # 断言文本**逐字**写进卡（`\t` 保持两个字面字符：replay 侧会归一，gate 侧的 pyyaml 会解成真制表符）
    assert_txt = (f'{{kind: {a["kind"]}, text: "{a["text"]}"}}' if a["kind"] == "contains"
                  else '{kind: %s, texts: [%s]}' % (
                      a["kind"], ", ".join(f'"{t}"' for t in a["texts"])))
    prod = (f'g++ -std=c++17 -O2 -S -masm=intel {row["fixture_rel"]} -o {card["artifact"]}')
    fixture_sha16 = row["fixture_sha256"][:16]
    stem = "_atom_" + card["ev_id"].lower().replace("ev-", "").replace("-", "_")
    det_log = f"Examples/atoms/{stem}.out"
    probe_log = f"Examples/atoms/{stem}.win.out"
    return f"""---
id: {card["ev_id"]}
serves: [{card["atom"]}]
status: machine-derived          # 机器产出，**无人签**（human_review 另见原子卡）
kind: run
hypothesis: >-
  665 的独立生成探针 `{card["src_id"]}`（断言「{row["assertion_under_test"]}」）在真机检测器下
  得到判决 **{row["verdict"]}**（签名 `{row["signature"]}`，检测器 `{row["detector"]}`）——
  即该断言在**本夹具**上被当场{'否定' if row["verdict"] == 'catch' else '未呈现'}；本卡把这条**记录**钉住，
  并把「同一夹具在本机的汇编形态」作为第二个可复算载体。
controlled_vars: >-
  同一夹具文件（**文件字节** sha256 锁定 = `{file_sha[:16]}…`）+ 同一检测器；唯一变量 = 检测器是否报告。
  两档分列不混：**检测器档** -O1（665 原法，WSL g++ 13.3 + {row["detector"]}）、
  **工件档** -O2 `-S`（本机 {toolchain}）。本卡的机器口径（command）复核的是「记录未漂移」
  （夹具字节 + index 记录 + 工件 sha 三者）；检测器**复跑**见 `reproduce`（需 libasan/libubsan 的环境）。
matrix:
  compiler: [{toolchain}, WSL g++ (Ubuntu 13.3.0)]
  std: [c++17]
  opt: [-O1, -O2]
  arch: [x86-64]
fixture: {row["fixture_rel"]}
command: |
  {prod}
  g++ -std=c++17 -O2 {card["probe"]} -o build/_ev669_{card["src_id"].replace("-", "_")}.exe
  ./build/_ev669_{card["src_id"].replace("-", "_")}.exe
artifact: {card["artifact"]}
artifact_version: 1
artifact_producer: {prod}
artifact_sha256: {sha}
artifact_compiler: {toolchain}
artifact_assert:
  - {assert_txt}
detector_log: {det_log}
probe_log: {probe_log}
expected_key: run_record
expected:
  run_record: >-
    记录复算：探针输出的 record 行必须与事实源逐字一致 —— detector / verdict / signature /
    measured_at 来自 `data/cards_665/index_665.json`，`fixture_file_sha` 现算自夹具**文件字节**，
    `index_fixture_sha` 是 665 记的（= sha(code)，差一个结尾 LF；见 §1 缺陷登记）。
expected_sanitizer: [{card["san"]}]
actual:
  run_record: "{line}"
verdict: confirm
falsification: >-
  三条可失败对照（都能量化）：① 夹具**文件** sha 若从 `{file_sha[:16]}…` 变为**任何**其它值
  （哪怕只改一个字节或结尾换行）⇒ 本卡记录的观测对象已换，作废；② 665 记录里 verdict 若是 `miss`
  而非 `{row["verdict"]}`（取值只有 catch/miss/unknown）⇒ 「检测器可见」不成立；
  ③ 汇编断言 {assert_txt} 若消失（例如改用 `-O0`：折叠不再发生，`main` 里会出现真实的读改写与比较）⇒
  「该 UB 已被优化器吸收」这条结构观察只在 -O2 档成立。三条任一失败即本卡作废。
reproduce: |
  # 检测器复跑（665 原法；需 libasan/libubsan——本机 MinGW 无该运行库，CI Linux 有）
  wsl -e bash -lc "g++ -std=c++17 -O1 -g -fsanitize={card["san_flag"]} -pthread {row["fixture_rel"]} -o /tmp/ev669_{card["src_id"]} && /tmp/ev669_{card["src_id"]}"
  # 记录复算（本卡 command 的机器口径）
  python tools/ev_ub_atoms_669.py --check
---

# {card["ev_id"]} · 「{row["assertion_under_test"]}」的机器记录（{card["src_id"]}）

> 机器卡：`status: machine-derived`，**没有人签**。它记录的是「在什么命令下会观测到什么」，
> 不是「人已核准这条知识」。要把它变成人级结论，须走 `atoms/{Path(card["atom_path"]).parent.name}/{card["atom"]}.md` 的人审。

## 1. 被测断言（664 独立生成）/ 反例（665 复跑）

| 项 | 值 |
|---|---|
| 断言 | {row["assertion_under_test"]} |
| 反例 | {row["counterexample"]} |
| 夹具 | `{row["fixture_rel"]}` |
| 夹具**文件** sha256 | `{file_sha}`（`sha256sum` 可复算；探针 `fixture_file_sha` 即此值） |
| index 记的 sha256 | `{row["fixture_sha256"]}`（665 口径，**差一个结尾 LF** —— 见下方缺陷登记） |
| 夹具源码 | `{_fixture_code(row["fixture_rel"])}` |

> ⚠ **665 口径缺陷（本批实测登记，不代 665 打补丁）**：`index_665.json` 的 `fixture_sha256`
> 是**源码字符串**的 sha（`sha(code)`），而不是**文件字节**的 sha —— 665 落盘时补了一个结尾 LF
> （`_write(code + "\\n")`），两者恰好差一个 `\\n`：
> `index = {row["fixture_sha256"][:16]}…`（= `sha(code)`）、`file = {file_sha[:16]}…`（= `sha(code + "\\n")`）。
> ⇒ 任何「拿 index 里的 sha 去校验文件字节」的写法都会误判（差一字节）；反过来，
> **只改结尾换行不会被 index 的 sha 发现**。本卡两个都记：`fixture_file_sha` 用于"文件未漂移"的
> 机器判据（探针输出 + `--check`），`index_fixture_sha` 用于与 665 产物对账。

## 2. 真机观测记录（665 实跑，{row["measured_at"]}）

| 项 | 值 |
|---|---|
| 检测器 | `{row["detector"]}`（WSL g++ Ubuntu 13.3.0 / `-O1 -g`） |
| 判决 | **{row["verdict"]}**（期望 `{row["expect"]}`） |
| 签名 | `{row["signature"]}` |
| 实跑次数 | {row["runs"]} |
| 664 对照 | 判 B 是否推翻断言：`{str(row["b_refuted_664"]).lower()}`；664 验证器结论：`{row["validator_verdict_664"]}` |

实测输出（前几行，完整见 `data/cards_665/index_665.json`）：

```
{_excerpt(row["measured_out"])}
```

## 2b. 669 双平台**实跑留痕**（各平台一份，可核对）

| 平台 | 留痕文件 | 内容 |
|---|---|---|
| WSL（Linux x86-64） | `{det_log}` | 检测器 **真跑**的原始输出（ubsan/asan；MinGW 无 libasan/libubsan，故只能在此侧跑） |
| Windows（MinGW x86-64） | `{probe_log}` | 记录探针在另一平台的输出（同一条 `record=` 行必须复现） |

两份都由 `python tools/ev_ub_atoms_669.py --reprobe` **现跑现写**（不是转录）：头部记命令、夹具文件 sha、
rc 与签名/记录行的核对结论；`--check` 复核其存在性与一致性。

**本卡的 command 不重跑检测器**：Windows/MinGW **没有 libasan/libubsan**（本机实测 `ld: cannot find -lasan / -lubsan`），
故 command 走「记录复算」（探针 + 夹具文件 sha 链），`reproduce` 给出检测器原法；
在**有 sanitizer 运行库的环境**（CI Linux）上，replay 的 sanitizer 校验会
**真的重跑一遍检测器**（`expected_sanitizer: [{card["san"]}]` ⇒ 报出即计入 confirm，是本卡的第三份独立测量）。

## 3. 第二个载体：本机汇编形态（工件档 -O2）

工件 `{card["artifact"]}`（`{sha[:16]}…`，{toolchain}）的 `main` 里：

{card["asm_obs"]}

{ASSERT_NOTE}

## 4. 边界（这张卡**不**声明什么）

- 不声明"换编译器/平台/标准版本仍然如此"：矩阵只覆盖 `{toolchain}` 与 `WSL g++ (Ubuntu 13.3.0)`、
  C++17、x86-64、`-O1/-O2`。
- 不声明**语义级**结论（"所有同类写法都会被检测器抓到"）：本卡只钉住"这一支夹具上观测到了什么"。
- 不声明**人已核准**：`status: machine-derived`，人级结论见原子卡的 `human_review: required`。
- 记录口径：`record=...` 行由 `tools/ev_ub_atoms_669.py` 从 `data/cards_665/index_665.json` **读出**生成
  （不是手打）；index 一旦重跑漂移，本卡 `--check` 与 replay 的 run_match 都会红。
"""


def _fixture_code(rel: str) -> str:
    p = ROOT / rel
    txt = p.read_text(encoding="utf-8").strip() if p.is_file() else "（缺失）"
    return txt.replace("`", "'")


def _excerpt(s: str, n: int = 260) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[:n] + "\n…[truncated]"


def _toolchain_id() -> str:
    import atom_evidence_replay as replay
    return replay._current_toolchain_id()


def build() -> int:
    idx = _load_index()
    tc = _toolchain_id()
    PROBE_DIR.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for card in CARDS:
        row = idx.get(card["src_id"])
        if not row:
            return _fail(f"index_665.json 缺 {card['src_id']}")
        fx = ROOT / row["fixture_rel"]
        if not fx.is_file():
            return _fail(f"夹具缺失：{row['fixture_rel']}")
        file_sha = _sha_file(fx)
        if not row.get("fixture_sha256"):
            return _fail(f"{card['src_id']} index 缺 fixture_sha256（记录不完整）")
        line = _record_line(card, row, file_sha)
        probe = ROOT / card["probe"]
        probe.write_text(_probe_source(line), encoding="utf-8", newline="\n")
        _compile_artifact(row["fixture_rel"], card["artifact"])
        sha = _sha_file(ROOT / card["artifact"])
        ev = ROOT / card["ev_rel"]
        ev.parent.mkdir(parents=True, exist_ok=True)
        ev.write_text(_render_card(card, row, sha, tc, line, file_sha),
                      encoding="utf-8", newline="\n")
        written.append(card["ev_rel"])
        print(f"  {card['ev_id']:<22} {card['src_id']:<6} {row['detector']:<7} "
              f"{row['verdict']:<8} artifact={sha[:16]}…")
    print(f"[ev669] 已写 {len(written)} 张证据卡 + {len(CARDS)} 个探针 + {len(CARDS)} 个工件"
          f"（生成器 {GENERATOR_VERSION}）")
    print("[ev669] 下一步：把这 5 张卡的 id 挂进对应原子卡的 `evidence:`（命题级 + 顶层）")
    return 0


def check() -> int:
    """漂移复核：夹具 sha / 工件 sha / 探针记录 / 卡面记录 四者必须一致。"""
    idx = _load_index()
    bad: list[str] = []
    for card in CARDS:
        row = idx.get(card["src_id"])
        if not row:
            bad.append(f"{card['ev_id']}: index 缺 {card['src_id']}")
            continue
        fx = ROOT / row["fixture_rel"]
        if not fx.is_file():
            bad.append(f"{card['ev_id']}: 夹具缺失（{row['fixture_rel']}）")
            continue
        file_sha = _sha_file(fx)
        ev = ROOT / card["ev_rel"]
        if not ev.is_file():
            bad.append(f"{card['ev_id']}: 证据卡缺失")
            continue
        text = ev.read_text(encoding="utf-8")
        line = _record_line(card, row, file_sha)
        if file_sha not in text:
            bad.append(f"{card['ev_id']}: 夹具**文件** sha 漂移（{file_sha[:16]}…）")
        if row["fixture_sha256"] not in text:
            bad.append(f"{card['ev_id']}: index 记录的 sha 未出现在卡面（对账断链）")
        if line not in text:
            bad.append(f"{card['ev_id']}: 卡面记录与 index 不一致（index 漂移？重跑 --build）")
        art = ROOT / card["artifact"]
        if not art.is_file():
            bad.append(f"{card['ev_id']}: 工件缺失 {card['artifact']}")
        else:
            sha = _sha_file(art)
            if f"artifact_sha256: {sha}" not in text:
                bad.append(f"{card['ev_id']}: 工件 sha 与卡面不符（工件被改/卡未重生成）")
        probe = ROOT / card["probe"]
        if not probe.is_file() or f'std::puts("{line}")' not in probe.read_text(encoding="utf-8"):
            bad.append(f"{card['ev_id']}: 探针缺失或与 index 记录不一致")
        # 双平台留痕（669 新增）：存在 + 内容可核对
        stem = "_atom_" + card["ev_id"].lower().replace("ev-", "").replace("-", "_")
        det_log = ROOT / f"Examples/atoms/{stem}.out"
        probe_log = ROOT / f"Examples/atoms/{stem}.win.out"
        for lg, what, needle in ((det_log, "检测器留痕", row["signature"].split(":", 1)[-1]),
                                 (probe_log, "探针留痕", line)):
            if not lg.is_file():
                bad.append(f"{card['ev_id']}: {what}缺失（{lg.name}）⇒ 跑 --reprobe")
                continue
            t = lg.read_text(encoding="utf-8", errors="replace")
            if needle.lower() not in t.lower():
                bad.append(f"{card['ev_id']}: {what}内容不含期望（{needle[:32]!r}）")
            if file_sha not in t and what == "检测器留痕":
                bad.append(f"{card['ev_id']}: {what}未记录当前夹具文件 sha（夹具已变）")
    for b in bad:
        print(f"[DRIFT] {b}")
    print(f"[ev669] check: {'PASS' if not bad else 'FAIL'}（{len(CARDS) - len(bad)}/{len(CARDS)} 一致）")
    return 0 if not bad else 1


def _fail(msg: str) -> int:
    print(f"[ev669] ❌ {msg}")
    return 1


def selftest() -> int:
    fails: list[str] = []

    def chk(name: str, cond: bool) -> None:
        if not cond:
            fails.append(name)

    chk("5 张卡映射齐", len(CARDS) == 5 and len({c["ev_id"] for c in CARDS}) == 5)
    chk("记录行无 `|`（run_* 分隔符）", all("|" not in _record_line(c, {
        "detector": "d", "verdict": "v", "signature": "s", "fixture_sha256": "0" * 64,
        "measured_at": "2026-01-01 00:00:00"}, "0" * 64) for c in CARDS))
    chk("每卡一个断言且 kind 合法", all(
        len(c["assert"]) == 1 and c["assert"][0]["kind"] in ("contains", "contains_any")
        for c in CARDS))
    for f in fails:
        print(f"FAIL: {f}")
    print(f"ev_ub_atoms_669 selftest: {'PASS' if not fails else 'FAIL'}")
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="669 P0-2：5 张机器卡的独立证据卡生成/复核")
    ap.add_argument("--build", action="store_true",
                    help="生成探针 + 汇编工件 + 证据卡（并按需复跑双平台留痕）")
    ap.add_argument("--reprobe", action="store_true",
                    help="真机复跑：WSL 检测器日志 + Windows 探针输出（两份留痕落盘）")
    ap.add_argument("--check", action="store_true", help="漂移复核（只读）")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.check:
        return check()
    if a.reprobe:
        return reprobe()
    if a.build:
        rc = build()
        if rc:
            return rc
        print("[ev669] --build 连带复跑双平台留痕（WSL + Windows）")
        return reprobe()
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
