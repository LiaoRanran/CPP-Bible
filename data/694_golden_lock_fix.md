# 694-A · Golden Lock 修复记录（warn_findings 203 → 204）

批次：694（pre-push 门禁 quality + metrics 全绿） · 起点 HEAD `acc9cf9b`（693-G） · 日期 2026-10-08

---

## 1. 现象

```
python tools/cppbible.py check --stage quality
  ❌ Golden Lock FAIL
      [golden] 恶化 1 · 改善 0
      WORSE warn_findings: 203 → 204
      [golden] warn 四桶：real 14 · false_positive 0 · legacy 173 · accepted 16 · 未分类 1
      unclassified: EV-FM-YAML-HARDENING(1)
```

基线快照（`tools/golden_state.json`，`updated=2026-10-02`，`commit=8f1092c4`）：
`warn_findings=203`、`block_findings=0`、`atoms_total=52`、`evidence_total=71`、
`verified_atoms=31`（human 23 / redteam 3 / machine 5）、`dal_gap=0`、`replay_confirm=71`、
`replay_infra_error=0`。

---

## 2. 根因（**不是基线变化，是环境缺依赖**）

任务卡给的假设是"693 新增文档导致统计基线变化（cpp_blocks 515→7515 那类）"。
**实测否证**：693 改的是 `README.md` / `docs/` / `tools/utils`，而本次恶化的唯一增量
是一条 `EV-FM-YAML-HARDENING` 的 **warn**，且它落在"未分类"桶里（此前从未出现过）。

追到 `tools/gate_engine.py:1327-1344`：

```python
try:
    import yaml as yaml_mod
    from yaml.constructor import ConstructorError as _ctor_error
except ImportError:
    yaml_mod = None
out: list[Finding] = []
if yaml_mod is None:
    out.append(Finding(
        "EV-FM-YAML-HARDENING", "warn", ".",
        f"跳过 YAML 硬化的 ②/③/④ 信号：当前解释器缺 pyyaml"
        f"（{sys.executable}）——重复键/语法错误/解析分歧将不被检出"
        f"（缩进走私①仍生效）", ...))
```

即：**当期跑门禁的解释器没有 pyyaml ⇒ 硬化层只跑信号①，另发 1 条 warn 让"检查没跑"可见**。
warn 总数因此 203 → 204。

哪个解释器？`tools/cppbible.py:82` 的 `PYTHON_EXE = find_managed_python()`，
经 `toolchain.toml` 的 `[python].prefer = ["C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.*/python.exe"]`
解析到受管解释器。实测两个解释器：

| 解释器 | pyyaml |
|---|---|
| `C:\Users\ASUS\AppData\Local\Python\pythoncore-3.14-64\python.exe`（shell 里的 `python`） | ✅ 6.0.3 |
| `C:\Users\ASUS\.workbuddy\binaries\python\versions\3.13.12\python.exe`（受管，**实为 3.13.14**） | ❌ `ModuleNotFoundError: No module named 'yaml'` |

交叉验证（**同仓库、同代码，只换解释器**）：

```
# 3.14（有 pyyaml）
python tools/golden_lock.py check
  [golden] 恶化 0 · 改善 0
  [golden] warn 四桶：real 14 · false_positive 0 · legacy 173 · accepted 16 · 未分类 0
  [golden] ✅ 无恶化
```

同一份仓库，换解释器即 203 与 204 两态 ⇒ **根因锁定为环境，不是内容、也不是基线漂移**。

**这不是"可选依赖"**：`pyproject.toml:27-29` 把 `pyyaml>=6.0` 放在 `[project].dependencies`
（528 任务5 显式注释：此前只在 dev extras，核心安装跑 `gate_engine` 会 ImportError）。
即：门禁链缺了一个**声明的硬运行时依赖**，属于真实环境缺陷。

---

## 3. 处理方式（**未使用 `--accept`**）

判据：Golden Lock 的 `--accept` 只在"数量真变了但可接受"时用（真实债 / 基线迁移）。
本次是**环境缺依赖导致的假恶化**，一旦装上 pyyaml，warn 自然回落到 203——
若在这里 `--accept`，等于把"门禁少跑了三个信号"永久写进基线，是**把环境故障伪造成已裁决债务**。
故：**修环境，不留痕接受**。

执行：

```
C:\Users\ASUS\.workbuddy\binaries\python\versions\3.13.12\python.exe -m pip install --disable-pip-version-check "pyyaml>=6.0"
  Successfully installed pyyaml-6.0.3
```

---

## 4. 修复后实测

```
C:\Users\ASUS\.workbuddy\binaries\python\versions\3.13.12\python.exe tools/golden_lock.py check
  [golden] 恶化 0 · 改善 0
  [golden] warn 四桶：real 14 · false_positive 0 · legacy 173 · accepted 16 · 未分类 0
  [golden] ✅ 无恶化
```

| 项 | 修复前 | 修复后 |
|---|---|---|
| warn_findings | 204（WORSE 203→204） | 203（恶化 0） |
| 未分类桶 | EV-FM-YAML-HARDENING(1) | 0 |
| 其余 10 项指标 | — | 全部无恶化（恶化 0 · 改善 0） |
| `tools/golden_state.json` | — | **未改动**（`git diff --stat` 为空） |

`python tools/cppbible.py check --stage quality` → **27 passed / 0 failed**（修复前 25 passed / 2 failed）。

---

## 5. 残留风险（诚实登记）

修复落在**环境**（受管解释器的 site-packages），**不由 git 承载**。若将来
`toolchain.toml` 的 `[python].prefer` 解析到另一个/重建的受管解释器，而那个解释器又没装
pyyaml，本条会**原样复现**（warn +1 且 P43f 漏网）。

现有兜底（非静默）：`gate_engine.py:1338` 在缺 pyyaml 时**必定发一条可见 warn**（"跳过＝永久免检"
是 368 P1-2 已确立的反模式，本规则正是为此写的），因此不会退化成"检查没跑但看起来通过"。
本批未新增依赖预检门禁（超出 694 范围），登记为已知环境风险。
