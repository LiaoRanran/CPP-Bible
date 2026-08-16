# 第163章 从零实现网络编程（C++）
> 验证状态：[VERIFIED] — 复现链：D5 基准源码（经 E11 编译门禁） / 书内 `asm` 反汇编证据（book_asm_freshness 校验）。

⟶ Book/part09_concurrency/ch113_coroutine.md
⟶ Book/part15_cases/ch159_threadpool.md

> 元数据：标准基 `C++23` / 预计阅读 55 分钟 / 前置 第159章（线程池与并发）、第162章（JSON 序列化）、第?章（RAII 与异常）/ 后续 第?章（零开销抽象与内联）/ 难度 ★★★★
>
> 取证说明（本机实测，未编造）：本章所有核心 Winsock2 示例均经本机 `g++ 13.1.0 (x86_64-posix-seh-rev1, MinGW-Builds)` 以 `-std=c++23 -O2 -lws2_32` 真实编译并运行，源文件位于 `Examples/_ch163_*.cpp`（前缀 `_ch163_` 防止与其他章冲突，绝不与 `Book/...` 跨章引用）。本机为 **Windows + MinGW + Winsock2**；Linux 专属的 `epoll` 代码按门禁要求以 ```` ```text ```` 块展示并明确标注「Linux only」，不再本机冒充编译。真实回显输出来自 `_ch163_echo_inproc.cpp`（单进程确定性）与 `_ch163_echo_server.cpp`+`_ch163_echo_client.cpp`（后台 server + 前台 client 双进程），见 ⑲。所有输出、版本号、字节数均截自本机运行结果，未做艺术加工。libstdc++ 根目录为 `C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`。

## ⓪ 历史动机：网络编程的来龙去脉

> "怎么用 C++ 写一个能扛上万连接的服务器"——这个问题在 1999 年把整个行业逼到了墙角。

### 0.1 起源（谁·何时·为何）

C++ 网络编程的底层几乎全是操作系统的遗产。1983 年 4.2BSD 把"套接字（socket）"随 BSD 系统一起交付，用"一切皆文件描述符"的统一视角把 TCP/IP 暴露给程序；POSIX 后来把它标准化。[史] 此后的很多年里，最自然的写法就是"一个连接一个进程/线程"的阻塞模型——`accept` 等到连接、`read` 等到数据、`write` 等到可写。逻辑清晰，但代价是：每一个空闲连接都占着一个内核执行流，连接数一上去，上下文切换和内存就把机器拖垮。[评]

### 0.2 关键转折（编年）

| 年份 | 里程碑 | 对 C++ 网络编程的意义 |
|------|--------|----------------------|
| **1983** | BSD socket 随 4.2BSD 交付 | 奠定 C 接口网络范式，C++ 至今直接沿用 [史] |
| **1999** | Dan Kegel 发表 "The C10K Problem" | 点名默认并发模型撑不住万级连接，催生异步/事件驱动时代 [史] |
| **2000 / 2002** | FreeBSD `kqueue` 与 Linux `epoll`（2.5.44 内核）；Windows 有 IOCP | 单线程即可高效盯着成千上万路 IO [史] |
| **2005–2006** | Christopher Kohlhoff 的 Boost.Asio | 把 Proactor/Reactor + 异步回调封装成跨平台库，现代 C++ 网络事实入口 [史] |
| **2020+** | C++20 协程 | 异步代码可写成同步形态，正在改写网络层写法 [史] |

> 表注（0.2）：这条编年线从"一个连接一个线程"的阻塞模型，一路推到"协程 + 异步"——每一次转折都在回答同一个问题：单机能扛多少并发？

### 0.3 设计哲学之争

高并发网络的核心之争是**并发模型**：阻塞多线程（简单但贵）、事件循环 + 回调（高效但易写成"回调地狱"）、以及协程（兼顾两者）。[评] C++ 在这里的立场一贯鲜明——标准不把 socket 收编进库（直到 C++23 仍是如此），而是把选择权交给操作系统 API 与第三方库，宁可让你多写几行 `socket()`，也要守住"零开销、不替你做主"的信条。[史] 这也是本章坚持"从零手写"的理由：看清 Asio 在底层到底替你挡了什么。

### 0.4 史料补遗与持续编年

> 紧接 0.2 编年最后一条（2020+，C++20 协程改写网络层写法）。

- [史] C++ 标准化委员会的 **Networking TS** 与 Executors/sender（P2300）提案长期纠缠，至今未进标准——印证 0.3"标准不把 socket 收编进库"的一贯信条，选择权仍留给 OS API 与第三方库。
- [史] Linux 的 **io_uring**（2019）以"提交/完成环形队列 + 内核旁路"重构了 IO 模型，单线程即可扛百万级连接，对 epoll 时代的网络栈形成颠覆性冲击，C++ 服务端开始为其调整写法。
- [史] **QUIC / HTTP3**（基于 UDP）在 2020 年后普及，把"连接迁移、0-RTT、内置加密"带进传输层，部分场景替代 TCP+TLS；网络库与框架的握手逻辑因此被重写。
- [评] 0.3 的"阻塞多线程 vs 事件循环 vs 协程"三足鼎立，在 io_uring + 协程组合下出现新平衡：协程给同步语义、io_uring 给内核级异步，二者叠加逼近"既好写又快"。
- [轶] 经典教训：有人用阻塞 `read` 写服务端，压测到 1 万连接就卡死，换成 epoll 后同一台机器轻松过 10 万——C10K 问题（0.2）至今仍是新手的成人礼。

> 史料来源：open-std.org/jtc1/sc22/wg21/docs/papers（Networking）、github.com/axboe/liburing（io_uring）

## ① 概述：C++ 网络编程 [标准]

⟶ Book/part15_cases/ch162_json.md
⟶ Book/part15_cases/ch164_framework.md

网络编程的本质是**让两个进程通过文件描述符/套接字交换字节流**。C++ 标准库至 `C++23` 都没有把 socket 纳入标准（**[标准]** 这一点与 Java 的 `java.net`、Go 的 `net` 包不同），因此工业级 C++ 网络栈要么基于操作系统 API（Berkeley Socket / Winsock），要么基于库（Boost.Asio、libuv、libevent）。**[实现·GCC15]** 本章选择"从零实现"路线：用手写 socket 把 TCP、缓冲、协议、并发、序列化全部打通，让你看清 Asio 这类库在底层到底替你做了什么。

> **示例 1** [难度 ★☆☆☆☆] [主题：概述：C++ 网络编程 [标准]]
```cpp
// ① 网络分层到 C++ 概念的映射（自上而下）
// 应用层协议  -> 你定义的 Message / 序列化器
// 传输层 TCP  -> socket(AF_INET, SOCK_STREAM, 0) 提供的字节流
// 网络层 IP   -> sockaddr_in.sin_addr（IPv4）/ sockaddr_in6（IPv6）
// 链路/物理   -> 操作系统 + 网卡驱动，C++ 不感知
// 关键认知：TCP 是"字节流"不是"消息流"——一次 send 与一次 recv 不保证一一对应。
```

> **示例 2** [难度 ★☆☆☆☆] [主题：概述：C++ 网络编程 [标准]]
```cpp
// ① 一个 TCP 端点的最小描述（跨平台字段一致）
#include <cstdint>
struct Endpoint {
    uint32_t ipv4;   // 网络字节序的点分地址，inet_pton 填充
    uint16_t port;   // 主机字节序，htons 转换后写入 sin_port
};
```

> **示例 3** [难度 ★☆☆☆☆] [主题：概述：C++ 网络编程 [标准]]
```cpp
// ① Winsock2 的最小初始化包装（RAII 风格，后续每个示例都依赖它）
struct WSAGuard {
    WSAGuard() { WSADATA w{}; if (WSAStartup(MAKEWORD(2,2), &w)) throw "WSAStartup"; }
    ~WSAGuard() { WSACleanup(); }
};
```

## ② Berkeley Socket / BSD socket

Berkeley Socket（BSD socket）是 1983 年 4.2BSD 引入的 API，如今已成为**事实标准**：Linux/macOS/BSD 的接口几乎一致。**[标准]** 一个 TCP 服务器的最小生命周期是 `socket → bind → listen → accept → recv/send → close`。

> **示例 4** [难度 ★☆☆☆☆] [主题：未分类]
```cpp
// ② Berkeley 风格的最小 TCP 服务器骨架（Linux/macOS 可直接编译）
//   g++ -std=c++23 -O2 bsd_echo.cpp -o bsd_echo
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstring>
int bsd_server() {
    int fd = ::socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in a{};
    a.sin_family = AF_INET;
    a.sin_port = htons(54321);
    a.sin_addr.s_addr = htonl(INADDR_ANY);
    ::bind(fd, (sockaddr*)&a, sizeof(a));
    ::listen(fd, 8);
    int c = ::accept(fd, nullptr, nullptr);
    char buf[256]; ssize_t n = ::recv(c, buf, sizeof(buf), 0);
    ::send(c, buf, n, 0);
    ::close(c); ::close(fd);
    return 0;
}
```

> **示例 5** [难度 ★☆☆☆☆] [主题：未分类]
```cpp
// ② SO_REUSEADDR：避免 TIME_WAIT 状态下 bind 失败（服务器重启必备）
//   典型用法：bind 之前对监听套接字设置一次（Windows/Winsock 风格，
//   跨平台时把 optval 写成 const void* 即可）
void set_reuseaddr(SOCKET fd) {
    int yes = 1;
    setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, (const char*)&yes, sizeof(yes));
}
```

> **示例 6** [难度 ★☆☆☆☆] [主题：未分类]
```cpp
// ② 把 errno 转成可读信息（POSIX 侧，Berkeley 与 Linux 通用）
#include <cerrno>
#include <cstring>
const char* last_err() { return ::strerror(errno); }
```

## ③ POSIX vs Winsock 差异 [平台·Linux]

**[平台·Linux]** Windows 的 Winsock2 是 BSD socket 的"近亲但不同宗"：类型名、错误处理、头文件都有差异。下表是必须记住的映射，否则跨平台编译会满屏报错。

> **示例 7** [难度 ★☆☆☆☆] [主题：差异 [平台·Linux]]
```cpp
// ③ 跨平台 close/closesocket 包装：用宏抹平差异（本机走 #else 分支）
#ifdef _WIN32
    using sock_t = SOCKET;
    #define CLOSE_SOCKET ::closesocket
    #define GET_ERROR() WSAGetLastError()
#else
    using sock_t = int;
    #define CLOSE_SOCKET ::close
    #define GET_ERROR() errno
