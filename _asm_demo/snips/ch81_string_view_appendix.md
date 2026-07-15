## 附录：std::string_view 真机汇编实证（ASM-81-string_view · GCC 15.3.0 / C++26 / -O2）

> 证据：`_asm_demo/ch81_string_view_test.cpp` + `ch81_string_view_test.s`（真实编译 + `objdump -d -M intel -C`）。
> 工具链：`g++.exe (MinGW-W64 x86_64-msvcrt-posix-seh) 15.3.0`；`objdump.exe 2.46.1`。

**结论 1 — `string_view` = `{size_t _M_len, const char* _M_str}`，固定 16 字节**
`static_assert(sizeof(std::string_view)==16)`。libstdc++ 布局为 **len@offset0、ptr@offset8**（与直觉相反——长度在前）：

```asm
; sv_size : 直接取 len 字段（offset 0）
mov    rax, QWORD PTR [rcx]
ret
; sv_at : 取 ptr 字段（offset 8）后单字节加载，无边界检查
add    rdx, QWORD PTR [rcx+0x8]
movzx  eax, BYTE PTR [rdx]
ret
```

**结论 2 — `substr` 是 O(1) 指针/长度算术，零分配零拷贝**

```asm
; sv_substr : 仅改 ptr/len，全程无 call、无 memcpy
mov    rdx, QWORD PTR [rdx]        ; _M_str
mov    rcx, QWORD PTR [rcx+0x8]    ; _M_len
cmp    rdx, r8                     ; pos vs len
jb     ...
sub    rdx, r8                     ; len - pos
cmp    rdx, r9
cmova  rdx, r9                     ; new_len = min(cnt, len-pos)
add    rcx, r8                     ; new_ptr = ptr + pos
mov    QWORD PTR [rax+0x8], rcx
mov    QWORD PTR [rax], rdx
ret
```

**结论 3 — 对比 `std::string::substr` 是 O(n)：真实拷贝（超 SSO 还需堆分配）**

```asm
; str_substr : 含长度溢出守卫 + 字符拷贝 + 析构路径，体量约为 sv_substr 的 7 倍
...
cmp    rbx, 0xf          ; SSO 阈值(15) 判断
...
call   <...>             ; _M_create / _M_copy（分配或拷贝）
...
```

→ 在只想"看一段子串"的解析/切片场景，用 `string_view::substr` 可避免每次 O(n) 拷贝；仅在确实需要独立拥有的字符串时才用 `std::string::substr`。

| 操作 | 代码生成 | 复杂度 | 分配 |
|------|----------|:------:|:----:|
| `sv.substr(p,c)` | 指针+长度算术 | O(1) | 无 |
| `s.substr(p,c)` | 长度守卫 + `_M_copy`/`_M_create` | O(n) | 超 SSO 时堆分配 |
| `sv[i]` | `movzx eax,[ptr+i]`，无检查 | O(1) | 无 |
| `sv.size()` | `mov rax,[sv+0]`（取 len 字段） | O(1) | 无 |
