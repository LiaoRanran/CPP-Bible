# 资料研究第四十二轮：TCP 与拥塞控制——状态机、三次握手、流量控制、慢启动、CUBIC、BBR、QUIC、内核协议栈

> 2026-09-11，底层工程资料研究员。主题：TCP 连接生命周期（状态机/三次握手/四次挥手）、可靠传输机制（序列号/确认/重传）、流量控制（窗口）、拥塞控制（AIMD/慢启动/拥塞避免/CUBIC/BBR）、高带宽时延积网络、丢包 vs 延迟的信号之争、QUIC/UDP 化的 TCP、Linux 内核协议栈实现路径。
> 检索方式：general_search + IETF RFC 9002（QUIC 丢包恢复）+ BBR draft（IETF CCWG）+ RFC 9438（CUBIC）+ CSDN TCP 深度解析 + cemergin 网络深度 + theinternetpapers TCP 解剖 + god.ad TCP 工作原理 + haotianblog TCP 可靠性 + routeharden 拥塞控制。
> **网络域第二轮**。第一轮：26 网络异步 IO。与第二十六轮（epoll/io_uring）、第四十七轮（TLS 在 TCP 上）、第二十九轮（分布式信任）衔接。

---

## 一、TCP 的三大承诺与实现手段

| 承诺 | 实现 |
|---|---|
| 可靠传输 | 序列号 + ACK + 重传（超时/快速重传） |
| 有序 | 序列号排序缓冲 |
| 拥塞控制 | 拥塞窗口 cwnd 算法族 |

TCP 是"字节流 + 连接 + 滑动窗口"协议：发送方有发送缓冲，接收方有接收窗口（rwnd），网络有拥塞窗口（cwnd），实际在途字节 = min(rwnd, cwnd)。

## 二、连接生命周期

### 1. 三次握手

```
Client                          Server
CLOSED                          LISTEN
  |---- SYN(seq=ISN_c) ------->|  SYN_SENT → SYN_RCVD
  |<--- SYN+ACK(seq=ISN_s) ----|  (半连接：SYN backlog)
  |---- ACK ------------------>|  ESTABLISHED
ESTABLISHED
```

- 作用：确认双方可达、同步初始序列号（ISN，防伪造）、协商选项（MSS、窗口缩放、SACK）
- SYN flood：半连接队列被塞满 → SYN cookie 缓解

### 2. 四次挥手与状态

```
主动方 FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT（2MSL）
被动方 CLOSE_WAIT → LAST_ACK → CLOSED
```

- TIME_WAIT（2×MSL，约 60s）：保证最后 ACK 可达、旧连接报文不会串到新连接——**大量短连接服务器 TIME_WAIT 堆积**是经典工程问题（端口耗尽）
- CLOSE_WAIT 堆积：对端关了你不关 → fd 泄漏的标志

- **来源**：theinternetpapers + god.ad + CSDN
- **可信度**：S

---

## 三、可靠传输机制

### 1. 序列号与确认

- 每个字节有序列号；ACK 表示"期望的下一个字节"（累积确认）
- 发送窗口：已发未确认的字节数上限

### 2. 重传策略

| 机制 | 触发 | 特点 |
|---|---|---|
| 超时重传（RTO） | 超时（RTT 估计：指数退避） | 保守，等待最久 |
| 快速重传 | 收到 3 个重复 ACK | 快速发现单包丢失 |
| SACK（选择性确认） | 接收方报告收到的乱序段 | 只重传丢的，避免全窗口重传 |
| 快速恢复 | 重传后降低速率而非回到慢启动 | 应对突发丢包 |

### 3. 流量控制（接收方窗口 rwnd）

- 接收方通过 ACK 通告自己的空闲缓冲 → 发送方不能超出 rwnd
- **零窗口探测**：接收窗口为 0 时发送方定期探测，避免死锁

- **来源**：god.ad + haotianblog + CSDN
- **可信度**：S

---

## 四、拥塞控制：网络公平的分布式算法

拥塞控制是最精彩的分布式算法之一：每个发送方**只凭自己的丢包/延迟观测**推断全网拥塞，没有中央协调。

### 1. AIMD（加性增、乘性减，Reno 基础）

- 拥塞避免阶段：每个 RTT cwnd +1（加性增，线性）
- 检测到丢包：cwnd 减半（乘性减）
- 数学性质：**收敛公平**——多个流最终均分带宽（线性图上收敛到公平线）

### 2. 慢启动（Slow Start）

- 新连接 cwnd 从 1-10 MSS 开始，**每个 ACK 翻倍**（每 RTT 指数增长）——"慢启动"其实增长很快，名字指起点保守
- 直到 ssthresh（拥塞阈值）或丢包
- HyStart++（RFC 9406）：根据 RTT 增加判定退出点，避免过度增长

### 3. CUBIC（Linux 默认，RFC 9438）

- 丢包后窗口函数用**时间的三次函数**（不受 RTT 影响）：
  - 离上次拥塞点远 → 快速爬升（填满高带宽时延积网络）
  - 接近上次拥塞点 → 平缓（在"安全区"附近谨慎）
  - 超过 → 继续加速
- 2007 年起 Linux 默认，高 BDP 网络远优于 Reno 线性增长

### 4. BBR（模型驱动，draft-ietf-ccwg-bbr）

- **范式转变**：Reno/CUBIC 把"丢包"当拥塞信号（先破坏再退让）；BBR 直接用**测量的带宽与 RTT 建模**
- 核心：估算瓶颈带宽（BtlBw）与最小 RTT（RTprop），维持"管道填满但不过量"的在途数据（BDP = BtlBw × RTprop）
- 每轮 RTT 探测带宽上限、定期探测最小 RTT（PROBE_RTT）
- 优点：高 BDP 网络吞吐远超丢包驱动算法，延迟更低
- 争议：对传统丢包驱动流不够公平（"抢占"批评）、与队列管理的交互复杂

