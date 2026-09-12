# 资料研究第五十三轮：虚拟化与模拟器——QEMU、KVM、TCG 动态翻译、半虚拟化 virtio、内存虚拟化 EPT、中断注入

> 2026-09-11，底层工程资料研究员。主题：全虚拟化 vs 半虚拟化 vs 硬件辅助虚拟化、QEMU 的两种加速器（TCG 软件模拟 vs KVM 硬件虚拟化）、TCG 动态二进制翻译（JIT 的又一形态）、KVM 内核模块如何把 Linux 变成 hypervisor、CPU 虚拟化（VT-x VMX）、内存虚拟化（影子页表 → EPT/NPT 两级地址转换）、virtio 半虚拟化 IO 与 vhost、中断注入与虚拟设备、Firecracker/云原生轻量虚拟化。
> 检索方式：general_search + QEMU 官方 TCG 文档与术语表 + UCSD KVM/QEMU/Firecracker 讲义 + Yizhou Shan 虚拟化栈笔记 + hackingnote KVM + olivierpierre virt-101（VT-x/EPT/VT-d）+ openEuler EPT/THP。
> **虚拟化/模拟器域第一轮（全新域）**。与 32 编译器后端（TCG=JIT）、35 JIT、28 GPU（设备模拟）、48 Rust（内核组件）衔接。

---

## 一、虚拟化的三阶段

| 阶段 | 技术 | 原理 | 性能 |
|---|---|---|---|
| 纯软件模拟 | QEMU TCG | 逐指令翻译执行（如模拟 ARM 在 x86 上跑） | 慢（10x+ 损耗） |
| 半虚拟化 | virtio/Xen | 客户机"知道"自己在虚拟化，用超调用（hypercall）与主机协作 | 接近原生 |
| 硬件辅助 | KVM + VT-x/EPT | CPU 硬件原生跑客户机指令，Hypervisor 只插桩 | 近原生（<5%） |

- 现代组合：**QEMU（设备模拟/管理）+ KVM（CPU/内存加速）**——一个软件、两种加速器（QEMU 术语表明确 TCG 和 KVM 是并列的 accel）

## 二、TCG：动态二进制翻译（模拟器的心脏）

### 1. 是什么

- QEMU 的 **Tiny Code Generator**：把客户机指令 JIT 翻译成主机指令
- 首次遇到代码块时翻译并缓存（块缓存），后续直接执行翻译后的代码——**解释器 + JIT 缓存的结合**（衔接 35 轮 JIT 思想）
- 中间表示：TCG IR（类 RISC 的中间指令）→ 主机后端生成机器码——**与 LLVM 同构的分层设计**（衔接 63 轮 MLIR 渐进降低）

### 2. 为什么还能"快"

- 翻译一次、执行多次（循环体/热路径）→ 摊薄翻译成本
- 只翻译实际执行的代码（惰性）
- 但仍是模拟：无硬件加速、状态维护开销大——适合交叉开发/测试，不适合生产性能

## 三、KVM：把 Linux 变成 hypervisor

- **KVM = 内核模块**：加载后 Linux 内核本身拥有 hypervisor 能力（/dev/kvm 设备）
- 客户机代码在 **VMX non-root 模式**原生执行：普通指令直接跑（硬件加速），敏感指令（特权操作）触发 **VM-exit** 陷入 KVM 处理，处理完 VM-entry 回客户机
- 定位分工：
  - KVM（内核）：CPU/内存/中断的底层虚拟化
  - QEMU（用户态）：设备模拟、BIOS、管理面
  - 二者通过 ioctl 通信（/dev/kvm）

## 四、内存虚拟化：从影子页表到 EPT

### 1. 问题

客户机有虚拟地址（GVA）→ 客户机物理地址（GPA）→ 主机物理地址（HPA）**三级地址**，每次访存都要换算

### 2. 影子页表（旧方案）

- Hypervisor 维护"GVA → HPA"的直接映射表（把两级合并），客户机 CR3 指向影子页表
- 问题：每次客户机改页表都要重做影子页表（页表切换频繁 → 开销大）

### 3. EPT/NPT（Intel Extended Page Table / AMD Nested Page Table）

- **硬件直接做 GVA→GPA→HPA 两级转换**（VT-x 的 EPT 机制）：
  - 客户机自己管 GVA→GPA（它以为自己是真机）
  - EPT 由 hypervisor 管 GPA→HPA
  - CPU 硬件查两级页表，**无需软件介入每次访存**
- 配套：**透明大页（THP）**减少 EPT 条目；TLB 缓存两级转换结果
- 这就是"硬件辅助虚拟化"性能近原生的核心

- **来源**：olivierpierre virt-101 + openEuler + hackingnote
- **可信度**：S

---

