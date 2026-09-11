---
id: MIS-MEM-019
name: "写了析构函数就够了（违反 Rule of 3/5：漏写拷贝/移动）"
level: deep
domain: MEM
trigger_patterns:
  - "类里有指针就要写析构函数，写完析构就安全了"
  - "析构写了就齐了"
refutations:
  - "实测 EV-MEM-024：只写析构、不写拷贝构造 → 隐式浅拷贝（allocs=1 same_ptr=1），同一块资源被析构两次（dtor_runs=2）；析构真释放时即 double free（WSL ASan 实报 attempting double-free in ~Buggy）"
  - "隐式拷贝/移动的生成规则由'用户声明了什么'驱动（[class.copy.ctor]）：声明析构函数 → 隐式拷贝仍生成但已废弃语义（浅拷贝）；正确的做法是三件套（析构/拷贝构造/拷贝赋值）或五件套（+ 移动）齐写，或直接 Rule of Zero 用 RAII 成员（见 ATOM-MEM-RAII-002 / EV-MEM-023 对照组）"
source: References/32 G5 第二批指令 §一.2；ATOM-MEM-RAII-002 / EV-MEM-024
related_atoms: [ATOM-MEM-RAII-002, ATOM-MEM-MOVE-002]
---

# MIS-MEM-019 · "写了析构函数就够了"（违反 Rule of 3/5）

**层级**：deep —— 结构性误解，源于"析构=安全"的单点心智模型、不了解隐式拷贝/移动的生成与废弃规则；须 ≥2 条独立反例才可能纠偏

## 触发模式（学习者常这么说 / 这么写）
- 类里有指针就要写析构函数，写完析构就安全了
- 析构写了就齐了

## 为什么它不成立
1. 实测 EV-MEM-024：只写析构、不写拷贝构造 → 隐式浅拷贝（allocs=1 same_ptr=1），同一块资源被析构两次（dtor_runs=2）；析构真释放时即 double free（WSL ASan 实报 attempting double-free in ~Buggy）
2. 隐式拷贝/移动的生成规则由"用户声明了什么"驱动（[class.copy.ctor]）：声明析构函数 → 隐式拷贝仍生成但已废弃语义（浅拷贝）；正确的做法是三件套（析构/拷贝构造/拷贝赋值）或五件套（+ 移动）齐写，或直接 Rule of Zero 用 RAII 成员（见 ATOM-MEM-RAII-002 / EV-MEM-023 对照组）

## 出处与关联
- 出处：References/32 G5 第二批指令 §一.2；ATOM-MEM-RAII-002 / EV-MEM-024
- 关联原子：ATOM-MEM-RAII-002、ATOM-MEM-MOVE-002
