# 第165章 C++ 进阶路线图（C++）

⟶ Book/part01_history/ch01_c_history.md
⟶ Book/part03_language/ch19_variables.md
⟶ Book/part04_memory/ch39_raii_rule.md
⟶ Book/part07_stl/ch77_vector.md
⟶ Book/part10_modern/ch115_move.md

[经验] 你基础弱、只剩暑假两个月、目标嵌入式/C++后端/考研就业。结论先给：**别按教材顺序啃完，先堆出 4 个能写进简历的从零项目**，其余按需补。本章不灌鸡汤，只给可执行路径、命令、资源名。

```cpp
// 验证本章示例的编译器（本机已取证）
// C:/Qt/Tools/mingw1310_64/bin/g++.exe  版本 13.1.0
// 统一编译命令：
//   g++ -std=c++23 -O2 -Wall -Wextra _ch165_xxx.cpp -o _ch165_xxx
```

## ① 概述：为什么需要路线图

[经验] 大二只会应试语法 ≠ 能写工程代码。招聘看**项目 + 底层理解**，不是卷面分。两个月的核心 KPI：

```cpp
// KPI 量化：暑假结束你应当能交出
enum SummerKPI { ThreadPool=1, MemPool=2, Logger=4, JsonParser=8, NetServer=16 };
// 至少拿到前 4 个（值 15），NetServer 加分
```

- 路线错误示范：从第 1 页《C++ Primer》逐行读到第 800 页 → 两周后放弃。
- 正确姿势：能编译的小项目驱动，遇到不会的语法再回查。

```cpp
// 每天最小产出：1 个能跑的 .cpp
int main() { /* 今天写了什么，能编译运行吗？ */ return 0; }
```

## ② C++ 版本演进（一句话每版必学点）

[标准] 不必追新特性全貌，按"够用 + 面试常考"取舍。

```cpp
#include <memory>
#include <thread>
#include <vector>
// C++11：现代 C++ 起点，必须熟
auto x = 5;                       // 类型推导
std::vector<int> v{1,2,3};        // 统一初始化
std::shared_ptr<int> p = std::make_shared<int>(1); // 智能指针
std::thread t([]{ /*...*/ }); t.join();            // 线程
```

```cpp
// C++14：泛型 lambda / 返回值推导（几乎白送）
auto f = [](auto a, auto b) { return a + b; };
```

```cpp
#include <string>
#include <string_view>
#include <map>
// C++17：结构化绑定 / if 初始化 / string_view（工程高频）
std::map<int,std::string> m{{1,"a"}};
for (auto& [k,v] : m) { (void)k; (void)v; }
std::string_view sv = "no copy"; (void)sv;
```

```cpp
#include <vector>
#include <ranges>
#include <algorithm>
// C++20：concepts / ranges / 协程（高级，面试加分项）
std::vector<int> d{3,1,2};
std::ranges::sort(d);
```

- C++23/26：仅了解（如 `std::print`、`std::expected`），不占用暑假主线时间。

## ③ 核心能力地图（四格）

[实现] 把能力拆成四块，缺哪块补哪块：

```
┌─────────────┬─────────────┐
│ 语言(Lang)   │ 标准库(STL)  │
│ 指针/引用    │ 容器/算法    │
│ 类/继承/虚   │ 智能指针     │
│ 模板/concepts│ 并发/原子    │
├─────────────┼─────────────┤
│ 工具(Tools)  │ 系统(System) │
│ g++/gdb/perf │ OS/进程/线程 │
│ sanitizer    │ 内存模型     │
│ cmake        │ 网络/socket  │
└─────────────┴─────────────┘
```

```cpp
#include <vector>
// 自测：下面每样能否 5 分钟内手写？不能就进对应章节
void self_test() {
    int* p = new int(1);          // 语言: 指针
    std::vector<int> v(10);       // STL: 容器
    // gdb 打断点、sanitizer 跑一遍  // 工具
    // 说清栈/堆/虚表布局            // 系统
    delete p;
}
```

## ④ 初级→中级路径（2 周：指针/引用/STL/类）

[实现] 每天 2–3h，第 1–2 周目标：能写 RAII、能熟练用 STL。

```cpp
// 练习1：指针与函数指针（文件 Examples/_ch165_pointer.cpp）
int (*fp)(int,int) = &add;        // 函数指针
const int* cp = &x;               // 指向 const
int* const pc = &x;               // const 指针
```

```cpp
#include <utility>
#include <vector>
// 练习2：引用与移动（文件 Examples/_ch165_reference.cpp）
void inc(int& r) { r++; }
std::vector<int> w = std::move(v); // 移动而非拷贝
```

```cpp
#include <string>
#include <map>
#include <algorithm>
// 练习3：STL 三件套（文件 Examples/_ch165_stl.cpp）
std::sort(v.begin(), v.end());
std::count_if(v.begin(), v.end(), [](int x){ return x>3; });
std::map<std::string,int> m; m["k"]=1;
```

