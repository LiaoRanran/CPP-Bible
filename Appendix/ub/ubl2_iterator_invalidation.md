# UB-L2 iterator invalidation（迭代器失效）

**分类**：容器/生命周期 UB ｜ **检测工具**：ASan / 崩溃
**源码**：[ub_iterator_invalidation.cpp](./ub_iterator_invalidation.cpp)

---

## ① 真实代码

```cpp
#include <cstdio>
#include <vector>

int main() {
    std::vector<int> v{1, 2, 3};
    for (auto it = v.begin(); it != v.end(); ++it) {
        v.push_back(*it);          // ❌ 遍历中 push_back 可能 realloc，使 it/end 悬垂
    }
    std::printf("final size = %zu\n", v.size());
}
```

## ② 编译器行为（本机实测）

**无警告**。迭代器失效是运行时语义，静态不报。

## ③ 运行时表现（本机实测）

```
size now 4 ... size now 956 ...   (持续打印后)
Segmentation fault (exit 139 = SIGSEGV)
```

> `push_back` 触发扩容，vector 把元素搬到新缓冲；旧 `it`/`end` 仍指向**已释放的旧缓冲**，
> 解引用即崩。前若干次"看似正常"是因为小容量尚未触发 realloc——再次印证 UB 的非确定性。

## ④ ASan 报告格式（DOC-REPORT，非本机捕获）

```
==12345==ERROR: AddressSanitizer: heap-use-after-free on address 0x...
    #0 0x... in operator++ / __gnu_cxx  (失效迭代器自增)
```

## ⑤ 根因（哪些操作使哪些迭代器失效）

| 容器/操作 | 失效的迭代器 |
|----------|------------|
| `vector::push_back`/`insert`/`erase`（触发扩容）| **全部**迭代器、引用、指针 |
| `vector::reserve` 后扩容 | 全部 |
| `deque::insert`/`erase` | 所有（除某些实现首尾）|
| `list`/`forward_list`/`set`/`map` 的 `insert` | 不失效（`erase` 仅失效被删者）|
| `unordered_*` 的 `rehash` | 全部 |

## ⑥ 修复

```cpp
// 正确：先算总数，再一次性 push（不边遍历边改）
std::vector<int> v{1,2,3};
size_t n = v.size();
for (size_t i = 0; i < n; ++i) v.push_back(v[i]);   // ✅ 拷贝基于原大小，迭代器不悬垂

// 或删除用 erase 返回值接管：
// for (auto it = v.begin(); it != v.end(); ) it = v.erase(it);
```
