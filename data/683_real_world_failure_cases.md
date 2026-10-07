# 683-A3 · 失败案例深度归因（≥30 条 miss 深读）

筛选：`or_verdict == miss` 全量 45 条，按'类型覆盖优先 + 信息量'排序取前 40 条深读；归因分类 a–f 为**AI 启发式归类**（规则见 tools/analyze_683_realworld.py），逐条可复核。

分类定义：a 检测器能力盲区（逻辑/并发/挂起语义）；b 样本复杂度（多文件/环境依赖）；c 检测器配置缺口（UB 子类未启用）；d 真实 bug 与自造样本的本质差异；e 检测器误报（报了无关错误——本批 catch 口径下不产生 e 类，如实说明）；f 不可复现（环境/版本依赖，超时观测）。

### F1. RW-090 · CVE-2016-8655 · Linux kernel （`data_race`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2016-8655｜年份 2016｜严重度 HIGH
- **机制**：AF_PACKET 的 setsockopt(PACKET_RX_RING) 与 packet_set_ring 之间的
- **poc**：`data/real_world/RW-090.cpp`（sha256 bd7c01e626451c52…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**d_真实与自造的差异** —— 真实缺陷的跨模块/长生命周期形态与合成样本不同，检测链观测口径存在差异（需逐条复核）
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) rx ring reconfigure race exercised; -O2(rc=0) rx ring reconfigure race exercised]
- **改进建议**：tsan 主力 + 压力重现（本项目 setarch -R 关 ASLR 稳定化）。

### F2. RW-035 · CVE-2018-13785 · libpng （`integer_overflow`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2018-13785｜年份 2018｜严重度 MEDIUM
- **机制**：pngrutil.c 中 PNG 高度/行尺寸计算整数溢出（height * rowbytes），
- **poc**：`data/real_world/RW-035.cpp`（sha256 81aec6c3fc129237…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**c_配置缺口_未启用检查** —— UB 子类未启用（如 float-cast-overflow / alignment 报告面不足）
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) allocated 0 bytes for 65536x65536 image; -O2(rc=0) allocated 0 bytes for 65536x65536 image]
- **改进建议**：ubsan 有符号溢出覆盖；无符号回绕需补 -fsanitize=unsigned-integer-overflow（clang）。

### F3. RW-069 · CVE-2012-2677 · Boost （`integer_overflow`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2012-2677｜年份 2012｜严重度 MEDIUM
- **机制**：Boost.pool ordered_malloc 的块数×块大小乘积整数溢出，
- **poc**：`data/real_world/RW-069.cpp`（sha256 e916b842d898e087…）
- **8 资产判定**：asan=unknown；ubsan=unknown；tsan=unknown；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**c_配置缺口_未启用检查** —— UB 子类未启用（如 float-cast-overflow / alignment 报告面不足）
- **检测器输出摘录**（asan）：检测器不可用(asan)：-O0 编译失败: /mnt/c/Users/ASUS/AppData/Local/Temp/tmpca1wa6um/RW-069.cpp: In function ‘int ma; -O2 编译失败: /mnt/c/Users/ASUS/AppData/Local/Temp/tmpca1wa6um
- **改进建议**：ubsan 有符号溢出覆盖；无符号回绕需补 -fsanitize=unsigned-integer-overflow（clang）。

### F4. RW-078 · CVE-2021-33909 · Linux kernel （`integer_overflow`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2021-33909｜年份 2021｜严重度 HIGH
- **机制**：Sequoia —— seq_file 路径名拼接中 size_t 下溢（~2GB 深目录路径），
- **poc**：`data/real_world/RW-078.cpp`（sha256 5e9a6479dddcc394…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**c_配置缺口_未启用检查** —— UB 子类未启用（如 float-cast-overflow / alignment 报告面不足）
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) remaining-underflow value: 2147487096; -O2(rc=0) remaining-underflow value: 2147487096]
- **改进建议**：ubsan 有符号溢出覆盖；无符号回绕需补 -fsanitize=unsigned-integer-overflow（clang）。

