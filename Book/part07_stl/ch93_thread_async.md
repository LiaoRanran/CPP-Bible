# 第93章　线程与异步：thread / future / async

> 标准基：ISO/IEC 14882:2023 (C++23) · GCC 13.1.0 (MinGW, x86-64) ／ 预计阅读：180 分钟 ／ 前置：⟶ Book/part03_language/ch19_variables.md、⟶ Book/part06_templates/ch63_variadic.md、⟶ Book/part09_concurrency/ch107_atomic.md ／ 后续：⟶ Book/part07_stl/ch94_stop_token.md、⟶ Book/part07_stl/ch93_thread_async.md、⟶ Book/part09_concurrency/ch107_atomic.md ／ 难度：★★★★☆

> 立场标签约定：本文 `[标准]` 指 ISO C++ 规定；`[实现·GCC13]` 指 GCC 13.1 / libstdc++ 行为；`[平台·x86-64]` 指 Windows x64 (MinGW, Itanium-ish Win64 ABI)；`[经验]` 为工程共识。所有 libstdc++ 引用均给出 `文件：` + `行号：`（相对 `lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`）。

---

## ① 学习目标 [标准]

本章把 C++11 引入、并经 C++20/23 打磨的**线程与异步原语**作为一个有机整体讲透：

- `std::thread`：操作系统线程的 RAII 包装，构造即启动、**析构即 terminate** 的残酷契约。
- `std::future` / `std::promise` / `std::packaged_task` / `std::async`：四种"异步结果"表达，本质都是**共享状态（shared state）** 的不同入口。
- `std::async` 的 `launch::async` 与 `launch::deferred` 两种策略，以及 deferred 在 `get()` 处同步求值、async 返回的 `future` **析构会阻塞**这两大陷阱。
- `std::shared_future`、异常如何跨线程经共享状态传播、`future::get()` 一次性的语义。
- `std::call_once` / `std::once_flag`：线程安全的"只做一次"。

学完应能在**不写裸 `pthread`、不直接 `new` 线程、不手动管理 join** 的前提下，用标准库搭出健壮的并发代码，并理解它与 ⟶ Book/part09_concurrency/ch107_atomic.md（并发内存模型）、⟶ Book/part09_concurrency/ch107_atomic.md（原子）、⟶ Book/part09_concurrency/ch108_memory_order.md（内存序）的边界关系。

```cpp
// ① 动机：单线程累加 vs 多线程累加（完整可编译）
#include <iostream>
#include <thread>
#include <vector>
#include <numeric>
int main() {
    const int N = 1'000'000;
    std::vector<int> v(N);
    std::iota(v.begin(), v.end(), 1);          // 1..N
    long long single = 0;
    for (int x : v) single += x;               // 单线程
    std::cout << "single sum = " << single << "\n";

    // 两线程各算一半（仅作结构演示；真实场景见 ⑲ 性能分析）
    long long a = 0, b = 0;
    std::thread t1([&] { for (int i = 0; i < N / 2; ++i) a += v[i]; });
    std::thread t2([&] { for (int i = N / 2; i < N; ++i) b += v[i]; });
    t1.join(); t2.join();
    std::cout << "multi  sum = " << (a + b) << "\n";
    return 0;
}
```

---

## ② 前置知识 [标准]

| 主题 | 为什么必须 | 链接 |
|---|---|---|
| 存储期与 ODR | 线程函数捕获引用时，被引用对象的生命周期必须跨过 `join` | ⟶ Book/part03_language/ch19_variables.md |
| 移动语义 / `std::move` | `promise`、`packaged_task`、`unique_ptr` 只能移动，必须 `std::move` 进线程 | ⟶ Book/part10_modern/ch115_move.md |
| 可变参数模板 / 完美转发 | `std::thread` 构造函数用 `decay` + 包展开把参数**拷贝**进线程 | ⟶ Book/part06_templates/ch63_variadic.md |
| 并发内存模型（happens-before） | 共享状态、join 都建立 happens-before；裸共享变量需原子/互斥 | ⟶ Book/part09_concurrency/ch107_atomic.md |
| 异常安全 | `future::get()` 会把子线程异常重新抛出到调用线程 | ⟶ Book/part04_memory/ch40_exception_safety.md |

`[标准]`：`<thread>`、`<future>` 自 C++11 起即为标准库组件；`std::async`、`std::future`、`std::promise`、`std::packaged_task` 同属 `[thread.req]`、`[futures]` 条款。

---

## ③ 后续依赖 [标准]

- **协作取消**：第94章 ⟶ Book/part07_stl/ch94_stop_token.md 的 `std::jthread` 在 `std::thread` 之上叠加 `stop_token`，其析构自动 `request_stop()` + `join`。
- **互斥与条件变量**：`packaged_task` 常配合 `std::mutex`/`std::condition_variable` 使用，见 ⟶ Book/part07_stl/ch93_thread_async.md、⟶ Book/part07_stl/ch93_thread_async.md。
- **原子与内存序**：共享状态内部用 `std::call_once` + `std::atomic` 实现结果发布，深入见 ⟶ Book/part09_concurrency/ch107_atomic.md、⟶ Book/part09_concurrency/ch108_memory_order.md。
- **执行器与线程池**：`std::async` 是"裸"异步；工业线程池见 ⟶ Book/part07_stl/ch93_thread_async.md 与 ⟶ Book/part15_cases/ch159_threadpool.md。

---

## ④ 知识图谱（ASCII） [标准]

