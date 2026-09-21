# slash-command 文档（618 C3 · 按类别触发验证的命令参考）

> 本文档**只描述**按类别触发验证的命令约定，不实现 slash-command 本身（IDE/工具层职责）。
> 分类口径来自 `data/test_classification_618.md`（618 C2，落地 617 C1 taxonomy）；机器可读映射见 `tests/test_category_map.json`（618 C4）。

## 一、命令总览
| 命令 | 作用 | 对应类别 | 触发范围 |
|---|---|---|---|
| `/verify replay` | 运行 replay 相关测试 | replay | atom_evidence_replay 相关测试 |
| `/verify poison` | 运行 poison 相关测试 | poison | poison_drill 相关测试 |
| `/verify gate` | 运行 gate 相关测试 | gate | gate_engine 相关测试 |
| `/verify all` | 运行全部测试 | 全部 | 整个 tests/ |
| `/verify real` | 运行真实验证测试（排除脚本自测）| 真实验证 | 命中 8 类之一者 |
| `/verify classify` | 重新生成分类报告 + 映射 | — | 触发 `test_classifier_618.py` + `test_category_map.py` |

## 二、各命令对应的 pytest 命令与预期输出

### `/verify replay`
```powershell
cd C:\CodeLearnling\note\note\C++\CPP-Bible
.venv\Scripts\python.exe -m pytest tests -k "replay" -q
```
- 预期：仅运行名称/import 命中 `replay` 的测试（见 C2 三向：约 30 个）。
- 判定：全绿（0 failed）即 replay 验证通过；refute=0 的"声称零逃逸"口径由 618 A3 L2b 约束。

### `/verify poison`
```powershell
cd C:\CodeLearnling\note\note\C++\CPP-Bible
.venv\Scripts\python.exe -m pytest tests -k "poison" -q
```
- 预期：运行名称/import 命中 `poison` 的测试（C2 三向：约 7 个）。
- 判定：全绿 ⇒ 124/124 触发 + 覆盖率口径有效（诚实 60/63）。

### `/verify gate`
```powershell
cd C:\CodeLearnling\note\note\C++\CPP-Bible
.venv\Scripts\python.exe -m pytest tests -k "gate" -q
```
- 预期：运行名称/import 命中 `gate` 的测试（C2 三向：约 43 个）。
- 判定：全绿 ⇒ 63 规则命中口径有效（block=0）。

### `/verify all`
```powershell
cd C:\CodeLearnling\note\note\C++\CPP-Bible
.venv\Scripts\python.exe -m pytest tests -q
```
- 预期：运行全部测试（C2：216 个 .py）。
- 判定：全绿 ⇒ 工具链整体健康。注意：脚本自测（snapshot 等）仅保障工具链自身，不计入"验证覆盖"。

### `/verify real`
```powershell
cd C:\CodeLearnling\note\note\C++\CPP-Bible
.venv\Scripts\python.exe -m pytest tests -q   # 全量即可；CI 可据 test_category_map.json 排除 script_self_test
```
- 预期：真实验证测试（C2：89 个，41.2%）全绿，是逃逸率可信度的基础。

### `/verify classify`
```powershell
cd C:\CodeLearnling\note\note\C++\CPP-Bible
.venv\Scripts\python.exe tools/test_classifier_618.py      # 刷新 data/test_classification_618.md
.venv\Scripts\python.exe tools/test_category_map.py        # 刷新 tests/test_category_map.json
```
- 用途：新增/重命名测试后，刷新分类报告与机器可读映射。

## 三、与 C2 分类计数的对应关系
- 三向计数（replay/poison/gate）来自 `test_classifier_618.py` 的成员关系扫描；`/verify replay|poison|gate` 的 `-k` 关键字即对应这些类别。
- `tests/test_category_map.json` 提供每个测试文件的 `{categories, is_real_verification}`，CI 可直接读取以决定运行集与覆盖率口径（剔除 script_self_test）。

## 四、纪律
- 上述命令均**不跑监工门禁**（gate --check / poison / replay --check / tool_integrity --check）；那是监工职责。
- 分类为启发式（文件名 + import），未分类文件（C2 列出 126 个）需人工归并到 taxonomy 后再纳入 `/verify real` 的硬口径。
