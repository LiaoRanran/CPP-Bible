# 619 B3 · PCK 试点证书报告（10 张，只读派生）

> B2 验证结果：**PASS=10 / FAIL=0**（目标 10/10 通过）

## 试点清单
- `atoms/conc/ATOM-CONC-FENCE-001.md` → `pck_pilot/ATOM-CONC-FENCE-001.pck.yaml`：PASS （verifiers=1 · review=batch_authorization · negative_tests=10 · commit=7602058d）
    note: 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
    note: review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）
- `atoms/conc/ATOM-CONC-LOCK-001.md` → `pck_pilot/ATOM-CONC-LOCK-001.pck.yaml`：PASS （verifiers=1 · review=batch_authorization · negative_tests=10 · commit=d6c3e045）
    note: 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
    note: review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）
- `atoms/hist/ATOM-HIST-AUTOPTR-001.md` → `pck_pilot/ATOM-HIST-AUTOPTR-001.pck.yaml`：PASS （verifiers=1 · review=batch_authorization · negative_tests=10 · commit=d6c3e045）
    note: 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
    note: review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）
- `atoms/lang/ATOM-LANG-INLINE-001.md` → `pck_pilot/ATOM-LANG-INLINE-001.pck.yaml`：PASS （verifiers=1 · review=batch_authorization · negative_tests=10 · commit=d6c3e045）
    note: 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
    note: review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）
- `atoms/mem/ATOM-MEM-LEAK-001.md` → `pck_pilot/ATOM-MEM-LEAK-001.pck.yaml`：PASS （verifiers=1 · review=batch_authorization · negative_tests=10 · commit=4802c68c）
    note: 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
    note: review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）
- `evidence/conc/EV-CONC-001.md` → `pck_pilot/EV-CONC-001.pck.yaml`：PASS （verifiers=1 · review=batch_authorization · negative_tests=27 · commit=e374517d）
    note: 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
    note: review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）
- `evidence/conc/EV-CONC-002.md` → `pck_pilot/EV-CONC-002.pck.yaml`：PASS （verifiers=1 · review=batch_authorization · negative_tests=26 · commit=d3b2cb70）
    note: 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
    note: review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）
- `evidence/hist/EV-HIST-001.md` → `pck_pilot/EV-HIST-001.pck.yaml`：PASS （verifiers=1 · review=batch_authorization · negative_tests=24 · commit=d3b2cb70）
    note: 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
    note: review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）
- `evidence/lang/EV-LANG-001.md` → `pck_pilot/EV-LANG-001.pck.yaml`：PASS （verifiers=1 · review=batch_authorization · negative_tests=28 · commit=d3b2cb70）
    note: 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
    note: review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）
- `evidence/mem/EV-MEM-001.md` → `pck_pilot/EV-MEM-001.pck.yaml`：PASS （verifiers=1 · review=batch_authorization · negative_tests=23 · commit=d3b2cb70）
    note: 单验证器：verifier_disagreement 不适用（与 A1 雷2 口径一致）
    note: review_method=batch_authorization：非逐条独立审阅（615 诚实审计结论）

## 缺口诚实登记（10 张一致）
- `verifiers` = 1（仅 gate_engine）：verifier_disagreement 不适用（A1 雷2 口径）
- `human_authority.review_method` = batch_authorization：非逐条独立审阅（615）
- `uncertainty` 引用全局 estimand L1=0.9062%，卡内无本地置信字段
- `provenance.commit` 由 git 反查；`first_authorized_at` 取自卡 verified_at
- `negative_tests` 来自 v7 baseline 真实 results[]（(card,op,point) 三元组）