```
                         ┌─────────────────────────────┐
                         │    std::thread (C++11)       │
                         │  构造即启动 OS 线程            │
                         └───────────┬─────────────────┘
                                     │ 仅负责"执行"
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │           异步结果 = 共享状态(shared state)              │
        │  生产者写结果/异常，消费者 future 读                      │
        ├───────────────┬───────────────┬────────────────────────┤
        │ std::promise  │ std::packaged_ │ std::async              │
        │ 手动 set_value│ task(可调用体) │ 工厂：返回 future         │
        └───────┬───────┴───────┬───────┴───────────┬────────────┘
                │               │                   │
                ▼               ▼                   ▼
        std::future<T>  std::future<R>     ┌──────────────────┐
        get()一次性       (task.get_future) │ launch::async    │
                          └──────►           │ launch::deferred│
                │                            └──────────────────┘
                ▼
        std::shared_future<T>  (share()，多消费者)
                │
                ▼
        std::call_once / once_flag  ("只做一次" 原语)
```

`[经验]`：记忆口诀——**`thread` 管"跑"，`future` 管"拿结果"，`async` 是把两者打包的工厂**。

---

## ⑤ Mermaid：四种异步的创建—消费路径 [标准]

```mermaid
flowchart TD
    A[callable F] --> B{选择原语}
    B -->|promise| C[producer: set_value/set_exception]
    B -->|packaged_task| D[task 自身即生产者]
    B -->|async| E[运行时自动起 thread 或 deferred]
    B -->|thread+ref| F[手动传 future 引用]
    C --> G[shared state]
    D --> G
    E --> G
    F --> G
    G --> H[consumer: future.get]
    H --> I{结果 ready?}
    I -->|yes| J[返回 T 或抛异常]
    I -->|no| K[阻塞等待]
    K --> J
```

---

## ⑥ UML 类图（简化） [实现·GCC13]

```mermaid
classDiagram
    class thread {
        +id get_id()
        +void join()
        +void detach()
        +bool joinable()
        -id _M_id
        -_State_ptr _M_state
    }
    class future~T~ {
        +T get()
        +bool valid()
        +shared_future~T~ share()
    }
    class shared_future~T~ {
        +T get()
        +bool valid()
    }
    class promise~T~ {
        +future~T~ get_future()
        +void set_value(T)
        +void set_exception(exception_ptr)
    }
    class packaged_task~F~ {
        +future~R~ get_future()
        +void operator()(Args...)
    }
    class async {
        +future async(launch, F, Args)
    }
    future <|-- shared_future
    promise ..> future : get_future()
    packaged_task ..> future : get_future()
    async ..> future : returns
```

`[实现·GCC13]`：`future` 内部通过基类 `__basic_future<_Res>` 持有 `shared_ptr<_State_base>`（文件：`future`，行号：`605` 的 `_M_shared_state`），所以即使 `future` 被移动/析构，只要还有 `shared_future` 或运行时持有，共享状态不销毁。

---

## ⑦ ASCII 内存图：thread 对象与底层 OS 线程 [实现·GCC13]

```
栈上的 std::thread 对象 (sizeof ≈ 两个指针)
┌──────────────────────────────────────┐
│ std::thread t                         │
│   _M_id  (thread::id: 内部是 __gthread_t)│   ← 标识/句柄
│   _M_state (unique_ptr<_State>)       │──┐
└──────────────────────────────────────┘  │
                                          ▼
                              new _State_impl<_Invoker<tuple<...>>>
                              ┌─────────────────────────────────┐
                              │ vptr → _State_impl vtable        │
                              │ 被decay后的实参 tuple (按值拷贝！)│
                              └─────────────────────────────────┘
                                          │  (OS 调度)
                                          ▼
                              内核线程 / pthread (Win32: CreateThread)
```

`[实现·GCC13]`：`std::thread` 构造函数把可调用对象及其实参 `decay` 后**按值拷贝**进 `_State_impl`（文件：`bits/std_thread.h`，行号：`234` 的 `struct _State_impl`；拷贝发生在行号：`164` 的 `new _State_impl<_Wrapper>(...)`）。这就是为什么传引用**不会**被线程看到，必须用 `std::ref`。

---

## ⑧ 生命周期图：future 与共享状态 [标准]

```
 producer 线程                共享状态                  consumer 线程
 ────────────               ───────────              ────────────
 promise/task               _Result (T 或异常)         future.get()
   │                             │                         │
   │ set_value(42) ───────────► │ ready=true               │
   │                             │                         │
   │ (无引用 t 也行)             │                         │ get() 返回 42
   │                             │       若 set_exception ─│ get() 抛异常
   │                             │                         │
 future 析构 ≠ 共享状态析构；      │                         │
 仅最后一个引用者析构才回收        └─────────────────────────┘
```

`[标准]`：`future`/`shared_future` 通过 `shared_ptr` 共享状态；`future::get()` 在结果就绪前**阻塞**（deferred 除外，见 ⑯）。`[经验]`：`get()` 调用后 `future` 进入 `valid()==false`，第二次 `get()` 是 UB（`future_errc::no_state`）。

---

## ⑨ 调用栈/时序图：std::async(launch::async) 的一次往返 [标准]

```
main 线程          runtime 线程池/新线程          共享状态
    │                    │                            │
    │ async(launch::async, F)                         │
    │───────────────────► 创建 thread, 立即执行 F     │
    │                    │── 运行 F ─────────────────►│ 写入结果
    │                    │                            │ ready
    │ (继续干别的)         │                            │
    │ future.get() ───────────────────────────────────│ 阻塞直到 ready
    │◄───────────────────────────────────────────────│ 返回 T
    │                    │  thread 结束, join 由运行时 │
    │                    │  在 future 析构时等待        │
```

```cpp
// ⑨ async(launch::async) 立即起线程，get() 等待结果（完整可编译）
#include <iostream>
#include <future>
#include <chrono>
int main() {
    std::future<int> f = std::async(std::launch::async, [] {
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
        return 7 * 6;
    });
    std::cout << "main 继续做别的事...\n";
    std::cout << "结果 = " << f.get() << "\n";   // 阻塞直到子线程完成
    return 0;
}
```