### F5. RW-002 · CVE-2022-0778 · OpenSSL （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2022-0778｜年份 2022｜严重度 HIGH
- **机制**：BN_mod_sqrt() 对非素数模的 Tonelli-Shanks 循环缺少出口，解析
- **poc**：`data/real_world/RW-002.cpp`（sha256 9403079ddf0b67a1…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=-1) wsl_error:Command '['wsl', '-e', 'bash', '-lc', 'setarch -R /tmp/rv_bin_O0']' timed out after 120 seconds; -O2(rc=-1) wsl_error:Command '['wsl', '-e', 'bash', '-lc', 'setarch -R /tmp/rv_bin_O2']' t
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F6. RW-009 · CVE-2015-1793 · OpenSSL （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2015-1793｜年份 2015｜严重度 MEDIUM
- **机制**：证书链验证中"替代链"处理缺陷——中间 CA 用合法链进入信任判断后，
- **poc**：`data/real_world/RW-009.cpp`（sha256 9a3f80c346ab6953…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) crafted chain accepted = no; -O2(rc=0) crafted chain accepted = no]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F7. RW-010 · CVE-2016-2107 · OpenSSL （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2016-2107｜年份 2016｜严重度 MEDIUM
- **机制**：AES-NI CBC 路径下填充校验与 MAC 校验的顺序/短路使 padding oracle 成立
- **poc**：`data/real_world/RW-010.cpp`（sha256 cad99571ac916db7…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) oracle result = 0; -O2(rc=0) oracle result = 0]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F8. RW-012 · CVE-2023-4911 · glibc （`out_of_bounds`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2023-4911｜年份 2023｜严重度 HIGH
- **机制**：Looney Tunables —— ld.so 解析 GLIBC_TUNABLES 时对 "tunable=value"
- **poc**：`data/real_world/RW-012.cpp`（sha256 3abb81118e8cfc55…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**d_真实与自造的差异** —— 真实缺陷的跨模块/长生命周期形态与合成样本不同，检测链观测口径存在差异（需逐条复核）
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) tunables parsed: glibc.malloc.mxfast=aaaa...; -O2(rc=0) tunables parsed: glibc.malloc.mxfast=aaaa...]
- **改进建议**：asan + 有界容器；对栈越界补 -fstack-protector/CFI 类告警面。

### F9. RW-023 · CVE-2021-23017 · nginx （`out_of_bounds`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2021-23017｜年份 2021｜严重度 HIGH
- **机制**：resolver 解析 CNAME 时，DNS 应答中的压缩指针指向自身/越界，
- **poc**：`data/real_world/RW-023.cpp`（sha256 ea82acedfde24ef9…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**d_真实与自造的差异** —— 真实缺陷的跨模块/长生命周期形态与合成样本不同，检测链观测口径存在差异（需逐条复核）
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) name len=64; -O2(rc=0) name len=64]
- **改进建议**：asan + 有界容器；对栈越界补 -fstack-protector/CFI 类告警面。

### F10. RW-076 · CVE-2022-0185 · Linux kernel （`out_of_bounds`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2022-0185｜年份 2022｜严重度 HIGH
- **机制**：legacy_parse_param（fs_context 字符串选项）长度计算不当 —— 超长
- **poc**：`data/real_world/RW-076.cpp`（sha256 839006ed0ba3320c…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**d_真实与自造的差异** —— 真实缺陷的跨模块/长生命周期形态与合成样本不同，检测链观测口径存在差异（需逐条复核）
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) option length = 8191 parsed oversized fs_context option; -O2(rc=0) option length = 8191 parsed oversized fs_context option]
- **改进建议**：asan + 有界容器；对栈越界补 -fstack-protector/CFI 类告警面。

### F11. RW-005 · CVE-2023-0286 · OpenSSL （`type_punning`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2023-0286｜年份 2023｜严重度 HIGH
- **机制**：X.400 地址（ADDRESS 类型）在比较/渲染时被按 GENERAL_NAME 联合体
- **poc**：`data/real_world/RW-005.cpp`（sha256 1346443b6504baac…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**c_配置缺口_未启用检查** —— UB 子类未启用（如 float-cast-overflow / alignment 报告面不足）
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) other:  (len=1073741824); -O2(rc=0) other:  (len=1073741824)]
- **改进建议**：-fsanitize=undefined 的 alignment 子检查 + 强类型重构；联合体误用建议 clang -Wstrict-aliasing。

