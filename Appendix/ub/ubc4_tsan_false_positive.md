# UB-C4 TSan 误报（benign race）识别与抑制

**分类**：并发 / 工具链误报 ｜ **检测工具**：TSan + suppression / `no_sanitize`
**源码**：[ub_tsan_false_positive.cpp](./ub_tsan_false_positive.cpp)

---

## ① 背景

并非 TSan 报出的每处 race 都需改代码。**良性竞争（benign race）** 指：并发访问在
逻辑上不影响程序正确性（如一次性初始化标志、调试计数、只读快照）。盲目"修复"
可能引入不必要的锁开销或改变语义。正确做法是**识别 → 确认良性 → 抑制报告**。

## ② 代码示例（单写者初始化标志）

```cpp
#include <atomic>
#include <cstdio>
#include <thread>

std::atomic<bool> initialized{false};
int config = 0;

void init_once() {
    if (!initialized.load(std::memory_order_relaxed)) {
        config = 42;                                       // 写受 initialized 保护（单写者）
        initialized.store(true, std::memory_order_relaxed);
    }
}
int main() {
    std::thread t1(init_once), t2(init_once);
    t1.join(); t2.join();
    std::printf("config = %d\n", config);
}
```

本例实际是安全的（单写者写 `config`，`initialized` 用 relaxed atomic 同步），
但 TSan 若看到 `config` 的非原子写与读，可能标 race。

## ③ 抑制手段一：注解（局部）

```cpp
[[gnu::no_sanitize("thread")]]   // GCC/Clang：此函数不插桩 TSan
void init_once() { /* ... */ }
```

## ④ 抑制手段二：suppression 文件（全局，适合第三方库）

```text
# tsan.supp
race:init_once
```
运行：`TSAN_OPTIONS="suppressions=tsan.supp" ./prog`

## ⑤ 何时该"真修"而非抑制

| 症状 | 判断 |
|------|------|
| 单写者 + atomic 标志保护 | 良性 → 抑制 / 注解 |
| 调试计数器，丢失几次无所谓 | 良性 → 抑制 |
| 多写者并发写同一非原子 | **真 race → 必须修**（加锁/原子）|
| 读可能看到半写状态影响控制流 | **真 race → 必须修**|

> 经验法则：抑制前必须**论证**"无论竞争结果如何程序都正确"。无法论证则必须修。

## ⑥ 本机说明

本机 MinGW 无 `libtsan`，上述 `[[gnu::no_sanitize]]` 注解与 suppression 机制在
具备 TSan 的工具链（Linux GCC/Clang）上生效。代码本身在本机可编译（注解被忽略）。