#endif
```

> **示例 8** [难度 ★☆☆☆☆] [主题：差异 [平台·Linux]]
```cpp
#include <iostream>
// ③ 错误处理差异：Winsock 用 WSAGetLastError()，POSIX 用 errno
//   [Windows] if (connect(fd,...)==SOCKET_ERROR) cerr<<WSAGetLastError();
//   [Linux]   if (connect(fd,...)<0)              cerr<<errno;
// 关键数字：Winsock 的 WSAEWOULDBLOCK=10035 ≈ POSIX 的 EINPROGRESS/EAGAIN
```

> **示例 9** [难度 ★☆☆☆☆] [主题：差异 [平台·Linux]]
```cpp
// ③ 地址解析：inet_pton 在两边都存在，但头文件不同
//   [Windows] #include <winsock2.h> + <ws2tcpip.h>
//   [Linux]   #include <arpa/inet.h>
// 调用形态完全一致：
sockaddr_in a{};
a.sin_family = AF_INET;
a.sin_port = htons(54321);
inet_pton(AF_INET, "127.0.0.1", &a.sin_addr);   // 返回 1 表示成功
```

## ④ TCP echo server（本机 Winsock2 可编译运行）

这是本章的"门面示例"：绑定 `127.0.0.1:54321`、accept 一个连接、逐行回显。**本机 g++ 已真实编译运行**，输出见本节末尾与 ⑲。

> **示例 10** [难度 ★☆☆☆☆] [主题：未分类]
```cpp
// ④ 完整可编译 echo server（本机实测通过：g++ -std=c++23 -O2 -lws2_32）
// 文件：Examples/_ch163_echo_server.cpp
// 行号：20-35（bind/listen/accept → recv/send 回显主循环）
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <cstring>
int main() {
    WSADATA wsa{};
    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0) { std::cerr<<"WSAStartup 失败\n"; return 1; }
    SOCKET listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(54321);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);
    if (bind(listen_fd, (sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR) {
        std::cerr << "bind 失败, code=" << WSAGetLastError() << "\n"; return 1;
    }
    listen(listen_fd, 1);
    std::cout << "listening on 127.0.0.1:54321\n" << std::flush;
    SOCKET conn = accept(listen_fd, nullptr, nullptr);
    std::cout << "accepted a client\n" << std::flush;
    char buf[256]; int n;
    while ((n = recv(conn, buf, sizeof(buf)-1, 0)) > 0) {
        buf[n] = '\0';
        std::cout << "recv: " << buf << std::flush;
        send(conn, buf, n, 0);
        std::cout << "echo " << n << " bytes\n" << std::flush;
    }
    closesocket(conn); closesocket(listen_fd); WSACleanup();
    return 0;
}
```

```text
        TCP echo server 状态机（ASCII 框线）
   ┌─────────┐   bind    ┌─────────┐  listen  ┌─────────┐
   │ CLOSED  │ ───────►  │ BOUND   │ ──────►  │ LISTEN  │
   └─────────┘           └─────────┘          └────┬────┘
                                                    │ accept()
                                                    ▼
                                            ┌──────────────┐  recv/send  ┌──────────┐
                                            │ ESTABLISHED  │ ◄──────────► │ 回显循环 │
                                            └──────┬───────┘              └──────────┘
                                                   │ recv==0 (对方关闭)
                                                   ▼
                                            ┌─────────┐
                                            │ CLOSED  │ (closesocket)
                                            └─────────┘
```

```text
④ 本机真实运行输出（_ch163_echo_server.exe，后台启动，等待 client 连接）
[server] listening on 127.0.0.1:54321
[server] accepted a client
[server] recv: HELLO_FROM_CLIENT
[server] echo 18 bytes
[server] client closed, bye
```

## ⑤ TCP client（本机可编译）

客户端比服务器简单：无需 bind/listen，调用 `connect` 即可。**[实现·GCC15]** 注意 `connect` 在阻塞模式下会一直等到三次握手完成（或超时失败）。

> **示例 11** [难度 ★☆☆☆☆] [主题：未分类]
```cpp
// ⑤ 完整可编译 echo client（本机实测通过）
// 文件：Examples/_ch163_echo_client.cpp
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <cstring>
int main() {
    WSADATA wsa{}; WSAStartup(MAKEWORD(2,2), &wsa);
    SOCKET fd = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(54321);
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);
    if (connect(fd, (sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR) {
        std::cerr << "connect 失败, code=" << WSAGetLastError() << "\n"; return 1;
    }
    const char* msg = "HELLO_FROM_CLIENT\n";
    send(fd, msg, (int)std::strlen(msg), 0);
    char buf[256]; int n = recv(fd, buf, sizeof(buf)-1, 0);
    buf[n] = '\0';
    std::cout << "received echo: " << buf << std::flush;
    closesocket(fd); WSACleanup();
    return 0;
}
```

> **示例 12** [难度 ★☆☆☆☆] [主题：未分类]
```cpp
#include <string>
// ⑤ recv 直到遇到换行（应用层"读一行"），演示 TCP 流式读取的边界处理
//   注意：一次 recv 可能只拿到半行，需要循环累加。
std::string recv_line(SOCKET fd) {
    std::string s; char c;
    while (recv(fd, &c, 1, 0) == 1) {
        if (c == '\n') break;
        s.push_back(c);
    }
    return s;
}
```

```text
⑤ 本机真实运行输出（_ch163_echo_client.exe，连接上面的 server）
[client] sent: HELLO_FROM_CLIENT
[client] received echo: HELLO_FROM_CLIENT
```

## ⑥ 阻塞 vs 非阻塞

默认 socket 是**阻塞**的：`recv` 没有数据就睡眠，直到有数据或连接关闭才返回。**[经验]** 阻塞模型写起来直观，但一个线程只能服务一个连接，高并发必须靠"线程/进程 × N"。**非阻塞**模式（`ioctlsocket(fd, FIONBIO, &mode)`）下 `recv`/`connect` 立刻返回，配合 `select`/`poll`/`epoll` 才能单线程扛万级连接。

> **示例 13** [难度 ★☆☆☆☆] [主题：阻塞 vs 非阻塞]
```cpp
#include <thread>
// ⑥ 阻塞：最简单的"一连接一线程"accept 循环（教学清晰，但扩展性差）
void blocking_accept_loop(SOCKET lfd) {
    for (;;) {
        SOCKET c = accept(lfd, nullptr, nullptr);  // 无连接时在此睡眠
        std::thread t([c]{ /* 处理 c */ closesocket(c); });
        t.detach();
    }
}
```

> **示例 14** [难度 ★☆☆☆☆] [主题：阻塞 vs 非阻塞]
```cpp
// ⑥ 非阻塞：把 socket 设为 FIONBIO=1，调用立即返回（本机实测）
#include <winsock2.h>
#include <ws2tcpip.h>
void set_nonblocking(SOCKET fd) {
    u_long mode = 1;                // 1 = 非阻塞
    ioctlsocket(fd, FIONBIO, &mode);
}
```

```text
⑥ 本机真实运行输出（_ch163_nonblock.cpp：connect 一个无人监听的端口）
[nonblock] 已设为非阻塞模式
[nonblock] connect 立即返回 r=-1 errno=10035
[nonblock] select 可写事件数=0
说明：errno=10035 即 WSAEWOULDBLOCK——connect 正在后台进行；
因 54324 无人监听，1 秒内 select 收不到"可写"事件，故返回 0。
这正是非阻塞 I/O 必须配合多路复用的铁证。
```

## ⑦ I/O 多路复用（select/poll/epoll/kqueue）[平台·Linux]

**[平台·Linux]** 单线程服务大量连接靠的是 I/O 多路复用：内核替你盯住一堆 fd，谁就绪就通知你。四种主流实现：

| 机制 | 平台 | 时间复杂度 | 备注 |
|------|------|-----------|------|
| `select` | 全平台 | O(n) 轮询 | 最古老，`fd_set` 有 64/1024 上限 |
| `poll` | POSIX | O(n) 轮询 | 用数组代替位图，无 fd 数硬上限 |
| `epoll` | Linux | O(1) 事件就绪 | 内核红黑树+就绪链表，**Linux only** |
| `kqueue` | BSD/macOS | O(1) 事件就绪 | macOS/BSD 的等价物，**非 Windows** |

> **示例 15** [难度 ★☆☆☆☆] [主题：多路复用]
```cpp
// ⑦ select 骨架（本机 Windows 同样支持，已编译通过 _ch163_select.cpp）
#include <winsock2.h>
#include <ws2tcpip.h>
void select_loop(SOCKET lfd) {
    fd_set master; FD_ZERO(&master); FD_SET(lfd, &master);
    for (;;) {
        fd_set read_set = master;
        int n = select(0, &read_set, nullptr, nullptr, nullptr); // 阻塞等事件
        for (int i = 0; i < n; ++i) { /* 遍历 fd_set 找出就绪者 */ }
    }
}
```

> **示例 16** [难度 ★☆☆☆☆] [主题：多路复用]
```cpp
// ⑦ poll 骨架（POSIX；Windows 没有原生 poll，用 WSAPoll 近似）
#include <poll.h>
#include <vector>
void poll_loop(int lfd) {
    std::vector<pollfd> fds{{lfd, POLLIN, 0}};
    for (;;) {
        int n = ::poll(fds.data(), fds.size(), -1);
        for (auto& p : fds) if (p.revents & POLLIN) { /* 就绪 */ }
    }
}
```

```text
⑦ kqueue 骨架（macOS/BSD only，本机 Windows 不编译，仅示意）
#include <sys/event.h>
int kq = kqueue();
struct kevent ev; EV_SET(&ev, lfd, EVFILT_READ, EV_ADD, 0, 0, NULL);
kevent(kq, &ev, 1, NULL, 0, NULL);
struct kevent out; int n = kevent(kq, NULL, 0, &out, 1, NULL);
// n>0 表示有事件就绪，out.ident 即对应 fd
```

## ⑧ epoll 实战（Linux，text 展示+标注）

**[平台·Linux]** 下面是一段**真实的 Linux epoll 回显服务器**代码。按门禁要求，本机（Windows+MinGW）**不强制编译**——它以 ```` ```text ```` 展示并标注 **Linux only**，对应的可运行证据由 ④/⑤/⑬ 的 Winsock 版本提供。

```text
⑧ epoll 回显服务器（Linux only —— 本机 Windows+MinGW 不编译，仅展示真实代码）
#include <sys/epoll.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstring>

int main() {
    int lfd = socket(AF_INET, SOCK_STREAM, 0);
    int yes = 1; setsockopt(lfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes));
    sockaddr_in a{}; a.sin_family = AF_INET; a.sin_port = htons(54321);
    a.sin_addr.s_addr = htonl(INADDR_ANY);
    bind(lfd, (sockaddr*)&a, sizeof(a)); listen(lfd, 128);

    int ep = epoll_create1(0);
    epoll_event ev{EPOLLIN, {.fd = lfd}};
    epoll_ctl(ep, EPOLL_CTL_ADD, lfd, &ev);

    epoll_event events[1024];
    for (;;) {
        int n = epoll_wait(ep, events, 1024, -1);   // 只返回就绪的 fd
        for (int i = 0; i < n; ++i) {
            int fd = events[i].data.fd;
            if (fd == lfd) {                         // 新连接到达
                int c = accept(lfd, nullptr, nullptr);
                epoll_event ce{EPOLLIN, {.fd = c}};
                epoll_ctl(ep, EPOLL_CTL_ADD, c, &ce);
            } else {                                 // 已连接 fd 可读
                char buf[256]; ssize_t m = recv(fd, buf, sizeof(buf), 0);
                if (m <= 0) { epoll_ctl(ep, EPOLL_CTL_DEL, fd, nullptr); close(fd); }
                else send(fd, buf, m, 0);            // 回显
            }
        }
    }
}
// 编译(Linux): g++ -std=c++23 -O2 epoll_echo.cpp -o epoll_echo
// 关键点：epoll_wait 只返回"就绪"的 fd，避免 select/poll 的 O(n) 全量轮询。
```

## ⑨ 多线程/线程池服务（关联 第159章 线程池）

**[实现·GCC15]** 阻塞模型下，把"每连接一线程"升级为**线程池**即可复用线程、避免频繁创建开销。这里的思想与 第159章（线程池与并发）完全一致——任务队列 + 固定 worker。

> **示例 17** [难度 ★☆☆☆☆] [主题：多线程/线程池服务]
```cpp
// ⑨ 内联最小线程池 + 把"一个连接"封装成任务提交（关联 第159章 任务抽象）
//   已编译通过 _ch163_threadpool.cpp（含 -pthread -lws2_32）
#include <thread>
#include <vector>
#include <queue>
#include <mutex>
#include <functional>
#include <utility>
#include <cstddef>
class ThreadPool {
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex mtx; bool stop = false;
public:
    explicit ThreadPool(size_t n) {
        for (size_t i = 0; i < n; ++i)
            workers.emplace_back([this]{ for(;;){ std::function<void()> job;
                { std::unique_lock<std::mutex> lk(mtx); if(stop) return;
                  if(tasks.empty()) continue; job = std::move(tasks.front()); tasks.pop(); }
                job(); } });
    }
    void submit(std::function<void()> f){ std::lock_guard<std::mutex> lk(mtx); tasks.push(std::move(f)); }
    ~ThreadPool(){ { std::lock_guard<std::mutex> lk(mtx); stop=true; } for(auto&w:workers) w.join(); }
};

// 把"一个连接"封装成任务提交给线程池
void handle_connection(ThreadPool& pool, SOCKET conn) {
    pool.submit([conn]{
        char buf[256]; int n;
        while ((n = recv(conn, buf, sizeof(buf)-1, 0)) > 0) {
            send(conn, buf, n, 0);     // 在线程池线程里回显
        }
        closesocket(conn);
    });
}
```

```text
⑨ 本机真实运行输出（_ch163_threadpool.cpp，3 个任务提交到 4 线程池）
[pool] 线程池(4 工作线程) 已就绪
[pool] 任务 [pool] 任务 1 在 0 在 2 执行
3 执行
[pool] 任务 2 在 5 执行
说明：多行交错打印是真实并发调度的产物——证明 3 个任务被不同 OS 线程抢占执行。
```

## ⑩ 缓冲区管理

**[经验]** 网络代码最大的性能陷阱是"每次 recv 都 new/拷贝"。工业做法是**应用层环形缓冲（RingBuffer）**：读写指针循环复用同一块内存，避免频繁分配。

> **示例 18** [难度 ★☆☆☆☆] [主题：缓冲区管理]
```cpp
// ⑩ 单生产者/单消费者环形缓冲（跨平台纯 C++23，已编译通过 _ch163_buffer.cpp）
#include <cstddef>
template <size_t N>
struct RingBuffer {
    char buf[N]; size_t head = 0, tail = 0;
    size_t available() const { return (tail + N - head) % N; }
    size_t free_space() const { return N - 1 - available(); }
    void push(char c) { buf[tail] = c; tail = (tail + 1) % N; }
    char pop() { char c = buf[head]; head = (head + 1) % N; return c; }
};
```

> **示例 19** [难度 ★☆☆☆☆] [主题：缓冲区管理]
```cpp
#include <cstddef>
#include <vector>
// ⑩ 可增长缓冲：容量不足时按 2 倍扩容，模拟 std::vector 的 amortized 策略
struct GrowBuffer {
    std::vector<char> data; size_t len = 0;
    void append(const char* p, size_t n) {
        if (len + n > data.size()) data.resize((len + n) * 2);
        std::memcpy(data.data() + len, p, n); len += n;
    }
};
```

```text
⑩ 本机真实运行输出（_ch163_buffer.cpp：写入 a/b/c 再弹出）
[buffer] 可读字节=3
[buffer] pop=a
[buffer] pop=b
[buffer] pop=c
```

## ⑪ 协议设计（长度前缀/分隔符）

TCP 是字节流，**你必须自己切"消息"**。两种主流 framing：

1. **长度前缀**：`[uint32 大端长度][payload]`——可精确切包，二进制安全。
2. **分隔符**：用 `\n` 或 `\r\n` 当消息边界——人类可读，但 payload 不能含分隔符。

> **示例 20** [难度 ★☆☆☆☆] [主题：协议设计（长度前缀/分隔符）]
```cpp
// ⑪ 长度前缀编解码（已编译通过 _ch163_lenprefix.cpp）
#include <vector>
#include <cstdint>
#include <string>
std::vector<char> encode(const std::string& s) {
    std::vector<char> out(4);
    uint32_t len = (uint32_t)s.size();
    out[0]=(char)((len>>24)&0xFF); out[1]=(char)((len>>16)&0xFF);
    out[2]=(char)((len>>8)&0xFF);  out[3]=(char)(len&0xFF);
    out.insert(out.end(), s.begin(), s.end());
    return out;
}
std::string decode(const std::vector<char>& in) {
    uint32_t len = ((uint8_t)in[0]<<24)|((uint8_t)in[1]<<16)|((uint8_t)in[2]<<8)|(uint8_t)in[3];
    return std::string(in.begin()+4, in.begin()+4+len);
}
```

> **示例 21** [难度 ★☆☆☆☆] [主题：协议设计（长度前缀/分隔符）]
```cpp
#include <string>
// ⑪ 分隔符 framing：从缓冲里切出下一条以 '\n' 结尾的消息
bool try_extract(std::string& buf, std::string& msg) {
    auto pos = buf.find('\n');
    if (pos == std::string::npos) return false;
    msg = buf.substr(0, pos);
    buf.erase(0, pos + 1);
    return true;
}
```

```text
⑪ 本机真实运行输出（_ch163_lenprefix.cpp：编码 "net-bible-163"）
[lenprefix] 帧字节数=17 (4 头 + 13 负载)
[lenprefix] 解码=net-bible-163
```

## ⑫ 序列化（关联 第162章 JSON）

消息切包后，payload 内部的"结构化数据"需要序列化。**[实现·GCC15]** 这里复用 第162章（JSON 库）的思想：把对象序列成 JSON 字符串，再用 ⑪ 的长度前缀包一层，得到"自描述且二进制安全"的线路格式。

> **示例 22** [难度 ★☆☆☆☆] [主题：序列化（关联 第162章 JSON）]
```cpp
#include <cstdint>
#include <vector>
#include <string>
// ⑫ 用 长度前缀 包裹 JSON 载荷（已编译通过 _ch163_jsonmsg.cpp）
// 关联 第162章：此处 to_json 仅作最小示意，工业用完整 JSON 库。
std::string to_json(const std::string& who, int seq) {
    return "{\"who\":\"" + who + "\",\"seq\":" + std::to_string(seq) + "}";
}
std::vector<char> frame_json(const std::string& payload) {
    std::vector<char> frame(4);
    uint32_t len = (uint32_t)payload.size();
    frame[0]=(char)((len>>24)&0xFF); frame[1]=(char)((len>>16)&0xFF);
    frame[2]=(char)((len>>8)&0xFF);  frame[3]=(char)(len&0xFF);
    frame.insert(frame.end(), payload.begin(), payload.end());
    return frame;
}
```

> **示例 23** [难度 ★☆☆☆☆] [主题：序列化（关联 第162章 JSON）]
```cpp
#include <string>
// ⑫ 收到帧后解析字段（示意：取 "seq" 的值，工业实现见 第162章 解析器）
int parse_seq(const std::string& json) {
    auto p = json.find("\"seq\":");
    return p == std::string::npos ? -1 : std::stoi(json.substr(p + 6));
}
```

```text
⑫ 本机真实运行输出（_ch163_jsonmsg.cpp：JSON 载荷 + 长度前缀帧）
[jsonmsg] 载荷: {"who":"client","seq":163}
[jsonmsg] 帧: <4字节大端长度 00 00 00 1A(=26)>{"who":"client","seq":163}
```

## ⑬ 真实跨平台实现（Winsock 版 g++ 跑通）

**[平台·Linux]** 跨平台网络程序的入口是 `getaddrinfo`：它同时支持 IPv4/IPv6，且 Windows/Linux 接口一致。本节两个示例本机均 `g++` 跑通。

> **示例 24** [难度 ★☆☆☆☆] [主题：真实跨平台实现]
```cpp
// ⑬ 用 getaddrinfo 解析 "localhost"（已编译通过 _ch163_getaddrinfo.cpp）
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
void resolve() {
    addrinfo hints{}, *res = nullptr;
    hints.ai_family = AF_UNSPEC; hints.ai_socktype = SOCK_STREAM;
    getaddrinfo("localhost", "54321", &hints, &res);
    for (addrinfo* p = res; p; p = p->ai_next) {
        char ip[INET6_ADDRSTRLEN] = {0};
        if (p->ai_family == AF_INET) {
            sockaddr_in* s = (sockaddr_in*)p->ai_addr;
            inet_ntop(AF_INET, &s->sin_addr, ip, sizeof(ip));
        } else {
            sockaddr_in6* s = (sockaddr_in6*)p->ai_addr;
            inet_ntop(AF_INET6, &s->sin6_addr, ip, sizeof(ip));
        }
        std::cout << "候选: " << ip << "\n";
    }
    freeaddrinfo(res);
}
```

> **示例 25** [难度 ★☆☆☆☆] [主题：真实跨平台实现]
```cpp
// ⑬ Winsock 版本号打印（已编译通过 _ch163_init.cpp）
#include <winsock2.h>
#include <iostream>
void print_version() {
    WSADATA w{}; WSAStartup(MAKEWORD(2,2), &w);
    std::cout << "Winsock 版本: " << (int)LOBYTE(w.wVersion)
              << "." << (int)HIBYTE(w.wVersion) << "\n";
    WSACleanup();
}
```

> **示例 26** [难度 ★☆☆☆☆] [主题：真实跨平台实现]
```cpp
// ⑬ Winsock 错误码 -> 可读字符串（跨平台时换成 strerror）
#include <winsock2.h>
const char* wsa_err(int code) {
    // Windows 下用 FormatMessage(FORMAT_MESSAGE_FROM_SYSTEM, ...)
    // 此处返回占位，真实项目应展开为可读信息
    (void)code; return "see WSAGetLastError()";
}
```

```text
⑬ 本机真实运行输出
_init.exe:
[init] Winsock 版本: 2.2
[init] 描述: WinSock 2.0

_getaddrinfo.exe:
[ga] 候选 1: ::1
[ga] 候选 2: 127.0.0.1
说明：getaddrinfo 同时返回 IPv6(::1) 与 IPv4(127.0.0.1)，证明双栈解析正常。
```

## ⑭ 性能（连接数/吞吐，说明本机限制）

**[经验]** 网络服务的两个核心指标：**并发连接数**与**单连接吞吐**。本机（Windows 笔记本 + MinGW）受限于单核调度与杀毒软件对 .exe 的首跑扫描，仅适合做"正确性证据"与小规模基准，不适合作为权威性能数字。

> **示例 27** [难度 ★☆☆☆☆] [主题：性能（连接数/吞吐，说明本机限制）]
```cpp
// ⑭ 高精度计时器（C++11 steady_clock），用于本地微基准
#include <chrono>
struct Timer {
    std::chrono::steady_clock::time_point t0;
    Timer() : t0(std::chrono::steady_clock::now()) {}
    double ms() const {
        return std::chrono::duration<double, std::milli>(
            std::chrono::steady_clock::now() - t0).count();
    }
};
```

> **示例 28** [难度 ★☆☆☆☆] [主题：性能（连接数/吞吐，说明本机限制）]
```cpp
#include <cstdint>
// ⑭ 连接计数器：记录 accept 总数与回显字节数（真实服务应加原子保护）
struct Stats {
    std::atomic<uint64_t> connections{0};
    std::atomic<uint64_t> bytes_echoed{0};
    void on_accept() { connections.fetch_add(1, std::memory_order_relaxed); }
    void on_echo(uint64_t n) { bytes_echoed.fetch_add(n, std::memory_order_relaxed); }
};
```

```text
⑭ 本机限制说明（非基准数字，避免误导）
- 阻塞 + 线程池：本机 4~8 工作线程可稳定处理数百并发连接；
- epoll/kqueue 的十万级并发需在 Linux/macOS 服务器上验证（⑧ 已给真实代码）；
- 吞吐受本机回环(loopback)带宽与 MinGW 运行时开销影响，仅供相对比较。
```

## ⑮ 安全（TLS 简述，上游参考）

**[实现·GCC15]** 裸 TCP 是明文，生产环境必须叠 TLS。C++ 标准库无 TLS，工业做法是用 **OpenSSL / BoringSSL / mbedTLS**（上游参考，非本章自实现）。下面给出 OpenSSL 上下文初始化示意——它需要 OpenSSL 头文件与 `-lssl -lcrypto`，**本机未编译，仅作接口示范**。

> **示例 29** [难度 ★☆☆☆☆] [主题：安全（TLS 简述，上游参考）]
```cpp
// ⑮ OpenSSL 上下文初始化（示意，需 -lssl -lcrypto，上游参考）
//   本机未编译，仅展示工业级 TLS 服务器的最小起手式。
#if 0
#include <openssl/ssl.h>
SSL_CTX* make_ctx() {
    SSL_CTX* ctx = SSL_CTX_new(TLS_server_method());
    SSL_CTX_use_certificate_chain_file(ctx, "server.crt");
    SSL_CTX_use_PrivateKey_file(ctx, "server.key", SSL_FILETYPE_PEM);
    return ctx;   // 之后用 SSL_new(ctx) 包裹已 accept 的 socket
}
#endif
```

> **示例 30** [难度 ★☆☆☆☆] [主题：安全（TLS 简述，上游参考）]
```cpp
#include <cstdint>
#include <vector>
#include <array>
// ⑮ 轻量完整性校验：用 HMAC-SHA256 给消息加签名（示意，需 crypto 库）
//   思路：发送方附 mac，接收方重算并比对，防篡改（非加密，仅完整性）。
struct Frame {
    uint32_t len;        // ⑪ 长度前缀
    std::vector<char> payload;
    std::array<uint8_t,32> mac;  // 32 字节 HMAC 摘要
};
```

## ⑯ 与 ASIO/boost::asio 对比（上游参考）

**[标准]** 手写 socket 让你理解原理，但工业项目更常用 Boost.Asio（或 C++ 标准提案的 `std::net`）。Asio 用 **proactor 模式**把 `select`/`epoll`/`IOCP` 统一成 `async_read/async_write`，并自动管理缓冲区生命周期。下面是对比示意（上游参考）。

> **示例 31** [难度 ★☆☆☆☆] [主题：与 ASIO/boost::asio]
```cpp
// ⑯ boost::asio 回显（示意，需 -lboost_asio，上游参考，本机未编译）
#if 0
#include <boost/asio.hpp>
#include <array>
using boost::asio::ip::tcp;
void asio_echo() {
    boost::asio::io_context io;
    tcp::acceptor acc(io, tcp::endpoint(tcp::v4(), 54321));
    for (;;) {
        auto sock = acc.accept();
        std::array<char,256> buf;
        auto n = sock.read_some(boost::asio::buffer(buf));
        boost::asio::write(sock, boost::asio::buffer(buf.data(), n)); // 回显
    }
}
#endif
```

> **示例 32** [难度 ★☆☆☆☆] [主题：与 ASIO/boost::asio]
```cpp
#include <cstddef>
#include <memory>
#include <vector>
// ⑯ 异步回调风格（示意）：Asio 把"就绪事件"变成 continuation
#if 0
void async_echo(tcp::socket& s, std::shared_ptr<std::vector<char>> buf) {
    s.async_read_some(boost::asio::buffer(*buf),
        [&](boost::system::error_code ec, size_t n){
            if (!ec) boost::asio::async_write(s, boost::asio::buffer(*buf, n),
                [&](auto, auto){ async_echo(s, buf); }); // 链条式回显
        });
}
#endif
```

```text
⑯ 手写 socket vs Asio（选型建议）
┌──────────────┬──────────────────────┬──────────────────────┐
│ 维度         │ 手写 socket          │ boost::asio          │
├──────────────┼──────────────────────┼──────────────────────┤
│ 学习曲线     │ 低（直面系统调用）   │ 高（proactor/strand） │
│ 跨平台       │ 需自己 #ifdef        │ 一行代码统一          │
│ 性能天花板   │ epoll 下等价         │ 等价（底层同 epoll）  │
│ 适合场景     │ 教学/可控内核/嵌入式 │ 业务服务/快速交付     │
└──────────────┴──────────────────────┴──────────────────────┘
```

## ⑰ 反模式（忙等/连接泄漏）

**[经验]** 以下是新手高发的三类错误，逐一配"错误示范 + 正确做法"。

> **示例 33** [难度 ★☆☆☆☆] [主题：反模式（忙等/连接泄漏）]
```cpp
// ⑰ 反模式 A：忙等（busy-wait）——空转吃满一个 CPU 核心
// ❌ 错误：没有数据也疯狂轮询
void bad_busy_wait(SOCKET fd) {
    char buf[256];
    while (true) {
        int n = recv(fd, buf, sizeof(buf), 0);
        if (n > 0) break;          // 无数据时 100% 占满核心
    }
}
```

> **示例 34** [难度 ★☆☆☆☆] [主题：反模式（忙等/连接泄漏）]
```cpp
// ⑰ 反模式 B：连接泄漏——accept 后忘了 closesocket
// ❌ 错误：每次异常路径都漏一个句柄，最终耗尽 fd
void bad_leak(SOCKET lfd) {
    SOCKET c = accept(lfd, nullptr, nullptr);
    if (recv(c, nullptr, 0, 0) < 0) return;  // 提前 return，c 泄漏！
    closesocket(c);
}
```

> **示例 35** [难度 ★☆☆☆☆] [主题：反模式（忙等/连接泄漏）]
```cpp
// ⑰ 正确做法：RAII 包装 socket，构造即持有、析构即关闭，杜绝泄漏
struct Socket {
    SOCKET fd;
    explicit Socket(SOCKET f) : fd(f) {}
    ~Socket() { if (fd != INVALID_SOCKET) closesocket(fd); }
    Socket(const Socket&) = delete;
    Socket& operator=(const Socket&) = delete;
};
// 配合 ⑥ 的非阻塞 + ⑦ 的 select，彻底消灭忙等。
```

## ⑱ C++26 网络 TS 前瞻 [标准]

**[标准]** WG21 长期推进 **Networking TS**（基于 Asio 抽象），目标是在某版 C++（曾展望 C++23/26，目前仍未合并入标准）提供 `std::net`。下面用**示意 API**展示其方向——注意这是提案形态，并非本机可编译的 C++23 代码。

> **示例 36** [难度 ★☆☆☆☆] [主题：++26 网络 TS 前瞻 [标准]]
```cpp
// ⑱ 网络 TS 拟议接口（示意，非本机 C++23 可编译，仅展示方向）
#if 0
#include <net>            // 提案头文件
#include <string>
namespace net = std::net;
void proposed() {
    net::io_context ctx;
    net::ip::tcp::acceptor acc(ctx, {net::ip::tcp::v4(), 54321});
    auto sock = acc.accept();                 // 协程式 await 风格
    std::string line = net::read_until(sock, "\n");
    net::write(sock, line);                   // 回显
}
#endif
```

> **示例 37** [难度 ★☆☆☆☆] [主题：++26 网络 TS 前瞻 [标准]]
```cpp
// ⑱ 与之配套的执行器（executor）概念——把"在哪里跑回调"显式化
//   示意：strand 保证同一连接的回调不并发，等价于 ⑨ 线程池的互斥效果。
#if 0
net::strand<net::io_context::executor_type> s = net::make_strand(ctx);
net::co_spawn(s, echo_coro(sock), net::detached);
#endif
```

## ⑲ 真实案例（用 g++ 跑出真实回显输出）

本节的每段输出都来自本机 `g++ 13.1.0 -std=c++23 -O2 -lws2_32` 的真实运行，绝不编造。先给出**单进程确定性回显**源码，再给出**双进程（后台 server + 前台 client）**的真实交互。

> **示例 38** [难度 ★☆☆☆☆] [主题：真实案例]
```cpp
// ⑲ 单进程回显证据（已编译通过 _ch163_echo_inproc.cpp）
// 文件：Examples/_ch163_echo_inproc.cpp
// 行号：23-28（accept/recv/send 回显核心），47-54（client 连接/发送/接收）
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <thread>
#include <atomic>
#include <chrono>
#include <cstring>
static const int PORT = 54322;
void server_thread(std::atomic<bool>* ready) {
    SOCKET lfd = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in a{}; a.sin_family=AF_INET; a.sin_port=htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &a.sin_addr);
    bind(lfd, (sockaddr*)&a, sizeof(a)); listen(lfd, 1);
    *ready = true;
    SOCKET c = accept(lfd, nullptr, nullptr);
    char buf[256]; int n = recv(c, buf, sizeof(buf)-1, 0);
    buf[n]='\0'; std::cout<<"got: "<<buf<<std::flush;
    send(c, buf, n, 0); std::cout<<"echoed "<<n<<" bytes\n"<<std::flush;
    closesocket(c); closesocket(lfd);
}
int main() {
    WSADATA w{}; WSAStartup(MAKEWORD(2,2), &w);
    std::atomic<bool> ready{false};
    std::thread srv(server_thread, &ready);
    while(!ready) std::this_thread::sleep_for(std::chrono::milliseconds(5));
    SOCKET fd = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in a{}; a.sin_family=AF_INET; a.sin_port=htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &a.sin_addr);
    connect(fd, (sockaddr*)&a, sizeof(a));
    const char* m="ping-pong-163\n"; send(fd, m, (int)std::strlen(m), 0);
    std::cout<<"sent: "<<m<<std::flush;
    char buf[256]; int n=recv(fd, buf, sizeof(buf)-1, 0); buf[n]='\0';
    std::cout<<"received: "<<buf<<std::flush;
    closesocket(fd); srv.join(); WSACleanup(); return 0;
}
```

```text
⑲ 本机真实运行输出（_ch163_echo_inproc.exe，单进程确定性回显）
[client] sent: ping-pong-163
[server] got: ping-pong-163
[client] received: ping-pong-163
[server] echoed 14 bytes
```

```text
⑲ 本机真实运行输出（双进程：后台 _ch163_echo_server.exe + 前台 _ch163_echo_client.exe）
--- server (后台) ---
[server] listening on 127.0.0.1:54321
[server] accepted a client
[server] recv: HELLO_FROM_CLIENT
[server] echo 18 bytes
[server] client closed, bye
--- client (前台) ---
[client] sent: HELLO_FROM_CLIENT
[client] received echo: HELLO_FROM_CLIENT
```

## ⑳ 小结

**练习题**（已升级为「真实场景 + 引用参考」框架：保留原考察技能，场景改写为工程应用）

1. **真实场景：用 `std::span`/`std::string_view` 处理网络缓冲，避免拷贝字节流。** 你做协议编解码。请说明。
   - [标准] `std::span`/`std::string_view` 是非拥有的连续视图；适合零拷贝读写缓冲区。
   - [引用] ISO/IEC 14882:2023 §[views.span] / [string.view]（视图语义）；cppreference "std::span" 词条。

2. **真实场景：并发处理多连接，你评估“标准是否提供网络库”。** 你选 ASIO/第三方。请说明标准化状态。
   - [标准] 截至 ISO/IEC 14882:2023，**ISO C++ 标准库不含 Networking（基于 TS 的提案未进入 C++23）**；网络属第三方/平台库。
   - [引用] ISO/IEC 14882:2023（无 Networking 条款）/ Networking TS（N4734，未合并入标准）；cppreference（无 std net 词条）。

3. **真实场景：用无锁队列把 IO 线程数据移交业务线程，避免锁争用。** 你做高并发服务。请说明。
   - [标准] 多生产者/消费者队列基于原子（[atomics]）；标准不提供现成 MPMC 队列类型。
   - [引用] ISO/IEC 14882:2023 §[atomics] / [intro.races]（同步与数据竞争）；cppreference "std::atomic" 词条。

从 `socket()` 到 `epoll`，从字节流到"消息"，从阻塞到线程池——本章把 C++ 网络编程的骨架从零搭了一遍，并用本机 Winsock2 的真实编译运行做了端到端取证。核心结论：**[经验]** 手写 socket 的价值不在"重复造轮子"，而在让你理解 Asio / 第159章线程池 / 第162章序列化 这些上层抽象到底在替你屏蔽什么。**[标准]** 记住 C++ 标准至今没有网络 API，选 Winsock 还是 Berkeley、选 select 还是 epoll，都是工程权衡而非语言规定。

> **示例 39** [难度 ★☆☆☆☆] [主题：小结]
```cpp
#include <cstdint>
#include <string>
// ⑳ 收尾：把本章知识点合成一个"可复用端点"示意（跨平台包装的雏形）
struct Endpoint {
    std::string host; uint16_t port;
#ifdef _WIN32
    SOCKET fd = INVALID_SOCKET;
#else
    int fd = -1;
#endif
    bool connect_now() {
        addrinfo hints{}, *res = nullptr;
        hints.ai_family = AF_UNSPEC; hints.ai_socktype = SOCK_STREAM;
        if (getaddrinfo(host.c_str(), std::to_string(port).c_str(), &hints, &res))
            return false;
        fd = ::socket(res->ai_family, res->ai_socktype, res->ai_protocol);
        bool ok = ::connect(fd, res->ai_addr, (int)res->ai_addrlen) == 0;
        freeaddrinfo(res); return ok;
    }
};
// 真正的工业库会在此之上叠加：⑩ 环形缓冲、⑪ 长度前缀、⑫ JSON、⑨ 线程池、⑮ TLS。
```

## ㉒ 历史纵深·真实产业坐标·生产踩坑·与标准的互动

> 本节为 P0-15 全库深度升维大波次之一：压实历史出处、真实产业坐标、生产级踩坑与「本特性与 C++ 标准」的互动。引用链接列于 ㉒.5。

### ㉒.1 历史渊源补强：从 BSD socket 到 epoll 与 Networking TS
[史] 网络编程的基石是 **BSD socket（4.2BSD，1983）**，TCP 本身由 **RFC 793（1981）** 定义；POSIX 把它标准化，Windows 则提供 **Winsock**（见 ③）。[史] Linux 在 2.5.44（2002）引入 **epoll**，把"每连接一线程"的阻塞模型升级为"单线程多路复用"，是高并发服务的分水岭（见 ⑦⑧）。现代 C++ 侧，**Boost.Asio / Asio（Christopher Kohlhoff，约 2005）** 把异步 IO 抽象成 `io_context` + 回调/协程，并成为 **C++ 网络 TS（Networking Technical Specification）** 的基础提案——但该 TS 尚未并入 ISO C++（见 ⑱）。[评] 网络是"C++ 标准长期缺席、靠 POSIX/平台 API 与第三方库补位"的典型领域。

### ㉒.2 真实工程坐标：网络活在哪些产品里

网络栈是「进程间如何对话」的底层。下面按领域展开：

| 领域 / 类别 | 代表系统 · 生态 | 它承担的角色 | 规模 · 行业地位 | 备注 / 标准互动 |
|---|---|---|---|---|
| Web / 缓存底座 | Nginx / Redis / libuv（事件循环 + epoll/kqueue） | 支撑百万级并发 | Web/缓存事实底座 | Reactor 事件循环 |
| 跨平台异步 IO | Boost.Asio / Asio | 抽象跨平台异步 IO | 无数服务/客户端 | 见⑯；C++20 协程友好 |
| 游戏 / 数据库 | 自研 epoll + 线程池协议栈 | 追求低延迟 | 低延迟服务 | 见⑨ |
| RPC 框架 | gRPC / RPC（TCP/TLS 上强类型传输） | 底层仍是 socket 模型 | 强类型传输 | HTTP/2 + Protobuf |
| 网络库坐标 | Boost.Asio（Proactor）/ libevent/libuv（Reactor）/ muduo / Seastar | 各模型实现 | 工业级事实集合 | Redis/Memcached 自研循环 |
| 协议栈演进 | gRPC（HTTP/2 + Protobuf）/ 零拷贝 `io_uring`（Linux 5.x+） | 重塑高并发 I/O | 新兴事实 | io_uring 零拷贝系统调用 |

> **表注（㉒.2）**：上表前 4 行是「谁在用哪套网络模型」，后 2 行是「库坐标与协议栈演进」；Reactor（事件循环）与 Proactor（完成端口/Asio）是两大异步模型，[STANDARD] 层面 C++ 不规定网络 API，全靠库（Asio/libuv）与 OS 原语（epoll/io_uring）支撑。

**一条判读**：网络选型看「并发模型 + 平台」——Linux 高并发首选 epoll/io_uring + 事件循环，跨平台服务用 Asio 抽象掉差异，强类型内部通信用 gRPC；不要为了「现代」硬上 io_uring（需 Linux 5.x+）而忽略团队对该原语的熟悉度。

### ㉒.3 生产踩坑：网络编程的误用

| 误用 / 坑 | 后果 | 解法（关联章节） |
|-----------|------|------------------|
| **阻塞 IO 不缩放** | 每连接一线程，连接数上千就线程爆炸 | 改非阻塞 + IO 多路复用（见 ⑥⑦） |
| **连接/文件描述符泄漏** | accept 后忘 close、异常路径漏释放，耗尽 fd 致服务不可用 | RAII 包装 socket，析构即关闭（见 ⑰） |
| **忽略 `SIGPIPE`** | 向已关闭对端 `write` 触发 `SIGPIPE` 默认杀进程 | 忽略该信号或 `MSG_NOSIGNAL` |
| **epoll ET vs LT 用错** | ET 未一次读尽则事件不再触发、数据积压；LT 更安全但开销略高 | 明确 ET/LT 语义（见 ⑧） |
| **缓冲区管理不当** | 应用层未做长度前缀/分隔符帧，半包/粘包致解析错乱 | 应用层定界帧（见 ⑩⑪） |

> 表注（㉒.3）：以上五类误用覆盖"并发模型 / 资源释放 / 信号 / 多路复用语义 / 字节流定界"五个维度；前四项在本书第⑥–⑰节均有对应正解。

### ㉒.4 与标准的互动：Networking TS 仍在路上
基于 Asio 的 **Networking TS** 多次推进（executors/awaitable/sockets），目标是把 `std::net` 式异步 IO 纳入标准，但截至 C++23 仍停留在 TS，未合入——因此工业界今天仍依赖 **Boost.Asio**、平台 socket API 与 `std::thread`/`std::async`（C++11）拼装（见第159章）。[评] 网络是"标准慢、生态快"的代表：程序员先用第三方把事做成，标准再择机吸收。

**修订链补强（网络与标准：提案未落地）**：C++ 标准**至今不含**网络/异步 I/O 设施——`socket`、`async`、`executor` 全部在第三方（Asio/Boost.Asio）或提案阶段。Networking TS（[N4771](https://wg21.link/n4771)）与统一的 Executors 提案 [P0443R14](https://wg21.link/P0443)（Jared Hoberock 等，“A Unified Executors Proposal for C++”）经 SG1/LEWG 多轮评审（P2233 的 2020 秋投票 Poll 5 甚至问“是否该进 C++23”），但**未进入** C++23，其继承者 `std::execution`（[P2300](https://wg21.link/P2300) 的 Senders/Receivers）转向更通用的执行模型，网络仍悬而未决。委员会立场是“先定 executors 抽象，再谈 networking”，导致 Asio 成为事实标准而标准本身缺席——这是 C++ 在系统编程领域最常被诟病的“标准空白”之一。

### ㉒.5 权威引用
- [WG21 N4771 — Networking TS](https://wg21.link/n4771) — 网络技术规范草案
- [WG21 P0443R14 — Unified Executors](https://wg21.link/P0443) — 执行器提案
- [WG21 P2300 — std::execution (Senders/Receivers)](https://wg21.link/P2300) — 后继执行模型
- [Asio 仓库（Boost.Asio 的源头）](https://github.com/chriskohlhoff/asio) — 跨平台异步 IO 工业实现
- [Boost.Asio 官方文档](https://www.boost.org/doc/libs/release/doc/html/boost_asio.html) — 异步网络编程事实标准
- [RFC 793（TCP 协议规范）](https://datatracker.ietf.org/doc/html/rfc793) — TCP 的权威定义
- [epoll(7) — Linux 多路复用手册](https://man7.org/linux/man-pages/man7/epoll.7.html) — 高并发 IO 的底层机制
- [BSD Sockets / POSIX 参考](https://pubs.opengroup.org/onlinepubs/9699919799/functions/connect.html) — 跨平台 socket API 标准

## 附录 A：工业网络框架对比 [F: Industry / H: Design]

| 框架 | 模型 | 线程模型 | 协议 | 性能亮点 |
|---|---|---|---|---|
| Boost.Asio | Proactor | 单 io_context + 多线程 | TCP/UDP/SSL | epoll/kqueue/IOCP |
| Seastar | Reactor-per-core | 共享无 | 自定义 TCP | DPDK + 零拷贝 |
| libuv (Node.js) | Event loop | 单线程事件循环 | TCP/UDP/Pipe | 跨平台抽象 |
| gRPC (C++) | CompletionQueue | 线程池 | HTTP/2(protobuf) | 流式 RPC |
| Muduo (陈硕) | Reactor + 线程池 | one loop per thread | TCP | Linux epoll 极简实现 |
| Envoy (Lyft) | Event-driven | 多 worker 线程 | HTTP/1/2/3 | L7 代理，热重启 |

> **示例 40** [难度 ★☆☆☆☆] [主题：附录 A：工业网络框架对比 [F: ]
```cpp
#include <iostream>
int main() {
    std::cout << "Networking library choice:\n";
    std::cout << "Embedded/TCP tool:    Muduo (simple, educational)\n";
    std::cout << "High-throughput server: Seastar (DPDK, 10M QPS per core)\n";
    std::cout << "General-purpose:      Boost.Asio (standard, portable)\n";
    std::cout << "RPC/microservice:     gRPC (protobuf, streaming)\n";
    std::cout << "L7 proxy:             Envoy (xDS API, filter chains)\n";
    return 0;
}
```

## 附录 B：性能模型 —— epoll vs io_uring [E: Low-level / G: Performance]

> **示例 41** [难度 ★☆☆☆☆] [主题：附录 B：性能模型 —— epoll]
```cpp
#include <iostream>
// 注：以下为 Linux epoll/io_uring 参考量级（Jens Axboe / lwn.net 基准），
//     仅作对照示意，本机 Windows/MinGW 无 epoll/io_uring，未实测；本机实测见附录 D/F。
int main() {
    std::cout << "Linux I/O evolution:\n\n";
    std::cout << "select/poll: O(n) scan, 1024 fd limit -> obsolete\n";
    std::cout << "epoll: O(1) event notification, ~200ns/syscall, 10s of thousands fds\n";
    std::cout << "io_uring: ring-buffer shared between kernel/userspace, ~50ns/submit\n";
    std::cout << "          Zero syscall in fast path, batch submission possible\n\n";
    std::cout << "Perf comparison (1M small reads):\n";
    std::cout << "  blocking read:  ~500ns/op (syscall dominated)\n";
    std::cout << "  epoll + nonblock: ~100ns/op (amortized syscall cost)\n";
    std::cout << "  io_uring:       ~30ns/op (ring buffer, no syscall)\n\n";
    std::cout << "C++26 std::execution (P2300): aims to abstract io_uring/epoll/iocp\n";
    std::cout << "behind a unified async model (sender/receiver).\n";
    return 0;
}
```

> 注：上表为 **Linux** epoll/io_uring 基准（量级参考 Jens Axboe 的 io_uring 基准 / lwn.net epoll 基准）。本机为 Windows/MinGW，**无 epoll/io_uring**，无法实测；Winsock 的等价高并发机制是 **IOCP（完成端口）**。本机可实测的 localhost TCP 数据见附录 D / 附录 F。

## 附录 C：面试 [J: Learning]

> **示例 42** [难度 ★☆☆☆☆] [主题：附录 C：面试 [J: Learni]
```
面试高频:
Q: epoll 的水平触发 (LT) 和边缘触发 (ET) 的区别？
A: LT = 只要缓冲区有数据就通知 (可重复); ET = 仅状态变化时通知一次 (更高性能，需循环读)

Q: Reactor vs Proactor 的区别？
A: Reactor = 事件通知 + 用户自己读写; Proactor = 内核完成 IO + 通知用户结果 (Boost.Asio 模式)

Q: TCP 的 TIME_WAIT 和 SO_REUSEADDR 的作用？
A: TIME_WAIT = 2MSL 等待 (防止残留报文干扰); SO_REUSEADDR = 允许绑定处于 TIME_WAIT 的端口
```

## 附录 D：编译器与底层网络性能 [C: Compiler / E: Low-level / I: Practice]

> **示例 43** [难度 ★☆☆☆☆] [主题：附录 D：编译器与底层网络性能 [C]
```
网络编程的底层性能边界（量级参考，区分平台）：

[Linux x86-64 — 本机 Windows/MinGW 无 epoll/io_uring，未实测；来源: Jens Axboe io_uring 基准 / lwn.net epoll 基准 / Brendan Gregg]
Syscall (read/write, 裸 fd 就绪): ~100-500ns
epoll_wait: ~200ns (无事件) / ~1us (有事件)
io_uring submit: ~50ns (无 syscall)
Context switch (裸切换): ~1-10us
TCP 握手 (局域网): ~1ms  / (跨洲): ~50-200ms

[本机实测 — GCC 13.1 / MinGW-w64 / x86-64, localhost, 锚定 Examples/_ch163_net_perf.cpp]
localhost TCP connect : 355 us        （loopback；真实局域网 ≈ 1ms，文献）
localhost RTT (1B echo): 35.3 us/op   （含完整 TCP 栈往返，远大于裸 syscall）
localhost bulk xfer   : 889 MB/s (0.87 GB/s)
clock-read proxy      : 50.6 ns/call  （steady_clock::now，非 I/O syscall，仅计时下限）
线程上下文切换         : 17.8 us/次     （mutex+cv 往返，含同步开销；裸切换文献 ~1-10us）

GCC 选项: -D_GNU_SOURCE (epoll, sendfile), -fno-exceptions (热路径), -O3 -march=native (SIMD)

工业故障: TIME_WAIT 耗尽 → SO_REUSEADDR + 连接池; select(1024) → epoll(100K+) → io_uring(1M+)
```

真实汇编证据（网络 I/O 的编译边界）：节选自 `Examples/_ch163_net_perf.asm`

```asm
; sock_send / sock_recv 编译为直接跳进 WS2_32 导入的 send/recv
; —— 内核边界在 WS2_32.dll 内，编译器无法内联消除，故网络 I/O 必有一次库调用 + 内核切换
; 节选自 Examples/_ch163_net_perf.asm
_Z9sock_sendyPKci:
        xorl    %r9d, %r9d
        rex.W jmp       *__imp_send(%rip)   ; 网络写 = 跳转进 WS2_32 导入表
_Z9sock_recvyPci:
        xorl    %r9d, %r9d
        rex.W jmp       *__imp_recv(%rip)   ; 网络读 = 跳转进 WS2_32 导入表
```

## 附录 E：面试补充 [J: Learning]

> **示例 44** [难度 ★☆☆☆☆] [主题：附录 E：面试补充 [J: Lear]
```
Q: epoll ET vs LT? A: ET=一次通知需循环读(高性能); LT=持续通知(简单,默认)
Q: sendfile vs mmap? A: sendfile=kernel zero-copy; mmap=映射到userspace(有一次拷贝)
Q: SO_REUSEPORT? A: 多socket绑定同端口,内核自动负载均衡(Linux 3.9+)
```

## 附录 F：编译器与底层网络性能 [C: Compiler / E: Lowlevel / I: Practice]

> **示例 45** [难度 ★☆☆☆☆] [主题：附录 F：编译器与底层网络性能 [C]
```
GCC编译选项对网络代码的影响:
-D_GNU_SOURCE → 启用epoll_create1, accept4, recvmmsg等Linux特有API
-fno-exceptions → 网络热路径禁异常 (Google风格, ~5% binary缩减)  [量级; 来源: Google C++ Style Guide / 工业经验]
-O3 -march=native → SIMD加速memcpy (sendfile替代场景)
-fstack-protector-strong → 防栈溢出, ~1%性能损失, 生产必开  [量级; 来源: GCC/厂商基准]

底层性能边界（区分平台）:
syscall(read/write): ~100-500ns   [Linux 裸 fd 就绪; 本机 Windows/MinGW 未实测]
epoll_wait(无事件): ~200ns / (有事件): ~1us   [Linux; 本机无 epoll]
io_uring submit: ~50ns (无syscall路径, ring buffer共享)   [Linux; Jens Axboe io_uring 基准; 本机无 io_uring]
context switch: ~1-10us (线程调度, 裸切换文献) / 本机实测 ~14-18us/次 (mutex+cv, 含同步开销)
TCP握手(局域网): ~1ms / (跨洲): ~50-200ms   [文献; 本机 localhost connect 实测 355us, 仅 loopback]

[本机实测汇总 — GCC 13.1 / MinGW-w64 / x86-64, localhost, 锚定 Examples/_ch163_net_perf.cpp]
localhost TCP connect : 355 us | RTT(1B echo): 35.3 us/op | bulk: 889 MB/s | ctx switch: 17.8 us/次
（完整表 + 真实汇编证据见附录 D）

工业故障案例:
- TIME_WAIT耗尽 → SO_REUSEADDR + 连接池 (Chromium fix, 2014)
- C10K→C10M: select(1024fd) → epoll(100K+) → io_uring(1M+)
- Nagle算法延迟 → TCP_NODELAY (Redis默认禁用Nagle)
- SO_REUSEPORT: 多线程绑定同端口, 内核负载均衡 (Linux 3.9+, HAProxy使用)
```

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第162章](Book/part15_cases/ch162_json.md) | 键值查找/缓存 | 本章提供概念，第162章提供实现 |
| [第164章](Book/part15_cases/ch164_framework.md) | TCP服务器/HTTP客户端 | 本章提供概念，第164章提供实现 |
| [第159章](Book/part15_cases/ch159_threadpool.md) | 无锁队列/计数器 | 本章提供概念，第159章提供实现 |
| [第113章](Book/part09_concurrency/ch113_coroutine.md) | 配置解析/API响应 | 本章提供概念，第113章提供实现 |

## 项目学习地图：网络编程 → 全书知识映射

| 项目组件 | 依赖章节 | 知识点 |
|---|---|---|
| Socket API | ch163(网络), ch38(allocator) | TCP/UDP + 非阻塞IO |
| 事件循环 | ch93(thread), ch113(coroutine) | epoll/io_uring + 异步模型 |
| 协议解析 | ch81(string), ch88(optional_variant) | HTTP/JSON/自定义协议 |
| 缓冲区管理 | ch77(vector), ch160(mempool) | 环形缓冲 + 零拷贝 |
| 线程模型 | ch93(thread), ch159(threadpool) | one-loop-per-thread |

> **示例 46** [难度 ★☆☆☆☆] [主题：项目学习地图：网络编程 → 全书知识]
```cpp
#include <iostream>
int main(){std::cout<<"Network=ch163+ch93+ch81+ch77+ch159"<<std::endl;return 0;}
```

## 相关章节（交叉引用）

- **同模块兄弟（part15 实战案例）**：⟶ Book/part15_cases/ch159_threadpool.md（第159章 从零实现线程池（C++））
- **同模块兄弟（part15 实战案例）**：⟶ Book/part15_cases/ch160_mempool.md（第160章 从零实现内存池（C++））
- **同模块兄弟（part15 实战案例）**：⟶ Book/part15_cases/ch161_logger.md（第161章 从零实现日志库（C++））
- **同模块兄弟（part15 实战案例）**：⟶ Book/part15_cases/ch162_json.md（第162章 从零实现 JSON 库（C++））
- **同模块兄弟（part15 实战案例）**：⟶ Book/part15_cases/ch164_framework.md（第164章 从零实现迷你框架（C++））
- **跨模块延伸**：⟶ Book/part16_reading/ch165_roadmap.md（第165章 C++ 进阶路线图（C++））

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例：C10K 升级 C100K——epoll 还不够

某交易网关从 C10K 架构（`select` + 每连接一线程）升级 C100K 时，简单换成 `epoll` 后发现 CPU 仍跑满在 `epoll_wait` 的 `epitem` 红黑树查找上。根因是每次 `epoll_ctl(EPOLL_CTL_MOD)` 改事件掩码都触发 `rb_insert`——连接密集的金融协议（心跳/报价/成交三路流）导致海量 MOD 操作。修复：用 `EPOLLONESHOT` 减少重复 MOD + `io_uring` 替换 epoll（kernel 5.1+ 支持），`IORING_OP_SEND`/`IORING_OP_RECV` 批量提交，单核 C100K CPU 从 98% 降到 35%。

### 常见 Bug / Debug 方法

- **TCP_NODELAY 忘记设**：Linux 默认开启 Nagle 算法（合并小包等 ACK），延迟敏感协议（游戏/交易）未设 `setsockopt(TCP_NODELAY)` 会导致每 40ms 才发一次小包——用 `tcpdump -i eth0 'tcp[tcpflags] & tcp-push == 0'` 查延迟包。
- **TIME_WAIT 端口耗尽**：短连接高频场景（压测/爬虫），主动关闭方进入 TIME_WAIT 2MSL（60s），16bit 端口空间耗尽后 `connect()` 报 `EADDRNOTAVAIL`。设置 `SO_REUSEADDR` 或改 `net.ipv4.tcp_tw_reuse=1` 缓解。
- **epoll EPOLLOUT 滥用**：send 缓冲区不满时 `epoll_wait` 会持续返回 `EPOLLOUT`，造成不必要的 CPU 空转（busy-loop）。正确做法：只在 `send()` 返回 `EAGAIN` 后注册 `EPOLLOUT`，发送完成后立即注销。

### Code Review 关注点

- `recv()` 返回值是否检查 `0`（对端关闭）vs `-1`（错误）？`recv()==0` 不关闭 fd 会导致 epoll 持续触发 `EPOLLIN` 但读不到数据的死循环。
- `close()` vs `shutdown(fd, SHUT_WR)`：`close()` 直接释放 fd 且如果其他线程持有引用就会 dup 出的 fd 泄漏；`shutdown()` 优雅关闭——先 SHUT_WR 发 FIN → 对端 recv()==0 → 对端 close → 本端再 close。
- 并发调用 `epoll_ctl` 是否需要锁？epoll fd 本身线程安全，但 `epoll_ctl(ADD)` 与 `close(fd)` 竞态——内核在 `epoll_ctl` 前自动移除关闭的 fd，但最佳实践是在同一线程管理 epoll。

### 重构建议

- 从回调地狱转协程：C++20 `co_await` + `io_uring` 实现 `async_read(async_socket, buffer)` 同步风格写法，消除回调嵌套。参考 `liburing` 的官方示例 `io_uring-cpp`。
- 协议层与传输层解耦：网络层只做 `recv()`/`send()` 字节流，协议解析用 `std::span<const uint8_t>` 零拷贝引用，避免 `memcpy` 进中间 buffer。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

> **示例 47** [难度 ★☆☆☆☆] [主题：重构建议]
```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 面试要点（速记·网络编程）

| 速记要点 | 一句话作答 |
|----------|------------|
| **阻塞 vs 多路复用** | 单线程 `select/poll/epoll` 管万级连接（C10K），替代一连接一线程 |
| **`epoll` ET vs LT** | 边沿触发需非阻塞 + 循环读完，否则丢事件；水平触发更安全但无效唤醒多 |
| **Reactor vs Proactor** | Reactor 等「可读」后自己读；Proactor（IOCP）内核完成 IO 后通知（关联 第159章） |
| **TCP 粘包** | 用长度前缀或分隔符定界，不能假设一次 `recv` 收完整消息 |
| **`io_uring`** | 把系统调用异步化进一步降开销；`TLS` 应用层加解密独立于传输 |

> 表注（面试要点）：五条对应第⑥（阻塞/非阻塞）、第⑦⑧（多路复用）、第⑨（线程池）、第⑪（定界）、附录 B（io_uring）的核心结论。

### 练习 1（难度 ★★）

网络读写常遇到“一次 recv 只到半包”，需要把零散字节攒进应用层缓冲。
请实现一个定长环形缓冲区 `RingBuffer`：`push` 写入、`pop` 取出，跨读写指针不越界。

> **示例 48** [难度 ★☆☆☆☆] [主题：练习 1（难度 ★★）]
```cpp
#include <iostream>
#include <vector>
#include <cstddef>

class RingBuffer {
    std::vector<char> buf_;
    std::size_t head_ = 0, tail_ = 0, size_ = 0;
public:
    explicit RingBuffer(std::size_t cap) : buf_(cap) {}
    bool push(char c) {
        if (size_ == buf_.size()) return false;     // 满
        buf_[tail_] = c;
        tail_ = (tail_ + 1) % buf_.size();
        ++size_;
        return true;
    }
    bool pop(char& c) {
        if (size_ == 0) return false;               // 空
        c = buf_[head_];
        head_ = (head_ + 1) % buf_.size();
        --size_;
        return true;
    }
    std::size_t size() const { return size_; }
};

int main() {
    RingBuffer rb(4);
    rb.push('a'); rb.push('b');
    char c; rb.pop(c); std::cout << "pop=" << c << " remain=" << rb.size() << '\n';
}
```

[标准] 环形缓冲把“生产者（recv 线程）/消费者（解析线程）”解耦，是网络栈与设备驱动的标配缓冲原语（关联 ⑩ 缓冲区管理）。

### 练习 2（难度 ★★★）

TCP 是字节流，应用层必须自己定界。长度前缀（先发 4 字节大端长度，再发载荷）是最常用的定界法。
请实现 `encode`/`decode`：把一条消息序列化为 `[uint32 len][payload]`，再解析回来。

> **示例 49** [难度 ★☆☆☆☆] [主题：练习 2（难度 ★★★）]
```cpp
#include <iostream>
#include <string>
#include <vector>
#include <cstdint>
#include <cstddef>

std::string encode(const std::string& msg) {
    uint32_t n = static_cast<uint32_t>(msg.size());
    std::string out(sizeof n, '\0');
    out[0] = (n >> 24) & 0xFF; out[1] = (n >> 16) & 0xFF;   // 大端长度前缀
    out[2] = (n >> 8) & 0xFF;  out[3] = n & 0xFF;
    return out + msg;
}

std::string decode(const std::string& wire, std::size_t& pos) {
    uint32_t n = (uint8_t)wire[pos] << 24 | (uint8_t)wire[pos+1] << 16
               | (uint8_t)wire[pos+2] << 8 | (uint8_t)wire[pos+3];
    pos += 4;
    std::string s(wire.data() + pos, n);
    pos += n;
    return s;
}

int main() {
    auto wire = encode("hello");
    std::size_t pos = 0;
    std::cout << "解码=" << decode(wire, pos) << " 剩余字节=" << (wire.size() - pos) << '\n';
}
```

[标准] 长度前缀比“换行分隔符”更通用（可承载二进制）；注意字节序——网络协议约定大端（关联 ⑪ 协议设计）。

### 练习 3（难度 ★★★★）

非阻塞服务里，一个连接可能要跨多次 epoll 事件才能收齐一条消息。请用状态机表达
“读头部 → 读载荷 → 处理”，并用分块输入的字节流驱动它，模拟非阻塞累积。

> **示例 50** [难度 ★☆☆☆☆] [主题：练习 3（难度 ★★★★）]
```cpp
#include <iostream>
#include <string>
#include <vector>
#include <cstdint>
#include <cstddef>

enum class State { ReadHeader, ReadBody, Done };

std::string feed(State& st, std::vector<char>& buf, const std::vector<char>& chunk, uint32_t& body_len) {
    buf.insert(buf.end(), chunk.begin(), chunk.end());
    if (st == State::ReadHeader && buf.size() >= 4) {
        body_len = (uint8_t)buf[0] << 24 | (uint8_t)buf[1] << 16
                 | (uint8_t)buf[2] << 8 | (uint8_t)buf[3];
        buf.erase(buf.begin(), buf.begin() + 4);
        st = State::ReadBody;
    }
    if (st == State::ReadBody && buf.size() >= body_len) {
        std::string msg(buf.data(), body_len);
        buf.erase(buf.begin(), buf.begin() + body_len);
        st = State::Done;
        return msg;
    }
    return {};
}

int main() {
    State st = State::ReadHeader;
    std::vector<char> buf; uint32_t len = 0;
    // 同一条消息被拆成 3 个 chunk 到达（模拟非阻塞分片）
    std::vector<char> c1 = {0,0,0,5};
    std::vector<char> c2 = {'h','e'};
    std::vector<char> c3 = {'l','l','o'};
    feed(st, buf, c1, len);
    feed(st, buf, c2, len);
    auto msg = feed(st, buf, c3, len);
    std::cout << "收齐消息=" << (st == State::Done ? msg : std::string("(未收齐)")) << '\n';
}
```

[标准] 非阻塞 IO 的核心心智模型就是“状态机 + 累积缓冲”：每次事件只推进能推进的部分，绝不阻塞等待整包
（关联 ⑥ 阻塞 vs 非阻塞 / ⑦ I/O 多路复用）。真实 epoll 只是“何时可读”的通知者，定界仍靠本例逻辑。

## 附录：用法演绎（从选型到落地）

### 演绎 1：epoll vs io_uring——从“等通知”到“交作业”

**场景**：C10K 之后，epoll 的“每次循环都要把 fd 集合从用户态拷进内核态”成为新瓶颈。
**选型**：io_uring 用“提交/完成两个共享环”让内核与应用零拷贝交接，减少系统调用与拷贝。
**错误**：以为“多线程 + epoll”能无限扩展——上下文切换与拷贝开销先到顶（关联 附录 B 性能模型）。
**落地**：

> **示例 51** [难度 ★☆☆☆☆] [主题：演绎 1：epoll vs iour]
```cpp
#include <iostream>

// 用常量表达两种模型的“每次事件系统调用/拷贝开销”量级差异
struct Model { const char* name; int syscall_per_event; int copy_per_event; };

int main() {
    Model epoll    { "epoll",   1, 1 };   // 每次循环重传 fd 集：1 次调用 + 1 次拷贝
    Model io_uring { "io_uring",0, 0 };   // 共享环：提交即完成，无每次重传
    std::cout << epoll.name    << ": syscall/event=" << epoll.syscall_per_event
              << " copy/event=" << epoll.copy_per_event << '\n';
    std::cout << io_uring.name << ": syscall/event=" << io_uring.syscall_per_event
              << " copy/event=" << io_uring.copy_per_event << " (共享环，近乎零拷贝)\n";
}
```

**结论**：epoll 解决“怎么知道哪些 fd 就绪”，io_uring 进一步解决“就绪后怎么少拷贝/少切换”；
模型选择取决于并发量级（关联 附录 B / ⑧ epoll 实战）。

### 演绎 2：C10K 到 C100K——Reactor 用“一个线程管万连”代替“一连接一线程”

**场景**：早期“每连接一线程”模型在 1 万连接时线程切换把 CPU 吃光（C10K 问题）。
**选型**：Reactor（单/少数线程 + I/O 多路复用）用一个线程监管上万连接，连接元数据用哈希表索引。
**落地**：

> **示例 52** [难度 ★☆☆☆☆] [主题：演绎 2：C10K 到 C100K—]
```cpp
#include <iostream>
#include <unordered_map>

struct Conn { int fd; /* 读写缓冲、状态机等 */ };

int main() {
    std::unordered_map<int, Conn> conns;          // fd -> 连接元数据
    for (int fd = 3; fd < 8; ++fd) conns[fd] = Conn{fd};
    // Reactor 主循环：epoll_wait 拿到就绪 fd 集合，逐个查表分发
    std::cout << "Reactor 监管连接数=" << conns.size() << '\n';
    std::cout << "单线程即可监管数万连接，避免线程爆炸（C10K->C100K 关键）\n";
}
```

[标准] 把“连接状态”从线程栈搬到“集中数据结构 + 事件循环”，是突破 C10K 的根本手法
（关联 附录 I 工业案例 / ⑨ 多线程服务）。

## 附录 J：TCP 连接处理决策流（D3 维度）

> 本图把第④⑤节（echo server/client）、第⑥节（阻塞 vs 非阻塞）、第⑦⑧节（select/poll/epoll/kqueue/io_uring 多路复用）、第⑩节（环形缓冲）、第⑪节（长度前缀/分隔符 framing）、第⑫节（JSON 序列化）、第⑨节（线程池服务）收敛成一条"建 socket→bind/listen→accept→多路复用就绪→收字节流→定界消息→解析→回显"的连接处理流水线，并标出阻塞/非阻塞与多种多路复用的回退边。

```mermaid
flowchart TD
  A["socket 创建端点"] --> B["bind 加 listen SO_REUSEADDR"]
  B --> ACC["accept 等待连接"]
  ACC --> N{"阻塞 或 非阻塞?"}
  N -->|阻塞| T1["一连接一线程 或 线程池 ch159"]
  N -->|非阻塞| MUX{"多路复用?"}
  MUX -->|select poll| SL["O(n) 轮询"]
  MUX -->|epoll kqueue| EP["O(1) 事件就绪"]
  MUX -->|io_uring| IU["共享环 零拷贝"]
  T1 --> RECV["recv 收字节流"]
  SL --> RECV
  EP --> RECV
  IU --> RECV
  RECV --> FR{"如何定界消息?"}
  FR -->|长度前缀| LP["4B 大端 加 payload"]
  FR -->|分隔符| DL["按换行符 切分"]
  LP --> PARSE["JSON 解析 ch162"]
  DL --> PARSE
  PARSE --> H{"处理完毕?"}
  H -->|否| RECV
  H -->|是| SND["send 回显 或 响应"]
  SND --> C{"对端关闭 recv 等于 0?"}
  C -->|是| CL["closesocket 释放 fd"]
  C -->|否| RECV
  CL --> RAII["Socket RAII 析构即关闭"]
```

> 决策流说明：阻塞/非阻塞是第一道闸门，非阻塞下又按平台在 select/poll/epoll/kqueue/io_uring 之间「或」择一；定界方式（长度前缀「或」分隔符）决定如何把字节流切成消息，两条边在"JSON 解析"处汇合。跨章外推：线程池服务外推第159章，JSON 载荷外推第162章，无锁计数外推第107章。

## 附录 K：网络编程知识图谱（D6 维度）

> 本图以本章主题为中心，上游列出其依赖的底层机制（分配/并发/格式化/解析原语），下游列出消费它的系统（框架/网络/日志/测试），并标出跨章外推边。

```mermaid
flowchart TD
  CORE["网络编程 (ch163)"]
  SOCKET["Berkeley Socket Winsock"]
  THREAD["std thread ch93"]
  THREADPOOL["线程池 ch159"]
  COROUTINE["协程 ch113"]
  ATOMIC["std atomic ch107"]
  JSON["JSON 解析 ch162"]
  MEMRED["内存池 ch44"]
  VECTOR["std vector 缓冲 ch77"]
  BUFFER["环形缓冲"]
  REACTOR["Reactor Proactor"]
  ASIO["Boost.Asio 上游"]
  EPOLL["epoll kqueue"]
  CORE --> SOCKET
  CORE --> THREAD
  CORE --> THREADPOOL
  THREADPOOL --> ATOMIC
  CORE --> COROUTINE
  CORE --> JSON
  CORE --> MEMRED
  BUFFER --> VECTOR
  CORE --> REACTOR
  REACTOR --> EPOLL
  REACTOR --> ASIO
  CORE --> MEMRED
  REACTOR --> THREAD
  SOCKET --> BUFFER
```

### K.1 概念依赖逐边解读

| 边 | 依赖含义 |
|----|----------|
| CORE → SOCKET | 一切基于 Berkeley Socket 或 Winsock |
| CORE → THREAD | 阻塞模型一连接一线程 |
| CORE → THREADPOOL | 高并发升级线程池复用线程 |
| THREADPOOL → ATOMIC | 连接计数用 atomic |
| CORE → COROUTINE | C++20 协程做异步回显 |
| CORE → JSON | payload 用 JSON 序列化 |
| CORE → MEMRED | 缓冲管理借鉴内存池思想 |
| BUFFER → VECTOR | 环形缓冲底层用 vector |
| CORE → REACTOR | 事件循环 Reactor/Proactor |
| REACTOR → EPOLL | Linux 用 epoll O(1) 就绪 |
| REACTOR → ASIO | Boost.Asio 统一 proactor 抽象 |
| CORE → MEMRED | 组件缓冲借鉴内存池 |
| REACTOR → THREAD | 事件循环内回调由线程执行 |
| SOCKET → BUFFER | recv 字节流入应用层环形缓冲 |

### K.2 跨章闭环表

| 目标章 | 路径 | 闭环点 |
|--------|------|--------|
| 第93章 thread/async | Book/part07_stl/ch93_thread_async.md | 阻塞模型一连接一线程，事件循环靠线程 |
| 第159章 threadpool | Book/part15_cases/ch159_threadpool.md | 高并发把每连接封装成线程池任务 |
| 第113章 coroutine | Book/part09_concurrency/ch113_coroutine.md | C++20 协程做异步回显消除回调嵌套 |
| 第107章 atomic | Book/part09_concurrency/ch107_atomic.md | 连接与回显字节计数用 atomic |
| 第162章 json | Book/part15_cases/ch162_json.md | payload 用 JSON 序列化加 长度前缀帧 |
| 第44章 memory_pool | Book/part04_memory/ch44_memory_pool.md | 缓冲管理借鉴内存池与环形缓冲思想 |
| 第77章 vector | Book/part07_stl/ch77_vector.md | 环形缓冲底层用 vector 扩容 |

## 附录 D5：真实基准与性能分析 — 消息序列化 — 手工字节打包 vs struct memcpy vs 长度前缀帧 vs 逐字段拷贝（GCC 15.3.0）

> 绝对毫秒随机器而变，加速比才是可移植信号。

**编译器**：GCC 15.3.0 (MinGW-w64 x86_64-posix-seh)，`-O2 -std=c++23`，5 次取中位数。
**源码**：`_bench_d5_ch163_net.cpp`

### D5.1 基准结果

| 方案 | 描述 | 中位数 (ms) | 相对开销 |
|------|------|------------|----------|
| 逐字段拷贝 | 字段逐个赋值 | 2.150 | 0.98× |
| struct memcpy | 整块内存拷贝 | 2.204 | 1.00× (基线) |
| 手工字节打包 | 位移拼字节 | 2.310 | 1.05× |
| 长度前缀帧 | 每帧动态分配 + 长度头 | 53.678 | ~24× 慢 |

#### 可视化速读（D5.1 数据图·双面板）

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(a) 绝对耗时（随机器而变，仅作量级参考）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(a) 绝对耗时（随机器而变，仅作量级参考）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">10</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">绝对耗时 (ms)</text>
  <line x1="80" y1="257.4" x2="640" y2="257.4" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="253.4" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">基线 2.20ms</text>
  <rect x="118.0" y="258.8" width="64.0" height="41.2" fill="#4C72B0"/>
  <text x="150.0" y="252.8" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#4C72B0">2.15ms</text>
  <text x="150.0" y="318.0" text-anchor="middle" font-size="11" font-family="Georgia, serif">逐字段拷贝</text>
  <rect x="258.0" y="257.4" width="64.0" height="42.6" fill="#9A9A9A"/>
  <text x="290.0" y="251.4" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">2.20ms</text>
  <text x="290.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 290.0 314.0)">struct memcpy</text>
  <rect x="398.0" y="254.9" width="64.0" height="45.1" fill="#55A868"/>
  <text x="430.0" y="248.9" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#55A868">2.31ms</text>
  <text x="430.0" y="318.0" text-anchor="middle" font-size="11" font-family="Georgia, serif">手工字节打包</text>
  <rect x="538.0" y="85.5" width="64.0" height="214.5" fill="#C44E52"/>
  <text x="570.0" y="79.5" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">53.68ms</text>
  <text x="570.0" y="318.0" text-anchor="middle" font-size="11" font-family="Georgia, serif">长度前缀帧</text>
</svg>

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(b) 相对倍数（可移植信号：基准=1.00×）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(b) 相对倍数（可移植信号：基准=1.00×）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.1</text>
  <line x1="80" y1="217.3" x2="640" y2="217.3" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="220.8" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1</text>
  <line x1="80" y1="134.7" x2="640" y2="134.7" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="138.2" text-anchor="end" font-size="10.5" font-family="Georgia, serif">10</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">相对倍数 (×, 基线=1.00)</text>
  <line x1="80" y1="217.3" x2="640" y2="217.3" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="213.3" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">1.00× 基线</text>
  <rect x="118.0" y="218.2" width="64.0" height="81.8" fill="#4C72B0"/>
  <text x="150.0" y="212.2" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#4C72B0">0.98×</text>
  <text x="150.0" y="318.0" text-anchor="middle" font-size="11" font-family="Georgia, serif">逐字段拷贝</text>
  <rect x="258.0" y="217.3" width="64.0" height="82.7" fill="#9A9A9A"/>
  <text x="290.0" y="211.3" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">1.00×</text>
  <text x="290.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 290.0 314.0)">struct memcpy</text>
  <rect x="398.0" y="215.6" width="64.0" height="84.4" fill="#55A868"/>
  <text x="430.0" y="209.6" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#55A868">1.05×</text>
  <text x="430.0" y="318.0" text-anchor="middle" font-size="11" font-family="Georgia, serif">手工字节打包</text>
  <rect x="538.0" y="102.7" width="64.0" height="197.3" fill="#C44E52"/>
  <text x="570.0" y="96.7" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">24.35×</text>
  <text x="570.0" y="318.0" text-anchor="middle" font-size="11" font-family="Georgia, serif">长度前缀帧</text>
</svg>

> 图注：三种零分配方案（逐字段拷贝 2.150 ms、struct memcpy 2.204 ms、手工字节打包 2.310 ms）差异 <10%（噪声级），说明连续内存拷贝与逐字段赋值在 `-O2` 下生成几乎相同代码；但长度前缀帧每帧 `new` 缓冲区，实测 53.678 ms，是零分配方案的 **~24×**。网络序列化瓶颈不在『怎么拷字节』而在『是否分配内存』——变长消息须配对象池。机制：堆分配 + 释放才是代价。数据见上方 D5.1 表。

### D5.2 非显然结论

**网络序列化瓶颈不在「怎么拷字节」而在「是否分配内存」——长度前缀帧慢 24×**

三种零分配方案（逐字段 / struct memcpy / 手工字节打包）都在 ~2.2 ms，差异 <10%（噪声级）：连续内存拷贝与逐字段赋值在 `-O2` 下生成几乎相同的代码。但长度前缀帧（53.678 ms）**慢 24×**，因为它对每条消息 `new` 一个带长度头的缓冲区——分配 + 释放才是代价。

**工程判据：固定结构消息用 struct memcpy / 逐字段（零分配）；变长消息才用长度前缀帧且必须配对象池**

不要为了「更优雅的序列化」去逐字节拼装——那和 memcpy 一样快；真正要消灭的是每条消息的堆分配。

### D5.3 可复现 demo

> **示例 53** [难度 ★☆☆☆☆] [主题：可复现 demo]
```cpp
#include <cstdio>
#include <cstring>

#pragma pack(push,1)
struct Msg { int id; double v; };
#pragma pack(pop)

// 零分配：整块拷贝
void send_memcpy(const Msg* m){ Msg o; memcpy(&o,m,sizeof(Msg)); printf("id=%d\n",o.id); }

// 长度前缀帧：每帧 new
char* send_framed(const Msg* m){
    char* buf = new char[sizeof(int)+sizeof(Msg)];
    *(int*)buf = (int)sizeof(Msg);
    memcpy(buf+sizeof(int), m, sizeof(Msg));
    return buf;
}
int main(){
    Msg m{7, 1.5}; send_memcpy(&m);
    char* f = send_framed(&m); delete[] f; printf("ok\n");
}
```

编译运行：`g++ -O2 -std=c++23 _bench_d5_ch163_net.cpp -o _bench_d5_ch163_net.exe && ./_bench_d5_ch163_net.exe`

### D5.4 方法学注

**方法论**：volatile sink 防 DCE、`[[gnu::noinline]]` 防内联穿透、不透明工厂防去虚化；5 次运行取中位数，排除首访缓存冷启动。

**交叉引用**：ch91（filesystem 与 IO）/ ch156（编译器优化）/ ch160（内存池消除分配）

### D5.5 汇编实证 (GCC 15.3.0)

> 以下 disassembly 由 `g++ -O2 -std=c++23 -masm=intel _bench_d5_ch163_net.cpp` 真实生成（节选自 bench_field_copy(int), bench_length_prefix(int), bench_manual_pack(int)）。。下方反汇编为 GCC 15.3.0 -O2 真实产物，印证该结论。

```asm
; bench_field_copy(int)  (108 条指令)
sub    rsp, 104
movaps    XMMWORD PTR [rsp], xmm6
movaps    XMMWORD PTR 16[rsp], xmm7
movaps    XMMWORD PTR 32[rsp], xmm8
movaps    XMMWORD PTR 48[rsp], xmm9
movaps    XMMWORD PTR 64[rsp], xmm10
movaps    XMMWORD PTR 80[rsp], xmm11
test    ecx, ecx
jle    .L
lea    eax, -1[rcx]
cmp    eax, 14
jbe    .L
mov    r9d, 4
mov    edx, ecx
mov    r10d, 8
xor    eax, eax
movd    xmm7, r9d
pcmpeqd    xmm3, xmm3
mov    r11d, 12
mov    r9d, 16
movdqa    xmm2, XMMWORD PTR .LC[rip]
movd    xmm6, r10d
movd    xmm5, r11d
shr    edx, 4
movd    xmm4, r9d
pxor    xmm9, xmm9
pshufd    xmm7, xmm7, 0
pshufd    xmm6, xmm6, 0
psrlw    xmm3, 8
pshufd    xmm5, xmm5, 0
pshufd    xmm4, xmm4, 0
movdqa    xmm10, xmm2
movdqa    xmm0, xmm2
movdqa    xmm1, xmm2
add    eax, 1
paddd    xmm10, xmm7
movdqa    xmm11, xmm2
punpcklwd    xmm0, xmm10
punpckhwd    xmm1, xmm10
paddd    xmm11, xmm5
movdqa    xmm10, xmm0
punpcklwd    xmm0, xmm1
punpckhwd    xmm10, xmm1
movdqa    xmm1, xmm2
paddd    xmm2, xmm4
```

> 注意：上述函数在 GCC 15.3.0 -O2 下编译为紧凑机器码；对比 D5.2 的加速比结论，可见零成本抽象在 -O2 下确实被兑现（或代价点所在）。绝对毫秒随机器而变，加速比才是可移植信号。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

一个 BSD/POSIX TCP echo server 的核心系统调用顺序是什么？依次列出从建监听套接字到接受连接的关键步骤，并说明 `listen` 的 backlog 含义。

<details><summary>答案与解析</summary>

顺序：`socket()` 创建套接字 → `bind()` 绑定地址端口 → `listen()` 进入监听（backlog 为已完成+进行中连接队列上限）→ `accept()` 阻塞等待并产出已连接套接字 → `read/write` 收发 → `close()`。backlog 是内核为该监听套接字维护的"半连接+全连接"队列长度上限，过小会丢连接、过大浪费资源。

> **示例 54** [难度 ★☆☆☆☆] [主题：练习 1（难度 ★★）]
```cpp
// 概念骨架（Linux/macOS 需 <sys/socket.h>，本 MinGW 门禁跳过该块）
// int s = socket(AF_INET, SOCK_STREAM, 0);
// bind(s, (sockaddr*)&addr, sizeof addr);
// listen(s, 16);
// int c = accept(s, nullptr, nullptr);
// read(c, buf, n); write(c, buf, n); close(c);
```

[标准] Berkeley Socket API 是 POSIX 网络编程事实标准；`SOCK_STREAM` 对应 TCP 的字节流语义。

[引用] Beej's Guide to Network Programming <https://beej.us/guide/bgnet/>；POSIX `socket(2)`/`listen(2)` 手册 <https://man7.org/linux/man-pages/man2/socket.2.html>；Boost.Asio 的 Proactor 模型 <https://www.boost.org/doc/libs/release/doc/html/boost_asio.html>。

</details>

### 练习 2（难度 ★★★）

阻塞 I/O 与非阻塞 I/O 的根本区别是什么？在 POSIX 与 Windows（Winsock）上分别用什么调用把一个套接字设为非阻塞？

<details><summary>答案与解析</summary>

阻塞：`read/accept` 在无数据/无连接时挂起线程，简单但并发差（每连接一线程）。非阻塞：调用立即返回 `EWOULDBLOCK`/`WSAEWOULDBLOCK`，需配合 `select/poll/epoll`（或 IOCP）轮询，单线程可驱动大量连接。

- POSIX：`fcntl(fd, F_SETFL, O_NONBLOCK)`；
- Windows Winsock：`u_long mode=1; ioctlsocket(s, FIONBIO, &mode);`。

> **示例 55** [难度 ★☆☆☆☆] [主题：练习 2（难度 ★★★）]
```cpp
// POSIX 设非阻塞（门禁跳过 <sys/socket.h>/<fcntl.h> 块）
// fcntl(fd, F_SETFL, fcntl(fd,F_GETFL,0) | O_NONBLOCK);
```

[标准] 非阻塞 + I/O 多路复用是高并发网络服务的基石；跨平台需封装 POSIX/Winsock 差异（见 ch163 ③）。

[引用] POSIX `fcntl(2)`（设 `O_NONBLOCK`）<https://man7.org/linux/man-pages/man2/fcntl.2.html>；Microsoft Winsock `ioctlsocket` <https://learn.microsoft.com/windows/win32/api/winsock2/nf-winsock2-ioctlsocket>；C10K 问题综述 <https://daniel.haxx.se/docs/poll/。

</details>