## 五、virtio：半虚拟化 IO

### 1. 为什么设备模拟慢

- QEMU 模拟真实网卡（如 e1000）：客户机驱动发一个包 → 模拟设备 → 主机 I/O → 中断注入——每步都经过软件，慢

### 2. virtio 方案

- **客户机装专用 virtio 驱动**，与主机共享**环形描述符队列**（virtqueue）：
  - 客户机把请求写入共享内存环 → 通知（kick）主机 → 主机处理 → 完成事件回客户机
  - 无逐设备模拟：共享内存 + 少量通知（类似 io_uring 的 SQ/CQ 思想！）
- **vhost**：把 virtio 的后端处理**下沉到内核/DPDK**（vhost-user）——数据面绕开 QEMU 进程，性能大幅提升
- 半虚拟化的本质：**客户机配合（知情）换取性能**——"协议/接口"成为第一公民

## 六、中断注入与虚拟设备

- 客户机"外设中断"由 KVM 注入（VM-entry 时设置中断向量）——虚拟设备的完成事件靠**中断注入**唤醒客户机
- 中断延迟是虚拟化 IO 的关键指标（事件驱动的设备模拟 vs 轮询 virtio 对比）
- 虚拟设备生命周期：QEMU 主循环线程管理设备、信号通知（lastweek.io 笔记：QEMU 设备经 Linux 信号向主循环"fire interrupts"）

## 七、现代趋势：轻量虚拟化

- **Firecracker（AWS Lambda 底座）**：去掉 BIOS/PCI 等"传统"设备，极简虚拟化（KVM + 极简 virtio）→ 微秒级启动、GB 级内存粒度的安全隔离
- 云原生：容器（共享内核，弱隔离）vs VM（独立内核，强隔离）vs Firecracker（VM 的隔离 + 容器的密度）
- 安全边界：虚拟化隔离是云安全的第一层（旁路攻击如 Spectre/Meltdown 让虚拟化安全研究持续活跃——衔接 47 轮密码学/安全）

## 八、知识网络

```
虚拟化
├── 三路线：TCG 模拟 / virtio 半虚拟化 / KVM 硬件辅助
├── TCG：动态翻译、TCG IR、块缓存（JIT 形态）
├── KVM：VMX non-root、VM-exit/entry、内核+用户态分工
├── 内存：影子页表 → EPT/NPT 两级硬件转换、THP
├── virtio：virtqueue 共享环、kick、vhost(-user)
├── 中断注入与虚拟设备
└── Firecracker：极简虚拟化、云原生隔离
```

---

## 九、本轮最重要的资料

1. **QEMU 官方 TCG 文档**（S）——动态翻译权威
2. **UCSD KVM/QEMU/Firecracker 讲义**（S）——三件套系统讲解
3. **olivierpierre virt-101**（S）——VT-x/EPT/VT-d 机制
4. **hackingnote KVM 笔记**（A+）——EPT/virtio 简洁
5. **Yizhou Shan 虚拟化栈笔记**（A+）——QEMU 内部结构

## 十、适合进入 CPP-Bible 的原子

- "TCG：模拟器里的 JIT"（SYS/COMP，衔接 JIT 轮）
- "EPT：三级地址如何变成两级硬件转换"（SYS/ARCH，虚拟内存的延伸）
- "virtio 共享环：客户机与主机的 io_uring"（SYS/NET，跨域同构洞见）
- "VM-exit：敏感指令如何陷入 Hypervisor"（SYS/ARCH）
- "Firecracker：极简虚拟化的设计取舍"（SYS/ENG 案例）

## 十一、与已有调研的关联

- 第三十五轮 JIT：TCG 是 JIT 的模拟器变体
- 第六十三轮 MLIR：TCG IR 与 LLVM/MLIR 同分层哲学
- 第五十一轮内存管理：页表/THP 是 EPT 的基础
- 第二十八轮 GPU：设备模拟（虚拟 GPU）是 virtio 家族
- 第五十二轮 eBPF：vhost-user 与 DPDK 在云网络中的组合

## 十二、下一轮方向

软件测试工程（单测/性质测试/fuzzing/变异测试）。

---

*本轮新增知识节点：虚拟化、hypervisor、QEMU、KVM、TCG、Tiny Code Generator、动态二进制翻译、动态翻译、JIT、全虚拟化、半虚拟化、paravirtualization、硬件辅助虚拟化、VT-x、VMX、VM-exit、VM-entry、EPT、NPT、影子页表、两级地址转换、GVA、GPA、HPA、THP、virtio、virtqueue、kick、vhost、vhost-user、中断注入、Firecracker、AWS Lambda、Xen、hvf、whpx、MSHV、云原生隔离。补齐了"虚拟化/模拟器"域核心空白。*