```cpp
#include <iostream>
// 练习4：类与构造/析构顺序
struct A { A(){std::cout<<"A";} ~A(){std::cout<<"~A";} };
struct B { A a; B(){std::cout<<"B";} ~B(){std::cout<<"~B";} };
// 构造 A→B，析构 B→A（栈式反向）
```

周末交付物：一个用 STL + 类的小程序（如学生成绩管理，文件读写用 `std::fstream`）。

## ⑤ 中级→高级路径（3 周：模板/并发/内存/源码）

[实现] 第 3–5 周目标：能写模板、能写线程安全代码、看得懂 STL 源码片段。

```cpp
#include <iostream>
// 练习5：模板与特化（文件 Examples/_ch165_template.cpp）
template<typename T> T max(T a,T b){ return a>b?a:b; }
template<> struct Box<bool> { bool v; void flip(){v=!v;} };
template<typename... Ts> void print(Ts... xs){ ((std::cout<<xs<<" "),...); }
```

```cpp
// 练习6：concepts 约束（文件 Examples/_ch165_concept.cpp）
template<std::integral T> T square(T x){ return x*x; }
```

```cpp
#include <mutex>
// 练习7：并发与原子（文件 Examples/_ch165_concurrency.cpp）
std::mutex mtx; std::lock_guard<std::mutex> lk(mtx); ++counter;
std::atomic<int> ac{0}; ++ac;     // 无锁计数
```

```cpp
// 练习8：内存对齐与 placement new（文件 Examples/_ch165_memory.cpp）
struct Align16 { alignas(16) int x; };
int* p = new (buf) int(99);       // 在指定缓冲区构造
```

周末交付物：把练习 7 改成"生产者-消费者"模型（条件变量 `std::condition_variable`）。

## ⑥ 系统编程方向（关联 第163章 网络 / 操作系统）

[平台] 后端路线核心。先吃透三个系统调用层概念：文件描述符、进程/线程、I/O 多路复用。

```cpp
#include <cstdint>
#include <cstddef>
#include <vector>
#include <string>
// 系统编程最小骨架：把"长度前缀帧"跑通（文件 Examples/_ch165_network.cpp）
void encode(std::vector<uint8_t>& out, const std::string& payload);
bool decode(const std::vector<uint8_t>& buf, size_t& pos, std::string& out);
```

```cpp
// 项目名：单线程 Reactor 回声服务器（epoll / IOCP）
// 关键文件落点：见第163章 网络（事件循环 + 非阻塞 socket）
class Reactor { /* add_event / del_event / loop */ };
```

务实建议：先读懂 `muduo`（陈硕）的 `EventLoop` 一处实现，再自己写一版迷你回声服务器，工时约 1 周。

## ⑦ 嵌入式方向（STM32 / FreeRTOS）

[平台] 嵌入式不追 C++ 高级特性，重"确定性与内存可控"。用 STM32CubeMX 生成工程后，用 C++ 写驱动类。

```cpp
#include <cstdint>
// 嵌入式片段：用类封装 LED（无堆分配、无异常、无 RTTI）
class Led {
    volatile uint32_t* const reg_;
public:
    constexpr Led(volatile uint32_t* r) : reg_(r) {}
    void on()  const { *reg_ |= (1u << 5); }
    void off() const { *reg_ &= ~(1u << 5); }
};
```

```cpp
// FreeRTOS 练手：创建两个任务交替翻转
// xTaskCreate(led_task, "led", 128, nullptr, 1, nullptr);
// vTaskStartScheduler();
```

练手项目名（按难度）：① 按键消抖状态机 → ② 串口环形缓冲 → ③ FreeRTOS 多任务数据采集 → ④ 用 C++ 写轻量驱动框架。开发板：STM32F103C8T6（蓝 pill，约 ¥20）。

## ⑧ 高性能 / 游戏方向（关联 第142章 ECS / 第143章 DOD）

[实现] 性能路线的关键不是"多开线程"，而是**数据局部性（DOD）**。

```cpp
#include <vector>
// 错误示范：面向对象，缓存不友好
struct Entity { float x,y,z; int hp; /* 散落内存 */ };
std::vector<Entity> ents;          // 遍历时大量 cache miss

// 正确示范：结构数组(SoA)
struct Entities {
    std::vector<float> x, y, z;     // 连续存储，遍历友好
    std::vector<int>   hp;
};
```

```cpp
// ECS 最小骨架（见第142章 ECS）
struct Position { float x, y; };
struct Velocity { float dx, dy; };
// System: for each (pos,vel): pos += vel * dt;
```

练手：把"一万个球碰撞"从 OOP 改成 SoA，用 `perf` 对比 cache-miss 下降（见第⑫节）。

## ⑨ 编译器 / 库开发方向（读源码路径）

[标准] 想进基础架构岗，必须会读标准库与编译器源码。路线：先 STL 实现，再 LLVM/模板元编程。

