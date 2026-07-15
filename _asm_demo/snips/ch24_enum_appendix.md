## 附录：enum class 真机汇编实证（ASM-24-enum · GCC 15.3.0 / C++26 / -O2）

> 证据：`_asm_demo/ch24_enum_test.cpp` + `ch24_enum_test.s`（真实编译 + `objdump -d -M intel -C`）。
> 工具链：`g++.exe (MinGW-W64 x86_64-msvcrt-posix-seh) 15.3.0`；`objdump.exe 2.46.1`。

**结论 1 — `enum class` 的强类型是纯编译期约束，运行期与裸 int 逐字节同码**

```asm
; use_enum(Color) : switch 被优化为 c+1 加越界守卫，等价于 int 运算
movzx  eax, cl           ; 零扩展 uint8_t 枚举值
add    eax, 0x1
cmp    cl, 0x3
cmovae eax, edx          ; c >= 3（非法）→ 返回 0
ret
; enum_underlying : 显式 static_cast<uint8_t> 也是单条 mov
mov    eax, ecx
ret
```

→ 指定底层类型 `: uint8_t` 后，枚举值只占 1 字节；`static_cast` 取出底层值零成本。**类型安全不产生任何运行时代价**——`enum class` 比无作用域 `enum` 多出来的全部是编译期检查。

**结论 2 — 无作用域 `enum` 的隐式 int 转换是零成本——这正是它危险的根源**

```asm
; use_plain(Plain) : 隐式转换为 int + 1，单条 lea，免费
lea    eax, [rcx+0x1]
ret
```

→ 无作用域 `enum` 可静默与任意 `int` 混用（`if (p == 1)`、`int x = p`、`p + 3` 都合法），且这个转换**免费**——既没有编译告警也没有运行期保护，错误只在逻辑层爆发。用 `enum class` 把这类混用挡在编译期，是零成本的防御性写法。

| 写法 | 运行期代码 | 隐式转 int | 代价 |
|------|-----------|:----------:|:----:|
| `enum class Color : uint8_t` | `movzx`/`mov`/`add`+越界 `cmovae` | 禁止（需 `static_cast`） | 零 |
| 无作用域 `enum Plain` | `lea [rcx+1]` | 允许（免费） | 零，但无保护 |
| `switch(c)` on enum class | `add` + 越界 `cmovae` | — | 零 |
