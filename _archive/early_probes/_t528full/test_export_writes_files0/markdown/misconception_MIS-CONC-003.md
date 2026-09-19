# MIS-CONC-003（misconception）

## 正面

【误解】MIS-CONC-003 没被 TSan 报就是没有数据竞争 / 数据竞争只是偶尔算错
触发说法：没被 TSan 报就是安全的

## 背面

为什么错：TSan 只分析被 -fsanitize=thread 插桩的 TU；第三方库/内联汇编/未插桩 TU 内的竞争它看不到（漏报），故「没被报 ≠ 没有」
反例 1：数据竞争是 C++ 标准明文的未定义行为，不是「答案偶尔错」：编译器可据此做激进优化（寄存器缓存、删除看似冗余的读），行为完全不可预测
反例 2：C++ 的 volatile 不建立线程间 happens-before，不能防数据竞争——TSan 对 volatile 竞争照样报；防竞争靠 atomic/mutex/barrier
关联原子：ATOM-CONC-RACE-001
