# ITT 口径纪律（E2，意向治疗）

> 门禁：`G-ITT-DISCIPLINE`（L0）；工具 `tools/itt_discipline_671g.py`；
> 登记 `data/671g/itt_exclusions.json`；测试 `tests/test_e_671g.py`。

## 规则

所有入检测集的样本必须计入某一口径，**不能因为"检测器不支持"就静默踢掉**：

* unknown（无检测器）可以不进**可测主分母**（catch+miss），但必须：
  1. 显式登记 id（或聚合 id）+ 理由；
  2. 排除**预注册**（PAP 的 exclusion_criteria，preregistered=true）；
  3. 同时报告全样本保守口径（unknown 记 miss），不许只报可测率；
* not_error（测量类本就非缺陷）：显式登记为 measure_class_not_error；
* 允许理由枚举：`detector_unavailable / measure_class_not_error / sample_corrupt`；
* 事后排除（preregistered=false）/无 pap_id/无理由 ⇒ block。

## 本项目登记（聚合）

| 实验 | unknown | not_error | 预注册 PAP |
|---|---|---|---|
| holdout | h2/h10/h11/h12/h37/h39 共 6 条 detector_unavailable | — | holdout-reveal（posthoc 补注，协议早有 unknown 剔除条款） |
| corpus | 9 条 unknown（perf/compile-time/other 本机无检测器） | 3 条测量类 | corpus-reveal（同上；665 起就分层不合并） |

逐 id 见 reveal 明细；聚合登记原因见 `data/671g/itt_exclusions.json`。

## 用法

```bash
python tools/itt_discipline_671g.py --check
```
