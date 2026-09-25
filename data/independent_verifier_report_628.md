# 628 B1 · 独立验证者报告（他验三件套 #1）

## 对比表（独立重算 vs 系统口径）

| 项目 | 独立重算 | 系统口径 | 一致 |
|---|---|---|---|
| W2 分布 | {'IN': 79, 'OUT': 42, 'UNDEC': 0} | IN114/OUT7/UNDEC0 | True |
| W2 逐节点 | vs grounded_labels 冻结输出 | 121 节点 | True |
| PCK authorized | 27（{'approved': 27, 'pending': 56}） | 27 | True |
| ledger 哈希链 | valid（452 条） | 452 条 valid | True |
| unique 审查项 | 93（93 records） | 93 | True |

## 实现说明

- **零 import**：只 import 标准库（json/hashlib/os/sys/argparse/re/typing）。
- W2 朴素重实现：节点 credibility 取自卡面；生效攻击=ledger APPROVE∪MODIFY 去重；
  击败=cred(A)>cred(B) 严格大于；其上求 grounded 不动点。无任何优化或捷径。
- PCK 用**行级最小 YAML 子集解析器**（固定 schema），不用 pyyaml。
- 哈希链公式独立重写：sha256(f"{prev_hash}|{payload}")，
  payload=事件 dict 去 self_hash/event_id 后 sort_keys JSON。

## 他验意义

- 这是系统第一次有**不依赖本项目代码的验证**：若 626 求解器/账本工具有隐性 bug，
  独立重算与之不符即暴露。当前全部一致 ⇒ 两个独立实现交叉确认同一结论。
- 局限：验证者仍由本项目作者编写（写代码的人相同），真正的第三方独立需
  外部验证者 + 非对称签名（VSA/B2-B4 是其原型）。

- **总判定**：全部一致 ✅
