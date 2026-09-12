---
id: MIS-MEM-017
name: "std::forward 只是个 cast，写不写都行（忽略省略 forward 的运行时代价）"
level: deep
domain: MEM
trigger_patterns:
  - "std::forward 和 std::move 差不多，就是个类型转换"
  - "转发函数里写不写 forward 结果一样"
refutations:
  - "实测 EV-MEM-022：转发链省略 forward 后，右值实参 copies=1 moves=0——形参是具名变量、函数体内按左值处理（[basic.lval] Note 3），每次转发多付一次拷贝"
  - "std::forward<T>(x) 按**推导出的 T** 恢复实参值类别（[temp.deduct.call] 特判 + 引用折叠）：右值转回右值、左值保持左值；它是'按 T 恢复类别'的 cast，不是无差别 cast，省略后类别信息丢失不可恢复（见 ATOM-MEM-VALUE-002 / EV-MEM-021）"
source: References/32 G5 第二批指令 §一.1；ATOM-MEM-VALUE-002 / EV-MEM-022
related_atoms: [ATOM-MEM-VALUE-002, ATOM-MEM-MOVE-002]
---

# MIS-MEM-017 · "std::forward 只是个 cast，写不写都行"

**层级**：deep —— 结构性误解，源于把 std::move/std::forward 都归入"类型转换"心智模型、未区分"转换 + 按推导恢复类别"；须 ≥2 条独立反例才可能纠偏

## 触发模式（学习者常这么说 / 这么写）
- std::forward 和 std::move 差不多，就是个类型转换
- 转发函数里写不写 forward 结果一样

## 为什么它不成立
1. 实测 EV-MEM-022：转发链省略 forward 后，右值实参 copies=1 moves=0——形参是具名变量、函数体内按左值处理（[basic.lval] Note 3），每次转发多付一次拷贝
2. std::forward<T>(x) 按**推导出的 T** 恢复实参值类别（[temp.deduct.call] 特判 + 引用折叠）：右值转回右值、左值保持左值；它是"按 T 恢复类别"的 cast，不是无差别 cast，省略后类别信息丢失不可恢复（见 ATOM-MEM-VALUE-002 / EV-MEM-021）

## 出处与关联
- 出处：References/32 G5 第二批指令 §一.1；ATOM-MEM-VALUE-002 / EV-MEM-022
- 关联原子：ATOM-MEM-VALUE-002、ATOM-MEM-MOVE-002