### F12. RW-053 · CVE-2021-30551 · Chromium/V8 （`type_punning`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2021-30551｜年份 2021｜严重度 HIGH
- **机制**：V8 TurboFan 对 Map 迁移类型假设错误，优化后代码把一种 JS 对象
- **poc**：`data/real_world/RW-053.cpp`（sha256 8b8cec9497020a38…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**c_配置缺口_未启用检查** —— UB 子类未启用（如 float-cast-overflow / alignment 报告面不足）
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) confused value = 2261634.509804; -O2(rc=0) confused value = 2261634.509804]
- **改进建议**：-fsanitize=undefined 的 alignment 子检查 + 强类型重构；联合体误用建议 clang -Wstrict-aliasing。

### F13. RW-054 · CVE-2020-16040 · Chromium/V8 （`type_punning`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2020-16040｜年份 2021｜严重度 MEDIUM
- **机制**：V8 优化编译器在整数回绕（speculative number）假设上被绕过，
- **poc**：`data/real_world/RW-054.cpp`（sha256 13018ffce761e593…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**c_配置缺口_未启用检查** —— UB 子类未启用（如 float-cast-overflow / alignment 报告面不足）
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) confused read = 424242; -O2(rc=0) confused read = 424242]
- **改进建议**：-fsanitize=undefined 的 alignment 子检查 + 强类型重构；联合体误用建议 clang -Wstrict-aliasing。

### F14. RW-088 · CVE-2021-3490 · Linux kernel （`integer_overflow`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2021-3490｜年份 2021｜严重度 HIGH
- **机制**：eBPF ALU32 边界跟踪缺陷 —— 32 位操作后 verifier 的 umin/umax
- **poc**：`data/real_world/RW-088.cpp`（sha256 f1172ffc788fbc2f…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**c_配置缺口_未启用检查** —— UB 子类未启用（如 float-cast-overflow / alignment 报告面不足）
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) tracked umax=0x7FFFFFFF real=2147483647 crafted=2147483647 outside=no; -O2(rc=0) tracked umax=0x7FFFFFFF real=2147483647 crafted=2147483647 outside=no]
- **改进建议**：ubsan 有符号溢出覆盖；无符号回绕需补 -fsanitize=unsigned-integer-overflow（clang）。