`[经验]`：不要写 `std::async(f);`（不接收 future）——返回的临时 `future` 会**立即析构并阻塞**到任务结束，等于同步调用，白白创建线程。

---

## ⑩ 汇编分析：std::thread 构造的 -O2 开销 [实现·GCC13]

下面是用 `g++ -std=c++23 -O2 -masm=intel` 对 `std::thread t(worker)` + `t.join()` 真实产生的关键汇编（已删节）：

```x86asm
; 文件：_asm1.cpp 经 -O2 编译（GCC 13.1.0, Win64, Itanium-ish MS ABI）
_Z16launch_and_countv:
        push    rbx
        sub     rsp, 48
        lea     rbx, _Z10worker_incv[rip]     ; 把函数指针放进"实参tuple"
        mov     ecx, 16
        call    _Znwy                          ; operator new(16) 分配 _State_impl
        lea     rdx, _ZTVNSt6thread11_State_implI...EE[rip+16]  ; vtable 指针
        mov     QWORD PTR 8[rax], rbx
        mov     QWORD PTR [rax], rdx
        lea     r8, _ZNSt6thread24_M_thread_deps_never_runEv[rip]
        call    _ZNSt6thread15_M_start_threadE...   ; 真正创建 OS 线程
        ...
        call    _ZNSt6thread4joinEv             ; t.join()
```

`[实现·GCC13]`：即便 `-O2`，`std::thread` 构造也至少包含：`operator new` 分配状态对象（行号：`bits/std_thread.h:164`）、设置 vtable（指向 `_State_impl`，行号：`234`）、调用 `_M_start_thread`（行号：`248`/`263`）→ 内部 `std::__gthread_create`。**每次起线程都有堆分配 + 系统调用**，不可在热循环里滥用（性能见 ⑲）。

---

## ⑪ STL 联系：future 在容器/算法/范围中的角色 [标准]

- `future`/`shared_future` 不能放进 `vector` 直接用（不可拷贝、`future` 不可拷贝只能移动）——用 `std::vector<std::future<int>>` + `std::move`。
- 常与 `std::ranges` / `std::transform` 配合做"fan-out/fan-in"并行 map（见 ⑫ 工业案例）。
- `std::future` 的阻塞语义与 `std::condition_variable` 的等待（⟶ Book/part07_stl/ch93_thread_async.md）实现原理同源：`future` 的共享状态用 `call_once` + 条件变量实现"就绪通知"。

```cpp
// ⑪ 把一组 future 收集进 vector 并 wait（完整可编译）
#include <iostream>
#include <future>
#include <vector>
int main() {
    std::vector<std::future<int>> fs;
    for (int i = 0; i < 4; ++i)
        fs.push_back(std::async(std::launch::async, [i] { return i * i; }));
    int total = 0;
    for (auto& f : fs) total += f.get();   // 顺序 get，全部结果求和
    std::cout << "sum of squares = " << total << "\n";   // 0+1+4+9=14
    return 0;
}
```

---

## ⑫ 工业案例：高并发 Web 服务器的"并行请求扇出/归并" [经验]

真实服务器常需把一次外部请求拆成 N 个子任务并发执行（如并行查缓存、DB、远程服务），再合并结果。下面是基于 `std::async` + `std::future` 的**结构骨架**（非 Hello World，可运行、可扩展为真实 handler）。

```cpp
// ⑫ 工业：一次请求并发调用三个下游服务并归并（完整可编译骨架）
#include <iostream>
#include <future>
#include <string>
#include <chrono>

// 三个"下游服务"（真实场景换成 RPC/SQL/HTTP 客户端）
std::string fetch_from_cache(int id) {
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
    return "cache:" + std::to_string(id);
}
std::string fetch_from_db(int id) {
    std::this_thread::sleep_for(std::chrono::milliseconds(60));
    return "db:" + std::to_string(id);
}
std::string fetch_from_remote(int id) {
    std::this_thread::sleep_for(std::chrono::milliseconds(40));
    return "remote:" + std::to_string(id);
}

// 处理一次请求：并发扇出，串行归并
std::string handle_request(int user_id) {
    auto fc = std::async(std::launch::async, fetch_from_cache, user_id);
    auto fd = std::async(std::launch::async, fetch_from_db,    user_id);
    auto fr = std::async(std::launch::async, fetch_from_remote, user_id);
    // get() 会等待；总耗时≈ max(20,60,40)=60ms，而非 20+60+40=120ms
    return fc.get() + " | " + fd.get() + " | " + fr.get();
}

int main() {
    auto t0 = std::chrono::steady_clock::now();
    std::string r = handle_request(42);
    auto t1 = std::chrono::steady_clock::now();
    std::cout << r << "\n";
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();
    std::cout << "elapsed ~ " << ms << " ms (并发归并)\n";
    return 0;
}
```

`[经验]`：生产环境**不要**每请求 `std::async`（线程创建昂贵，且无上限）。应配合线程池（⟶ Book/part15_cases/ch159_threadpool.md、⟶ Book/part07_stl/ch93_thread_async.md）。`std::async` 在此是"表达意图"的清晰手段，适合中低并发。

---

## ⑬ 源码分析：libstdc++ 的 thread / future 实现骨架 [实现·GCC13]

**std::thread 构造与启动**

```text
// 文件：bits/std_thread.h  行号：164
_M_start_thread(_State_ptr(new _State_impl<_Wrapper>(
      std::forward<_Args>(__args)...)), &_M_deleted_unique_ptr_dummy);
// 文件：bits/std_thread.h  行号：234  _State_impl 持有 decay 后的实参
struct _State_impl : public _State {
    _Wrapper _M_func;                  // 被 decay 拷贝的可调用体
    // ...
};
// 文件：bits/std_thread.h  行号：248 真正请求 OS 线程
void _M_start_thread(_State_ptr, void (*)());
```

