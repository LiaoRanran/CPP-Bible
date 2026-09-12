---
id: MIS-MEM-015
name: 结构体成员紧密排列、sizeof 等于各成员之和；指针强转可读字段
level: deep
domain: MEM
trigger_patterns:
  - "struct 成员一个接一个排，sizeof 就是各成员相加"
  - "把 struct 强转成 char* 就能按偏移读任意字段"
refutations:
  - "成员按自身对齐排列，编译器插 padding，sizeof 含 padding：实测 Padded{char a; int b} 的 sizeof=8 而非 5，int 偏移 4 而非 1 [basic.align]/[class.mem]（见 ATOM-MEM-ALIGN-001 / EV-MEM-019）"
  - "reinterpret_cast 强转指针对齐/类型双关是 UB（未对齐访问 + [strict.aliasing]），轻则读错值重则崩溃；按字节搬运用 memcpy/std::bit_cast（安全，见 ATOM-MEM-ALIGN-001 / EV-MEM-020 roundtrip=7）"
source: ATOM-MEM-ALIGN-001 / EV-MEM-019/020（padding 量化 + memcpy 安全）
related_atoms: [ATOM-MEM-ALIGN-001]
---

# MIS-MEM-015 · 结构体成员紧密排列、sizeof 等于各成员之和；指针强转可读字段

**层级**：deep —— 结构性误解，源于"内存就是成员顺次排"的心智模型；须 ≥2 条独立反例才可能纠偏

## 触发模式（学习者常这么说 / 这么写）
- struct 成员一个接一个排，sizeof 就是各成员相加
- 把 struct 强转成 char* 就能按偏移读任意字段

## 为什么它不成立
1. 成员按自身对齐排列，编译器插 padding，sizeof 含 padding：实测 Padded{char a; int b} 的 sizeof=8 而非 5，int 偏移 4 而非 1 [basic.align]/[class.mem]（见 ATOM-MEM-ALIGN-001 / EV-MEM-019）
2. reinterpret_cast 强转指针对齐/类型双关是 UB（未对齐访问 + [strict.aliasing]），轻则读错值重则崩溃；按字节搬运用 memcpy/std::bit_cast（安全，见 ATOM-MEM-ALIGN-001 / EV-MEM-020 roundtrip=7）

## 出处与关联
- 出处：ATOM-MEM-ALIGN-001 / EV-MEM-019/020（padding 量化 + memcpy 安全）
- 关联原子：ATOM-MEM-ALIGN-001
