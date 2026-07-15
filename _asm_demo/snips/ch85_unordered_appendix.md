## 附录：std::unordered_map 节点布局真机汇编实证（ASM-85-unordered · GCC 15.3.0 / C++26 / -O2）

> 证据：`_asm_demo/ch85_unordered_test.cpp` + `ch85_unordered_test.s`（真实编译 + `objdump -d -M intel -C`）。
> 工具链：`g++.exe (MinGW-W64 x86_64-msvcrt-posix-seh) 15.3.0`；`objdump.exe 2.46.1`。

**结论 1 — 节点堆分配 + 桶数组堆分配（元素增多触发 rehash）**
`build()` 每次 `m[k]=v` 调用插入内部例程（含 `operator new` 分配节点）；哈希表构造时另分配**桶数组**（默认 `max_load_factor = 1.0`，即 asm 中写入的 `0x3f800000`）：

```asm
; build() : 每元素一次节点堆分配
call   <insert 内部例程>          ; 内含 operator new
mov    DWORD PTR [rax], 0xa       ; 写入 value = 10
...
; 哈希表头：max_load_factor 默认 1.0f = 0x3f800000
mov    DWORD PTR [rcx+0x20], 0x3f800000
```

**结论 2 — find = 一次除法取桶 + 桶内单链表 next 指针追逐**

```asm
; find_it : hash 定位桶（int 键 = 自身，桶序 = k % bucket_count）
mov    r11, QWORD PTR [rcx+0x8]   ; bucket_count
movsxd rax, edx                   ; k
xor    edx, edx
div    r11                         ; edx = k % bucket_count  ← 整数除法！
mov    rax, QWORD PTR [rcx]        ; 桶数组基址
mov    rcx, QWORD PTR [rax+rdx*8]  ; 取 bucket[hash] 头节点
; 桶内沿 _M_next 单链表遍历，比较键
mov    rax, QWORD PTR [rcx]        ; node->_M_next
mov    r10d, DWORD PTR [rax+0x8]   ; node->key
cmp    r10d, r8d
je     found
mov    r9, QWORD PTR [rax]         ; node = node->_M_next
test   r9, r9
jne    <loop>
```

→ "O(1)" 并非免费：每次 `find` 先付出一条**整数除法** `div`（算桶索引），再沿桶内 `next` 单链表指针追逐。节点布局：`+0x00=_M_next`、`+0x08=键`。最坏情况（大量哈希冲突）桶退化为链表，查找退化为 O(n)。

**结论 3 — 与 std::map 的工程取舍**

| 维度 | std::map（红黑树） | std::unordered_map（哈希） |
|------|-------------------|----------------------------|
| 访问复杂度 | O(log n) 比较 + 指针追逐 | 平均 O(1)：1 次 `div` + 链表追逐 |
| 有序 | 是 | 否 |
| 隐藏成本 | 每次插入堆分配节点 | 桶数组堆分配 + **rehash**（增长时整体重散列，O(n)） |
| 小数据量 | 仅靠比较，常比哈希快（无 `div`、无 rehash） | `div` + 桶数组 cache 不友好，未必更快 |

→ 实测启示：元素少或需要有序遍历时用 `std::map`；查找为主且数据量大、哈希质量好时用 `std::unordered_map`。两者都**非连续内存、都付堆分配代价**，不能当作"廉价"容器——嵌入式/热路径优先考虑 `std::vector` + 排序后二分，或 `std::array`/`std::span` 等连续结构。
