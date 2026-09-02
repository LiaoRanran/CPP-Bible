# 人文素材索引（主题 → 素材 → 可挂章节）

> 体例：「历史注脚」「事故现场」为**可选盒子**，宁缺毋滥——宁可 30 章有，不可 147 章齐刷刷。
> 所有引用必须挂键（SOURCING §3.9），**禁止编造轶事**；素材本体在 `docs/references/external/humanities/`（gitignored，仅本机）。

## 历史 / 来路

| 素材 | 键 | 内容亮点 | 可挂章节 |
|------|----|----------|----------|
| Ritchie《The Development of the C Language》(1993) | `ritchie:chist` | C 从 BCPL/B 一路被 UNIX 逼出来的演化史；类型系统是妥协而非设计；NB→C 的改名动机 | ch01、Part0 C1、C5 |
| HOPL-II《A History of C++: 1979–1991》 | `hopl:hopl2` | "C with Classes"→C++ 的命名；异常与模板为何长成这样；标准化前夜 | ch01、ch03、ch60 |
| HOPL-III《Evolving a language in and for the real world: C++ 1991–2006》 | `hopl:hopl3` | 异常/模板/RTTI 如何成形；标准化委员会如何运转；C++98 的取舍 | ch03、ch60、ch67 |
| HOPL-IV《Thriving in a Crowded and Changing World: C++ 2006–2020》 | `hopl:hopl4` | C++11/14/17/20 的设计政治；Concepts 十年提案史；现代委员会运作 | ch02、ch07、ch67 |
| QCon 2009 C. A. R. Hoare | `qcon:2009-hoare-null` | 「空引用：十亿美元的错误」原话出处 | ch41、ch88、C5 |
| Stroustrup《The Design and Evolution of C++》(1994) | `de:<ch>` | **引用（reference）为运算符重载而生**：§3.7 原文——"References were introduced primarily to support operator overloading"；轶事：Bjarne 向 Doug McIlroy 解释重载前身方案时，McIlroy 一句 "reference" 点醒他，次日即带回完整方案（Algol68 启发）；并解释为何引用不可重绑定（避免 Algol68 r1=r2 歧义）、const 引用可绑临时（Release 2.0 修正非 const 引用绑临时之误） | ch20（const& 红线**已核证**）、ch01、ch03 |
| K&R《The C Programming Language》(1978/1988) | `book:krc:<ch>` | C 的极简/正交设计基因：少而精的运算符、类型即契约、`(since C)` 风格的克制；「可信赖的小工具」审美源头 | ch01、Part0 C1、C5（历史气质素材） |
| Exceptional C++（Sutter，第一册） | `book:exceptional-cpp:<item>` | 异常安全十部曲（Item 8–17）：Cargill 1994《Exception Handling: A False Sense of Security》证明当时社区尚不懂异常安全 → Sutter 1997 给出三个完整解（"Exception-Safe Generic Containers"）→ 确立 basic/strong/nothrow 三级承诺 | ch40（异常安全）、C5 |

## 哲学 / 设计观

| 素材 | 键 | 亮点 | 可挂章节 |
|------|----|------|----------|
| Stepanov《Notes on Programming》 | `stepanov:notes` | 「数学高于对象」；泛型=把算法从类型中解放；效率是一种道德要求 | ch76、ch60、part07 导言 |
| Stepanov《Elements of Programming》 | `stepanov:eop` | 概念与迭代器分类学的公理化 | ch76、ch90 |

## 书内「作者声音」范本（拿来学笔法）

- Meyers 三部曲的 Item 骨架：问题 → 直觉 → 反直觉 → 规则 → 边界（`book:*-items.md` 已条目化）
- Josuttis 4e 的「实现注释」笔法（`book:stdlib4`）——讲库不讲玄学

## 待补

- （三本待补书已全部入库：D&E `de:<ch>`、K&R `book:krc:<ch>`、Exceptional C++ `book:exceptional-cpp:<item>`。）

## 写作约定（与 AGENT.md 对齐）

1. 每个盒子 ≤ 6 行；历史注脚必须落在真实文献的具体事实（年份/人名/决策），而非感想。
2. 事故现场必须带可复现程序或已登记案例键（`cert:` / `ubsan:` / `so:`）。
3. 人文层放段尾或盒子，正文事实密度不许被稀释。
