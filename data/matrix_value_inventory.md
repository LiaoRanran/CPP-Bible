# matrix 取值台账（587 任务0.1 机器生成，只读）

> 生成时间 2026-09-18 23:34:53 · 扫描 `evidence/**/EV-*.md` 共 56 张证据卡（无 matrix 或非映射：0 张）。
> 本台账**由脚本生成、只读**，供 0.2 反推合法值口径；不得手工编辑。

## 概览

- 证据卡总数：**56**；其中 matrix 非映射/缺失：**0**
- `compiler/std/opt` 中存在**非列表**形态的键：无
- matrix 内出现、但本批不校验的其它键：`sanitizer`×4, `sanitizer_note`×1

## `compiler`（去重值 8 个）

| 取值 | 卡数 | 形态标注 | 卡（前 5） |
|---|---|---|---|
| `Clang (ubuntu-latest runner 默认)` | 1 | 带括号注释、⚠ 无族名或无版本 | EV-UB-001 |
| `GCC 13.1.0` | 3 | 族名+版本齐 | EV-MEM-001, EV-MEM-004, EV-UB-001 |
| `GCC 13.3.0 (WSL)` | 8 | 带括号注释、族名+版本齐 | EV-CONC-001, EV-CONC-002, EV-CONC-003, EV-CONC-004, EV-CONC-005 |
| `GCC 14.2.0 (WSL —— 同驱动跑 libstdc++ 与 libc++ 各一次)` | 1 | 带括号注释、族名+版本齐 | EV-MEM-038 |
| `GCC 14.2.0 (WSL)` | 9 | 带括号注释、族名+版本齐 | EV-CONC-001, EV-CONC-002, EV-MEM-039, EV-MEM-040, EV-MEM-041 |
| `GCC 15.3.0` | 40 | 族名+版本齐 | EV-HIST-001, EV-MEM-001, EV-MEM-002, EV-MEM-003, EV-MEM-004 |
| `GCC 15.3.0 (MinGW-w64)` | 16 | 带括号注释、族名+版本齐 | EV-CONC-001, EV-CONC-002, EV-CONC-003, EV-CONC-004, EV-CONC-005 |
| `GCC 8.1.0` | 2 | 族名+版本齐 | EV-MEM-001, EV-UB-001 |

## `std`（去重值 5 个）

| 取值 | 卡数 | 形态标注 | 卡（前 5） |
|---|---|---|---|
| `c++11` | 2 | — | EV-MEM-004, EV-MEM-005 |
| `c++14` | 4 | — | EV-HIST-001, EV-MEM-003, EV-MEM-004, EV-MEM-005 |
| `c++17` | 6 | — | EV-HIST-001, EV-MEM-001, EV-MEM-004, EV-MEM-005, EV-MEM-038 |
| `c++20` | 2 | — | EV-MEM-004, EV-MEM-005 |
| `c++23` | 54 | — | EV-CONC-001, EV-CONC-002, EV-CONC-003, EV-CONC-004, EV-CONC-005 |

## `opt`（去重值 5 个）

| 取值 | 卡数 | 形态标注 | 卡（前 5） |
|---|---|---|---|
| `-O0` | 22 | — | EV-LANG-001, EV-LANG-002, EV-MEM-001, EV-MEM-002, EV-MEM-004 |
| `-O1（sanitizer 观测档）` | 1 | — | EV-MEM-043 |
| `-O2` | 54 | — | EV-CONC-001, EV-CONC-002, EV-CONC-003, EV-CONC-004, EV-CONC-005 |
| `-O2（本卡）/ -O1（同夹具在 EV-MEM-043 的 sanitizer 观测）` | 1 | — | EV-MEM-042 |
| `-O2（零依赖判据档）` | 1 | — | EV-MEM-043 |

## `arch`（去重值 1 个）

| 取值 | 卡数 | 形态标注 | 卡（前 5） |
|---|---|---|---|
| `x86-64` | 56 | — | EV-CONC-001, EV-CONC-002, EV-CONC-003, EV-CONC-004, EV-CONC-005 |

## `stdlib`（去重值 6 个）

| 取值 | 卡数 | 形态标注 | 卡（前 5） |
|---|---|---|---|
| `libc++-18` | 1 | — | EV-MEM-038 |
| `libstdc++` | 13 | — | EV-LANG-001, EV-LANG-002, EV-MEM-034, EV-MEM-035, EV-MEM-036 |
| `libstdc++ (GCC 15.3.0 MinGW-w64)` | 2 | 带括号注释 | EV-MEM-032, EV-MEM-033 |
| `libstdc++ ×2 平台（MinGW 与 glibc/Linux）` | 1 | — | EV-MEM-039 |
| `none` | 2 | — | EV-CONC-001, EV-CONC-002 |
| `pthread` | 4 | — | EV-CONC-003, EV-CONC-004, EV-CONC-005, EV-CONC-006 |

## 0.2 草稿口径空跑结果（存量零误伤前置自证）

口径（终稿，由真实分布反推）：先剥掉**半角/全角**括号注释、再按 `/` 拆段，逐段校验——
- `std`：`^(gnu|c)\+\+(98|03|11|14|17|20|23|26)$`；
- `opt`：`^-O([0-3sgz]|fast)$`；
- `arch`：限**存量真实出现集合**（当前仅 `x86-64`）；
- `compiler`：带括号注释 ⇒ 只要求注释外的核心含族名关键词（gcc/g++/clang/clang++/msvc，大小写不敏感）；不带注释 ⇒ 族名关键词 **且** 至少一段版本数字；
- `stdlib` 等其余键**本批不校验**（可选键，形态自由）。

口径依据（实测，非拍脑袋）：① opt 有 **3 个值带全角括号注释**（EV-MEM-042/043）、1 个值含 `/` 并列（`-O2（本卡）/ -O1（…）`）⇒ 两种括号都剥、`/` 拆段；② arch 存量只出现 `x86-64` ⇒ 本批只对它开口；③ std 存量 5 值全在建议集合内。

**交人（未自作主张）**：compiler 值 `Clang (ubuntu-latest runner 默认)`（EV-UB-001，全库仅此 1 例）**有族名、无版本数字**。按任务书 0.2「括号注释一律放行」取「带注释 ⇒ 只要求族名」⇒ 存量 0 命中；若改判为「必须带版本数字」，存量将 **+1 warn（违反 191 零误伤）**，须监工裁决。

- 存量命中：**0**

