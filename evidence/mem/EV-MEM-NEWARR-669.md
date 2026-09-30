---
id: EV-MEM-NEWARR-669
serves: [ATOM-MEM-NEWARR-001]
status: machine-derived          # 机器产出，**无人签**（human_review 另见原子卡）
kind: run
hypothesis: >-
  665 的独立生成探针 `ig-14`（断言「new[] 分配的数组可以用 delete 释放」）在真机检测器下
  得到判决 **catch**（签名 `hit:AddressSanitizer`，检测器 `asan`）——
  即该断言在**本夹具**上被当场否定；本卡把这条**记录**钉住，
  并把「同一夹具在本机的汇编形态」作为第二个可复算载体。
controlled_vars: >-
  同一夹具文件（**文件字节** sha256 锁定 = `cb38bdb21e113142…`）+ 同一检测器；唯一变量 = 检测器是否报告。
  两档分列不混：**检测器档** -O1（665 原法，WSL g++ 13.3 + asan）、
  **工件档** -O2 `-S`（本机 GCC 15.3.0 (MinGW-w64)）。本卡的机器口径（command）复核的是「记录未漂移」
  （夹具字节 + index 记录 + 工件 sha 三者）；检测器**复跑**见 `reproduce`（需 libasan/libubsan 的环境）。
matrix:
  compiler: [GCC 15.3.0 (MinGW-w64), WSL g++ (Ubuntu 13.3.0)]
  std: [c++17]
  opt: [-O1, -O2]
  arch: [x86-64]
fixture: data/cards_665/fixtures/ig-14.cpp
command: |
  g++ -std=c++17 -O2 -S -masm=intel data/cards_665/fixtures/ig-14.cpp -o Examples/atoms/_atom_mem_newarr_669.asm
  g++ -std=c++17 -O2 data/cards_669/probe_mem_newarr_669.cpp -o build/_ev669_ig_14.exe
  ./build/_ev669_ig_14.exe
artifact: Examples/atoms/_atom_mem_newarr_669.asm
artifact_version: 1
artifact_producer: g++ -std=c++17 -O2 -S -masm=intel data/cards_665/fixtures/ig-14.cpp -o Examples/atoms/_atom_mem_newarr_669.asm
artifact_sha256: 27ee6ce96da0f9ed1e3f9a9dcb5344a48df9aff58155e08560df510d040e1704
artifact_compiler: GCC 15.3.0 (MinGW-w64)
artifact_assert:
  - {kind: contains_any, texts: ["_Zna", "_ZdlPv"]}
detector_log: Examples/atoms/_atom_mem_newarr_669.out
probe_log: Examples/atoms/_atom_mem_newarr_669.win.out
expected_key: run_record
expected:
  run_record: >-
    记录复算：探针输出的 record 行必须与事实源逐字一致 —— detector / verdict / signature /
    measured_at 来自 `data/cards_665/index_665.json`，`fixture_file_sha` 现算自夹具**文件字节**，
    `index_fixture_sha` 是 665 记的（= sha(code)，差一个结尾 LF；见 §1 缺陷登记）。
expected_sanitizer: [address]
actual:
  run_record: "EV-MEM-NEWARR-669 rec=index_665/ig-14 detector=asan verdict=catch sig=hit:AddressSanitizer fixture_file_sha=cb38bdb21e113142457c900c00b02712fbba8a5fd65e6caa0cd39cf571bde71d index_fixture_sha=3557ed2c40078bff7c4aa77f858d25513ee08cbbcd7e975dd67e35dd02855c5c measured_at=2026-09-29T00:18:22"
verdict: confirm
falsification: >-
  三条可失败对照（都能量化）：① 夹具**文件** sha 若从 `cb38bdb21e113142…` 变为**任何**其它值
  （哪怕只改一个字节或结尾换行）⇒ 本卡记录的观测对象已换，作废；② 665 记录里 verdict 若是 `miss`
  而非 `catch`（取值只有 catch/miss/unknown）⇒ 「检测器可见」不成立；
  ③ 汇编断言 {kind: contains_any, texts: ["_Zna", "_ZdlPv"]} 若消失（例如改用 `-O0`：折叠不再发生，`main` 里会出现真实的读改写与比较）⇒
  「该 UB 已被优化器吸收」这条结构观察只在 -O2 档成立。三条任一失败即本卡作废。
reproduce: |
  # 检测器复跑（665 原法；需 libasan/libubsan——本机 MinGW 无该运行库，CI Linux 有）
  wsl -e bash -lc "g++ -std=c++17 -O1 -g -fsanitize=address -pthread data/cards_665/fixtures/ig-14.cpp -o /tmp/ev669_ig-14 && /tmp/ev669_ig-14"
  # 记录复算（本卡 command 的机器口径）
  python tools/ev_ub_atoms_669.py --check
---

# EV-MEM-NEWARR-669 · 「new[] 分配的数组可以用 delete 释放」的机器记录（ig-14）

> 机器卡：`status: machine-derived`，**没有人签**。它记录的是「在什么命令下会观测到什么」，
> 不是「人已核准这条知识」。要把它变成人级结论，须走 `atoms/mem/ATOM-MEM-NEWARR-001.md` 的人审。

## 1. 被测断言（664 独立生成）/ 反例（665 复跑）

