# 683-A3 · 成功案例（≥20 条 catch 深读，含「独苗命中」）

筛选：`or_verdict == catch` 共 65 条；优先收录「**单资产独苗命中**」（其余资产全 miss）——这类案例直接证明资产互补性。

独苗命中总数：**27** / 65 catch（41.5%）

### S1. RW-001 · CVE-2014-0160 · OpenSSL （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2014-0160｜机制：Heartbleed —— TLS heartbeat 响应长度取自攻击者声明的字段，
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==58==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffff5000064 at pc 0x7ffff78fb42e bp 0x7fffffffe31
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S2. RW-003 · CVE-2021-3711 · OpenSSL （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2021-3711｜机制：SM2 解密流程中密文字节长度被转换为 int 后参与缓冲区长度计算，
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==58==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x502000000020 at pc 0x7ffff78fb303 bp 0x7fffffffe350
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S3. RW-006 · CVE-2022-4450 · OpenSSL （`double_free`）— 独苗：**cross-compile**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2022-4450｜机制：PEM_read_bio_ex 在特定畸形输入下对同一缓冲释放两次。
- cross-compile 输出摘录：g++/clang++ 输出不一致
- 其余资产：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；linker=miss；compile-time=unknown

### S4. RW-008 · CVE-2022-3602 · OpenSSL （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2022-3602｜机制：X.509 名称约束检查中，punycode 解码到固定 4 字节栈缓冲，越界写 1 字节。
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==843==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffff4f00024 at pc 0x555555555380 bp 0x7fffffffe4
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S5. RW-015 · CVE-2023-6246 · glibc （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2023-6246｜机制：__vsyslog_internal 中消息长度计算与实际写入不一致，超长程序名/消息
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==20895==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x50200000001c at pc 0x7ffff78fb303 bp 0x7fffffffe
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S6. RW-016 · CVE-2023-38545 · curl （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2023-38545｜机制：SOCKS5 握手：目标主机名超长（>255）时本应回退本地解析，
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==97==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x511000000140 at pc 0x7ffff78fb303 bp 0x7fffffffe2d0
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S7. RW-019 · CVE-2016-8618 · curl （`double_free`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2016-8618｜机制：curl_maprintf 出错路径与调用者清理路径对同一缓冲二次释放。
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==569==ERROR: AddressSanitizer: attempting double-free on 0x50c000000040 in thread T0:     #0 0x7ffff78fc4d8 in free
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S8. RW-020 · CVE-2017-1000257 · curl （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2017-1000257｜机制：FTP 通配符（glob）响应解析时，服务端返回的超长文件名被拷贝进
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==25==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x511000000140 at pc 0x7ffff78a7923 bp 0x7fffffffe2e0
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S9. RW-027 · CVE-2024-6387 · OpenSSH （`data_race`）— 独苗：**tsan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2024-6387｜机制：regreSSHion —— SIGALRM 处理器中调用非 async-signal-safe 的
- tsan 输出摘录：tsan 命中[-O0(rc=66) log writes = 4000, last = timeout before a================== WARNING: ThreadSanitizer: data race (pid=21426)   Write of size 8 at 0x555555559040 by main thread:     #0 strncpy ../..
- 其余资产：asan=miss；ubsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S10. RW-029 · CVE-2022-23308 · libxml2 （`use_after_free`）— 独苗：**cross-compile**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2022-23308｜机制：xmlXPtrRangeToFunction / XML 指针范围求值中对已释放节点再次访问，
- cross-compile 输出摘录：g++/clang++ 输出不一致
- 其余资产：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；linker=miss；compile-time=unknown

### S11. RW-032 · CVE-2017-9047 · libxml2 （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2017-9047｜机制：xmlSnprintfElementContent 的递归拼接在复合内容模型上超过 5000 字节
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==25==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7ffff5601618 at pc 0x7ffff78ced69 bp 0x7fffffffcc3
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S12. RW-033 · CVE-2022-37434 · zlib （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2022-37434｜机制：inflateGetHeader 对 gzip 头 extra 字段长度复制越界（extra_max 与实际
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==181==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x502000000020 at pc 0x7ffff78fb303 bp 0x7fffffffe38
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S13. RW-034 · CVE-2018-25032 · zlib （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2018-25032｜机制：deflate 压缩特定"未跟踪块"模式时，sym_buf 写入量超过分配（内存破坏，
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==337==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x506000000060 at pc 0x55555555557a bp 0x7fffffffe3f
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S14. RW-043 · CVE-2016-5321 · libtiff （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2016-5321｜机制：DumpModeDecode（未压缩 raw 模式）中扫描行尺寸计算与实际读取不一致，
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==1997==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x506000000060 at pc 0x7ffff78fb42e bp 0x7fffffffe3
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S15. RW-045 · CVE-2016-0718 · expat （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2016-0718｜机制：对恶意 UTF-8 编码的 XML 内容，多字节解码循环中输出缓冲推进越界
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==3001==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x502000000020 at pc 0x555555555678 bp 0x7fffffffe3
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S16. RW-049 · CVE-2020-12284 · FFmpeg （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2020-12284｜机制：cbs_jpeg（JPEG 码流解析）中熵段长度处理越界写。
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==3647==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x506000000060 at pc 0x55555555550c bp 0x7fffffffe3
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S17. RW-051 · CVE-2023-49502 · FFmpeg （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2023-49502｜机制：vf_bwdif 反交错滤镜对奇数行尺寸/边界像素处理越界（堆缓冲区溢出）。
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==3961==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x51d0000008c0 at pc 0x555555555502 bp 0x7fffffffe3
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S18. RW-057 · CVE-2021-30663 · WebKit （`integer_overflow`）— 独苗：**cross-compile**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2021-30663｜机制：WebKit 图像/画布尺寸计算整数溢出导致缓冲不足（恶意网页内存破坏）。
- cross-compile 输出摘录：g++/clang++ 输出不一致
- 其余资产：asan=miss；ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；linker=miss；compile-time=unknown

### S19. RW-059 · CVE-2022-31747 · Firefox （`use_after_free`）— 独苗：**tsan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2022-31747｜机制：WebRTC 媒体通道关闭竞态：track 已被释放，统计回调仍访问其一
- tsan 输出摘录：tsan 命中[-O0(rc=66) stats: track 7 kind video================== WARNING: ThreadSanitizer: heap-use-after-free (pid=6037)   Read of size 4 at 0x720800000020 by main thread:     #0 stats_poll_once() /mnt
- 其余资产：asan=miss；ubsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S20. RW-060 · CVE-2022-35737 · SQLite （`integer_overflow`）— 独苗：**ubsan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2022-35737｜机制：printf 风格 %lld 角标处理在超大字符串参数（>2GB，或特定平台
- ubsan 输出摘录：ubsan 命中[-O0(rc=0) offset result: /mnt/c/Users/ASUS/AppData/Local/Temp/tmpvqroj1oj/RW-060.cpp:23:60: runtime error: signed integer overflow: 999999999999999999 * 10 cannot be represented in type 'long
- 其余资产：asan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S21. RW-062 · CVE-2019-13750 · SQLite（Chromium 内置） （`out_of_bounds`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2019-13750｜机制：FTS3/4 分词器处理畸形 MATCH 查询段时片段边界校验缺失（越界读）。
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==6435==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x502000000020 at pc 0x555555555456 bp 0x7fffffffe3
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S22. RW-064 · CVE-2023-5868 · PostgreSQL （`memory_leak`）— 独苗：**asan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2023-5868｜机制：aggregate 函数（如某些 JSON/数组聚合）内存上下文计算错误，
- asan 输出摘录：asan 命中[-O0(rc=1) ================================================================= ==6858==ERROR: LeakSanitizer: detected memory leaks  Direct leak of 16384 byte(s) in 64 object(s) allocated from:   
- 其余资产：ubsan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S23. RW-075 · CVE-2016-5195 · Linux kernel （`data_race`）— 独苗：**tsan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2016-5195｜机制：Dirty COW —— get_user_pages 与 COW 断链（FOLL_WRITE 重试）之间的
- tsan 输出摘录：tsan 命中[-O0(rc=66) dirty COW race window exercised================== WARNING: ThreadSanitizer: data race (pid=10102)   Write of size 1 at 0x7fffffffe4c4 by thread T2:     #0 fault_handler_thread(CowPa
- 其余资产：asan=miss；ubsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

### S24. RW-096 · CVE-2021-46143 · expat （`integer_overflow`）— 独苗：**ubsan**

- 出处：https://nvd.nist.gov/vuln/detail/CVE-2021-46143｜机制：doProlog（DTD 处理）中组计数以 int 累加，构造深层/重复 DTD 组
- ubsan 输出摘录：ubsan 命中[-O0(rc=0) group_count=-2147483624/mnt/c/Users/ASUS/AppData/Local/Temp/tmpsi28lx6l/RW-096.cpp:22:23: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int';
- 其余资产：asan=miss；tsan=miss；compiler-warn=miss；wunsequenced=unknown；cross-compile=miss；linker=miss；compile-time=unknown

## 多资产联合命中（抽样）

- RW-004（OpenSSL）：asan,cross-compile 同时命中（互补冗余的正面样本）
- RW-007（OpenSSL）：asan,tsan 同时命中（互补冗余的正面样本）
- RW-011（glibc）：asan,cross-compile 同时命中（互补冗余的正面样本）
- RW-013（glibc）：asan,cross-compile,tsan 同时命中（互补冗余的正面样本）
- RW-014（glibc）：asan,cross-compile 同时命中（互补冗余的正面样本）
- RW-021（curl）：asan,cross-compile 同时命中（互补冗余的正面样本）

## 结论

- 独苗命中率说明：**没有单一资产足够**；OR 组合的价值由这些样本直接支撑。
- 与 A5/682 的 Shapley 结论交叉：asan/ubsan 贡献最大；真实靶场上**linker 资产 0 catch**（110 条均为单 TU 重构，无多定义触发面）——这是'资产在真实样本上的适用面收窄'的直接观测，登记为坦白项而非缺陷。