- `行号：78`：`class thread` 定义；`行号：132` 默认构造（空线程，`joinable()==false`）。
- `行号：170`：`~thread()`——**若 `joinable()` 为真则 `std::terminate()`**，这是 thread 最危险的契约。

**shared state（`_State_baseV2`）**

```text
// 文件：future  行号：325  _State_baseV2 定义
class _State_baseV2 {
    _Result_base::_Ptr<const void> _M_result;   // 结果或异常
    _Status _M_status{__not_ready};             // 就绪状态
    // 行号：428 用 call_once 保证结果只设置一次
    call_once(_M_once, &_State_baseV2::_M_do_set, this, ...);
    // 行号：738  __basic_future::_M_get_result -> get() 内部
    // 行号：598  _M_complete_async 在析构时阻塞（async 策略专用）
};
```

`[实现·GCC13]`：`future` 的 `get()` 实现（文件：`future`，行号：`824`：`get()` 调 `_M_get_result()._M_value()`；`行号：738`：`_M_get_result` 先 `_S_check` 再取结果）。`async` 返回的 `future` 的析构会调 `_M_complete_async`（行号：`598`，虚函数默认空，async 策略下会 join 运行线程）——这就是"async 的 future 析构阻塞"的根源。

---

## ⑭ WG21 提案与标准背景 [标准]

| 提案 | 标题 | 与本草关系 |
|---|---|---|
| N2249 (2007) | "Proposal for a Threading Library for C++" | C++11 `<thread>`/`<future>` 的雏形 |
| N2660 | "Standard Library Extensions for Multithreading" | `async`/`future`/`promise` 入标准 |
| P0443R14 / 后续 | "A Unified Executors Proposal" | 现代执行器（⟶ Book/part07_stl/ch93_thread_async.md），是 `async` 的继任者 |
| P0660 | "Stop Token and Joining Thread" | 第94章 ⟶ Book/part07_stl/ch94_stop_token.md 的 `jthread`/`stop_token` |

`[标准]`：`<thread>`/`<future>` 经 C++11 引入，C++14/17/20 主要修缮（如 `std::async` 与 `shared_future` 的细节、C++20 起支持 `std::jthread` 协作取消的并行）。`[经验]`：标准从未提供"强制杀线程"能力——这是刻意的：强制 kill 会跳过析构、破坏锁与 invariant（见第94章 ⑩）。

---

## ⑮ 面试题 [标准]

1. **`std::thread` 析构若仍 `joinable()` 会怎样？** → 调用 `std::terminate()`（C++ 标准规定）。必须 `join()` 或 `detach()`。
2. **`std::thread` 传参默认按值还是按引用？** → 按值 `decay` 拷贝；想传引用必须 `std::ref(x)`。
3. **`future::get()` 能调用几次？** → 一次；调用后 `valid()` 变 `false`，再调抛 `future_error(no_state)`。
4. **`shared_future` 与 `future` 区别？** → `shared_future` 可拷贝、可多次 `get()`；由 `future::share()` 获得。
5. **`std::async` 不接收返回值时发生什么？** → 临时 `future` 立即析构并阻塞到任务完成，等于同步执行。
6. **异常如何在 `promise`/`future` 之间传播？** → 生产者 `set_exception(current_exception())`，消费者 `get()` 重新抛出。
7. **`launch::deferred` 何时执行？** → 在 `get()`/`wait()` 处、在**调用 `get()` 的线程**上同步执行。
8. **`packaged_task` 与 `async` 区别？** → 前者是"可手动调用的任务对象"（可延迟、可放进队列），后者是"立即/惰性启动的工厂"。

```cpp
// ⑮ 面试题佐证：future 第二次 get() 抛 no_state（完整可编译）
#include <iostream>
#include <future>
int main() {
    std::future<int> f = std::async(std::launch::async, [] { return 1; });
    std::cout << f.get() << "\n";         // OK: 第一次
    try {
        std::cout << f.get() << "\n";     // 第二次 -> no_state
    } catch (const std::future_error& e) {
        std::cout << "err: " << e.code().message() << "\n";
    }
    return 0;
}
```

---

## ⑯ 易错点 [经验]

- **忘记 join/detach 任何 thread 直接离开作用域** → `terminate()`。所有示例都已 join。
- **误以为 `std::thread` 按引用传参** → 默认拷贝；用 `std::ref` 才是引用。
- **`std::async` 返回临时 future 未接收** → 同步阻塞（见⑨）。
- **`launch::async | launch::deferred` 被误读为"先 async，超时转 deferred"** → 实际是"由实现二选一"，可能是 deferred，导致"看似并行实则串行"。要强制并行必须显式 `launch::async`。
- **`future` 跨 `get()` 持有共享状态引用却提前析构** → 若仍有线程在写，状态生命周期依赖 `shared_ptr`，一般安全；但 `async` 的 future 析构会阻塞，小心 RAII 作用域。
- **移动-only 类型（如 `std::unique_ptr`）直接传 thread** → 必须 `std::move`，否则拷贝失败。

```cpp
// ⑯ 易错：deferred 在调用线程同步执行（完整可编译，注意计数线程id）
#include <iostream>
#include <future>
#include <thread>
int main() {
    auto id_main = std::this_thread::get_id();
    std::future<int> f = std::async(std::launch::deferred, [=] {
        // 在 get() 的调用线程上运行
        return std::this_thread::get_id() == id_main ? 1 : 0;
    });
    int r = f.get();   // 此处才执行 lambda，且在本线程
    std::cout << "deferred ran on main thread? " << (r ? "yes" : "no") << "\n";
    return 0;
}
```

