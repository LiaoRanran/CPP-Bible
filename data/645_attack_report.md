# 645 攻击生成报告（A2，真变异 + 真实检查）

- 定向变异数：25（目标 ≥20）
- 随机对照数：8
- **定向逃逸：0**（结构合法但语义被改）
- 随机逃逸：0
- 定向逃逸率：0.0 / 随机逃逸率：0.0
- 真实逃逸发现：False（或证明当前无结构逃逸）

## 逐变异（节选前 30）
- `ATOM-CONC-FENCE-001` field_delete [targeted] → 拦截：缺失必填字段：['id']
- `ATOM-CONC-FENCE-001` value_tamper [targeted] → 拦截：ID 格式非法：ATOM-CONC-FENCE-001
- `ATOM-CONC-FENCE-001` break_ref [targeted] → 拦截：ID 格式非法：bad id with spaces
- `ATOM-CONC-FENCE-001` format_perturb [targeted] → 拦截：ID 格式非法：ATOM-CONC-FENCE-001
- `ATOM-CONC-FENCE-001` equiv_rewrite [targeted] → 拦截：缺失必填字段：['id', 'title', 'domain', 'type', 'status', 'claim']
- `ATOM-CONC-LOCK-001` field_delete [targeted] → 拦截：缺失必填字段：['id']
- `ATOM-CONC-LOCK-001` value_tamper [targeted] → 拦截：ID 格式非法：ATOM-CONC-LOCK-001
- `ATOM-CONC-LOCK-001` break_ref [targeted] → 拦截：ID 格式非法：bad id with spaces
- `ATOM-CONC-LOCK-001` format_perturb [targeted] → 拦截：ID 格式非法：ATOM-CONC-LOCK-001
- `ATOM-CONC-LOCK-001` equiv_rewrite [targeted] → 拦截：缺失必填字段：['id', 'title', 'domain', 'type', 'status', 'claim']
- `ATOM-CONC-RACE-001` field_delete [targeted] → 拦截：缺失必填字段：['id']
- `ATOM-CONC-RACE-001` value_tamper [targeted] → 拦截：ID 格式非法：ATOM-CONC-RACE-001
- `ATOM-CONC-RACE-001` break_ref [targeted] → 拦截：ID 格式非法：bad id with spaces
- `ATOM-CONC-RACE-001` format_perturb [targeted] → 拦截：ID 格式非法：ATOM-CONC-RACE-001
- `ATOM-CONC-RACE-001` equiv_rewrite [targeted] → 拦截：缺失必填字段：['id', 'title', 'domain', 'type', 'status', 'claim']
- `ATOM-HIST-AUTOPTR-001` field_delete [targeted] → 拦截：缺失必填字段：['id']
- `ATOM-HIST-AUTOPTR-001` value_tamper [targeted] → 拦截：ID 格式非法：ATOM-HIST-AUTOPTR-001
- `ATOM-HIST-AUTOPTR-001` break_ref [targeted] → 拦截：ID 格式非法：bad id with spaces
- `ATOM-HIST-AUTOPTR-001` format_perturb [targeted] → 拦截：ID 格式非法：ATOM-HIST-AUTOPTR-001
- `ATOM-HIST-AUTOPTR-001` equiv_rewrite [targeted] → 拦截：缺失必填字段：['id', 'title', 'domain', 'type', 'status', 'claim']
- `ATOM-LANG-INLINE-001` field_delete [targeted] → 拦截：缺失必填字段：['id']
- `ATOM-LANG-INLINE-001` value_tamper [targeted] → 拦截：ID 格式非法：ATOM-LANG-INLINE-001
- `ATOM-LANG-INLINE-001` break_ref [targeted] → 拦截：ID 格式非法：bad id with spaces
- `ATOM-LANG-INLINE-001` format_perturb [targeted] → 拦截：ID 格式非法：ATOM-LANG-INLINE-001
- `ATOM-LANG-INLINE-001` equiv_rewrite [targeted] → 拦截：缺失必填字段：['id', 'title', 'domain', 'type', 'status', 'claim']
- `ATOM-CONC-FENCE-001` random_noise [random] → 拦截：ID 格式非法：ATOM-CONC-FENCE-001
- `ATOM-CONC-LOCK-001` random_noise [random] → 拦截：ID 格式非法：ATOM-CONC-LOCK-001
- `ATOM-CONC-RACE-001` random_noise [random] → 拦截：ID 格式非法：ATOM-CONC-RACE-001
- `ATOM-HIST-AUTOPTR-001` random_noise [random] → 拦截：ID 格式非法：ATOM-HIST-AUTOPTR-001
- `ATOM-LANG-INLINE-001` random_noise [random] → 拦截：ID 格式非法：ATOM-LANG-INLINE-001