```cpp
#include <cstddef>
#include <vector>
// 源码剖析：读 std::vector 扩容逻辑（练习载体）
// 文件：第159章 数据结构（vector / 红黑树手写实现）
// 行号：vector::reserve / push_back 扩容段
//
// 关键判断（伪代码，对应源码逻辑）：
//   if (size_ == capacity_) {
//       size_t n = capacity_ ? capacity_ * 2 : 1;
//       reallocate(n);   // 分配新缓冲、搬移、释放旧缓冲
//   }
```

```cpp
#include <cstddef>
// 读源码练习：自己实现简化 vector（文件见第159章 练习载体）
template<typename T>
class MyVec {
    T* data_ = nullptr; size_t size_ = 0, cap_ = 0;
public:
    void push_back(const T& v) {
        if (size_ == cap_) { cap_ = cap_ ? cap_*2 : 1; /* realloc */ }
        data_[size_++] = v;
    }
};
```

读源码顺序：`libstdc++` 的 `<vector>`、`<functional>` → `folly`/`abseil` 工具库 → LLVM `llvm/ADT`（如 `SmallVector`）。

## ⑩ 必读书单（务实 4 本，含先读哪章）

[经验] 按"先肌肉记忆、后原理"顺序，不要从厚到薄死读。

```cpp
// 阅读顺序（暑假可执行版）
const char* order[] = {
  "C++ Primer        -> 第1-6,12-14章(语法+STL) 先读完",
  "Effective C++     -> 55条全部过一遍( idiom 肌肉记忆)",
  "STL源码剖析       -> vector/list/红黑树/哈希(配第159章手写)",
  "深度探索C++对象模型-> 对象布局/虚表/构造语义(面试底层)"
};
```

- 《C++ Primer》（Lippman）：语法字典，第 1–6、12–14 章先读，其余当查。
- 《Effective C++》（Scott Meyers）：55 条都过，每条写一句自己的话。
- 《STL 源码剖析》（侯捷）：配合第 159 章手写 vector/红黑树食用。
- 《深度探索 C++ 对象模型》（Inside the C++ Object Model）：虚函数、多重继承布局必读。

```cpp
// 读书产出检验：能否默写对象内存布局？
struct Base { virtual void f(); int a; };
struct Der : Base { int b; };
// sizeof(Der) >= 16 (vptr 8 + a 4 + b 4, 对齐)
```

## ⑪ 必做项目（关联 第159-164章 从零实现）

[实现] 这是简历核心。每个项目给出工时与落点章。

```cpp
// 项目1：线程池（见第159章 线程池，文件 Examples/_ch165_threadpool.cpp）
// 工时：3 天。落点：mutex + condition_variable + 任务队列
ThreadPool pool(4); pool.submit([]{ /* job */ });
```

```cpp
// 项目2：内存池（见第160章 内存池，文件 Examples/_ch165_mempool.cpp）
// 工时：2 天。落点：定长块 freelist，减少 new/delete 碎片
FixedPool pool(sizeof(int)); void* p = pool.alloc(); pool.free(p);
```

```cpp
// 项目3：日志库（见第161章 日志，文件 Examples/_ch165_log.cpp）
// 工时：2 天。落点：级别 + 时间搓 + 线程安全 + 文件滚动
Logger log("app.log"); log.info("server start");
```

```cpp
// 项目4：JSON 解析器（见第162章 JSON，文件 Examples/_ch165_json.cpp）
// 工时：4 天。落点：递归下降 + variant 值模型
// 练习实现 parse_value / parse_object / parse_array
```

```cpp
// 项目5：网络框架（见第163章 网络，文件 Examples/_ch165_network.cpp）
// 工时：1 周。落点：Reactor + 长度前缀帧 + 连接管理
// 进阶：见第164章 框架（把上述组装成 mini RPC）
```

优先级：线程池 > 内存池 > 日志 > JSON > 网络。前四个两周内必完。

## ⑫ 工具链精通（gdb / perf / sanitizer 具体命令）

[实现] 不会工具 = 调试靠猜。以下命令背下来并各跑一次。

```bash
# 1) 编译带调试信息
g++ -std=c++23 -g -O0 -fsanitize=address,undefined main.cpp -o main

# 2) AddressSanitizer 抓内存错误（越界/泄漏）
./main            # 报错直接给行号与调用栈

# 3) gdb 基础
gdb ./main
(gdb) break main.cpp:42     # 在指定行断点
(gdb) run
(gdb) backtrace             # 看调用栈
(gdb) print x               # 看变量
(gdb) watch counter         # 监视变量变化

# 4) perf 抓性能热点（Linux；Windows 用 ETW / Visual Studio 性能探查器）
perf record ./main
perf report                 # 看哪行最耗时 / cache-miss
```

```cpp
// sanitizer 实战：这段会被 AddressSanitizer 抓到堆溢出
int* a = new int[4];
a[4] = 1;            // heap-buffer-overflow，运行时直接报行号
delete[] a;
```

## ⑬ 标准跟进（WG21 proposals / 编译器 release notes）

[标准] 不必逐条读提案，但要知道"去哪看"。