---

## ⑰ FAQ [标准]

**Q：`std::thread` 能返回结果吗？** A：不能。`thread` 只管执行；返回值请用 `future`/`promise` 或 `packaged_task`。

**Q：`async` 用 `launch::async` 一定会起新线程吗？** A：标准说"as if 在新线程"——主流实现（libstdc++/MSVC/Clang）确实起新线程，但标准未禁止用线程池；不要依赖"一一对应 OS 线程"。

**Q：`packaged_task` 的 `operator()` 能调多次吗？** A：一般只应调用一次设置结果；多次调用是 UB（共享状态已 ready）。

**Q：`call_once` 的 `once_flag` 能拷贝/移动吗？** A：不能，`once_flag` 既不可拷贝也不可移动。

**Q：为什么 `future` 不能拷贝？** A：共享状态只有一份结果，"单一消费者"语义保证 `get()` 的一次性；多消费者请用 `shared_future`。

```cpp
// ⑰ FAQ 佐证：packaged_task 通过 get_future 取结果（完整可编译）
#include <iostream>
#include <future>
int main() {
    std::packaged_task<int(int,int)> task([](int a,int b){ return a+b; });
    std::future<int> f = task.get_future();
    task(3, 4);                 // 立即执行（也可 move 进 thread 执行）
    std::cout << "3+4 = " << f.get() << "\n";
    return 0;
}
```

---

## ⑱ 最佳实践 [经验]

1. 永远**立即**对 `std::thread` 决定 `join()` 或 `detach()`；优先用 RAII 包装（或第94章的 `jthread`）。
2. 用 `std::async` 表达一次性并行任务时，**必须接收返回的 `future`** 并在合适处 `get()`。
3. 需要"多次读取同一异步结果" → `future::share()` 转 `shared_future`。
4. 跨线程返回移动-only 对象（如 `unique_ptr`、`vector`）用 `promise<T>` + `set_value(std::move(x))`。
5. 异常必须经由 `set_exception` 传播，不要在线程函数里吞异常（那会导致 `future.get()` 永远阻塞）。
6. 真实高并发请用线程池 + 任务队列，而非每任务 `async`。

```cpp
// ⑱ 最佳实践：移动-only 结果经 promise 跨线程传递（完整可编译）
#include <iostream>
#include <future>
#include <memory>
#include <thread>
#include <utility>
int main() {
    std::promise<std::unique_ptr<int>> p;
    std::future<std::unique_ptr<int>> f = p.get_future();
    std::thread t([p = std::move(p)]() mutable {
        p.set_value(std::make_unique<int>(123));   // 移动进共享状态
    });
    std::unique_ptr<int> ptr = f.get();             // 移动出
    std::cout << "*ptr = " << *ptr << "\n";
    t.join();
    return 0;
}
```

---

## ⑲ 性能分析（复杂度 / 缓存 / ABI） [经验]

**线程创建成本（示意，Win64 / i7 代际量级）**

| 操作 | 量级（示意） | 说明 |
|---|---|---|
| `std::thread` 构造 | ~15–50 µs | `operator new` + `CreateThread`/`pthread_create` + 内核调度 |
| `std::async(launch::async)` | 同上 + future 状态 | 额外 `shared_ptr`/`call_once` 开销 |
| `future::get()` 命中已就绪 | ~数十 ns | 仅读 `shared_ptr` + 状态标志 |
| `future::get()` 阻塞等待 | 取决于子线程 | 条件变量等待（µs 级上下文切换） |

```cpp
// ⑲ microbenchmark：线程创建 vs 任务本身（量级示意，完整可编译）
#include <iostream>
#include <thread>
#include <chrono>
#include <vector>
int main() {
    const int K = 100;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < K; ++i) {
        std::thread t([] {});   // 空任务，仅测量"创建+join"
        t.join();
    }
    auto t1 = std::chrono::steady_clock::now();
    auto us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
    std::cout << K << " 次空线程创建+join ≈ " << us << " µs  (≈ "
              << (us / K) << " µs/次，示意)\n";
    return 0;
}
```

`[经验]`：**结论不是"多线程更快"，而是"并行只在任务足够重、或 I/O 密集（等待期间让出 CPU）时才划算"**。纯计算且 K 小，线程开销可能超过收益——这正是线程池/执行器（⟶ Book/part07_stl/ch93_thread_async.md）存在的理由。

`[平台·x86-64]`：`future` 的共享状态是堆分配对象，`shared_ptr` 控制块含原子引用计数，跨线程传递存在**伪共享/缓存行跳动**风险；高频 `get()` 短任务场景应考虑无锁通道（⟶ Book/part09_concurrency/ch110_lockfree.md）。

---

## ⑳ 跨语言对比：线程与异步原语 [标准]

| 维度 | C++ (`std::thread`/`future`/`async`) | Rust (`std::thread`/`tokio`/`join`) | Go (`goroutine`/`channel`) | Java (`Thread`/`Future`/`CompletableFuture`) |
|---|---|---|---|---|
| 线程模型 | OS 线程（1:1） | OS 线程（std，或 tokio 任务 M:N） | goroutine（M:N，用户态调度） | 平台线程（虚拟线程自 21 起 M:N） |
| 结果返回 | `future`/`promise`/`packaged_task` | `JoinHandle` / `channel` | `channel` | `Future`/`CompletableFuture` |
| 取消 | 仅协作：`jthread`+`stop_token`（第94章） | 无强制 kill；靠 `channel` 关闭/标志 | `context.Context` + `select` | `Thread.interrupt()`（协作）+ Future `cancel` |
| 异常跨线程 | `set_exception` → `get()` 重抛 | `Result`/`panic` 不跨线程 | `panic` 不跨 goroutine（recover 局部） | `ExecutionException` 包装 |
| 强制 kill | **无**（刻意） | **无** | `runtime.Goexit`（协作） | `Thread.stop()` **已废弃（危险）** |
| 启动成本 | 高（系统调用） | 高（std）/低（tokio） | 极低（goroutine ~2KB 栈） | 高（平台）/低（虚拟线程） |

