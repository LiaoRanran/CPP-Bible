---
id: MIS-MEM-022
name: "std::string 总是分配堆内存（不知道 SSO）"
level: surface
domain: MEM
trigger_patterns:
  - "每次构造 string 都要 new 一块内存"
  - "string 操作慢，因为总要走堆"
refutations:
  - "实测 EV-MEM-029：len≤15 的字符串构造零堆分配（SSO：短串存对象内部 32 字节缓冲），len=16 才首次落堆（本机 libstdc++ 阈值 15）"
  - "实测 EV-MEM-030：短字符串拷贝 allocs=0（只搬对象内缓冲；赋值走同一实现路径），长字符串同操作 allocs=1——'总是分配'与'总是慢'一起被推翻（见 ATOM-MEM-PERF-002）"
source: References/32 G5 第二批指令 §一.4；ATOM-MEM-PERF-002 / EV-MEM-029 / EV-MEM-030
related_atoms: [ATOM-MEM-PERF-002, ATOM-MEM-NEW-001]
---

# MIS-MEM-022 · "std::string 总是分配堆内存"（不知道 SSO）

**层级**：surface —— 表层误解，源于"对象成员=堆分配"的直觉、没见过 SSO 的对象内缓冲；两条带实测的反例即可纠偏

## 触发模式（学习者常这么说 / 这么写）
- 每次构造 string 都要 new 一块内存
- string 操作慢，因为总要走堆

## 为什么它不成立
1. 实测 EV-MEM-029：len≤15 的字符串构造零堆分配（SSO：短串存对象内部 32 字节缓冲），len=16 才首次落堆（本机 libstdc++ 阈值 15）
2. 实测 EV-MEM-030：短字符串拷贝 allocs=0（只搬对象内缓冲；赋值走同一实现路径），长字符串同操作 allocs=1——"总是分配"与"总是慢"一起被推翻（见 ATOM-MEM-PERF-002）

## 出处与关联
- 出处：References/32 G5 第二批指令 §一.4；ATOM-MEM-PERF-002 / EV-MEM-029 / EV-MEM-030
- 关联原子：ATOM-MEM-PERF-002、ATOM-MEM-NEW-001