### F15. RW-017 · CVE-2023-38546 · curl （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2023-38546｜年份 2023｜严重度 LOW
- **机制**：cookie 文件注入——libcurl 特定配置下可从"外部"文件读取 cookie，
- **poc**：`data/real_world/RW-017.cpp`（sha256 77408d5c8d169e99…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) cookies loaded: 0; -O2(rc=0) cookies loaded: 0]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F16. RW-018 · CVE-2022-32221 · curl （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2022-32221｜年份 2022｜严重度 CRITICAL
- **机制**：307/308 重定向后，当请求体已被消费（如 PUT）时方法被错误改写成 POST，
- **poc**：`data/real_world/RW-018.cpp`（sha256 444fed6d9d885c29…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) method after 307 redirect = POST (expected PUT); -O2(rc=0) method after 307 redirect = POST (expected PUT)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F17. RW-024 · CVE-2019-20372 · nginx （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2019-20372｜年份 2020｜严重度 MEDIUM
- **机制**：error_page 指向外部重定向时，未消费的请求体与请求行状态导致
- **poc**：`data/real_world/RW-024.cpp`（sha256 ae65c8cab418a607…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) HTTP/1.1 302 Found Location: /login  [leftover body interpreted as next request: GET /admin HTTP/1.1]; -O2(rc=0) HTTP/1.1 302 Found Location: /login  [leftover body interpreted as next request: GET 
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F18. RW-025 · CVE-2021-41773 · Apache HTTP Server （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2021-41773｜年份 2021｜严重度 CRITICAL
- **机制**：路径规范化（"." 处理）缺陷：%2e 编码的点使规范化函数返回失败但
- **poc**：`data/real_world/RW-025.cpp`（sha256 74fad5be97fa32cd…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) normalized form would be: /cgi-bin/../../../../etc/passwd; -O2(rc=0) normalized form would be: /cgi-bin/../../../../etc/passwd]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F19. RW-026 · CVE-2021-42013 · Apache HTTP Server （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2021-42013｜年份 2021｜严重度 CRITICAL
- **机制**：对 CVE-2021-41773 修复的不完整：双编码 %%32%65 组合在二次解码后
- **poc**：`data/real_world/RW-026.cpp`（sha256 59f5545f072355dd…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) request deemed safe = no (bug: bypass); -O2(rc=0) request deemed safe = no (bug: bypass)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F20. RW-028 · CVE-2018-15473 · OpenSSH （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2018-15473｜年份 2018｜严重度 MEDIUM
- **机制**：认证流程对无效用户名提前返回（不进入延迟/伪造认证），响应时延与
- **poc**：`data/real_world/RW-028.cpp`（sha256 45214fd3603b5b73…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) invalid-user rc=1 (fast), valid-user rc=2 (slow) -> oracle; -O2(rc=0) invalid-user rc=1 (fast), valid-user rc=2 (slow) -> oracle]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F21. RW-047 · CVE-2016-3714 · ImageMagick （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2016-3714｜年份 2016｜严重度 HIGH
- **机制**：ImageTragick —— 委托（delegate）命令模板中把用户控制的 URL/文件名
- **poc**：`data/real_world/RW-047.cpp`（sha256 f3c9c834875ff5b0…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) delegate cmd = curl -s 'https://evil.example/";touch /tmp/pwned;"a' > /tmp/out.img charset check would have rejected: YES; -O2(rc=0) delegate cmd = curl -s 'https://evil.example/";touch /tmp/pwned;"
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F22. RW-050 · CVE-2016-1897 · FFmpeg （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2016-1897｜年份 2016｜严重度 MEDIUM
- **机制**：HLS 播放列表解析允许 "concat:" 协议 + 本地文件路径，攻击者控制的
- **poc**：`data/real_world/RW-050.cpp`（sha256 fa9f1fbfd1fae0c8…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) resolved URI: concat:file:///etc/passwd|file:///etc/shadow local file content would be exposed: YES; -O2(rc=0) resolved URI: concat:file:///etc/passwd|file:///etc/shadow local file content would be 
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F23. RW-052 · CVE-2021-42574 · Unicode/LLVM/GCC 生态 （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2021-42574｜年份 2021｜严重度 HIGH
- **机制**：Trojan Source —— 源码注释/字符串中嵌入 Unicode 双向控制字符
- **poc**：`data/real_world/RW-052.cpp`（sha256 49533956b42c74bd…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) low-privilege user granted: YES (bug) bidi code points in source: U+202E U+2066 U+2069; -O2(rc=0) low-privilege user granted: YES (bug) bidi code points in source: U+202E U+2066 U+2069]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F24. RW-063 · CVE-2022-1552 · PostgreSQL （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2022-1552｜年份 2022｜严重度 HIGH
- **机制**：autovacuum 以更高权限执行用户可创建的维护函数（security definer 语义
- **poc**：`data/real_world/RW-063.cpp`（sha256 169a48746f1a858c…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) attacker maintenance fn runs as ROLE=2 (2=superuser); -O2(rc=0) attacker maintenance fn runs as ROLE=2 (2=superuser)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F25. RW-067 · CVE-2022-1941 · protobuf （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2022-1941｜年份 2022｜严重度 HIGH
- **机制**：解析深度/递归限制在 C++ 实现中可被绕过，超长嵌套消息造成
- **poc**：`data/real_world/RW-067.cpp`（sha256 f7a030151402e767…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) parse accepted nesting far beyond limit: no; -O2(rc=0) parse accepted nesting far beyond limit: no]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F26. RW-068 · CVE-2021-22569 · protobuf （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2021-22569｜年份 2022｜严重度 HIGH
- **机制**：Java 端为主的解析歧义（同一字节流两种解析）在 C++ 侧的对应形态：
- **poc**：`data/real_world/RW-068.cpp`（sha256 a3e8294172e7aa7b…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) values equal: yes, bytes differ: yes -> downstream divergence; -O2(rc=0) values equal: yes, bytes differ: yes -> downstream divergence]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F27. RW-070 · CVE-2023-34410 · Qt （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2023-34410｜年份 2023｜严重度 MEDIUM
- **机制**：QSslSocket/TLS 后端在特定配置下跳过主机名验证（策略判定错误），
- **poc**：`data/real_world/RW-070.cpp`（sha256 fd953943509a5edf…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) wrong-host cert accepted = YES (bug); -O2(rc=0) wrong-host cert accepted = YES (bug)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F28. RW-072 · CVE-2023-32762 · Qt （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2023-32762｜年份 2023｜严重度 MEDIUM
- **机制**：QHttp2 的 DATA/HEADERS 帧流控窗口计数错误，攻击者可让连接进入
- **poc**：`data/real_world/RW-072.cpp`（sha256 8344ec37efff8467…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) window_local=14335 window_remote=-25665 -> stalled=YES (bug); -O2(rc=0) window_local=14335 window_remote=-25665 -> stalled=YES (bug)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F29. RW-074 · CVE-2022-0847 · Linux kernel （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2022-0847｜年份 2022｜严重度 HIGH
- **机制**：Dirty Pipe —— 管道缓冲 page 的 flags 未初始化（关键：PIPE_BUF_FLAG_CAN_MERGE），
- **poc**：`data/real_world/RW-074.cpp`（sha256 cc52710f8d4382ca…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) reused buffer flags=0x10 (CAN_MERGE set => file page writable): YES (bug); -O2(rc=0) reused buffer flags=0x10 (CAN_MERGE set => file page writable): YES (bug)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F30. RW-083 · CVE-2019-5596 · FreeBSD （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2019-5596｜年份 2019｜严重度 HIGH
- **机制**：capsicum 能力模式下 F_GETOWN 等 fcntl 请求未受能力检查约束，
- **poc**：`data/real_world/RW-083.cpp`（sha256 97ce08805ba042da…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) sandboxed F_GETOWN allowed = YES (bug); -O2(rc=0) sandboxed F_GETOWN allowed = YES (bug)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F31. RW-084 · CVE-2020-7457 · FreeBSD （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2020-7457｜年份 2020｜严重度 HIGH
- **机制**：TCP 连接状态处理缺陷 —— connect() 对端在 SYN 窗口内的
- **poc**：`data/real_world/RW-084.cpp`（sha256 fb3fd2efb166b13d…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) accepted peer attacker at ack=1002 (iss=1000) hijacked state=2; -O2(rc=0) accepted peer attacker at ack=1002 (iss=1000) hijacked state=2]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F32. RW-085 · CVE-2021-29628 · FreeBSD （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2021-29628｜年份 2021｜严重度 HIGH
- **机制**：ktls 发送路径中多个 TLS 记录共享同一 mbuf 时的清零顺序问题，
- **poc**：`data/real_world/RW-085.cpp`（sha256 0d5a8aea72fdffdd…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) record stored=0 seq=1 (stale bytes exposed); -O2(rc=0) record stored=0 seq=1 (stale bytes exposed)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F33. RW-087 · CVE-2019-13272 · Linux kernel （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2019-13272｜年份 2019｜严重度 HIGH
- **机制**：ptrace PTRACE_TRACEME + suid 程序的父进程替换检查缺失，
- **poc**：`data/real_world/RW-087.cpp`（sha256 4482447103d4a4c7…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) forged parent can ptrace suid process = YES (bug); -O2(rc=0) forged parent can ptrace suid process = YES (bug)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F34. RW-092 · CVE-2022-26691 · CUPS （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2022-26691｜年份 2022｜严重度 MEDIUM
- **机制**：认证字符串比较使用非常量时间/前缀宽松匹配，本地攻击者可绕过
- **poc**：`data/real_world/RW-092.cpp`（sha256 adfcd7a36a26a363…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) prefix-only cert accepted = YES (bug); -O2(rc=0) prefix-only cert accepted = YES (bug)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F35. RW-098 · CVE-2022-32208 · curl （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2022-32208｜年份 2022｜严重度 MEDIUM
- **机制**：FTP PASV/EPSV 应答解析缺陷：非 IP 形式的应答被错误解析为地址，
- **poc**：`data/real_world/RW-098.cpp`（sha256 62a25bad136cc149…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) accepted malformed PASV reply (read 4/6 fields) connected to 10.0.0.1:0; -O2(rc=0) accepted malformed PASV reply (read 4/6 fields) connected to 10.0.0.1:0]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F36. RW-099 · CVE-2023-27534 · curl （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2023-27534｜年份 2023｜严重度 HIGH
- **机制**：SFTP 路径中 "~" 展开缺陷 —— 构造的路径使 curl 相对攻击者选择的
- **poc**：`data/real_world/RW-099.cpp`（sha256 0693fbc64ebbf2ba…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) SFTP will operate on: /home/deploy/../../../etc/shadow; -O2(rc=0) SFTP will operate on: /home/deploy/../../../etc/shadow]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F37. RW-101 · CVE-2021-22946 · curl （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2021-22946｜年份 2021｜严重度 HIGH
- **机制**：协议降级允许 —— 服务器可强制 client 在 STARTTLS/加密逻辑前
- **poc**：`data/real_world/RW-101.cpp`（sha256 7cb60efedc40c7d5…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) server refused STARTTLS; continuing in cleartext (bug) session tls=OFF (downgraded); -O2(rc=0) server refused STARTTLS; continuing in cleartext (bug) session tls=OFF (downgraded)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F38. RW-102 · CVE-2020-8177 · curl （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2020-8177｜年份 2020｜严重度 HIGH
- **机制**：curl -J（Content-Disposition 文件名）与 -i 组合时用服务器提供的
- **poc**：`data/real_world/RW-102.cpp`（sha256 325498a44ea115d3…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) writing to: important-local-file.conf (server-chosen, overwrite); -O2(rc=0) writing to: important-local-file.conf (server-chosen, overwrite)]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F39. RW-105 · CVE-2023-27536 · curl （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2023-27536｜年份 2023｜严重度 MEDIUM
- **机制**：GSSAPI 委托（delegation）标志在连接复用间保留，前一次请求的
- **poc**：`data/real_world/RW-105.cpp`（sha256 8e1744052012636b…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=unknown；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) reused conn: delegate=true (requested false), principal=svc-delegated@REALM; -O2(rc=0) reused conn: delegate=true (requested false), principal=svc-delegated@REALM]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