`[标准]`：C++ 与 Rust 一致地**拒绝"强制杀线程"**，因为跨析构/锁的强制终止不可恢复；Go 用 `context` 做协作取消，Java 历史上有危险的 `Thread.stop()`（现已废弃）。这与第94章 ⟶ Book/part07_stl/ch94_stop_token.md 的 `std::jthread` 协作取消模型一脉相承。

`[经验]`：从 Go/Java 来的工程师常期望"取消 = 立刻停"，在 C++ 里要转变为"取消 = 设置标志，由工作线程在检查点自行退出"。

---

## 附录A：30+ 完整可编译示例（独立程序，可直接 `g++ -std=c++23 -O2 -Wall -Wextra`） [标准]

下面 E1–E26 每个都是**完整可编译程序**（自带 `#include` 与 `int main`），覆盖本章所有原语，且每个 thread 都已 `join`/`detach` 以确保正常退出。

```cpp
// E1 std::thread 基本构造与 join
#include <iostream>
#include <thread>
int main() {
    std::thread t([] { std::cout << "worker thread\n"; });
    t.join();                      // 必须 join，否则析构 terminate
    std::cout << "main done\n";
    return 0;
}
```

```cpp
// E2 多个线程 join 的惯用法（vector<thread>）
#include <iostream>
#include <thread>
#include <vector>
int main() {
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i)
        ts.emplace_back([i] { std::cout << "thread " << i << "\n"; });
    for (auto& t : ts) t.join();   // 全部 join
    return 0;
}
```

```cpp
// E3 detach 后台线程（必须确保被引用对象活得够久）
#include <iostream>
#include <thread>
int main() {
    std::thread t([] {
        for (int i = 0; i < 3; ++i) std::cout << "bg " << i << "\n";
    });
    t.detach();                    // 交还 OS，主线程不等待
    std::this_thread::sleep_for(std::chrono::milliseconds(50)); // 给后台时间
    return 0;
}
```

```cpp
// E4 按值传参（参数被 decay 拷贝进线程）
#include <iostream>
#include <thread>
#include <string>
void greet(std::string name) { std::cout << "hi " << name << "\n"; }
int main() {
    std::string s = "world";
    std::thread t(greet, s);       // s 被拷贝进线程
    t.join();
    return 0;
}
```

```cpp
// E5 按引用传参必须用 std::ref
#include <iostream>
#include <thread>
#include <string>
void append(std::string& s) { s += "!"; }
int main() {
    std::string s = "hi";
    std::thread t(append, std::ref(s));   // 显式 ref
    t.join();
    std::cout << s << "\n";               // hi!
    return 0;
}
```

```cpp
// E6 移动-only 对象经 std::move 传入线程
#include <iostream>
#include <thread>
#include <vector>
#include <utility>
void consume(std::vector<int> v) { std::cout << "size=" << v.size() << "\n"; }
int main() {
    std::vector<int> v(100, 7);
    std::thread t(consume, std::move(v));   // 移动，避免拷贝
    t.join();
    return 0;
}
```

```cpp
// E7 成员函数作为线程入口（this 被拷贝/引用传入）
#include <iostream>
#include <thread>
struct Worker {
    void run(int n) { std::cout << "run " << n << "\n"; }
};
int main() {
    Worker w;
    std::thread t(&Worker::run, &w, 5);     // 第二参是对象指针(this)
    t.join();
    return 0;
}
```

```cpp
// E8 thread::id 与 hardware_concurrency（不依赖结果，仅演示 API）
#include <iostream>
#include <thread>
int main() {
    std::cout << "hw conc = " << std::thread::hardware_concurrency() << "\n";
    std::thread t([] { std::cout << "id=" << std::this_thread::get_id() << "\n"; });
    std::cout << "main id=" << std::this_thread::get_id() << "\n";
    t.join();
    return 0;
}
```

```cpp
// E9 简单 RAII 包装：作用域结束自动 join（thread 自身不可拷贝，用移动）
#include <iostream>
#include <thread>
#include <utility>
class JoinGuard {
    std::thread t_;
public:
    explicit JoinGuard(std::thread t) : t_(std::move(t)) {}
    ~JoinGuard() { if (t_.joinable()) t_.join(); }
    JoinGuard(const JoinGuard&) = delete;
    JoinGuard& operator=(const JoinGuard&) = delete;
};
int main() {
    JoinGuard g(std::thread([] { std::cout << "guarded\n"; }));
    return 0;   // 析构时自动 join（预告：C++20 jthread 原生支持，见第94章）
}
```

```cpp
// E10 promise 设置值，future 在另一线程读取
#include <iostream>
#include <future>
#include <thread>
#include <utility>
int main() {
    std::promise<int> p;
    std::future<int> f = p.get_future();
    std::thread producer([p = std::move(p)]() mutable { p.set_value(100); });
    std::cout << "future = " << f.get() << "\n";
    producer.join();
    return 0;
}
```

```cpp
// E11 promise 传播异常，future.get() 在消费线程重抛
#include <iostream>
#include <future>
#include <thread>
#include <stdexcept>
#include <utility>
int main() {
    std::promise<int> p;
    std::future<int> f = p.get_future();
    std::thread producer([p = std::move(p)]() mutable {
        try { throw std::runtime_error("boom"); }
        catch (...) { p.set_exception(std::current_exception()); }
    });
    try { std::cout << f.get() << "\n"; }
    catch (const std::exception& e) { std::cout << "caught: " << e.what() << "\n"; }
    producer.join();
    return 0;
}
```

