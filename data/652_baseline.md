# 652 阶段 0 · 开工基线快照（究极巨大建设 W4+）

> 写于 2026-09-27。批次 652：交人项自动化（A）+ W4+ 头部（B）+ W4+ 中间（C）+ W4+ 尾部（D）+ 差啥登记（E）+ 收工（F）。

## 一、协议确认
- 651 已收工：`_auto/status.json` `last_completed_batch=651`、`state=awaiting_review`。
- 本批仍在 **CPP-Bible**，T2（B7-B10 上岗）涉 **queyi-core**。

## 二、开工 git 状态
| 仓库 | HEAD | ahead |
|---|---|---|
| CPP-Bible | `20655109` | 13 |
| queyi-core | `b9832d1` | 7 |

## 三、环境可用性（决定 B/E 的边界）
| 依赖 | 可用 | 影响 |
|---|---|---|
| gcc 13.1.0 / clang 22.1.8 | ✅ | H5 积木闭环、M4 挑战者可真做 |
| `ots` CLI | ❌ | **OTS 重锚做不了** ⇒ E 登记（627/631 已登记同类） |
| `esbmc` | ❌ | **H6 falsification 试点无法真跑** ⇒ 工具降级 + E 登记 |
| GPU / 训域小模型 | ❌ | E 登记 |
| CVM / 云外部锚 | ❌ | E 登记 |
| Rust 重写（形式化） | ❌ | E 登记 |

## 四、既有资产
| 资产 | 位置 |
|---|---|
| 452 改判账本 | `data/authority/decision_event_v2_ledger.jsonl` |
| 648 十张 C 卡 | atoms/{lang,mem,ub}/*-001.md（10 张） |
| PCK 证书 | `data/pck/certificates/*.yaml`（619-pck-v1） |
| 人审队列（旧格式） | `data/authority/pending_review_621.jsonl`（30 条） |
| 信任根 | `tools/tool_integrity.py` + `data/supply_chain/merkle_roots.json` |
| OTS/merkle 工具 | `tools/ots_anchor_613.py` / `opentimestamps_anchor.py` / `merkle_integrity.py` |
| 两阶段纪律 | `docs/pytest_two_phase.md` |

## 五、已知工作区状态
- CPP-Bible 工作区 **166 个脏文件**（含 648 未提交的 `tests/conftest.py`）——本批 A 将提交 conftest.py；其余非本批引入，登记。

## 六、652 交付清单
| 阶段 | 交付 |
|---|---|
| A | 87 卡补 verified_at（git log 首次提交时间）；T1 452 真回填（新文件，原 sha256 不变）；M7 队列迁移（新文件）；conftest.py 提交；两阶段 pytest 复跑；OTS 重锚（⚠ 无 ots CLI） |
| B | `tools/probe_assembler_652.py`(H5)、`tools/esbmc_falsify_652.py`(H6，降级) |
| C | `tools/challenger_652.py`(M4)、`tools/embedded_adapter_652.py`(M5) |
| D | `tools/rats_closure_652.py`(T3)、`tools/pck_export_652.py`(T7)、T2(B7-B10 灰度上岗，queyi-core) |
| E | `data/652_gaps.md`（差啥清单：缺什么/为什么缺/何时能做） |
| F | `tools/run_652_gate.py` + 收工报告 + status |