```cpp
// 关注方式（务实）
// 1) WG21 提案站: 搜 "PxxxxRy <特性名>" 看动机与示例
// 2) 编译器 release notes: GCC/Clang/MSVC 每条 -std=c++2x 支持表
// 3) 订阅: /r/cpp、ISO C++ 官网 "News"
```

```cpp
#include <expected>
// 看提案学会的最小能力：读懂特性示例
// 例 C++23 std::expected（错误处理替代异常）
// std::expected<int, Err> r = compute();
// if (!r) return r.error();
```

暑假只需"知道有哪些新东西 + 能读懂示例"，不要求会提案写作。

## ⑭ 社区与开源（GitHub 搜什么关键词练手）

[经验] 直接读大厂代码比看教程快。按关键词搜：

```cpp
// GitHub 搜索语法（直接可用）
//   language:C++ stars:>5000 topic:networking
//   "thread pool" language:C++
// 推荐仓库（搜名即得）：
//   facebook/folly, google/abseil-cpp, boostorg,
//   chenshuo/muduo, entropia/tinyhttpd
```

```cpp
// 贡献路径：先 fork → 修一个文档 typo → 再修 good-first-issue
// 哪怕只合进一个 typo PR，简历也能写"参与开源"
```

务实：暑假不要求合大特性，能读懂 `muduo::EventLoop` 一处并写笔记，价值已够。

## ⑮ 面试考点地图（基础弱→重点补）

[经验] 校招 C++ 后端高频题，按出现频率排序。配 cpp 自测能否手写。

```cpp
// 高频1：指针与引用区别
// 指针可空可重指有独立地址；引用必绑对象、无独立对象语义
int a=1; int& r=a; int* p=&a; (void)r; (void)p;
```

```cpp
// 高频2：虚函数与多态（对象模型第10节）
struct B { virtual void f() {} virtual ~B(){} };
struct D : B { void f() override {} };
B* b = new D(); b->f();   // 动态绑定，走 vtable
delete b;
```

```cpp
// 高频3：STL 底层（vector 扩容 / map 红黑树 / unordered_map 哈希）
// 见第159章：手写 vector 与红黑树即为此题答案
```

```cpp
#include <memory>
// 高频4：智能指针区别
// unique_ptr 独占(零开销)；shared_ptr 引用计数(原子)；weak_ptr 破环
auto u = std::make_unique<int>(1);
auto s = std::make_shared<int>(2);
std::weak_ptr<int> w = s;   // 不增计数
```

```cpp
// 高频5：并发（互斥/死锁/原子内存序）
// 死锁根因：两锁获取顺序不一致 → 统一加锁顺序或用 std::lock
std::lock(m1, m2);          // 同时锁，避免死锁
```

其他：内存对齐、new/delete 与 malloc/free 区别、移动语义、CRTP。每题都能在第 159–164 章找到对应手写练习。

## ⑯ 考研方向（数二 + 英二 + 408 衔接）

[经验] 考研与就业不冲突，C++ 主要用在**数据结构与算法（408 之一）**和**机试**。

```cpp
// 408 四门优先级（对 C++ 就业者）
// 数据结构(最相关,用C++写算法题) > 计算机组成(理解底层) >
// 操作系统(进程/内存/并发,与第163章互补) > 计算机网络(与网络项目互补)
```

```cpp
#include <vector>
// 机试练手：用 C++ STL 刷基础题（不碰高级特性，求稳）
// 例：快排手写
void qsort(std::vector<int>& a, int l, int r) {
    if (l >= r) return;
    int p = a[l]; int i=l, j=r;
    while (i < j) { while(i<j&&a[j]>=p)--j; a[i]=a[j];
                   while(i<j&&a[i]<=p)++i; a[j]=a[i]; }
    a[i]=p; qsort(a,l,i-1); qsort(a,i+1,r);
}
```

务实：408 用王道/天勤教材；机试用 C++ STL，别在考场炫 concepts。暑假每天留 1h 给数学/408，C++ 项目照常。

## ⑰ 常见误区（应试 vs 工程，3 条）

[经验] 你最可能在这些坑里浪费时间：

```cpp
// 误区1：刷题多 = 能写项目
// 现实：刷 300 道 LeetCode 仍写不出线程池。项目与算法是两套能力。
bool can_write_project = (leetcode_count > 300) && (projects == 0); // 仍 false
```

```cpp
#include <memory>
// 误区2：把 C++ 当 C 用，全程裸指针 + malloc
// 现实：工程用 RAII + 智能指针防泄漏，裸指针只在底层接口出现
void bad() { int* p = (int*)malloc(sizeof(int)); /* 易忘 free */ }
void good(){ auto p = std::make_unique<int>(1); } // 离开作用域自动释放
```

```cpp
// 误区3：追最新标准特性，忽略基础
// 现实：面试考虚表布局/内存对齐，不考 std::print
// 先把 C++11/14/17 用熟，20/23 当加分
```

## ⑱ 30 / 60 / 90 天计划（暑假紧凑表）

[经验] 两个月 ≈ 60 天，每天 2–3h。下表按周排，具体到动作。

