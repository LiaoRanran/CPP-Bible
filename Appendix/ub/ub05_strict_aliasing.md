# UB-05 strict-aliasing violation（严格别名规则破坏）

**分类**：类型系统 UB ｜ **检测工具**：`-Wstrict-aliasing`（编译期）/ **UBSan 不覆盖此类 UB**
**源码**：[ub_strict_aliasing.cpp](./ub_strict_aliasing.cpp)

---

## ① 真实代码

```cpp
#include <cstdio>

// pi 与 pf 在源码层指向同一对象，但 int* 与 float* 不是「相容类型」
void f(int* pi, float* pf) {
    *pi = 0;          // 经 int* 写
    *pf = 1.0f;       // ❌ UB：经 float* 写同一内存（编译器可假定不别名）
    *pi = *pi + 1;    // -O2 可能直接使用寄存器中的旧值 0，忽略上方 float 写
}

int main() {
    int x = 0;
    f(&x, reinterpret_cast<float*>(&x));
    std::printf("x = %d\n", x);   // -O0 与 -O2 可能输出不同
    return 0;
}
```

## ② 编译器行为（本机实测，GCC 15.3.0）

**`-Wall -Wstrict-aliasing=2` 真实警告**：

```
ub_strict_aliasing.cpp: In function 'int main()':
ub_strict_aliasing.cpp:19:36: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
   19 |     f(&x, reinterpret_cast<float*>(&x));
```

> 注意：**UBSan 不检测严格别名 UB**——没有运行时检查器能覆盖别名假设。证据只能来自
> 编译期警告 + 优化器输出分歧。

## ③ 运行时表现（本机实测，关键证据：优化分歧）

| 编译 Flag | 运行输出 | 说明 |
|-----------|---------|------|
| `-O0` | `x = 1065353217` | 无优化：经 float* 的写确实落到 `x` 内存，int 读看到更新后的位模式（≈1.0f 的 IEEE754 表示）|
| `-O2 -fstrict-aliasing` | `x = 1` | 优化器假定 `pi` 与 `pf` 不别名，`*pi = *pi + 1` 直接用寄存器旧值 `0+1=1`，**忽略 float 写** |

**同一份源码、同一编译器、仅优化级别不同 → 输出不同**。这是严格别名 miscompile 的
铁证：UB 让程序的正确性依赖于「编译器恰好怎么优化了你」。

## ④ 为什么是 UB（根因）

C++ 严格别名规则（`[basic.lval]`）：通过 `T*` 访问对象，仅当 `T` 与对象动态类型
**相容**（或 `char*`/`unsigned char*`/`std::byte*` 等少数例外）时定义良好。
`int` 与 `float` 不相容，故经 `float*` 写 `int` 对象属 UB。优化器据此假设两类指针
永不指向同一内存，进而做激进的加载/存储合并与重排。

## ⑤ 修复

```cpp
#include <cstdio>
#include <bit>          // C++20 std::bit_cast：定义良好、零开销的位重解释

int main() {
    int x = 0;
    // 需要「读取 x 的位模式当作 float」时，用 bit_cast，绝不 reinterpret_cast 跨类型
    float f = std::bit_cast<float>(x);
    f = 1.0f;
    x = std::bit_cast<int>(f);
    std::printf("x = %d\n", x);   // 定义良好，任意优化级别结果一致
    return 0;
}
```

规则：
1. **跨类型位重解释用 `std::bit_cast`**（C++20）或 `std::memcpy`——两者定义良好且
   优化器知其语义，不会触发别名误判。
2. **绝不用 `reinterpret_cast<T*>(p)` 去访问 `p` 指向对象的非相容类型**。
3. 必须类型双关且共享同一地址时（如序列化缓冲区），统一经 `unsigned char*` /
   `std::byte*` 访问——这是标准明确允许的别名例外。
