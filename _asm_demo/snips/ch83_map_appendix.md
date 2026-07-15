## 附录：std::map 节点布局真机汇编实证（ASM-83-map · GCC 15.3.0 / C++26 / -O2）

> 证据：`_asm_demo/ch83_map_test.cpp` + `ch83_map_test.s`（真实编译 + `objdump -d -M intel -C`）。
> 工具链：`g++.exe (MinGW-W64 x86_64-msvcrt-posix-seh) 15.3.0`；`objdump.exe 2.46.1`。

**结论 1 — 每个元素独立堆分配（红黑树节点）**
`build()` 对 `m[1]=10; m[2]=20; m[3]=30;` 三次调用 `_M_emplace_hint_unique`，每次内部 `_M_get_node` → `operator new` 分配一个树节点：

```asm
; build() : 每个 m[k]=v 都是一次堆分配（call 进 _Rb_tree 的 emplace 内部）
call   <_Rb_tree<int,...>::_M_emplace_hint_unique...>   ; 内含 operator new
mov    DWORD PTR [rax+0x24], 0xa    ; 写入 value = 10
...
```

**结论 2 — 节点不连续，find 是 O(log n) 指针追逐**

节点布局（libstdc++ Rb 树）：`+0x10=左子指针`、`+0x18=右子指针`、`+0x20=键(int)`、`+0x24=值(int)`（另含父指针/颜色）。`find` 沿左右子指针比较键：

```asm
; find_it : 从根开始沿 left/right 指针追逐
mov    rax, QWORD PTR [rcx+0x10]    ; root
mov    r8,  QWORD PTR [rax+0x10]    ; node->_M_left
mov    r9,  QWORD PTR [rax+0x18]    ; node->_M_right
cmp    DWORD PTR [rax+0x20], edx    ; 比较 node->key 与 k
jl     ...                          ; key < k → 走左
mov    rax, r8                      ; 否则走右（或命中）
test   rax, rax
jne    <loop>
```

→ 元素彼此**独立堆分配、内存不连续**；查找每深入一层都是一次指针解引用（可能 cache miss），O(log n) 次比较。对比 `std::vector`/`std::array` 的连续内存、O(1) 下标、零分配，map 在随机访问与遍历上 cache 局部性差得多。

| 维度 | std::map | std::vector / std::array |
|------|----------|--------------------------|
| 内存 | 每元素独立堆分配，不连续 | 单块连续 |
| 访问 | O(log n) 指针追逐 | O(1) 下标（单条 mov） |
| 有序 | 是（中序有序） | 插入序 |
| 代价 | 分配 + 指针 chase + 比较 | 仅内存搬运 |