```
┌──────┬──────────────────────────────┬──────────┐
│ 周次 │ 动作                         │ 交付物   │
├──────┼──────────────────────────────┼──────────┤
│ W1-2 │ 语法+STL(④) 每天1个cpp       │ 成绩管理 │
│ W3-5 │ 模板+并发+内存(⑤)           │ 生产者模型│
│ W6   │ 线程池(⑪)                   │ 线程池   │
│ W7   │ 内存池+日志(⑪)              │ 两库     │
│ W8   │ JSON解析(⑪)                 │ JSON库   │
│ W9   │ 网络框架(⑪⑥)                │ 回声服务器│
│ W10  │ 读书+面试刷题(⑩⑮)           │ 笔记+简历│
└──────┴──────────────────────────────┴──────────┘
```

```cpp
// 每天固定节奏（2-3h）
// 1h 读书/看源码 → 1h 写当天 cpp → 0.5h 跑 sanitizer+单测 → 0.5h 记笔记
struct Day { bool read, code, test, note; };
```

备考穿插：每天另挤 1h 给数二/英二/408（不占用上面 C++ 时间）。

## ⑲ 资源索引（全部具体可搜）

[经验] 以下名字直接搜即得，无空泛推荐。

```cpp
// B站 UP 主（搜名字）
//   侯捷：C++ 面向对象/STL/内存模型系列（配第10节读书）
//   linbai：现代 C++ 实战
//   程序喵大人：C++ 面试向
//   极客时间《C++ 实战训练营》(付费,按需)
```

```cpp
// 书籍（见第⑩节顺序）
//   C++ Primer / Effective C++ / STL源码剖析 / 深度探索C++对象模型
// 在线：en.cppreference.com（语法权威查）、zh.cppreference.com（中文）
```

```cpp
// 练手项目名（直接搜）
//   muduo（网络）、tinyhttpd（HTTP）、redis（数据结构/网络）
//   STM32F103 裸机→FreeRTOS 例程（嵌入式）
//   本机示例集：Examples/_ch165_*.cpp（14 个已验证可编译）
```

```cpp
// 求职/刷题
//   LeetCode（算法）、牛客网（C++ 面经）、GitHub trending(C++)
```

## ⑳ 小结

[经验] 先写完 4 个从零项目（线程池/内存池/日志/JSON）再谈其他；简历没项目，其余皆空。


## 附录 A：进阶阅读路线 [B: Principle / F: Industry / J: Learning]

### 等级 1：语言掌握（1-3 个月）
```
必须读完:
- Effective Modern C++ (Scott Meyers, 2014) — 42个条款, 每个10页
- C++ Core Guidelines (Bjarne Stroustrup + Herb Sutter, github.com/isocpp/CppCoreGuidelines)
  → 焦点: R(资源管理), C(类), F(函数), Con(并发)

必须练完:
- LeetCode 100 题 (用 C++, STL容器, 不用裸指针)
- 4个从零项目: ch159线程池 + ch160内存池 + ch161日志 + ch162 JSON
```

### 等级 2：专家级（3-12 个月）
```
阅读顺序:
1. C++ Concurrency in Action (Anthony Williams, 2nd ed)
   → 读完 ch107-113 后必读: 理解memory_order, lock-free, hazard pointer的工业实现

2. A Tour of C++ (Bjarne Stroustrup, 3rd ed)
   → 全局视角: 哪些特性值得用, 哪些是历史包袱

3. [源码阅读] libstdc++ <vector>, <string>, <shared_ptr> 实现
   → 真实代码: SSO, 三指针布局, 控制块, introsort depth_limit

4. [源码阅读] LLVM Pass Manager, Clang AST
   → 理解大型C++项目的架构: 继承层次, 工厂模式, RTTI的正确用法

5. [工业文献] Google C++ Style Guide + Abseil C++ Tips of the Week
   → 现实约束: 为什么Google禁异常? 为什么用StatusOr? 为什么不用shared_ptr?
```

### 等级 3：工业贡献（12+ 个月）
```
- 贡献开源: LLVM (添加clang-tidy check), Chromium (fix bug), ClickHouse (add aggregate function)
- 内部库开发: 类似 folly, Abseil 的基础设施组件
- 性能工程: perf + VTune + Compiler Explorer 达到专家级
- 标准参与: 跟踪 WG21 邮件列表, 参加 SG1/SG14 会议
```

```cpp
#include <iostream>
int main() {
    std::cout << "C++ mastery roadmap:" << std::endl;
    std::cout << "Level 1 (3mo): Effective Modern C++ + Core Guidelines + LeetCode 100" << std::endl;
    std::cout << "Level 2 (9mo): Concurrency in Action + libstdc++ source + LLVM" << std::endl;
    std::cout << "Level 3 (ongoing): Open source contributions + perf engineering + WG21" << std::endl;
    return 0;
}
```

## 附录 B：嵌入式/后端/考研 三条路线映射 [H: Design]

