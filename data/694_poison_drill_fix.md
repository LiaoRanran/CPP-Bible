# 694-B · Poison Drill 修复记录（P43f 漏网，123/124 → 124/124）

批次：694 · 起点 HEAD `acc9cf9b`（693-G） · 日期 2026-10-08

---

## 1. 现象

```
python tools/cppbible.py check --stage quality
  ❌ Poison Drill FAIL
      [poison] P43f 门禁键 YAML1.1 隐式类型陷阱须 [type-diverge] 漏网: 拦截者 （无！） ❌
      [poison] 123/124 —— 制衡层有漏网，先修制衡！
```

---

## 2. 根因（与 694-A 同源：**受管解释器缺 pyyaml**）

毒载荷（`tools/poison_drill.py:1029-1039`）：

```python
# ── P43f（557 B2）：门禁关心键的 YAML 1.1 隐式类型陷阱（`command: 00000000`）⇒ [type-diverge] block ──
_write(ge.EVIDENCE / "mem" / "EV-MEM-TYPEDIV.md", {
    "id": "EV-MEM-TYPEDIV", "hypothesis": "h", "command": "00000000", ...})
hits = [f for f in ge.check_frontmatter_hardening() if f.severity == "block"]
ok = any("[type-diverge]" in f.message for f in hits)
```

而 `[type-diverge]` 的判定在 `tools/gate_engine.py:1461-1469`，位于
`if yaml_mod is None: return out`（:1429）**之后**——即这一支**必须先成功 `import yaml`**。
受管解释器（`C:\Users\ASUS\.workbuddy\binaries\python\versions\3.13.12\python.exe`，实为 3.13.14）
无 pyyaml ⇒ `check_frontmatter_hardening()` 提前返回 ⇒ 毒卡 `command: 00000000`
（YAML 1.1 下被隐式解析为 `int`）**零拦截** ⇒ P43f 报"漏网"，总数 123/124。

同一个函数的信号①（缩进走私，纯 Python）仍在跑，所以 P43（缩进走私）依旧通过——
这正是"只丢 pyyaml 部分"的指纹：**不是制衡层退化，是依赖缺失**。

---

## 3. 处理方式

与 694-A 同一处根因、同一次处置：**给受管解释器装上声明依赖 pyyaml**
（`pyproject.toml:29` `dependencies = ["pyyaml>=6.0", ...]`）：

```
C:\Users\ASUS\.workbuddy\binaries\python\versions\3.13.12\python.exe -m pip install --disable-pip-version-check "pyyaml>=6.0"
  Successfully installed pyyaml-6.0.3
```

**未改任何毒样例、未加豁免、未改 `poison_drill.py`、未改 `gate_engine.py`**
（`git diff --stat -- tools/poison_drill.py tools/gate_engine.py` 为空）。
按红线 7 的要求，先查失败原因再决定：本次失败是**环境依赖缺失**，不是"已知预期失败"，
也不该用豁免把它抹平（那会让 P43f 这条制衡永久失效）。

---

## 4. 修复后实测

```
C:\Users\ASUS\.workbuddy\binaries\python\versions\3.13.12\python.exe tools/poison_drill.py
  [poison] P43f 门禁键 YAML1.1 隐式类型陷阱须 [type-diverge] 拦下: 拦截者 EV-FM-YAML-HARDENING ✅
  [poison] 阴性对照（干净原子+干净卡）: gate block=0 · replay=confirm ✅
  [poison] 124/124 —— 制衡层有效（全部拦截 + 阴性放行）
```

| 项 | 修复前 | 修复后 |
|---|---|---|
| 毒样例通过数 | 123/124 | **124/124** |
| P43f | 漏网（拦截者 无） | 拦下（拦截者 EV-FM-YAML-HARDENING） |
| 行为覆盖规则 | 39/67 | 39/67（不变） |
| 表观覆盖率（含全部豁免） | 100.0%（67/67） | 100.0%（67/67） |
| 诚实覆盖率（仅背书豁免） | 95.5%（64/67） | 95.5%（64/67） |
| 机器不可触发（单列） | 3 | 3 |
| legacy 豁免（单列） | 27 | 27 |

覆盖率口径前后完全一致 ⇒ 修复只恢复了**应有拦截力**，没有顺手改宽/改严任何口径。

---

## 5. 残留风险（与 694-A 同一条）

修复落在环境（受管解释器 site-packages），**不入 git**。受管解释器若被重建或
`toolchain.toml` 解析到别的解释器而该解释器未装 pyyaml，P43f 会**原样复现**。
兜底：`gate_engine` 缺 pyyaml 时必发可见 warn（不静默跳过），Poison Drill 也会立即转红。