### F40. RW-107 · CVE-2023-44487 · HTTP/2 协议栈（nginx/httpd/Go 等） （`logic_error`）

- **来源**：https://nvd.nist.gov/vuln/detail/CVE-2023-44487｜年份 2023｜严重度 HIGH
- **机制**：HTTP/2 Rapid Reset —— 客户端立即 RST_STREAM 每个请求流，
- **poc**：`data/real_world/RW-107.cpp`（sha256 ccb8420431e457cb…）
- **8 资产判定**：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown
- **归因**：**a_能力盲区_逻辑与并发语义** —— 无法被内存/UB 检测器观测的逻辑缺陷
- **检测器输出摘录**（asan）：asan 两档均无报告[-O0(rc=0) server work units burned=10000000 with 100000 resets; -O2(rc=0) server work units burned=10000000 with 100000 resets]
- **改进建议**：启用静态分析（clang-tidy bugprone 系列）+ 状态机断言；把'用户可见行为差异'写成可测性质（四态判决里 unknown 不是失败）。

## 汇总

- 深读 40 条；全量 miss 45 条清单见判定矩阵 JSON。
- **e 类（误报）说明**：本批准入口径为'任一资产 catch 即 catch'，检测器报出无关错误时该样本仍记 catch（note 中保留原始输出可复核），因此 miss 集合中不存在 e 类样本——如实说明而非硬凑分类。