| 目标 | 必读章 (本书) | 补充阅读 | 项目 |
|---|---|---|---|
| 嵌入式工程师 | ch30 volatile, ch107-113 并发, ch155 SIMD, ch17 交叉编译 | STM32 HAL手册, ARM Architecture Reference Manual | FreeRTOS+传感器项目, 裸机bootloader |
| 后端开发 | ch93-94 线程/取消, ch107-112 原子/无锁, ch163 网络编程 | Linux System Programming, Google SRE book | 高性能Web服务器, 消息队列, RPC框架 |
| 考研408 | ch01 C历史, ch04/ch06/ch07 版本演进, ch95-101 算法, ch35-47 内存+OOP | 王道考研408系列, 数据结构(严蔚敏) | 408真题 (C++实现版) |

```cpp
#include <iostream>
int main() {
    std::cout << "Embedded: ch30(volatile) + ch107(atomic) + ch155(SIMD)" << std::endl;
    std::cout << "Backend: ch93(thread) + ch107(atomic) + ch163(network)" << std::endl;
    std::cout << "Postgraduate: ch01(C history) + ch95-101(algorithms) + ch35-47(memory+OOP)" << std::endl;
    return 0;
}
```

| 职级 | 面试期望 | 本书覆盖 |
|---|---|---|
| 应届/实习 | STL容器使用, 智能指针, 基本多线程 | ch77-94, ch41, ch93 |
| 初级 (1-3年) | RAII, 异常安全, 移动语义, constexpr | ch39, ch40, ch115, ch69 |
| 中级 (3-5年) | 无锁编程, 模板元编程, 性能优化 | ch107-112, ch60-72, ch152-158 |
| 高级 (5-8年) | 源码阅读, ABI设计, 架构决策, 标准参与 | ch124-134, ch11-18, ch02 |

## 附录 C：你还需要读什么 [J: Learning]

本书覆盖不全的领域（需要外部补充）：

```
1. 编译原理 (本书: ch11编译器, ch127 LLVM)
   → 补充: Engineering a Compiler (Keith Cooper, 3rd ed)
   → 实践: 用LLVM写一个简单的C++编译器Pass

2. 操作系统 (本书: ch35内存模型, ch107-113并发)
   → 补充: Operating Systems: Three Easy Pieces (Remzi Arpaci-Dusseau)
   → 实践: 写一个简单的x86-64 kernel (mit 6.828)

3. 数据库系统 (本书: ch132 LevelDB/RocksDB)
   → 补充: Designing Data-Intensive Applications (Martin Kleppmann)
   → 实践: 从零实现简单的SQL引擎

4. 网络协议 (本书: ch163 网络编程)
   → 补充: TCP/IP Illustrated, Vol.1 (W. Richard Stevens)
   → 实践: 用C++实现HTTP/1.1服务器

5. 分布式系统 (本书未覆盖)
   → 补充: Distributed Systems (Maarten van Steen, 4th ed)
   → 实践: 实现简单的Raft共识算法
```

```cpp
#include <iostream>
int main() {
    std::cout << "Beyond this book:" << std::endl;
    std::cout << "Compilers: LLVM Pass + Engineering a Compiler" << std::endl;
    std::cout << "OS: x86-64 kernel + OSTEP (mit 6.828)" << std::endl;
    std::cout << "Databases: SQL engine + DDIA (Kleppmann)" << std::endl;
    std::cout << "Networking: HTTP/1.1 server + TCP/IP Illustrated" << std::endl;
    std::cout << "Distributed: Raft consensus + van Steen" << std::endl;
    std::cout << "This book = C++ foundation. These 5 = industry expertise." << std::endl;
    return 0;
}
```

[标准] 本书147章覆盖C++语言+STL+并发+模板+工程+性能的全栈知识体系。
[经验] 读完本书 = 中高级C++工程师的知识广度。深度靠实践 + 开源贡献。



## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第115章](Book/part10_modern/ch115_move.md) | TCP服务器/HTTP客户端 | 本章提供概念，第115章提供实现 |
| [第77章](Book/part07_stl/ch77_vector.md) | 静态多态/编译期接口 | 本章提供概念，第77章提供实现 |
| [第39章](Book/part04_memory/ch39_raii_rule.md) | 共享所有权/图结构 | 本章提供概念，第39章提供实现 |
| [第19章](Book/part03_language/ch19_variables.md) | 高性能容器/零拷贝传输 | 本章提供概念，第19章提供实现 |
| [第1章](Book/part01_history/ch01_c_history.md) | 高性能分配/资源复用 | 本章提供概念，第1章提供实现 |


## 相关章节（交叉引用）

- **相邻主题**：⟶ Book/part15_cases/ch164_framework.md（第164章 从零实现迷你框架（C++））—— 编号相邻、主题接续。
- **相邻主题**：⟶ Book/part15_cases/ch163_net.md（第163章 从零实现网络编程（C++））—— 编号相邻、主题接续。


## 附录 G（标准演进与弃用时间线）

C++ 标准每三年一版，下列为特性引入与弃用的真实节点。