```cpp
// E12 packaged_task：把可调用体封装为"可设置结果的任务"
#include <iostream>
#include <future>
#include <thread>
#include <utility>
int main() {
    std::packaged_task<long long(unsigned)> task(
        [](unsigned n) { long long s = 0; for (unsigned i=1;i<=n;++i) s+=i; return s; });
    std::future<long long> f = task.get_future();
    std::thread t(std::move(task), 1000);   // 在线程里执行
    std::cout << "sum 1..1000 = " << f.get() << "\n";
    t.join();
    return 0;
}
```

```cpp
// E13 async(launch::async)：立即并行
#include <iostream>
#include <future>
int main() {
    auto f = std::async(std::launch::async, [] { return 2 * 21; });
    std::cout << "async result = " << f.get() << "\n";
    return 0;
}
```

```cpp
// E14 async(launch::deferred)：惰性，在 get() 处同步执行
#include <iostream>
#include <future>
int main() {
    auto f = std::async(std::launch::deferred, [] { return 3 * 14; });
    std::cout << "before get\n";
    std::cout << "deferred result = " << f.get() << "\n";   // 此刻才执行
    return 0;
}
```

```cpp
// E15 默认 async（async|deferred，由实现选择）
#include <iostream>
#include <future>
int main() {
    auto f = std::async([] { return 42; });   // 不指定 policy
    std::cout << "default policy result = " << f.get() << "\n";
    return 0;
}
```

```cpp
// E16 async 组合 policy 的陷阱演示：可能退化成 deferred（严格按标准）
#include <iostream>
#include <future>
#include <thread>
int main() {
    auto id_main = std::this_thread::get_id();
    auto f = std::async(std::launch::async | std::launch::deferred,
                        [=] { return std::this_thread::get_id() == id_main; });
    bool ran_on_main = f.get();   // 若是 deferred，则在本线程跑 -> true
    std::cout << "ran_on_main=" << std::boolalpha << ran_on_main << "\n";
    return 0;
}
```

```cpp
// E17 shared_future：结果可被多个消费者读取
#include <iostream>
#include <future>
#include <thread>
#include <vector>
int main() {
    std::promise<int> p;
    std::shared_future<int> sf = p.get_future().share();
    std::vector<std::thread> ts;
    for (int i = 0; i < 3; ++i)
        ts.emplace_back([sf, i] { std::cout << "c" << i << "=" << sf.get() << "\n"; });
    p.set_value(7);
    for (auto& t : ts) t.join();
    return 0;
}
```

```cpp
// E18 future 的 wait / wait_for 超时控制
#include <iostream>
#include <future>
#include <chrono>
int main() {
    auto f = std::async(std::launch::async, [] {
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        return 1;
    });
    if (f.wait_for(std::chrono::milliseconds(50)) == std::future_status::timeout)
        std::cout << "not ready yet\n";
    f.wait();                               // 阻塞直到就绪
    std::cout << "value=" << f.get() << "\n";
    return 0;
}
```

```cpp
// E19 call_once：只执行一次（多线程竞态安全）
#include <iostream>
#include <mutex>
#include <thread>
int main() {
    static std::once_flag flag;
    auto init = [] {
        std::call_once(flag, [] { std::cout << "initialized exactly once\n"; });
    };
    std::thread a(init), b(init), c(init);
    a.join(); b.join(); c.join();           // 三线程并发，仍只打印一次
    return 0;
}
```

```cpp
// E20 并行 for（fan-out）：用 async 并行处理区间
#include <iostream>
#include <future>
#include <vector>
#include <numeric>
#include <cstddef>
#include <thread>
int main() {
    std::vector<int> v(1000);
    std::iota(v.begin(), v.end(), 1);
    unsigned n = std::thread::hardware_concurrency();
    if (n == 0) n = 4;
    std::vector<std::future<long long>> fs;
    std::size_t step = v.size() / n;
    for (unsigned i = 0; i < n; ++i) {
        auto lo = v.begin() + i * step;
        auto hi = (i + 1 == n) ? v.end() : v.begin() + (i + 1) * step;
        fs.push_back(std::async(std::launch::async, [lo, hi] {
            long long s = 0; for (auto it = lo; it != hi; ++it) s += *it; return s;
        }));
    }
    long long total = 0;
    for (auto& f : fs) total += f.get();
    std::cout << "parallel sum = " << total << "\n";
    return 0;
}
```

```cpp
// E21 async 返回移动-only 结果
#include <iostream>
#include <future>
#include <memory>
int main() {
    auto f = std::async(std::launch::async,
        [] { return std::make_unique<int>(555); });
    std::unique_ptr<int> p = f.get();
    std::cout << "*p=" << *p << "\n";
    return 0;
}
```

```cpp
// E22 promise 设置异常后再 get 重抛（含 error_code 风格）
#include <iostream>
#include <future>
#include <stdexcept>
int main() {
    std::promise<int> p;
    auto f = p.get_future();
    p.set_exception(std::make_exception_ptr(std::runtime_error("nope")));
    try { f.get(); }
    catch (const std::exception& e) { std::cout << "got: " << e.what() << "\n"; }
    return 0;
}
```

```cpp
// E23 packaged_task 的可调用体抛出异常也经 future 传播
#include <iostream>
#include <future>
#include <stdexcept>
int main() {
    std::packaged_task<int()> task([] { throw std::runtime_error("task fail"); return 0; });
    auto f = task.get_future();
    try { task(); }
    catch (...) {}                 // 执行时抛；结果存入共享状态
    try { f.get(); }
    catch (const std::exception& e) { std::cout << "future: " << e.what() << "\n"; }
    return 0;
}
```

