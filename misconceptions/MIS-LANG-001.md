---
id: MIS-LANG-001
name: 以为 inline 函数各 TU 写成不同实现也没关系（编译器/链接器会发现并报错）
level: deep
domain: LANG
trigger_patterns:
  - "inline 就是「每个 TU 私有一份」，各写各的实现没关系"
  - "要是两个 TU 的定义不一样，编译器或链接器肯定会报错"
  - "就算定义不同，链接器随便选一个，结果反正是确定的"
  - "只要固定链接顺序就不会有问题"
refutations:
  - "ODR 要求同一实体的多个定义「consist of the same sequence of tokens」（[basic.def.odr]/16.4）；违反属 IFNDR——**无须诊断**：实测 -Wall -Wextra 编译两个不同定义的 TU，零警告零错误（EV-LANG-001 D1 行）"
  - "行为不是「确定的」：-O0 下链接器取先遇到的 weak 定义，仅交换两个 .o 的链接顺序，同一程序的输出就从 tu_a=1,tu_b=1 变成 tu_a=2,tu_b=2（EV-LANG-001 E1/E2）"
  - "「固定链接顺序」也兜不住：换到 -O2，两个 TU 各自内联自己看到的定义，形态变成「各用各的」（1/2）且与顺序无关——同一 UB 的第二种合法表现（EV-LANG-002 §1）"
source: 371 MCC 首次落地 · EV-LANG-001 / EV-LANG-002（预言冻结 docs/kernel/371_预言冻结_ATOM-LANG-INLINE-001.md）
related_atoms: [ATOM-LANG-INLINE-001]
---

# MIS-LANG-001 · 关于 ODR 的三个连环误解

**层级**：deep —— 误解有三层（"没关系" → "会报错" → "至少结果是确定的"），每层都要独立反例，
故须 ≥2 条证据卡合力纠偏。

## 触发模式（学习者常这么说 / 这么写）

- 「`inline` 就是让每个 TU 各有一份，我把实现写成展宏不同的版本也没什么吧」
- 「真要有两个不同定义，链接器肯定报 duplicate symbol」
- 「即使它不报，链接器挑一个就是了，结果总归是确定的」
- 「那我固定链接顺序，不就稳了」

## 为什么不成立（三条反例）

1. **不报错是标准规定的**：`[basic.def.odr]/16.2` 的违反属 **IFNDR**（ill-formed, no diagnostic
   required）——除具名模块实体外**不要求**任何诊断。实测两个 TU 定义 token 序列不同，`-Wall -Wextra`
   编译**零输出**（EV-LANG-001 falsification 第 1 条的实测结果）。
2. **结果随链接顺序改变**：`-O0` 下 `odr_fn` 未被内联，链接器只保留同名符号的一个定义（取先遇到的），
   于是 `g++ a.o b.o main.o` 与 `g++ b.o a.o main.o` 产出**不同程序**：前者 `tu_a=tu_b=1`，
   后者 `tu_a=tu_b=2`（EV-LANG-001 E1/E2，双编译器复现）。
3. **"固定顺序"不是解药**：`-O2` 下两 TU 各自内联自己看到的定义，形态变成 `tu_a=1, tu_b=2`
   且与顺序无关——这仍是同一 UB 的另一种合法表现，不代表"安全"（EV-LANG-002 §1/§3）。

## 正确做法（一句话）

**inline 函数的定义在跨 TU 时必须 token 序列一致**：把它放进**同一个头文件**（单一源头）是唯一
可维护的写法；"两个 TU 各写一份等价实现"即使语义相同也脆弱（空白/注释之外，任何 token 差异即越界）。

## 出处与关联

- 出处：371 MCC 首次真实落地；证据见 `EV-LANG-001`（顺序依赖 + 零诊断）、`EV-LANG-002`（档位决定形态）。
- 预言冻结：`docs/kernel/371_预言冻结_ATOM-LANG-INLINE-001.md`（实验前写死，git 时间戳为见证）。
- 关联原子：`ATOM-LANG-INLINE-001`。