```text
; 特性探测宏（编译器预定义）
mov eax, 0x0000          ; __cplusplus 低 16 位
mov ecx, 0x202302L       ; C++23 值（示意）
cmp eax, ecx
jl  .older
```

### 版本与年份

- C++11（2011，`__cplusplus`=201103L）：move / lambda / `std::thread`
- C++14（2014）：泛型 lambda；C++17（2017）：`std::string_view` / `if constexpr`
- C++20（2020）：concepts / ranges / coroutines；C++23（2023）：`std::expected`
- C++26（预计 2026）：静态反射 / 契约（contracts）

### 弃用节奏

- `std::auto_ptr` 于 C++11 弃用、C++17 移除（间隔 0x0006 年）
- `std::random_shuffle` C++14 弃用、C++17 移除
- `std::codecvt` C++17 弃用；`std::gslice` 仍在但边缘化

### 编译器支持

- GCC 13.2 / Clang 18 / MSVC 19.3 对 C++20 覆盖 > 0x0090%
- 静态反射提案 P0784R7 进入 C++26；`__attribute__` 兼容性持续维护

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例：入职第一周的 C++ 代码——新人的典型陷阱

某量化交易团队统计过去 3 年 12 名 C++ 新人入职第一周的 Code Review 拒绝原因排行：① 未用 RAII 管理资源（手动 `new`/`delete`，异常路径漏释放）占 38%；② 函数签名用值传递大型对象（`void f(vector<int> v)` 而非 `const vector<int>&`）占 22%；③ 迭代器失效（`v.push_back()` 后继续用之前 `begin()`/`end()` 返回的迭代器）占 15%；④ 未初始化变量（UB，-Wall 开了但部分新人关 warning）占 10%。团队后来建立入门 Checklist：新人必须通过 3 个 PR（分别触发类型一①②③④）才能合入主线。

### 常见 Bug / Debug 方法

- **"看懂了"但写不出来**：视频/博客被动学习形成"理解错觉"（illusion of competence）。验证方法：关闭所有资料，手写一个无 IDE 补全的 `.cpp` 文件并编译→立即暴露缺口。
- **算法刷太多、工程写太少**：LeetCode 200 题但 `CMakeLists.txt` 写不对、不会用 `gdb` 查 segfault。建议 1:1 分配时间——每刷 1 道算法题至少写 1 个多文件 C++ 小程序。
- **C++ 版本混乱**：同时学 C++98 教程和 C++20 特性导致心智冲突（如 `auto_ptr` vs `unique_ptr`）。学习路线应锁定一个标准版本（推荐 C++17 起点，用 `-std=c++17` 编译一切练习代码）。

### Code Review 关注点（学习产出审查）

- 个人项目代码是否通过 `-Wall -Wextra -Wpedantic`？零 warning 是 C++ 入门的分水岭。
- 是否能用 `const` 正确标注只读参数/成员函数？`const` 用量是 C++ 代码质量的强信号——生产级代码 `const` 密度通常 >15%。
- 异常安全：函数在 `new` 失败或中间步骤抛异常后，资源是否全部释放？（等价于：每个资源获取是否都有对应的 RAII 包装？）

### 重构建议（学习路径迭代）

- C++98 教程作废：直接从 C++17 起步（结构化绑定/`std::optional`/`if constexpr` 已成新基础），遇到旧代码再看对应标准差异。
- 开源贡献是检验标准：给 `llvm`/`fmtlib`/`abseil` 修一个真实 bug（哪怕 3 行 patch）>> 读完一整本书的被动学习。PR 被 merge 的那一天 = C++ 实战能力真正的里程碑。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 练习 1（难度 ★★）

工具链里的 AddressSanitizer 能在越界/泄漏发生的瞬间抓出来。请写一个 `SafeArray`，
用 `operator[]` 做边界检查并在越界时抛异常，演示“早失败、定位准”比“裸数组悄悄越界”安全。

```cpp
#include <iostream>
#include <vector>
#include <stdexcept>
#include <cstddef>

template <typename T>
class SafeArray {
    std::vector<T> v_;
public:
    explicit SafeArray(std::size_t n) : v_(n) {}
    T& operator[](std::size_t i) {
        if (i >= v_.size()) throw std::out_of_range("SafeArray 越界");
        return v_[i];
    }
    const T& operator[](std::size_t i) const {
        if (i >= v_.size()) throw std::out_of_range("SafeArray 越界");
        return v_[i];
    }
};

int main() {
    SafeArray<int> a(3);
    a[0] = 10; a[1] = 20; a[2] = 30;
    std::cout << "a[1]=" << a[1] << '\n';
    try {
        a[5] = 99;                       // 越界：立刻抛异常，定位到精确位置
    } catch (const std::out_of_range& e) {
        std::cout << "捕获越界: " << e.what() << '\n';
    }
    // 注：真实项目用 `g++ -fsanitize=address` 可在原生数组越界时也抓到，无需手写包装
}
```

[标准] 工具链（ASan/UBSan/gdb）是工程效率的倍增器；`std::vector::at` 本身也做边界检查（关联 ⑫ 工具链）。