### 5. 丢包 vs 延迟的信号之争

- 丢包驱动（Reno/CUBIC）：简单可靠，但把队列填满才"知道"拥塞（bufferbloat）
- 延迟驱动（Vegas/BBR 的部分）：主动观测 RTT 增长，更早减速，但 RTT 噪声大、测量难
- 现代工程：BBR + fq（公平队列）组合；ECN（显式拥塞通知）让路由器主动标拥塞

- **来源**：RFC 9438 + BBR draft + dmccreary + routeharden + cemergin
- **可信度**：S

---

## 五、QUIC：把 TCP 搬上 UDP

- QUIC（RFC 9000 系）：传输层协议，跑在 UDP 上，Google 发起，HTTP/3 的底座
- 为什么：TCP 在操作系统内核里，**升级慢**（部署新算法要等 OS/中间件）；QUIC 在用户态，随应用发布迭代
- 关键改进：
  - **连接迁移**：连接 ID 不绑 IP 四元组，WiFi→蜂窝切换不断连（移动网络杀手级）
  - **0-RTT/1-RTT 握手**（TLS 1.3 内嵌，衔接第四十七轮）
  - **多路复用无队头阻塞**：TCP 一个流丢包阻塞整连接；QUIC 流独立（HTTP/2 队头阻塞的根治）
  - 用户态可控：自研拥塞控制、丢包恢复（RFC 9002：NewReno 基准 + 可插拔）
- 对 C++ 工程师：QUIC 是"协议栈用户态化"的样板——衔接第二十六轮 io_uring/用户态网络

## 六、Linux 内核协议栈路径

```
应用 send() → 系统调用 → socket 层 → TCP 层（序列号/窗口/重传/拥塞控制）
  → IP 层（路由/分片）→ 网络设备层（驱动/NAPI）→ NIC
收包：中断 → NAPI 轮询 → 协议栈逐层上送 → 应用 recv()
```

- 内核协议栈的每层都有对应 proc/sysctl 可观测：/proc/net/tcp、ss -i（cwnd/rtt）、netstat -s
- 高吞吐调优点：NAPI、GRO/GSO（合并包）、RPS/RFS（多队列）、零拷贝（splice、io_uring）
- 与第二十六轮衔接：epoll/io_uring 是应用侧，协议栈处理在内核

- **来源**：综合 + 与 26 轮衔接
- **可信度**：A+

---

## 七、知识网络

```
TCP
├── 连接：三次握手、四次挥手、状态机、TIME_WAIT
├── 可靠：序列号/ACK/重传（RTO/快速重传/SACK）、流量控制 rwnd
├── 拥塞控制
│   ├── AIMD（公平收敛）、慢启动（ssthresh）
│   ├── CUBIC（三次函数、RTT 无关）
│   ├── BBR（带宽×RTT 建模、丢包 vs 延迟）
│   └── ECN、bufferbloat、fq
├── QUIC（UDP 用户态、连接迁移、无队头阻塞、0-RTT）
└── 内核协议栈（NAPI/GRO/sysctl/ss 观测）
```

---

## 八、本轮最重要的资料

1. **RFC 9438（CUBIC）**（S）——Linux 默认算法权威
2. **IETF BBR draft（CCWG）**（S）——模型驱动范式
3. **RFC 9002（QUIC 丢包恢复）**（S）——用户态传输
4. **theinternetpapers TCP 解剖**（A+）——握手/ISN 教学
5. **dmccreary 传输层**（A）——Reno→CUBIC 演进

## 九、适合进入 CPP-Bible 的原子

- "拥塞控制：无中央协调的公平分布式算法"（NET/DIST，与 29 轮共识对照：都在无协调下保证性质）
- "CUBIC vs BBR：丢包信号与延迟信号之争"（NET/ALGO）
- "TIME_WAIT 与 CLOSE_WAIT：服务器故障的第一现场"（NET 工程排查）
- "QUIC：为什么把 TCP 搬上 UDP"（NET/ENG 演进案例）
- 实验：ss -i 观察 cwnd/rtt、iperf3 测吞吐、netstat -s 看重传——全部本机可跑

## 十、与已有调研的关联

- 第二十六轮网络 IO：应用侧 epoll/io_uring，本轮是传输协议层
- 第四十七轮密码学：TLS 1.3 跑在 TCP/QUIC 上
- 第二十九轮分布式：共识在可靠传输之上，TCP 保证可靠性
- 第三十轮文件系统：网络文件系统依赖 TCP 可靠性
- 第四十三轮（数据库）：客户端-服务端网络栈

## 十一、下一轮方向

游戏引擎架构（ECS/渲染循环）或嵌入式/RTOS。

---

*本轮新增知识节点：TCP、三次握手、四次挥手、状态机、TIME_WAIT、CLOSE_WAIT、ISN、SYN flood、SYN cookie、序列号、累积确认、SACK、快速重传、RTO、流量控制、rwnd、拥塞窗口、cwnd、AIMD、慢启动、ssthresh、拥塞避免、CUBIC、BBR、BDP、bufferbloat、ECN、fq、HyStart、RTT、丢包恢复、QUIC、HTTP/3、连接迁移、队头阻塞、NAPI、GRO、GSO、RPS、RFS、/proc/net/tcp、ss、iperf3。补齐了"传输层/拥塞控制"域核心空白。*