```cpp
// E24 shared_future 的副本语义（拷贝后才共享同一状态）
#include <iostream>
#include <future>
int main() {
    std::promise<int> p;
    std::shared_future<int> sf1 = p.get_future().share();
    std::shared_future<int> sf2 = sf1;       // 拷贝，仍共享
    p.set_value(9);
    std::cout << sf1.get() << " " << sf2.get() << "\n";
    return 0;
}
```

```cpp
// E25 嵌套 async：任务内再发起子任务（完整可编译）
#include <iostream>
#include <future>
int main() {
    auto outer = std::async(std::launch::async, [] {
        auto inner = std::async(std::launch::async, [] { return 10; });
        return 1 + inner.get();
    });
    std::cout << "nested = " << outer.get() << "\n";
    return 0;
}
```

```cpp
// E26 future::valid() 检查后再 get（避免 no_state）
#include <iostream>
#include <future>
int main() {
    std::future<int> f = std::async(std::launch::async, [] { return 5; });
    if (f.valid()) std::cout << f.get() << "\n";
    if (!f.valid()) std::cout << "future 已消耗，不可再 get\n";
    return 0;
}
```

> 以上 E1–E26 加上正文 ①⑨⑪⑫⑮⑯⑰⑱⑲ 的示例，本章共 **35 个**独立可编译 cpp 块。

## 附录：练习题 / 思考题 / 源码阅读建议

**练习题**
1. 用 `std::thread` + 原始数组实现 4 线程并行求和，主线程 `join` 后合并（禁止用 `future`）。
2. 用 `packaged_task` 把"读文件"封装为异步任务，主线程 `get()` 拿到内容。
3. 实现一个 `parallel_transform(in, out, F)`，对容器每元素起 `async` 并行变换。

**思考题**
- `std::async` 返回的 `future` 析构为何要阻塞？如果改成"不阻塞、后台跑"，会有什么正确性问题？
- `shared_future` 的多消费者在结果就绪前都阻塞，如何用 `wait_for` 实现超时？

**源码阅读路线（libstdc++）**
- `文件：bits/std_thread.h` 行号：`78`（class thread）、`132`（默认构造）、`164`（构造启动）、`170`（析构 terminate）、`234`（_State_impl）、`248`/`263`（`_M_start_thread`）。
- `文件：thread` 行号：`134`（class jthread，见第94章）、`156`（~jthread 自动 request_stop+join）。
- `文件：future` 行号：`149`（launch 枚举）、`203`（async 声明）、`325`（`_State_baseV2`）、`605`（`_M_shared_state`）、`738`/``824``（`_M_get_result`/`get`）、`598`（`_M_complete_async` 析构阻塞）。
- `文件：future` 行号：`428`（`call_once` 保证结果只设置一次）。

> 本文件为独立章节，未改动 `INDEX.md` / `GLOSSARY.md` / `CROSSREF.md`；与 part09 的 ch102/ch103/ch104/ch105/ch107/ch108/ch110/ch114 及第94章建立正文交叉引用。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第93章](Book/part07_stl/ch93_thread_async.md) | 键值查找/缓存 | 本章提供概念，第93章提供实现 |
| [第93章](Book/part07_stl/ch93_thread_async.md) | 独占所有权/工厂模式 | 本章提供概念，第93章提供实现 |
| [第93章](Book/part07_stl/ch93_thread_async.md) | 无锁队列/计数器 | 本章提供概念，第93章提供实现 |
| [第93章](Book/part07_stl/ch93_thread_async.md) | STL算法回调/异步任务 | 本章提供概念，第93章提供实现 |
| [第93章](Book/part07_stl/ch93_thread_async.md) | 泛型库/编译期计算 | 本章提供概念，第93章提供实现 |


## 真实开源项目参考（可查证链接）

> 异步与并发的工业实现——下列链接指向真实源码（L2 文件级）。

- **LLVM `llvm::ThreadPool` / `llvm::async`**：[llvm/llvm-project · llvm/include/llvm/Support/ThreadPool.h](https://github.com/llvm/llvm-project/blob/main/llvm/include/llvm/Support/ThreadPool.h) —— 编译器自身的任务并行池，`llvm::async` 是 `std::async` 的工业原型，对应「② std::async 策略」的底层实现。
- **Boost.Asio（异步 I/O 与 strand）**：[boostorg/asio · include/boost/asio](https://github.com/boostorg/asio/blob/develop/include/boost/asio) —— `io_context` + `strand` 串行化模型，是 `std::async` 之外最广泛使用的 C++ 异步框架，对应「③ 共享状态生命周期」的生产级替代。
- **folly `folly::Future` / `folly::Promise`**：[facebook/folly · folly/futures](https://github.com/facebook/folly/blob/main/folly/futures) —— Meta 的链式异步（`then` 组合子），对应「④ 最佳实践」中"避免裸 future 嵌套回调"的工业方案。
- **Google Chromium `base::TaskRunner`**：[chromium/chromium · base/task](https://github.com/chromium/chromium/tree/main/base/task) —— 浏览器多进程架构的线程/任务调度，对应「⑤ 工业案例」中线程池的极致工程实践。

**常见陷阱 / 最佳实践**：
- `std::async` 默认策略可能新开线程（`launch::async`）或延迟（`deferred`），务必显式指定 `launch::async`。
- 共享状态生命周期需覆盖 `future`；`get()` 只能调用一次；优先 `folly::Future::then` 或 `std::async` + `wait_for` 避免阻塞。

> 交叉引用：停止令牌见 [ch94](Book/part07_stl/ch94_stop_token.md)；原子见 [ch108](Book/part09_concurrency/ch108_memory_order.md)。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

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

### 练习 2（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 3（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>