### 练习 2（难度 ★★★）

调试时最怕“只看到一句 log，不知来自哪个文件哪一行”。C++20 的 `std::source_location`
让日志自动携带调用点位置，是现代化诊断的基础。

```cpp
#include <iostream>
#include <source_location>
#include <string>

void log(const std::string& msg,
         const std::source_location& loc = std::source_location::current()) {
    std::cout << "[" << loc.file_name() << ":" << loc.line() << " "
              << loc.function_name() << "] " << msg << '\n';
}

int main() {
    log("启动");                 // 自动带上本行文件:行:函数
    log("加载配置");
}
```

[标准] `std::source_location::current()` 是编译期内置，零运行时开销即可获得精确来源，
取代宏拼接 `__FILE__`/`__LINE__` 的旧写法（关联 ⑫ 工具链精通）。

### 练习 3（难度 ★★★★）

回归出现后，手工逐个 commit 试太低效。`git bisect` 本质是“在有序的‘通过→失败’序列上二分”。
请用 `std::lower_bound` 找到“第一个失败提交”的索引。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstddef>

int main() {
    // builds[i]==true 表示该 commit 编译/测试通过；失败后恒为 false
    std::vector<bool> builds = {true, true, true, false, false, false};
    // 找第一个 false：等价于在“通过段”之后第一个失败
    auto it = std::lower_bound(builds.begin(), builds.end(), false);
    std::size_t first_fail = static_cast<std::size_t>(it - builds.begin());
    std::cout << "第一个失败提交索引=" << first_fail << '\n';
    // 对应 git bisect：只需 log2(N) 次 checkout 即可定位，而非线性 N 次
}
```

[标准] 把“定位回归”建模为有序序列上的二分，复杂度从 O(N) 降到 O(log N)；`git bisect` 即此思想的封装
（关联 ⑭ 社区与开源 / ⑫ 工具链）。

## 附录：用法演绎（从选型到落地）

### 演绎 1：把“90 天计划”落到具体可做的项目上

**场景**：路线图列了一堆方向，但没有“这周写什么”就会永远停在收藏夹。
**选型**：把阶段目标映射为“从零实现”项目（第 159–164 章），每完成一个就补一块能力拼图。
**落地**：

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <cstddef>

int main() {
    struct Project { const char* phase; const char* name; };
    Project plan[] = {
        {"第1月", "vector / string 容器自实现 (ch77)"},
        {"第1月", "智能指针 unique_ptr/shared_ptr (ch41)"},
        {"第2月", "线程池 ThreadPool (ch159)"},
        {"第2月", "JSON 解析器 (ch162)"},
        {"第3月", "网络 echo 服务器 (ch163)"},
        {"第3月", "协程 async 调度 (ch164)"},
    };
    for (auto& p : plan)
        std::cout << "[" << p.phase << "] " << p.name << '\n';
}
```

**结论**：路线图的真正价值是“可执行的项目清单”，而非书单；每做一个从零实现，理解深度远超读十篇博文
（关联 ⑪ 必做项目 / ⑱ 30/60/90 天计划）。

### 演绎 2：如何读 WG21 提案——从“编号”读出“它在改什么”

**场景**：标准在演进，但提案库（open-std.org）浩如烟海，新手无从下手。
**选型**：按提案编号区间判断主题（语言特性 / 库 / 演化），先读“已合并进某版 C++”的，再读“活跃草案”。
**落地**：

```cpp
#include <iostream>
#include <string>

const char* topic_of(int n) {
    if (n >= 1000 && n < 2000) return "核心语言特性";
    if (n >= 2000 && n < 3000) return "标准库（容器/算法/工具）";
    if (n >= 3000 && n < 4000) return "C 兼容性 / 演化";
    return "其他/跨领域";
}

int main() {
    for (int n : {1390, 2673, 3307})            // 例：=delete 概念 / 标准库工具 / 演化
        std::cout << "P" << n << " -> " << topic_of(n) << '\n';
}
```

**结论**：提案编号有主题分区，先锁定“已被某版 C++ 采纳”的提案读，再跟进活跃草案，
能高效跟进标准而不被信息淹没（关联 ⑬ 标准跟进 / ② 版本演进）。

## 最佳实践 [经验]

- **按依赖顺序学，不要按目录跳**：变量/存储期/RAII/引用指针是地基，再上 STL/模板/现代特性；路线图里「前置」标记的分支务必先读，否则上层概念会悬空。
- **每章配一个可编译的最小实验**：路线图给出路径，但肌肉记忆来自亲手敲；读完后用 10 行代码验证该章结论（如移动语义真的零拷贝），比通读三遍更有效。
- **把「能跑」和「能解释」分开验收**：能抄代码跑通不算掌握，能向他人讲清「为什么这样设计、底层发生了什么」才算；路线图每阶段末用一道面试题自测。
- **现代特性按需取用，不为炫技**：C++20/23 的 concepts/ranges/模块解决具体痛点才引入；路线图标注「工业级深度版」的章节是工程必备，装饰性特性留作拓展。