| 项 | 值 |
|---|---|
| 断言 | new[] 分配的数组可以用 delete 释放 |
| 反例 | UB（mismatched alloc/dealloc） |
| 夹具 | `data/cards_665/fixtures/ig-14.cpp` |
| 夹具**文件** sha256 | `cb38bdb21e113142457c900c00b02712fbba8a5fd65e6caa0cd39cf571bde71d`（`sha256sum` 可复算；探针 `fixture_file_sha` 即此值） |
| index 记的 sha256 | `3557ed2c40078bff7c4aa77f858d25513ee08cbbcd7e975dd67e35dd02855c5c`（665 口径，**差一个结尾 LF** —— 见下方缺陷登记） |
| 夹具源码 | `int main(){int*p=new int[4]; delete p; return 0;}` |

> ⚠ **665 口径缺陷（本批实测登记，不代 665 打补丁）**：`index_665.json` 的 `fixture_sha256`
> 是**源码字符串**的 sha（`sha(code)`），而不是**文件字节**的 sha —— 665 落盘时补了一个结尾 LF
> （`_write(code + "\n")`），两者恰好差一个 `\n`：
> `index = 3557ed2c40078bff…`（= `sha(code)`）、`file = cb38bdb21e113142…`（= `sha(code + "\n")`）。
> ⇒ 任何「拿 index 里的 sha 去校验文件字节」的写法都会误判（差一字节）；反过来，
> **只改结尾换行不会被 index 的 sha 发现**。本卡两个都记：`fixture_file_sha` 用于"文件未漂移"的
> 机器判据（探针输出 + `--check`），`index_fixture_sha` 用于与 665 产物对账。

## 2. 真机观测记录（665 实跑，2026-09-29 00:18:22）

| 项 | 值 |
|---|---|
| 检测器 | `asan`（WSL g++ Ubuntu 13.3.0 / `-O1 -g`） |
| 判决 | **catch**（期望 `catch`） |
| 签名 | `hit:AddressSanitizer` |
| 实跑次数 | 1 |
| 664 对照 | 判 B 是否推翻断言：`true`；664 验证器结论：`catch` |

实测输出（前几行，完整见 `data/cards_665/index_665.json`）：

```
=================================================================
==183==ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete) on 0x502000000010
    #0 0x7b63ff6ff5e8 in
```

## 2b. 669 双平台**实跑留痕**（各平台一份，可核对）

| 平台 | 留痕文件 | 内容 |
|---|---|---|
| WSL（Linux x86-64） | `Examples/atoms/_atom_mem_newarr_669.out` | 检测器 **真跑**的原始输出（ubsan/asan；MinGW 无 libasan/libubsan，故只能在此侧跑） |
| Windows（MinGW x86-64） | `Examples/atoms/_atom_mem_newarr_669.win.out` | 记录探针在另一平台的输出（同一条 `record=` 行必须复现） |

两份都由 `python tools/ev_ub_atoms_669.py --reprobe` **现跑现写**（不是转录）：头部记命令、夹具文件 sha、
rc 与签名/记录行的核对结论；`--check` 复核其存在性与一致性。

**本卡的 command 不重跑检测器**：Windows/MinGW **没有 libasan/libubsan**（本机实测 `ld: cannot find -lasan / -lubsan`），
故 command 走「记录复算」（探针 + 夹具文件 sha 链），`reproduce` 给出检测器原法；
在**有 sanitizer 运行库的环境**（CI Linux）上，replay 的 sanitizer 校验会
**真的重跑一遍检测器**（`expected_sanitizer: [address]` ⇒ 报出即计入 confirm，是本卡的第三份独立测量）。

## 3. 第二个载体：本机汇编形态（工件档 -O2）

工件 `Examples/atoms/_atom_mem_newarr_669.asm`（`27ee6ce96da0f9ed…`，GCC 15.3.0 (MinGW-w64)）的 `main` 里：

`new int[4]` → `operator new[]`（`_Zna…`），`delete p` → `operator delete(void*)`（`_ZdlPv…`）——**两个函数族不同**就是「配对不匹配」的机器指纹；拼写随平台变（MinGW `_Znay`/`_ZdlPvy`、Linux `_Znam@PLT`/`_ZdlPvm@PLT`），故断言取族名子串 `_Zna` / `_ZdlPv`。

断言依据（实测）：同一夹具在 MinGW GCC 15.3 与 WSL Linux GCC 13.3 下各 `-O2 -S` 编译一次，只保留两边都成立的指纹 ⇒ 跨编译器分支（CI）也是真校验。

## 4. 边界（这张卡**不**声明什么）

- 不声明"换编译器/平台/标准版本仍然如此"：矩阵只覆盖 `GCC 15.3.0 (MinGW-w64)` 与 `WSL g++ (Ubuntu 13.3.0)`、
  C++17、x86-64、`-O1/-O2`。
- 不声明**语义级**结论（"所有同类写法都会被检测器抓到"）：本卡只钉住"这一支夹具上观测到了什么"。
- 不声明**人已核准**：`status: machine-derived`，人级结论见原子卡的 `human_review: required`。
- 记录口径：`record=...` 行由 `tools/ev_ub_atoms_669.py` 从 `data/cards_665/index_665.json` **读出**生成
  （不是手打）；index 一旦重跑漂移，本卡 `--check` 与 replay 的 run_match 都会红。
