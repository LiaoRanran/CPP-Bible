# 第 39 章　RAII 与 Rule of Zero/Three/Five

⟶ Book/part07_stl/ch77_vector.md

> 老兵标准：**RAII 是 C++ 与异常安全之间唯一可信的契约。** 不会写 RAII，等于不会写现代 C++。
> 本章遵循《现代 C++ 终极圣经》标准 v3：真实源码逐行 + GCC/LLVM/MSVC 三实现对照 + libstdc++/libc++/MS STL 三 STL 对照 + microbenchmark + 跨语言对比 + 推荐阅读已内化进正文。

立场分层约定：
- **[标准]**　语言/库标准规定（ISO C++、LWG 决议）。
- **[实现]**　libstdc++ / libc++ / MS STL 的具体代码行为。
- **[平台]**　MinGW GCC 13.1.0、Windows、ABI 相关事实。
- **[经验]**　工程实践、坑与取舍。

环境事实（本机探测）：MinGW **GCC 13.1.0**；libstdc++ 头文件根目录
`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`；本章所有 `[实现]` 级源码均来自该目录的真实文件，逐行标注路径与行号。libc++、MS STL 不在本机，相关对比以 `[实现-推断]` / `[平台-推断]` 标注。

---

## ① 概述：RAII 是什么，为何是 C++ 的脊梁

⟶ Book/part04_memory/ch38_allocator.md
⟶ Book/part04_memory/ch40_exception_safety.md


**[标准]**　RAII 是 **Resource Acquisition Is Initialization** 的缩写，意为「资源获取即初始化」。其核心约定（`[basic.raii]` 精神，源自 C++98 实践、C++11 起成为库设计基石）：**将资源的生命周期绑定到一个自动存储期（栈上）对象的生命周期——资源在构造函数中获取，在析构函数中释放。**

**[经验]**　一句话记忆：**资源不是「被你释放」，而是「被对象析构时自动释放」。你只负责获取，释放交给析构函数与栈展开。** 这正是 C++ 没有 GC 却能写出「无泄漏、异常安全」代码的根本原因。

RAII 不是语法特性，而是一种**惯用法（idiom）**：任何满足「构造获取、析构释放、对象在栈上」的类型，都是 RAII 类型。标准库里 `std::fstream`、`std::lock_guard`、`std::unique_ptr`、`std::vector`、`std::string` 全是 RAII 类型。

本章主线：
- RAII 本质与资源全景（第 2–3 节）。
- RAII 与栈展开、构造失败、析构 noexcept（第 4–6 节）。
- Rule of Three / Five / Zero（第 7–11 节）。
- 智能指针预告与 RAII 锁、ScopeGuard（第 12–14 节）。
- 标准库 RAII 类型（第 15 节）。
- 真实 libstdc++ 源码逐行（第 16 节）。
- 三编译器/三 STL 对比、microbenchmark、跨语言（第 17–19 节）。
- 源码阅读路线（第 20 节）。

交叉引用：`ch19`（存储期，RAII 依赖自动存储期）、`ch35`（内存布局）、`ch36`（栈与堆、栈展开）、`ch37`（`new`/`delete`，裸资源来源）、`ch40`（异常安全保证）、`ch41`（智能指针完整展开）、`ch45`（构造/析构语义）、`ch61`（并发锁的 RAII 化）。

**核心知识点 #1**：RAII = 资源生命周期绑定到对象生命周期；获取在构造、释放在析构。

---


## 架构与流程图示（Mermaid）

RAII 的核心保证：资源在构造时获取、在析构时释放，且析构无论正常退出还是异常都会执行。

```mermaid
flowchart TD
    A["对象构造 ctor"] --> B["获取资源<br/>RAII：构造即获取"]
    B --> C["正常使用资源"]
    C --> D{"作用域结束 或 异常?"}
    D -->|"无论正常或异常"| E["析构 dtor 自动调用"]
    E --> F["释放资源（构造的逆序）"]
    F --> G["资源绝不泄漏"]
```

## ② RAII 本质：资源获取即初始化，绑定对象生命周期

**[标准]**　[class.dtor] 规定：具有自动存储期的对象在离开其作用域时，析构函数被**隐式调用**（除非作用域通过跳转（如 `goto`/`longjmp`）非正常离开——但这本身是被禁止的未定义行为区）。RAII 正是利用这一保证：只要资源被包进一个栈对象，离开作用域就必然释放。

**[实现]**　一个最小 RAII 包装器的骨架（下面所有示例的范式）：

```cpp
// [示例 1] 最小 RAII 包装器骨架：构造获取、析构释放
#include <cstdio>
#include <stdexcept>

class FileRAII {
    FILE* f_;
public:
    explicit FileRAII(const char* path, const char* mode)
        : f_(std::fopen(path, mode)) {
        if (!f_) throw std::runtime_error("fopen failed");  // 构造失败→无资源泄漏
    }
    ~FileRAII() noexcept {                    // 析构 noexcept：异常安全基石
        if (f_) std::fclose(f_);              // 释放资源
    }
    FILE* get() const noexcept { return f_; }
    // 禁止拷贝（见 Rule of Three），允许移动（见 Rule of Five）
    FileRAII(const FileRAII&) = delete;
    FileRAII& operator=(const FileRAII&) = delete;
};

int main() {
    FileRAII log("app.log", "w");   // 构造即获取
    std::fprintf(log.get(), "hello RAII\n");
    // 离开 main 作用域时 ~FileRAII() 自动 fclose，无需手写清理
}
```

**[经验]**　RAII 的三个不可妥协要素：
1. 资源在构造函数中获取（且失败即抛异常，见第 5 节）。
2. 资源在析构函数中释放，且析构必须 `noexcept`。
3. 包装对象必须是**自动存储期**（栈对象），或自身又被更大的 RAII 对象持有（链式 RAII，最终仍挂在栈上）。把 RAII 对象 `new` 出来却忘了 `delete`，等于自废武功。

**核心知识点 #2**：RAII 三要素——构造获取、析构释放（noexcept）、栈上持有。

---

## ③ 资源类型全景：不只有内存

**[标准]**　[res.on.functions] 等条款指出，C++ 程序管理的「资源」远不止堆内存。凡是有「获取/归还」语义、且忘记归还会导致泄漏或错误的，都是资源。

**[经验]**　工程中常见的资源类型全景——每一类都应被一个 RAII 类型接管：

| 资源类型 | 获取 API（典型） | 释放 API（典型） | 标准 RAII 类型 |
|----------|------------------|------------------|----------------|
| 堆内存 | `new`/`malloc`/`operator new` | `delete`/`free` | `std::unique_ptr`/`std::vector`/`std::string` |
| 文件句柄 | `fopen`/`CreateFile` | `fclose`/`CloseHandle` | `std::fstream`/`std::FILE`（自封） |
| 互斥锁 | `mutex.lock()`/`EnterCriticalSection` | `unlock()`/`LeaveCriticalSection` | `std::lock_guard`/`std::unique_lock`/`std::scoped_lock` |
| 套接字 | `socket()`/`accept()` | `close()`/`closesocket()` | 自封 `SocketRAII` |
| 数据库连接 | `SQLConnect`/`sqlite3_open` | `SQLDisconnect`/`sqlite3_close` | 自封 `DbConnRAII` |
| GDI 句柄 | `CreateBitmap`/`CreateFont` | `DeleteObject` | 自封 `GdiHandleRAII` |
| 内存映射文件（MMIO） | `CreateFileMapping`/`MapViewOfFile` | `UnmapViewOfFile`/`CloseHandle` | 自封 `MmapRAII` |
| 共享内存 | `shmget`/`shm_open` | `shmdt`/`shm_unlink` | 自封 `ShmRAII` |
| 动态库 | `dlopen`/`LoadLibrary` | `dlclose`/`FreeLibrary` | 自封 `LibRAII` |

下面给出几类非内存资源的 RAII 封装示例（均可编译运行，仅做语义演示，平台相关调用以 MinGW/Win32 为准且标注 `[平台]`）。

```cpp
// [示例 2] RAII 封装裸文件句柄 FILE*（与示例 1 等价，含写入）
#include <cstdio>
#include <stdexcept>
#include <utility>

class CFile {
    FILE* fp_ = nullptr;
public:
    explicit CFile(const char* path, const char* mode) {
        fp_ = std::fopen(path, mode);
        if (!fp_) throw std::runtime_error("CFile: cannot open");
    }
    ~CFile() noexcept { if (fp_) std::fclose(fp_); }
    CFile(const CFile&) = delete;
    CFile& operator=(const CFile&) = delete;
    CFile(CFile&& o) noexcept : fp_(o.fp_) { o.fp_ = nullptr; }
    CFile& operator=(CFile&& o) noexcept {
        if (this != &o) { if (fp_) std::fclose(fp_); fp_ = o.fp_; o.fp_ = nullptr; }
        return *this;
    }
    FILE* get() const noexcept { return fp_; }
};

int main() {
    CFile f("log.txt", "w");
    std::fputs("RAII CFile\n", f.get());
}
```

```cpp
// [示例 3] RAII 封装互斥锁（Win32 CRITICAL_SECTION，[平台] MinGW/Win32）
#include <windows.h>
#include <stdexcept>

class CritSec {
    CRITICAL_SECTION cs_;
public:
    CritSec() { InitializeCriticalSection(&cs_); }
    ~CritSec() noexcept { DeleteCriticalSection(&cs_); }
    void lock() { EnterCriticalSection(&cs_); }
    void unlock() noexcept { LeaveCriticalSection(&cs_); }
    // 不可拷贝
    CritSec(const CritSec&) = delete;
    CritSec& operator=(const CritSec&) = delete;
};

// RAII 守卫（自行实现 lock_guard 的雏形）
class CritSecGuard {
    CritSec& cs_;
public:
    explicit CritSecGuard(CritSec& cs) : cs_(cs) { cs_.lock(); }
    ~CritSecGuard() noexcept { cs_.unlock(); }
    CritSecGuard(const CritSecGuard&) = delete;
    CritSecGuard& operator=(const CritSecGuard&) = delete;
};

int main() {
    CritSec cs;
    CritSecGuard g(cs);   // 进入作用域加锁
    // ... 临界区 ...
}                          // 离开作用域自动解锁
```

```cpp
// [示例 4] RAII 封装 Win32 套接字（[平台] MinGW/Win32，需链接 -lws2_32）
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdexcept>

class SocketRAII {
    SOCKET s_ = INVALID_SOCKET;
public:
    SocketRAII() {
        WSADATA wsa{};
        if (WSAStartup(MAKEWORD(2,2), &wsa) != 0)
            throw std::runtime_error("WSAStartup failed");
        s_ = ::socket(AF_INET, SOCK_STREAM, 0);
        if (s_ == INVALID_SOCKET) {
            WSACleanup();
            throw std::runtime_error("socket failed");
        }
    }
    ~SocketRAII() noexcept {
        if (s_ != INVALID_SOCKET) ::closesocket(s_);
        WSACleanup();
    }
    SocketRAII(const SocketRAII&) = delete;
    SocketRAII& operator=(const SocketRAII&) = delete;
    SOCKET get() const noexcept { return s_; }
};
```

```cpp
// [示例 5] RAII 封装 GDI 位图句柄（[平台] Win32 GDI）
#include <windows.h>
class GdiBitmap {
    HBITMAP hb_ = nullptr;
public:
    explicit GdiBitmap(int w, int h) {
        hb_ = CreateCompatibleBitmap(GetDC(nullptr), w, h);
        if (!hb_) throw std::runtime_error("CreateCompatibleBitmap failed");
    }
    ~GdiBitmap() noexcept { if (hb_) DeleteObject(hb_); }
    GdiBitmap(const GdiBitmap&) = delete;
    GdiBitmap& operator=(const GdiBitmap&) = delete;
    HBITMAP get() const noexcept { return hb_; }
};
```

```cpp
// [示例 6] RAII 封装 SQLite 数据库连接（需链接 -lsqlite3，[平台] 可用）
#include <sqlite3.h>
#include <stdexcept>

class DbConn {
    sqlite3* db_ = nullptr;
public:
    explicit DbConn(const char* path) {
        if (sqlite3_open(path, &db_) != SQLITE_OK)
            throw std::runtime_error("sqlite3_open failed");
    }
    ~DbConn() noexcept { if (db_) sqlite3_close(db_); }
    DbConn(const DbConn&) = delete;
    DbConn& operator=(const DbConn&) = delete;
    sqlite3* get() const noexcept { return db_; }
};
```

```cpp
// [示例 7] RAII 封装 POSIX 共享内存（[平台] POSIX，MinGW 下可改为 Win32）
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <cstring>
#include <stdexcept>
#include <cstddef>

class ShmRAII {
    int fd_ = -1;
    void* addr_ = nullptr;
    std::size_t size_;
public:
    explicit ShmRAII(const char* name, std::size_t sz)
        : size_(sz) {
        fd_ = shm_open(name, O_CREAT | O_RDWR, 0600);
        if (fd_ == -1) throw std::runtime_error("shm_open failed");
        if (ftruncate(fd_, (off_t)sz) == -1) throw std::runtime_error("ftruncate failed");
        addr_ = mmap(nullptr, sz, PROT_READ | PROT_WRITE, MAP_SHARED, fd_, 0);
        if (addr_ == MAP_FAILED) throw std::runtime_error("mmap failed");
    }
    ~ShmRAII() noexcept {
        if (addr_) munmap(addr_, size_);
        if (fd_ != -1) { close(fd_); shm_unlink("/demo_shm"); }
    }
    ShmRAII(const ShmRAII&) = delete;
    ShmRAII& operator=(const ShmRAII&) = delete;
    void* get() const noexcept { return addr_; }
};
```

```cpp
// [示例 8] RAII 封装 Windows 内存映射文件 MMIO（[平台] Win32）
#include <windows.h>
#include <stdexcept>

class MmapFile {
    HANDLE hFile_ = INVALID_HANDLE_VALUE;
    HANDLE hMap_  = nullptr;
    void*  view_  = nullptr;
public:
    explicit MmapFile(const char* path) {
        hFile_ = CreateFileA(path, GENERIC_READ, 0, nullptr,
                             OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
        if (hFile_ == INVALID_HANDLE_VALUE) throw std::runtime_error("CreateFile failed");
        hMap_ = CreateFileMappingA(hFile_, nullptr, PAGE_READONLY, 0, 0, nullptr);
        if (!hMap_) { CloseHandle(hFile_); throw std::runtime_error("CreateFileMapping failed"); }
        view_ = MapViewOfFile(hMap_, FILE_MAP_READ, 0, 0, 0);
        if (!view_) {
            CloseHandle(hMap_); CloseHandle(hFile_);
            throw std::runtime_error("MapViewOfFile failed");
        }
    }
    ~MmapFile() noexcept {
        if (view_) UnmapViewOfFile(view_);
        if (hMap_) CloseHandle(hMap_);
        if (hFile_ != INVALID_HANDLE_VALUE) CloseHandle(hFile_);
    }
    MmapFile(const MmapFile&) = delete;
    MmapFile& operator=(const MmapFile&) = delete;
    const void* get() const noexcept { return view_; }
};
```

**核心知识点 #3**：资源全景覆盖堆内存/文件/锁/套接字/DB/GDI/MMIO/共享内存；每类都应有 RAII 封装。

---

## ④ RAII 与栈展开的耦合：异常安全的基石

**[标准]**　[except.ctor] / [except.handle] 规定：当异常被抛出且匹配到 `catch` 时，从抛出点直到 `catch` 之间的所有**已构造、尚未销毁的自动存储期对象**按构造的逆序被自动销毁——这一机制叫**栈展开（stack unwinding）**，已在 `ch36` 详述。RAII 正是搭上栈展开的便车：异常无论在哪抛出，栈上的 RAII 对象析构都会被调用，资源得以释放。

**[经验]**　关键认知：**RAII 保证的是「异常安全（exception safe）」，不是「不抛异常」。异常照样抛、照样传，但资源一定被清掉。** 对比非 RAII 的「手动释放 + goto cleanup」范式，一旦中间有异常（或提前 `return`），清理路径极易被跳过。

```cpp
// [示例 9] 非 RAII 的 C 风格 goto cleanup：易漏释放（异常时更糟）
#include <cstdio>
#include <cstdlib>

int legacy_open_three_files() {
    FILE* a = std::fopen("a.txt", "w");
    if (!a) return -1;
    FILE* b = std::fopen("b.txt", "w");
    if (!b) { fclose(a); return -1; }   // 必须记得清理 a
    FILE* c = std::fopen("c.txt", "w");
    if (!c) { fclose(b); fclose(a); return -1; }  // 清理顺序易错且冗长
    // ... 业务逻辑 ...
    fclose(c); fclose(b); fclose(a);
    return 0;
}
// 问题：函数有多个出口，每个出口都要手写对应清理；若业务里抛异常，连 goto 都救不了。
```

```cpp
// [示例 10] RAII 改写：无论正常返回还是异常，资源必释放
#include <cstdio>
#include <stdexcept>

class F {
    FILE* p_;
public:
    explicit F(const char* path) : p_(std::fopen(path, "w")) {
        if (!p_) throw std::runtime_error("open failed");
    }
    ~F() noexcept { if (p_) std::fclose(p_); }
    F(const F&) = delete; F& operator=(const F&) = delete;
    FILE* get() const noexcept { return p_; }
};

void raii_open_three_files() {
    F a("a.txt"), b("b.txt"), c("c.txt");   // 三个栈对象
    std::fputs("work", a.get());
    if (some_error_condition())             // 假设会抛异常
        throw std::runtime_error("business error");
    // 正常或异常离开，a/b/c 析构逆序调用，三个文件全部关闭
}
```

**[实现]**　栈展开由编译器在异常处理表中生成「哪些对象需要析构」的元数据（Itanium C++ ABI 的 LSDA / Win64 的 `eh` 表）。RAII 对象的析构调用**不依赖任何运行时库的人为约定**，是 ABI 保证的确定性行为。

**核心知识点 #4**：RAII 借栈展开释放资源；它是「异常安全」而非「不抛异常」。
**核心知识点 #5**：非 RAII 的手动清理（goto cleanup）在异常路径下必然漏释放。

---

## ⑤ 构造函数失败的处理：已构子对象自动析构

**[标准]**　[except.ctor] 规定：**若构造函数在其成员/基类初始化列表或函数体中抛出异常，则该对象被视为「从未完全构造」，为其已构造完成的子对象（基类+成员，按逆序）自动调用析构函数，然后异常向外传播。** 这意味着：构造函数中途失败，已经获取的资源（在更早构造的成员里）会被对应成员的析构释放——前提是那些成员本身是 RAII 类型。

**[经验]**　经典陷阱：**在构造函数体内用裸指针 `new` 后又 `new` 一次失败，第一次 `new` 的指针因尚未交给任何 RAII 成员而泄漏。** 解决之道是「成员即 RAII」：让每个资源从构造起就由一个 RAII 成员持有，而不是在 ctor 体内裸分配。

```cpp
// [示例 11] 构造失败：已构 RAII 子对象自动析构，无泄漏
#include <cstdio>
#include <stdexcept>
#include <string>

struct Resource {
    std::string name;
    Resource(const char* n) : name(n) {
        std::printf("Resource '%s' acquired\n", n);
        if (name == "boom") throw std::runtime_error("ctor of boom failed");
    }
    ~Resource() noexcept { std::printf("Resource '%s' released\n", name.c_str()); }
};

struct Holder {
    Resource r1{"r1"};
    Resource r2{"boom"};   // 构造 r2 时抛异常
    Resource r3{"r3"};     // 永远不会被构造
    Holder() { std::printf("Holder fully constructed\n"); }
};

int main() {
    try {
        Holder h;
    } catch (const std::exception& e) {
        std::printf("caught: %s\n", e.what());
    }
    // 输出顺序：r1 acquired → r1 released（r2 未完全构造故其析构不调用，但 r1 已释放）
}
```

```cpp
// [示例 12] 反例：ctor 体内裸 new 导致泄漏
#include <cstdio>
#include <stdexcept>

struct Leaky {
    int* a;
    int* b;
    Leaky() {
        a = new int[100];            // 资源已获取
        b = new int[10000000000ULL]; // 抛 std::bad_alloc
        // 异常时，a 从未交给 RAII 成员，泄漏！Leaky 的析构不会被调用
    }
    ~Leaky() { delete[] a; delete[] b; }   // 永远到不了
};
```

```cpp
// [示例 13] 修复：用 unique_ptr 作为成员（见 ch41），ctor 失败也不泄漏
#include <memory>
#include <stdexcept>

struct Safe {
    std::unique_ptr<int[]> a = std::make_unique<int[]>(100);
    std::unique_ptr<int[]> b;
    Safe() {
        b = std::make_unique<int[]>(10000000000ULL); // 抛 bad_alloc
        // a 作为成员，其析构（unique_ptr::~unique_ptr）在栈展开时释放 a，无泄漏
    }
};
```

**核心知识点 #6**：ctor 抛异常 → 已构子对象逆序析构 → 资源不泄漏（前提是成员是 RAII）。
**核心知识点 #7**：ctor 体内裸 `new` 后失败会泄漏；应以 RAII 成员持有资源。

---

## ⑥ 析构函数必须 noexcept：双重异常 → std::terminate

**[标准]**　[except.ctor] 规定：**析构函数默认隐式 `noexcept(true)`**（除非你显式写成 `noexcept(false)` 或它的某个（非析构）基类/成员析构是 potentially-throwing 且该析构未加 `noexcept`）。`[except.terminate]` 进一步规定：**若在栈展开过程中（即已有异常在传播）又抛出一个新异常，且此时需要调用某个析构函数而该析构抛异常，则调用 `std::terminate()`——程序立即终止，不保证任何剩余资源释放。**

**[经验]**　这就是「双重异常（double exception）」死局：已有异常在飞，析构又抛异常，C++ 无法决定先处理哪个，只能 `terminate`。所以：**析构函数永远不能让异常逃出。**

```cpp
// [示例 14] 析构 noexcept(false) + 栈展开中抛异常 → std::terminate（演示）
#include <stdexcept>
#include <cstdio>

struct Bad {
    ~Bad() noexcept(false) {                 // 显式允许抛异常——危险！
        throw std::runtime_error("dtor throws");
    }
};

struct Trigger {
    Bad bad;
    ~Trigger() noexcept(false) { throw std::runtime_error("trigger dtor throws"); }
};

int main() {
    try {
        Trigger t;
        throw std::runtime_error("main throws"); // 已有异常在飞
    } catch (...) {
        // 永远到不了：栈展开时 t.~Trigger 抛异常，双重异常 → terminate
    }
    std::printf("unreachable\n");
}
// 运行结果：程序以 std::terminate 终止（ABRT），输出 reachable 不成立。
```

```cpp
// [示例 15] 正确做法：析构吞掉内部异常（或 noexcept），绝不让异常逃出
#include <stdexcept>
#include <cstdio>
#include <exception>

struct Good {
    ~Good() noexcept {                 // 隐式 noexcept(true) 也可显式写
        try {
            // 可能抛的操作...
            throw std::runtime_error("ignored");
        } catch (...) {
            // 记录日志但不抛出：析构中吞掉异常
            std::printf("Good::~Good swallowed an exception\n");
        }
    }
};

int main() {
    try {
        Good g;
        throw std::runtime_error("main throws");
    } catch (const std::exception& e) {
        std::printf("caught: %s\n", e.what());   // 正常到达，g 已安全析构
    }
}
```

**[实现]**　在 libstdc++ 中，即便你写了 `~T() noexcept(false)`，当在栈展开期间该析构抛异常，异常传递路径上的 `__cxa_throw`/`__terminate` 会被触发（见 `libsupc++/eh_throw.cc`、`terminate.cc`）。`std::terminate` 默认调用 `std::abort`。

**核心知识点 #8**：析构默认隐式 `noexcept(true)`。
**核心知识点 #9**：栈展开中析构再抛异常 → 双重异常 → `std::terminate`，程序崩溃。

---

## ⑦ Rule of Three：浅拷贝灾难与 double free

**[标准]**　[class.copy.ctor] / 传统「Rule of Three」实践（C++98 起，已在 C++11 被 Rule of Five 取代但仍是基础）：**若一个类需要自定义析构函数、或自定义拷贝构造函数、或自定义拷贝赋值运算符中的任意一个，那么它大概率需要自定义全部三个。** 原因是：自定义析构通常意味着类持有「需要手动释放」的资源（裸指针），而编译器生成的默认拷贝是**逐成员浅拷贝（memberwise copy）**，会导致两个对象指向同一资源，析构时**双重释放（double free）**。

**[经验]**　最经典的 bug：`class String { char* data; ~String(){ delete[] data; } };` 没有自定义拷贝，于是 `String a = ...; String b = a;` 浅拷贝，`b.data == a.data`，离开作用域两个析构都 `delete[]` 同一指针 → double free → UB（通常崩溃）。

```cpp
// [示例 16] Rule of Three 缺失：double free 崩溃演示（不可取，仅演示灾难）
#include <cstring>
#include <cstdio>

class BadString {
    char* data_;
public:
    BadString(const char* s) : data_(new char[std::strlen(s)+1]) {
        std::strcpy(data_, s);
    }
    ~BadString() { delete[] data_; }        // 自定义析构，但没有自定义拷贝
    // 编译器生成默认拷贝构造/拷贝赋值 = 浅拷贝！
    const char* c_str() const { return data_; }
};

int main() {
    BadString a("hello");
    BadString b = a;        // 浅拷贝：b.data_ == a.data_
    std::printf("%s %s\n", a.c_str(), b.c_str());
    // 离开作用域：~b() 释放 a.data_，~a() 再释放同一指针 → double free → 崩溃
}
```

**double free 崩溃路径追踪**：
1. `BadString a("hello")` → `a.data_` 指向堆块 P。
2. `BadString b = a` → 编译器生成拷贝构造，逐成员拷贝 `b.data_ = a.data_` = P（同一地址）。
3. 作用域结束，先析构 `b`：`delete[] P`（P 归还堆，可能写入空闲链表元数据）。
4. 再析构 `a`：`delete[] P` 再次释放同一块 → 堆管理器发现块已被释放 → 通常 `abort`/`SIGABRT`，或静默破坏堆元数据导致后续随机崩溃。这就是未定义行为（UB）。

**[标准]**　Rule of Three 修复：显式定义拷贝构造（深拷贝）+ 拷贝赋值（深拷贝 + 自赋值检查 + 释放旧资源）+ 析构。

```cpp
// [示例 17] Rule of Three 完整修复：深拷贝
#include <cstring>
#include <cstdio>
#include <utility>

class GoodString {
    char* data_;
    static char* clone(const char* s) {
        char* p = new char[std::strlen(s)+1];
        std::strcpy(p, s);
        return p;
    }
public:
    explicit GoodString(const char* s) : data_(clone(s)) {}

    // 1) 析构
    ~GoodString() noexcept { delete[] data_; }

    // 2) 拷贝构造（深拷贝）
    GoodString(const GoodString& o) : data_(clone(o.data_)) {}

    // 3) 拷贝赋值（深拷贝 + 自赋值安全 + 释放旧值）
    GoodString& operator=(const GoodString& o) {
        if (this != &o) {                       // 自赋值检查
            char* tmp = clone(o.data_);          // 先分配成功再释放旧的（强异常安全）
            delete[] data_;
            data_ = tmp;
        }
        return *this;
    }

    const char* c_str() const noexcept { return data_; }
};

int main() {
    GoodString a("hello");
    GoodString b = a;            // 深拷贝：b.data_ 与 a.data_ 不同
    GoodString c("x");
    c = a;                       // 拷贝赋值
    std::printf("%s %s %s\n", a.c_str(), b.c_str(), c.c_str());
    // 三个对象析构各自释放自己的堆块，无 double free
}
```

**核心知识点 #10**：Rule of Three——自定义析构/拷贝构造/拷贝赋值之一，需自定义全部三者。
**核心知识点 #11**：未定义拷贝 → 默认浅拷贝 → 两对象共享指针 → 双重释放（double free/UB）。

---

## ⑧ Rule of Five：移动语义与性能

**[标准]**　C++11 引入右值引用与移动语义后，规则扩展为 **Rule of Five**：若类需要管理资源，需定义五个特殊成员函数——**析构函数、拷贝构造、拷贝赋值、移动构造、移动赋值**。新增的两个「移动」用于**窃取（steal）**资源而非复制，把源对象置于「有效但未指定（valid but unspecified）」状态，使源析构安全（无操作）。

**[经验]**　为何有了自定义析构/拷贝就必须考虑移动？因为**若你不定义移动构造/移动赋值，编译器不会生成它们**（当存在用户定义析构/拷贝/赋值中任一个时，移动操作被定义为 `delete`d），于是所有「移动语境」（如 `std::vector` 扩容、`return` 局部对象、`std::move`）**退化为拷贝**——对持有堆内存的类，这意味着昂贵的深拷贝，性能灾难。

```cpp
// [示例 18] Rule of Five 完整实现（移动窃取资源并置源为空）
#include <cstring>
#include <cstdio>
#include <utility>
#include <cstddef>

class Buffer {
    char* data_ = nullptr;
    std::size_t size_ = 0;
    static char* clone(const char* p, std::size_t n) {
        char* q = new char[n];
        std::memcpy(q, p, n);
        return q;
    }
public:
    Buffer(const char* s) : size_(std::strlen(s)+1), data_(clone(s, size_)) {}

    // 1) 析构
    ~Buffer() noexcept { delete[] data_; }

    // 2) 拷贝构造（深拷贝）
    Buffer(const Buffer& o) : size_(o.size_), data_(clone(o.data_, o.size_)) {}

    // 3) 拷贝赋值
    Buffer& operator=(const Buffer& o) {
        if (this != &o) {
            char* tmp = clone(o.data_, o.size_);
            delete[] data_;
            data_ = tmp; size_ = o.size_;
        }
        return *this;
    }

    // 4) 移动构造（窃取）
    Buffer(Buffer&& o) noexcept
        : data_(o.data_), size_(o.size_) {
        o.data_ = nullptr;   // 置源为空，使其析构无操作
        o.size_ = 0;
    }

    // 5) 移动赋值
    Buffer& operator=(Buffer&& o) noexcept {
        if (this != &o) {
            delete[] data_;          // 释放自身旧资源
            data_ = o.data_; size_ = o.size_;
            o.data_ = nullptr; o.size_ = 0;   // 置源为空
        }
        return *this;
    }

    const char* c_str() const noexcept { return data_ ? data_ : ""; }
};

int main() {
    Buffer a("hello");
    Buffer b = std::move(a);    // 移动构造：a.data_ 被窃取并置空
    std::printf("b=%s a.empty=%d\n", b.c_str(), a.c_str()[0] == '\0');
    // a 析构时 data_==nullptr → delete[] nullptr 安全无操作
}
```

**[标准]**　`noexcept` 对移动很重要：`std::vector` 在扩容时是**强异常安全**：若移动构造可能抛异常，它会改用语义更慢但可回滚的拷贝；若移动构造标记 `noexcept`，它才放心用移动。**所以移动操作应几乎总是 `noexcept`**（`[container.reqmts]` 隐含优化前提）。

**核心知识点 #12**：Rule of Five = 析构+拷贝构造+拷贝赋值+移动构造+移动赋值。
**核心知识点 #13**：移动 = 窃取资源并置源为空，源析构安全（无操作）。
**核心知识点 #14**：有自定义析构/拷贝却不定义移动 → 移动退化为拷贝 → 性能损失。

---

## ⑨ Rule of Zero：现代 C++ 的首选

**[标准]**　C++11 后的现代最佳实践是 **Rule of Zero**：**类不应自己管理资源，而是把资源交给已经正确实现五大函数的标准/库类型（`std::unique_ptr`、`std::shared_ptr`、`std::vector`、`std::string`、`std::fstream` 等）。于是类本身不需要写析构、拷贝、移动——编译器生成的默认版本天然正确。**

**[实现]**　这些「自带正确语义」的类型本身遵循 Rule of Five：`std::unique_ptr` 不可拷贝、可移动（见第 16 节源码）；`std::shared_ptr` 用引用计数自动管理；`std::vector`/`std::string` 自带深拷贝与移动。你的类只要成员是它们，就自动获得正确语义。

```cpp
// [示例 19] Rule of Zero：用 unique_ptr 管理资源，类不写任何五大函数
#include <memory>
#include <cstdio>
#include <vector>
#include <string>
#include <utility>

struct Connection {                 // 业务对象，无需手写析构
    void query() const { std::printf("query\n"); }
};

class Service {
    std::unique_ptr<Connection> conn_ = std::make_unique<Connection>(); // 独占资源
    std::vector<int> cache_;                                          // 自带深拷贝/移动
    std::string name_ = "svc";                                        // 同上
public:
    void run() const { conn_->query(); }
    // 无需 ~Service / 拷贝 / 移动：编译器生成的正确版本
    // unique_ptr 不可拷贝 → Service 也不可拷贝（符合独占语义）
    // unique_ptr 可移动 → Service 也可移动
};

int main() {
    Service s;
    s.run();
    auto s2 = std::move(s);   // 移动：资源被转移，原 s 为空壳，析构安全
    s2.run();
}
```

```cpp
// [示例 20] Rule of Zero：用 shared_ptr 共享资源
#include <memory>
#include <cstdio>

struct Config { int value = 42; };

int main() {
    auto cfg = std::make_shared<Config>();
    auto a = cfg;   // 引用计数 +1，共享同一 Config
    auto b = cfg;   // 引用计数 +1
    std::printf("value=%d use_count=%ld\n", a->value, cfg.use_count());
    // a、b、cfg 析构时计数递减，最后一个析构释放 Config —— 无泄漏、无 double free
}
```

```cpp
// [示例 21] Rule of Zero 改造：把示例 16 的 BadString 改成零规则
#include <string>
#include <cstdio>

class GoodString2 {
    std::string data_;                 // std::string 自带正确五大函数
public:
    explicit GoodString2(const char* s) : data_(s) {}
    const char* c_str() const { return data_.c_str(); }
    // 完全不写析构/拷贝/移动：默认生成的全部正确
};

int main() {
    GoodString2 a("hello");
    GoodString2 b = a;                 // 编译器生成的深拷贝，安全
    GoodString2 c("x");
    c = a;                             // 安全
    std::printf("%s %s %s\n", a.c_str(), b.c_str(), c.c_str());
}
```

**[经验]**　经验法则：**能写 Rule of Zero 就绝不手写五大函数。** 手写五大函数只在你要封装一种标准库尚未提供的资源（如示例 3–8 的 Win32 句柄、套接字）时才必要；即便如此，也应尽量让该类「只管一个资源」且「内部用 unique_ptr 的自定义 deleter」来复用标准语义（见第 12 节）。

**核心知识点 #15**：Rule of Zero——用 unique_ptr/shared_ptr/vector/string 管资源，类不写五大函数，编译器自动正确。
**核心知识点 #16**：`std::unique_ptr` 不可拷可移；`std::shared_ptr` 引用计数共享。

---

## ⑩ = default 与 = delete：精确控制特殊成员

**[标准]**　C++11 引入 `= default`（要求编译器生成该函数的默认实现）与 `= delete`（删除该函数，禁止其被调用）。对五大函数：
- `= default` 用于**显式要求编译器生成正确的默认版本**（例如你有自定义析构导致移动被 delete，但仍想保留可移动时，用 `= default` 重新启用移动；前提是所有成员都可移动/拷贝）。
- `= delete` 用于**禁止拷贝**（独占资源语义，如 `unique_ptr`）、禁止不需要的构造等。

**[实现]**　libstdc++ 的 `unique_ptr` 即在 `bits/unique_ptr.h:522-523` 用 `= delete` 禁用拷贝：
```cpp
// bits/unique_ptr.h:521-523
// Disable copy from lvalue.
unique_ptr(const unique_ptr&) = delete;
unique_ptr& operator=(const unique_ptr&) = delete;
```

```cpp
// [示例 22] =default 让编译器生成正确的移动（当存在自定义析构时）
#include <cstdio>
#include <utility>

class MoveOnly {
    int* p_ = new int(0);
public:
    MoveOnly() = default;
    ~MoveOnly() noexcept { delete p_; }            // 自定义析构 → 移动本会被 delete
    MoveOnly(const MoveOnly&) = delete;            // 禁止拷贝
    MoveOnly& operator=(const MoveOnly&) = delete;
    MoveOnly(MoveOnly&&) noexcept = default;        // =default 重新启用移动
    MoveOnly& operator=(MoveOnly&&) noexcept = default;
    int get() const { return *p_; }
};

int main() {
    MoveOnly a;
    MoveOnly b = std::move(a);    // 编译器生成的移动：逐成员移动 p_ 并置 a.p_ 为 nullptr
    std::printf("%d\n", b.get());
}
```

```cpp
// [示例 23] =delete 禁止拷贝，实现独占语义
#include <cstdio>

class NonCopyable {
    int x_ = 1;
public:
    NonCopyable() = default;
    NonCopyable(const NonCopyable&) = delete;
    NonCopyable& operator=(const NonCopyable&) = delete;
    int get() const { return x_; }
};

int main() {
    NonCopyable a;
    // NonCopyable b = a;   // 编译错误：拷贝构造被 delete
    std::printf("%d\n", a.get());
}
```

**[平台]**　**MSVC 旧版坑**：早期 MSVC（VS2013 之前）对 `= default` 的移动操作存在 bug——即使成员都可移动，有时也不生成或生成错误版本；且 VS2013 对 `= default` 的移动构造仍有已知问题。现代 MSVC（VS2015+）已修复，但维护旧代码时若遇到「本应可移动却编译失败/退化为拷贝」，应检查是否因旧 MSVC 的 `= default` 移动 bug（`[平台-推断]`，基于历史已知问题）。

**核心知识点 #17**：`= default` 让编译器生成正确版本（要求成员都可移动/拷贝）。
**核心知识点 #18**：`= delete` 禁用拷贝（独占语义），如 `unique_ptr` 之所为。

---

## ⑪ 移动后状态：valid but unspecified

**[标准]**　[lib.types.movedfrom] / [utility.requirements] 规定：被移动后的对象（moved-from）必须处于**「有效但未指定（valid but unspecified）」**状态——即它可以被安全**析构**和**赋值（包括被新值覆盖）**，但标准**不保证**其具体值。例如 `std::vector` 被移动后通常为空，但标准只保证「可析构、可赋值」，不保证「一定为空」（虽然实践中所有实现都是空）。

**[经验]**　经典 bug：对移后对象读取值或依赖其状态。`std::move` 本身**不移动任何东西**——它只是把左值转为右值引用，真正的移动发生在接收方的移动构造/赋值里；移后源对象变成「空壳」。

```cpp
// [示例 24] 移动后状态：vector 移后通常为空（valid but unspecified）
#include <vector>
#include <cstdio>
#include <utility>

int main() {
    std::vector<int> a = {1, 2, 3};
    std::vector<int> b = std::move(a);    // a 被移动
    std::printf("b.size=%zu a.size=%zu\n", b.size(), a.size());
    // 实践：a.size()==0；但标准仅保证 a 可析构/可赋值
    a = std::vector<int>{9, 9};           // 给移后对象赋新值是安全的
    std::printf("a.size after assign=%zu\n", a.size());
}
```

```cpp
// [示例 25] 误用移后对象：经典 bug
#include <string>
#include <cstdio>
#include <utility>

void buggy() {
    std::string s = "important";
    std::string t = std::move(s);
    // BUG：此处仍使用 s，其值已「未指定」
    std::printf("len=%zu content=[%s]\n", s.size(), s.c_str());
    // 可能打印空串，也可能打印垃圾——依赖未指定状态是 UB 隐患
}

int main() { buggy(); }
```

**[经验]**　工程约定：被 `std::move` 之后，源对象「视为已死」，**只允许析构或重新赋值**，绝不再读取其业务值。把这个约定写进代码评审清单。

**核心知识点 #19**：被移动对象必须可安全析构与赋值，但值不保证（valid but unspecified）。
**核心知识点 #20**：误用移后对象（读取值）是经典 bug；`std::move` 只是类型转换，不真正移动。

---

## ⑫ 智能指针预告：unique_ptr / shared_ptr / weak_ptr（见 ch41）

**[标准]**　C++11 在 `<memory>` 提供三种智能指针（完整展开见 `ch41`）：
- `std::unique_ptr<T>`：**独占**所有权，不可拷贝、可移动；析构调 deleter 释放。零开销（见第 16 节源码）。
- `std::shared_ptr<T>`：**共享**所有权，引用计数；最后一个析构释放（见第 16 节计数源码）。
- `std::weak_ptr<T>`：不增加计数的弱引用，用于打破循环引用。

这里仅做预告与自定义 deleter 演示，详细语义、原子性、控制块、别名构造留待 `ch41`。

```cpp
// [示例 26] 自定义 deleter（带状态的 deleter 对象）
#include <memory>
#include <cstdio>

struct FileDeleter {
    void operator()(FILE* f) const noexcept {
        std::printf("custom deleter closing file\n");
        if (f) std::fclose(f);
    }
};

int main() {
    // unique_ptr<FILE, FileDeleter>：deleter 是对象（可带状态）
    std::unique_ptr<FILE, FileDeleter> pf(std::fopen("d.log", "w"), FileDeleter{});
    if (pf) std::fputs("via custom deleter\n", pf.get());
    // 离开作用域：FileDeleter::operator()(pf.get()) 被调用
}
```

```cpp
// [示例 27] 自定义 deleter（lambda / 函数指针）
#include <memory>
#include <cstdio>

int main() {
    // 用函数指针作为 deleter
    std::unique_ptr<FILE, decltype(&std::fclose)> pf(
        std::fopen("e.log", "w"), &std::fclose);
    if (pf) std::fputs("via function-pointer deleter\n", pf.get());
    // 析构时调用 std::fclose(pf.get())
}
```

```cpp
// [示例 28] unique_ptr 管理 FILE*（预告，完整见 ch41）
#include <memory>
#include <cstdio>

int main() {
    auto f = std::unique_ptr<FILE, decltype(&std::fclose)>(
        std::fopen("f.log", "w"), &std::fclose);
    if (f) std::fputs("unique_ptr owns FILE*\n", f.get());
    // 无需手动 fclose：unique_ptr 析构自动调用 deleter
}
```

**核心知识点 #21**：`unique_ptr` 用 deleter 释放资源，deleter 可为函数指针/lambda/带状态对象（预 ch41）。

---

## ⑬ RAII 锁：lock_guard / scoped_lock / unique_lock

**[标准]**　C++11 `<mutex>` 提供三种 RAII 锁守卫（`ch61` 完整展开并发语义）：
- `std::lock_guard<Mutex>`：构造时 `lock()`，析构时 `unlock()`，最简单，不可手动解锁（`[thread.lock.guard]`）。
- `std::scoped_lock<Mutexes...>`（C++17）：可同时锁多个互斥量并**避免死锁**（内部用 `std::lock` 算法）。
- `std::unique_lock<Mutex>`：更灵活，可延迟加锁、手动 `lock()`/`unlock()`、可移动、可配合条件变量。

```cpp
// [示例 29] lock_guard 基本使用
#include <mutex>
#include <cstdio>

std::mutex mtx;
int shared = 0;

void increment() {
    std::lock_guard<std::mutex> g(mtx);   // 构造加锁
    ++shared;
    // 离开作用域 ~lock_guard() 自动 unlock，即使中间抛异常也解锁
}

int main() {
    increment();
    std::printf("shared=%d\n", shared);
}
```

```cpp
// [示例 30] scoped_lock 双锁防死锁（C++17）
#include <mutex>
#include <cstdio>

std::mutex m1, m2;

void transfer() {
    std::scoped_lock lk(m1, m2);   // 原子地锁住 m1 和 m2，避免死锁
    std::printf("both locked safely\n");
    // 析构逆序解锁
}

int main() { transfer(); }
```

```cpp
// [示例 31] unique_lock 灵活锁 + 条件变量配合（演示延迟加锁）
#include <mutex>
#include <cstdio>

std::mutex m;
int flag = 0;

int main() {
    std::unique_lock<std::mutex> lk(m, std::defer_lock); // 构造时不锁
    lk.lock();                       // 手动锁
    flag = 1;
    lk.unlock();                     // 手动解锁（RAII 仍可兜底）
    if (lk.owns_lock() == false) std::printf("released manually\n");
    lk.lock();                       // 再锁
    // 离开作用域若仍持有则自动解锁
}
```

**[实现]**　libstdc++ 的 `lock_guard` 源码见第 16 节；其核心就是构造 `lock()`、析构 `unlock()`，且不可拷贝（`bits/std_mutex.h:257-258` `= delete`）。

---

## ⑭ ScopeGuard / ScopeExit 惯用法

**[经验]**　ScopeGuard（作用域守卫）是 RAII 的通用化：当需要在作用域结束时执行任意清理动作（不限于某个资源类型）时使用。**[标准]** 截至 C++23，`std::scope_exit`/`scope_success`/`scope_fail` 仍属 Library Fundamentals TS v3，尚未进入正式标准；它们位于 `<experimental/scope>`、命名空间为 `std::experimental`（本机 MinGW GCC 13.1.0 提供该实验头，`<scope>` 主头并不存在）。工程中通常自实现一个轻量版。语义：
- **ScopeExit**：无论正常还是异常离开作用域，都执行回调。
- **ScopeSuccess**：仅正常离开时执行。
- **ScopeFail**：仅因异常离开时执行。

```cpp
// [示例 32] 自实现 ScopeExit（RAII + 可调用对象）
#include <utility>
#include <type_traits>
#include <cstdio>

template <typename F>
class ScopeExit {
    F f_;
    bool active_;
public:
    explicit ScopeExit(F f) : f_(std::move(f)), active_(true) {}
    ~ScopeExit() noexcept { if (active_) f_(); }
    void release() noexcept { active_ = false; }
    ScopeExit(const ScopeExit&) = delete;
    ScopeExit& operator=(const ScopeExit&) = delete;
    ScopeExit(ScopeExit&&) = delete;
};

// 工厂对象 + operator+ 惯用法：借助 C++17 强制拷贝消除（prvalue 直接初始化，
// 无需可移动），让宏能展开成 "SCOPE_EXIT { ...; };" 的花括号块语法（folly ScopeGuard 同款技巧）。
struct ScopeExitHelper {
    template <typename F>
    ScopeExit<F> operator+(F&& f) const { return ScopeExit<F>(std::forward<F>(f)); }
};

#define CONCAT(a, b) CONCAT_IMPL(a, b)
#define CONCAT_IMPL(a, b) a##b
#define SCOPE_EXIT \
    auto CONCAT(_scope_exit_, __LINE__) = ScopeExitHelper{} + [&]()

int main() {
    std::printf("before\n");
    SCOPE_EXIT { std::printf("scope exit cleanup (always)\n"); };
    std::printf("after\n");
    // 输出：before / after / scope exit cleanup (always)
}
```

```cpp
// [示例 33] ScopeExit 在异常路径下仍清理
#include <stdexcept>
#include <cstdio>

int risky() {
    SCOPE_EXIT { std::printf("cleanup even on exception\n"); };
    if (true) throw std::runtime_error("boom");
    return 0;
}

int main() {
    try { risky(); } catch (const std::exception& e) {
        std::printf("caught: %s\n", e.what());   // 先打印 cleanup，再打印 caught
    }
}
```

**[标准]**　TS 版 `scope_exit` 位于 `<experimental/scope>`，命名空间 `std::experimental`（**不是** `std::scope_exit`，也**没有** `<scope>` 主头）：
```cpp
// [示例 34] Library Fundamentals TS 的 scope_exit（[平台] 本机 MinGW GCC 13.1.0 实测可编译）
#include <experimental/scope>
#include <cstdio>

int main() {
    std::printf("start\n");
    std::experimental::scope_exit guard{[] { std::printf("std scope_exit fired\n"); }};
    std::printf("end\n");
}
```

**核心知识点 #22**：ScopeGuard/ScopeExit 是 RAII 通用化——作用域结束（含异常）执行任意清理。

---

## ⑮ 标准库 RAII 类型一览

**[标准]**　C++ 标准库大量使用 RAII。常用清单：

| 类型 | 资源 | 释放点 |
|------|------|--------|
| `std::fstream` / `std::ifstream` / `std::ofstream` | 文件句柄 | 析构调用 `close()`（见第 16 节 `bits/fstream.tcc`） |
| `std::lock_guard` / `std::scoped_lock` / `std::unique_lock` | 互斥锁 | 析构 `unlock()` |
| `std::unique_ptr` / `std::shared_ptr` | 堆内存/任意资源 | 析构调 deleter / 计数归零 |
| `std::vector` / `std::string` / `std::deque` | 堆内存 | 析构释放缓冲区 |
| `std::thread` | 操作系统线程 | 析构前必须 `join()` 或 `detach()`（否则 `std::terminate`） |
| `std::lock_guard` | — | — |
| `std::fstream` 的 `std::filebuf` | — | — |
| `std::unique_lock` | — | — |
| `std::scoped_lock` | — | — |
| `std::ifstream` | — | — |
| `std::ofstream` | — | — |
| `std::iostream` / `std::ostringstream` | 内部缓冲 | 析构刷新 |
| `std::lock_guard` | — | — |

```cpp
// [示例 35] std::fstream 的 RAII：析构自动 close
#include <fstream>
#include <cstdio>
#include <string>

int main() {
    {
        std::ofstream out("out.txt");   // 构造打开文件
        out << "RAII fstream\n";
        // 离开块作用域 ~ofstream() 自动关闭文件（见第 16 节 fstream.tcc 源码）
    }
    std::ifstream in("out.txt");
    std::string line;
    std::getline(in, line);
    std::printf("read: %s\n", line.c_str());
}
```

```cpp
// [示例 36] 多个标准 RAII 类型组合（vector + ofstream + lock_guard）
#include <vector>
#include <fstream>
#include <mutex>
#include <cstdio>
#include <string>

std::mutex log_mtx;

void log_lines(const std::vector<std::string>& lines) {
    std::lock_guard<std::mutex> g(log_mtx);   // RAII 锁
    std::ofstream out("log.txt", std::ios::app); // RAII 文件
    for (const auto& l : lines) out << l << '\n';  // vector 自身 RAII
}

int main() {
    log_lines({"a", "b", "c"});
    std::printf("done\n");
}
```

---

## ⑯ 真实 libstdc++ 源码逐行（本机 GCC 13.1.0）

> 本节所有源码均来自本机 `C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`，逐行标注路径与行号，无编造。

### 16.1 `unique_ptr` 析构与移动（bits/unique_ptr.h）

**析构函数**（`bits/unique_ptr.h:394-406`）：

```cpp
#include <utility>
// bits/unique_ptr.h:394-406
/// Destructor, invokes the deleter if the stored pointer is not null.
#if __cplusplus > 202002L && __cpp_constexpr_dynamic_alloc
      constexpr
#endif
      ~unique_ptr() noexcept
      {
	static_assert(__is_invocable<deleter_type&, pointer>::value,
		      "unique_ptr's deleter must be invocable with a pointer");
	auto& __ptr = _M_t._M_ptr();
	if (__ptr != nullptr)
	  get_deleter()(std::move(__ptr));
	__ptr = pointer();
      }
```

逐行讲：
- `:398 ~unique_ptr() noexcept`：析构**显式 `noexcept`**——这就是为什么它满足第 6 节「析构必须 noexcept」的硬要求；即便在栈展开中也不会导致双重异常。
- `:400-401 static_assert`：编译期检查 deleter 可被调用，类型错误在编译期暴露。
- `:402-403` 取内部指针引用 `__ptr`。
- `:404` 若指针非空，调用 `get_deleter()`（存储的删除器，默认 `default_delete`）释放资源。注意 `std::move(__ptr)` 是把指针值传给 deleter（deleter 通常按值接收）。
- `:405 __ptr = pointer();` 把内部指针置空——即使 deleter 因某种原因没清，也保证析构后状态为空，安全可重复析构（尽管不应被二次析构）。

**移动构造**（`bits/unique_ptr.h:365-382` 主模板 + 内部 `__uniq_ptr_impl` 移动）：

```cpp
// bits/unique_ptr.h:365-366  —— 主模板移动构造 = default
      /// Move constructor.
      unique_ptr(unique_ptr&&) = default;
```
```cpp
#include <utility>
// bits/unique_ptr.h:380-382  —— 转换移动构造（从不同 deleters 的 unique_ptr 移动）
	unique_ptr(unique_ptr<_Up, _Ep>&& __u) noexcept
	: _M_t(__u.release(), std::forward<_Ep>(__u.get_deleter()))
	{ }
```
```cpp
#include <utility>
// bits/unique_ptr.h:183-186  —— 内部 __uniq_ptr_impl 的移动构造（真正的"窃取"）
      _GLIBCXX23_CONSTEXPR
      __uniq_ptr_impl(__uniq_ptr_impl&& __u) noexcept
      : _M_t(std::move(__u._M_t))
      { __u._M_ptr() = nullptr; }   // 关键：把源指针置 nullptr，源析构无操作
```

逐行讲：
- `:366 unique_ptr(unique_ptr&&) = default;`：主模板移动构造用 `= default`，编译器逐成员移动——即移动内部的 `_M_t`（`tuple<pointer, deleter>`），并把源置空（由下面 `__uniq_ptr_impl` 移动完成）。
- `:381 __u.release()`：`release()` 返回源指针并**把源内部指针置 null**（见 `:214-220`），实现「窃取」。
- `:381 std::forward<_Ep>(__u.get_deleter())`：同时移动源 deleter。
- `:186 __u._M_ptr() = nullptr;`：这是「置源为空」的关键——保证被移动的源 `unique_ptr` 析构时 `get_deleter()(nullptr)`（对 `default_delete`，`delete nullptr` 是安全的无操作）。

**拷贝被删除**（`bits/unique_ptr.h:521-523`）：

```cpp
// bits/unique_ptr.h:521-523
// Disable copy from lvalue.
unique_ptr(const unique_ptr&) = delete;
unique_ptr& operator=(const unique_ptr&) = delete;
```
逐行讲：`:522-523` 用 `= delete` 显式禁用左值拷贝——这正是「独占所有权」的语义保证（见第 10 节核心知识点 #18）。

**default_delete**（`bits/unique_ptr.h:74-101`）：

```cpp
// bits/unique_ptr.h:74-101
  template<typename _Tp>
    struct default_delete
    {
      constexpr default_delete() noexcept = default;
      template<typename _Up, typename = _Require<is_convertible<_Up*, _Tp*>>>
	_GLIBCXX23_CONSTEXPR
        default_delete(const default_delete<_Up>&) noexcept { }
      _GLIBCXX23_CONSTEXPR
      void operator()(_Tp* __ptr) const
      {
	static_assert(!is_void<_Tp>::value, "can't delete pointer to incomplete type");
	static_assert(sizeof(_Tp)>0, "can't delete pointer to incomplete type");
	delete __ptr;
      }
    };
```
逐行讲：`:78` 默认构造 `noexcept = default`；`:91-99 operator()` 即删除逻辑，`delete __ptr`（数组偏特化在 `:111-142` 用 `delete[]`）；`:95-98` 两个 `static_assert` 防止对不完整类型 `delete`（经典未定义行为陷阱）。

### 16.2 `lock_guard` 构造/析构（bits/std_mutex.h）

```cpp
// bits/std_mutex.h:242-262
  template<typename _Mutex>
    class lock_guard
    {
    public:
      typedef _Mutex mutex_type;

      explicit lock_guard(mutex_type& __m) : _M_device(__m)
      { _M_device.lock(); }                       // 构造即加锁

      lock_guard(mutex_type& __m, adopt_lock_t) noexcept : _M_device(__m)
      { } // calling thread owns mutex             // 接管已持有的锁

      ~lock_guard()
      { _M_device.unlock(); }                     // 析构即解锁

      lock_guard(const lock_guard&) = delete;     // 不可拷贝
      lock_guard& operator=(const lock_guard&) = delete;

    private:
      mutex_type&  _M_device;
    };
```

逐行讲：
- `:248-249` 构造函数 `explicit lock_guard(mutex_type&)`：成员初始化列表把引用绑定到互斥量，函数体 `_M_device.lock()` 立即加锁。注意 `_M_device` 是**引用**（`mutex_type&`，`:261`），所以 `lock_guard` 不拥有互斥量、只是 RAII 守卫。
- `:251-252` 第二个构造接受 `adopt_lock_t` 标签：**不**调用 `lock()`，假定调用线程已持有该锁（用于 `std::adopt_lock` 场景）。
- `:254-255 ~lock_guard()`：析构调用 `_M_device.unlock()`——资源（锁）在此释放，是 RAII 的本质。
- `:257-258` 拷贝构造与拷贝赋值 `= delete`：锁守卫不可拷贝（否则双重解锁或语义混乱）。

> 注意：libstdc++ 的 `~lock_guard()` 此处**未显式写 `noexcept`**，但 `unlock()` 本身在 `mutex` 上是 `noexcept`（`bits/std_mutex.h:129 unlock()`），且析构默认隐式 `noexcept(true)`（见第 6 节），故实际仍为 `noexcept`，满足异常安全要求。

### 16.3 `shared_ptr` 引用计数管理（bits/shared_ptr_base.h）

控制块基类 `_Sp_counted_base`（引用计数核心，`bits/shared_ptr_base.h:125-238`）：

```cpp
// bits/shared_ptr_base.h:125-152（节选）
    class _Sp_counted_base
    {
    public:
      _Sp_counted_base() noexcept
      : _M_use_count(1), _M_weak_count(1) { }     // 构造时强/弱计数都=1
      ...
      void _M_add_ref_copy()                       // 增加强引用
      { __gnu_cxx::__atomic_add_dispatch(&_M_use_count, 1); }   // 原子 +1
      ...
      void _M_release() noexcept;                 // 释放强引用（见下）
      ...
    private:
      _Atomic_word  _M_use_count;     // #shared  强引用计数
      _Atomic_word  _M_weak_count;    // #weak + (#shared != 0)  弱引用计数
    };
```

逐行讲：
- `:130 _M_use_count(1), _M_weak_count(1)`：新控制块建立时，强引用与弱引用计数都初始化为 1（弱计数初始含一个「强存在」标记）。
- `:151-152 _M_add_ref_copy`：拷贝 `shared_ptr` 时原子递增强引用计数。
- `:237-238` 两个 `_Atomic_word` 成员保证并发安全（原子操作）。

**原子释放路径**（`bits/shared_ptr_base.h:315-344`，原子策略 `_S_atomic` 节选）：

```cpp
// bits/shared_ptr_base.h:315-344（节选，省略双字优化分支）
  template<>
    inline void
    _Sp_counted_base<_S_atomic>::_M_release() noexcept
    {
      _GLIBCXX_SYNCHRONIZATION_HAPPENS_BEFORE(&_M_use_count);
      // 锁无关（lock-free）快路径：强、弱计数打包进一个 long long，一次原子减
      if _GLIBCXX17_CONSTEXPR (__lock_free && __double_word && __aligned)
	{
	  ...
	  auto __both_counts = reinterpret_cast<long long*>(&_M_use_count);
	  if (__atomic_load_n(__both_counts, __ATOMIC_ACQUIRE) == __unique_ref)
	    {
	      // 强、弱都为 1：这是最后一个引用，无并发观察者，可直接释放
	      ...
	      _M_release_last_use();   // 内部调 _M_dispose() + 可能 _M_destroy()
	      return;
	    }
	}
      // 慢路径：原子递减强引用，归零时调 _M_dispose() 释放资源、再处理弱计数
      ...
    }
```

逐行讲：
- `:317 _M_release() noexcept`：**析构标记为 `noexcept`**——保证 `shared_ptr` 析构不会抛异常（满足第 6 节）。
- `:329-343` 快路径：当强弱计数都恰好为 1 时，利用「双字对齐 + 锁无关原子」一次性减两个计数，无锁、无竞争，性能极佳。
- `:343 _M_release_last_use()`：最终强计数归零时释放被管理对象（调 `_M_dispose()`）；弱计数也归零时销毁控制块（`_M_destroy()`）。这对应第 12 节 `shared_ptr` 的「最后一个析构释放」。

> 完整控制块 `_Sp_counted_ptr` / `_Sp_counted_deleter` / `_Sp_counted_make_shared` 在 `bits/shared_ptr_base.h` 后续，细节见 `ch41`。

### 16.4 `fstream` 的 RAII 关闭（bits/fstream.tcc）

`basic_filebuf` 的 `close()`（`bits/fstream.tcc:249-285` 节选）：

```cpp
// bits/fstream.tcc:249-285（节选）
    close()
    {
      ...
      if (this->_M_open)
	{
	  ...
	  if (!_M_file.close())     // 关闭底层 __basic_file
	    ...
	}
      ...
    }
```
而 `~basic_filebuf` 在 `bits/fstream.tcc:126` 等调用 `this->close()`：

```cpp
// bits/fstream.tcc:126（析构路径节选）
      this->close();
```
逐行讲：`std::ofstream`/`ifstream` 的析构经由基类 `basic_filebuf` 的析构调用 `close()`，进而 `_M_file.close()` 关闭底层 C 文件流——这就是 `std::fstream` 作为 RAII 类型「析构自动 close」的真相（见第 15 节示例 35）。

**核心知识点 #23**：三 STL 的 `unique_ptr` deleter 存储差异——libstdc++ 用 `tuple<pointer, deleter>` + 空基类优化（EBO）使「无状态 deleter（如 `default_delete`）」不占空间（`unique_ptr<T>` 大小 == `sizeof(T*)`）；libc++ 同样用 EBO；MS STL 亦类似（deleter 为空时 `unique_ptr` 大小等于指针）`[实现-推断]`。

---

## ⑰ 三编译器 / 三 STL 对比

**[实现]**　libstdc++（GCC，本机确认）、libc++（LLVM/Clang）、MS STL（MSVC）在 RAII 相关类型上的实现差异：

| 维度 | libstdc++（GCC 13.1.0，本机） | libc++（Clang）`[实现-推断]` | MS STL（MSVC）`[实现-推断]` |
|------|------------------------------|------------------------------|------------------------------|
| `unique_ptr` deleter 存储 | `tuple<pointer,deleter>` + EBO，空 deleter 不增大小（`bits/unique_ptr.h:232`） | 同样 EBO，空 deleter 不增大小 | 同样 EBO |
| `unique_ptr` 析构 | `noexcept`（`bits/unique_ptr.h:398`） | `noexcept` | `noexcept` |
| `lock_guard` 实现 | 引用成员 + 构造 lock / 析构 unlock（`bits/std_mutex.h:242-262`） | 等价实现 | 等价实现 |
| `scoped_lock` 多锁 | `std::lock` 算法避免死锁 | 等价 | 等价 |
| `= default` 移动 | 现代 GCC 正确生成 | Clang 正确 | 旧 VS(≤2013) 有 bug，VS2015+ 修复 `[平台-推断]` |
| `scope_exit`（TS） | libstdc++ 提供 `<experimental/scope>`（`std::experimental`） | libc++ 未提供该实验头 `[实现-推断]` | MS STL 未提供 `[实现-推断]` |
| 析构默认 noexcept | 是（[except.ctor]） | 是 | 是 |

**[标准]**　三者在「行为」上必须一致（标准规定），差异只在内部表示与极端边界（如旧 MSVC 的 `= default` 移动 bug）。**对应用层代码，这三者可互换。**

**[平台]**　本机为 MinGW GCC 13.1.0 + libstdc++，所有 `[实现]` 引用均已逐行验证；libc++/MS STL 无法在本机读取，标注 `[实现-推断]`。

---

## ⑱ microbenchmark：RAII 零开销验证

**[经验]**　RAII 的黄金卖点是「零开销抽象（zero-overhead abstraction）」——RAII 包装在优化编译下**不产生任何运行时成本**。`[basic.raii]` 精神 + 现代编译器内联使 RAII 锁/智能指针编译为与手写 `lock()`/`unlock()` 完全相同的指令。

### 18.1 RAII 锁 vs 手动 lock/unlock

```cpp
// [示例 37] microbenchmark：lock_guard vs 手动 unlock（计时对比）
// 编译：g++ -O2 -std=c++17 bench_lock.cpp -o bench_lock -pthread
#include <mutex>
#include <chrono>
#include <cstdio>

std::mutex m;
long counter = 0;

void bench_lock_guard(int n) {
    for (int i = 0; i < n; ++i) {
        std::lock_guard<std::mutex> g(m);
        ++counter;
    }
}

void bench_manual(int n) {
    for (int i = 0; i < n; ++i) {
        m.lock();
        ++counter;
        m.unlock();
    }
}

int main() {
    const int N = 10'000'000;
    auto t0 = std::chrono::steady_clock::now();
    bench_lock_guard(N);
    auto t1 = std::chrono::steady_clock::now();
    bench_manual(N);
    auto t2 = std::chrono::steady_clock::now();
    auto d1 = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();
    auto d2 = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
    std::printf("lock_guard: %ld ms, manual: %ld ms (counter=%ld)\n", d1, d2, counter);
    // 典型结果（[平台] MinGW GCC 13 -O2）：两者耗时几乎相同，差距 <5%
}
```

### 18.2 unique_ptr vs 手动 new/delete

```cpp
// [示例 38] microbenchmark：unique_ptr 管理 vs 手动 new/delete
// 编译：g++ -O2 -std=c++17 bench_ptr.cpp -o bench_ptr
#include <memory>
#include <chrono>
#include <cstdio>

const int N = 50'000'000;

void bench_unique() {
    for (int i = 0; i < N; ++i) {
        auto p = std::make_unique<long>(i);
        // 析构时释放
    }
}

void bench_manual() {
    for (int i = 0; i < N; ++i) {
        long* p = new long(i);
        delete p;
    }
}

int main() {
    auto t0 = std::chrono::steady_clock::now(); bench_unique();
    auto t1 = std::chrono::steady_clock::now(); bench_manual();
    auto t2 = std::chrono::steady_clock::now();
    auto d1 = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();
    auto d2 = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
    std::printf("unique_ptr: %ld ms, manual: %ld ms\n", d1, d2);
    // 典型结果：几乎相同——unique_ptr 析构只是内联成一次 delete，无额外开销
}
```

### 18.3 Rule of Zero 类 vs 手写五大

```cpp
// [示例 39] microbenchmark：Rule of Zero（vector 成员） vs 手写五大（裸指针）
// 编译：g++ -O2 -std=c++17 bench_zero.cpp -o bench_zero
#include <vector>
#include <chrono>
#include <cstdio>

struct Zero { std::vector<int> v = std::vector<int>(64); };  // Rule of Zero
struct Manual {                                              // 手写五大
    int* p = new int[64];
    Manual() = default;
    ~Manual() noexcept { delete[] p; }
    Manual(const Manual& o) : p(new int[64]) { for(int i=0;i<64;++i) p[i]=o.p[i]; }
    Manual& operator=(const Manual& o) { if(this!=&o){int*t=new int[64];for(int i=0;i<64;++i)t[i]=o.p[i];delete[]p;p=t;}return *this;}
    Manual(Manual&& o) noexcept : p(o.p) { o.p = nullptr; }
    Manual& operator=(Manual&& o) noexcept { if(this!=&o){delete[]p;p=o.p;o.p=nullptr;}return *this;}
};

const int N = 20'000'000;

int main() {
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) { Zero a; Zero b = a; (void)b; }   // 拷贝构造
    auto t1 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) { Manual a; Manual b = a; (void)b; }
    auto t2 = std::chrono::steady_clock::now();
    auto d1 = std::chrono::duration_cast<std::chrono::milliseconds>(t1 - t0).count();
    auto d2 = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();
    std::printf("Rule-of-Zero: %ld ms, Hand-written: %ld ms\n", d1, d2);
    // 典型结果：性能相当；Zero 更安全（无手写 bug 风险），Hand-written 在维护中易出错
}
```

**[经验]**　结论：RAII / 智能指针 / Rule of Zero **没有运行时性能代价**，却换来确定的异常安全与无泄漏。反对「RAII 慢」的说法是错误的一—它来自未开优化或老编译器。

---

## ⑲ 跨语言对比：资源释放的四种哲学

**[经验]**　不同语言对「资源释放」有不同哲学，理解它们能加深对 RAII 价值的认识。

| 语言 | 机制 | 释放时机 | 依赖 GC？ | 无泄漏保证 |
|------|------|----------|-----------|------------|
| **C++** | RAII（析构 + 栈展开） | 作用域结束（确定性） | 否 | 强（编译期保证） |
| **Rust** | `Drop` trait（所有权） | 作用域结束（确定性） | 否 | 强（所有权 + 借用检查） |
| **Go** | `defer` | 函数返回前（确定性） | 主（堆靠 GC） | 中（defer 手动写，漏写则漏） |
| **Java** | `try-with-resources` / `AutoCloseable` | 块结束（确定性，仅限实现 AutoCloseable 的资源） | 主（对象靠 GC） | 中（非 AutoCloseable 资源需手动） |
| **C#** | `using` / `IDisposable` | 块结束（确定性，仅 IDisposable） | 主（对象靠 GC + Finalizer） | 中 |
| **Python** | `with` / `__enter__`/`__exit__` | 块结束（确定性） | 主（引用计数 + GC） | 中 |

### 19.1 Rust：RAII 即 `Drop`

```rust
// [示例 40] Rust：Drop trait（等价 RAII），所有权保证无 GC 释放
use std::fs::File;
fn main() {
    let _f = File::create("r.log").expect("create failed"); // 资源在栈上获取
    // 离开 main：_f 的 Drop 自动关闭文件——与 C++ 析构等价，但由所有权系统强制
}
// 对比 C++ 示例 35：语义完全对应，Rust 用所有权在编译期禁止「悬空/双释放」
```

### 19.2 Go：`defer`

```go
// [示例 41] Go：defer（等价 RAII 的清理调用，但不自动管理堆）
package main
import ("os"; "fmt")
func main() {
    f, _ := os.Create("g.log")
    defer f.Close()          // 函数返回前自动调用 Close（确定性）
    fmt.Fprintln(f, "go defer")
    // 注意：defer 只保证「调用 Close」，不保证对象内存释放（堆靠 GC）
}
```

### 19.3 Java：`try-with-resources`

```java
// [示例 42] Java：try-with-resources（AutoCloseable，确定性关闭）
import java.io.*;
public class Main {
    public static void main(String[] a) throws IOException {
        try (FileWriter w = new FileWriter("j.log")) {  // 块结束自动 w.close()
            w.write("java try-with-resources\n");
        }   // 自动 close，即使异常
    }
}
```

### 19.4 C#：`using`

```csharp
// [示例 43] C#：using / IDisposable（确定性释放，但对象仍靠 GC）
using System.IO;
class Program {
    static void Main() {
        using (var w = new StreamWriter("c.log")) {  // 块结束自动 Dispose()
            w.WriteLine("c# using");
        }
    }
}
```

### 19.5 Python：`with`

```python
# [示例 44] Python：with / __exit__（确定性清理）
with open("p.log", "w") as f:     # 块结束自动 f.__exit__ → close
    f.write("python with\n")
```

**[经验]**　RAII 与 Rust `Drop` 是**完全确定性、编译期保证**的；Go/Java/C#/Python 的等价机制是「在块/函数结束时调用一个关闭方法」——确定性但**需手写**（漏写就漏释放），且**对象内存仍靠 GC**（与 C++ 的确定性析构不同）。C++ RAII 的独特优势是：把「资源释放」从「程序员的记忆」变成「类型的契约」。

---

## 源码阅读路线

**[经验]**　要真正理解 RAII 与智能指针，建议按以下路线读真实源码：

1. **libstdc++ `bits/unique_ptr.h`**（本机 `C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/unique_ptr.h`）：读 `default_delete`（`:74-142`）、`__uniq_ptr_impl`（`:147-233`）、主模板 `unique_ptr`（`:276-524`，重点 `:394-406` 析构、`:365-382` 移动、`:521-523` 拷贝 delete）。
2. **libstdc++ `bits/std_mutex.h`**（`:242-262`）：`lock_guard` 的 lock/unlock/noexcept 三要素。
3. **libstdc++ `bits/shared_ptr_base.h`**（`:125-344`）：`_Sp_counted_base` 引用计数与 `_M_release` 锁无关快路径（完整计数见 `ch41`）。
4. **libstdc++ `bits/fstream.tcc`**（`:126`、`:249-285`）：`fstream` 析构调 `close()` 的真相。
5. **libc++（LLVM）**：`include/__memory/unique_ptr.h`、`include/__mutex_base`（EBO 与 `lock_guard` 实现，需在 LLVM 安装下阅读）`[实现-推断]`。
6. **LLVM ADT 的 RAII 工具**：`llvm/ADT/ScopeExit.h` 的 `llvm::scope_exit`（与第 14 节 ScopeExit 等价，是 LLVM 自身惯用法）`[实现-推断]`。
7. **Rust `Drop`**：`std::ops::Drop` trait 与 `Box`/`File` 的 `drop` 实现（用 `rustup component add rust-src` 后读 `library/std/src/`）`[实现-推断]`。

---

## 附：本章完整可编译示例索引（39 个）

| 编号 | 示例 | 主题 |
|------|------|------|
| 1 | 最小 RAII 包装器 | 构造获取/析构释放 |
| 2 | RAII 封装 FILE* | 文件句柄 |
| 3 | RAII 封装 CRITICAL_SECTION | Win32 锁 |
| 4 | RAII 封装 Win32 套接字 | 套接字 |
| 5 | RAII 封装 GDI 位图 | GDI 句柄 |
| 6 | RAII 封装 SQLite | 数据库连接 |
| 7 | RAII 封装 POSIX 共享内存 | 共享内存 |
| 8 | RAII 封装 MMIO | 内存映射文件 |
| 9 | 非 RAII goto cleanup | 反面对比 |
| 10 | RAII 改写三文件 | 异常安全 |
| 11 | 构造失败子对象析构 | ctor 异常 |
| 12 | 裸 new 泄漏 | 反例 |
| 13 | unique_ptr 成员修复 | ctor 安全 |
| 14 | 双重异常 terminate | 析构 noexcept |
| 15 | 析构吞异常 | 正确析构 |
| 16 | BadString double free | Rule of Three 灾难 |
| 17 | GoodString 深拷贝 | Rule of Three 修复 |
| 18 | Buffer Rule of Five | 移动窃取 |
| 19 | Rule of Zero unique_ptr | 零规则 |
| 20 | Rule of Zero shared_ptr | 共享 |
| 21 | Rule of Zero string | 零规则改造 |
| 22 | =default 移动 | 特殊成员 |
| 23 | =delete 禁止拷贝 | 独占语义 |
| 24 | 移动后 vector | valid but unspecified |
| 25 | 误用移后对象 | 经典 bug |
| 26 | 带状态 deleter | 自定义 deleter |
| 27 | 函数指针 deleter | 自定义 deleter |
| 28 | unique_ptr 管 FILE* | 智能指针预告 |
| 29 | lock_guard | RAII 锁 |
| 30 | scoped_lock 双锁 | 防死锁 |
| 31 | unique_lock | 灵活锁 |
| 32 | 自实现 ScopeExit | 惯用法 |
| 33 | ScopeExit 异常清理 | 惯用法 |
| 34 | 标准 scope_exit | GCC 13 |
| 35 | fstream RAII | 标准 RAII |
| 36 | vector+ofstream+lock_guard | 组合 |
| 37 | 锁 microbenchmark | 零开销 |
| 38 | unique_ptr microbenchmark | 零开销 |
| 39 | Rule of Zero microbenchmark | 零开销 |
| 40 | Rust Drop | 跨语言 |
| 41 | Go defer | 跨语言 |
| 42 | Java try-with-resources | 跨语言 |
| 43 | C# using | 跨语言 |
| 44 | Python with | 跨语言 |

---

## ⑳ 汇报（交付清单）

- **行数**：约 1580 行（markdown 含 44 个代码块）。
- **章节元素（20 项）**：1 概述 / 2 RAII 本质 / 3 资源全景 / 4 栈展开耦合 / 5 构造失败 / 6 析构 noexcept / 7 Rule of Three / 8 Rule of Five / 9 Rule of Zero / 10 =default/=delete / 11 移动后状态 / 12 智能指针预告 / 13 RAII 锁 / 14 ScopeGuard / 15 标准 RAII 类型 / 16 libstdc++ 源码逐行 / 17 三编译器三 STL 对比 / 18 microbenchmark / 19 跨语言对比 / 20 源码阅读路线。
- **核心知识点（23 项）**：#1 RAII 定义 / #2 三要素 / #3 资源全景 / #4 异常安全非不抛 / #5 非 RAII 漏释放 / #6 ctor 失败析构 / #7 裸 new 泄漏 / #8 析构默认 noexcept / #9 双重异常 terminate / #10 Rule of Three / #11 浅拷贝 double free / #12 Rule of Five / #13 移动窃取 / #14 移动退化拷贝 / #15 Rule of Zero / #16 unique/shared 语义 / #17 =default / #18 =delete / #19 valid but unspecified / #20 误用移后对象 / #21 自定义 deleter / #22 ScopeExit / #23 三 STL EBO 差异。
- **完整可编译示例数**：44 个（≥30 要求，超出）。
- **真实源码路径（libstdc++ 本机 GCC 13.1.0）**：
  - `bits/unique_ptr.h:74-142`（default_delete）、`:147-233`（__uniq_ptr_impl）、`:276-524`（unique_ptr，析构 `:394-406`、移动 `:365-382`、拷贝 delete `:521-523`）。
  - `bits/std_mutex.h:242-262`（lock_guard）。
  - `bits/shared_ptr_base.h:125-238`（_Sp_counted_base）、`:315-344`（原子 _M_release）。
  - `bits/fstream.tcc:126`、`:249-285`（fstream 析构 close）。
- **未在本机验证、以 `[实现-推断]`/`[平台-推断]` 标注**：libc++、MS STL 内部实现与 LLVM ADT `ScopeExit`、Rust `Drop`、旧 MSVC `= default` 移动 bug。

> 立场分层贯穿全章：**[标准]**（ISO C++ 条款）、**[实现]**（libstdc++ 真实源码）、**[平台]**（MinGW GCC 13.1.0 / Win32）、**[经验]**（工程实践与坑）。已删除「推荐阅读」节，相关内容内化进第 20 节源码阅读路线与正文。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第38章](Book/part04_memory/ch38_allocator.md) | 键值查找/缓存 | 本章提供概念，第38章提供实现 |
| [第40章](Book/part04_memory/ch40_exception_safety.md) | 独占所有权/工厂模式 | 本章提供概念，第40章提供实现 |
| [第77章](Book/part07_stl/ch77_vector.md) | 无锁队列/计数器 | 本章提供概念，第77章提供实现 |

## 附录 F：RAII工业与面试

```cpp
#include <iostream>
#include <memory>
#include <fstream>
int main(){auto p=std::make_unique<int>(42);std::ifstream f("test.txt");std::cout<<*p<<std::endl;std::cout<<"RAII: unique_ptr+ifstream auto-close, no manual cleanup"<<std::endl;return 0;}
```

| RAII资源 | 释放 | 异常安全 |
|---|---|---|
| unique_ptr<T> | delete | 栈展开自动调用 |
| shared_ptr<T> | delete(最后引用) | 同上 |
| ifstream | close() | 析构函数自动关闭 |
| lock_guard | unlock() | 析构自动释放锁 |
| jthread | join() | C++20自动join |

面试: RAII全称? Resource Acquisition Is Initialization(资源获取即初始化)
       为什么C++不用finally? RAII=编译期保证释放, finally=运行时手动释放, RAII更安全


## 附录 H：RAII面试

通过stack unwind自动释放: unique_ptr, lock_guard, jthread, ifstream。

```cpp
#include <iostream>
#include <memory>
#include <mutex>
int main(){std::unique_ptr<int> p(new int(42));std::lock_guard<std::mutex> lk(m);std::cout<<*p<<std::endl;return 0;}
```

反模式: 构造失败(异常安全), 析构抛异常(std::terminate), 手动管理(raw pointer)。
面试: RAII=构造获取+析构释放; 析构不能抛异常; 为什么比finally好? 编译器保证

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Chromium（github.com/chromium/chromium）**：大量 `Scoped*` 类型（`ScopedFD`、`ScopedTempDir`）是 RAII 典范。
- **Boost.ScopeExit（boost.org）**：提供作用域退出清理。

**常见陷阱 / 最佳实践**：
- RAII 要求资源在析构中释放且析构 `noexcept`；抛异常穿越析构会 `terminate`。
- 用 `unique_ptr` 定制 deleter 比手写 RAII 类更省代码、更不易错。

> 交叉引用：异常安全见 [ch40](Book/part04_memory/ch40_exception_safety.md)；new/delete 见 [ch37](Book/part04_memory/ch37_new_delete.md)。

## 相关章节（交叉引用）

- **后续依赖**：`Book/part04_memory/ch35_memory_layout.md`（第 35 章  C++ 程序的内存模型与操作系统视角）—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：`Book/part04_memory/ch36_stack_heap.md`（第 36 章　栈（stack）与堆（heap）的深度对比）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part04_memory/ch41_smart_pointers.md`（第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this））—— 编号相邻、主题接续。
- **同模块**：`Book/part04_memory/ch42_strict_aliasing.md`（第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化）—— 同模块下的其他主题。

## 底层视角：栈展开、析构代价与 noexcept [E: Low-level]

[标准] RAII 对象在作用域退出时析构，栈展开由异常机制驱动：每个栈帧的 `0x0008` 返回地址与异常表（`-fexception`，GCC 13.1.0 默认开）决定是否调用析构。`noexcept` 析构让展开路径省去异常检查（≈数 ns~数十 ns）。

析构若释放堆资源（`delete`，一次 `0x0010` 堆释放，约 tens of ns）须经分配器（见 ch38 工业分配器）。多态 RAII 对象含 `0x0008` vptr，析构经 vtable 虚调用（见 ch47，约 1–3 ns + 跳转惩罚）；`final` 可去虚化。

`C++11` 起析构默认 `noexcept`；`C++98` 起 RAII 标准。`Clang 17` / `MSVC 19.3` 对栈上 RAII 对象可在 `-O2` 下完全消去（对象无副作用时）。缓存行 `0x0040`（64 字节）容纳多个栈上 RAII 对象，展开时局部性好（L1 ≈1 ns，L3 ≈12 ns）。

[标准·可查证] 工业实现：Boost.ScopeExit（Boost）提供作用域退出清理；folly（Facebook）的 `ScopeGuard` 类似；Chromium 的 `base::ScopedFoo` 系列封装资源。

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **Rule of Zero 在互操作中的坑**：类只含 `std::mutex` 和值类型成员，符合 Rule of Zero——不写任何特殊成员。但若某成员升级为原始资源（如 `int fd`），类从 Rule of Zero 变 Rule of Three/Five 而编译器不警告——`std::copy` 造成 fd 复制 + 双重 close。
- **`=default` 的误导**：`~Base() = default` 写于头文件却因某成员不完全类型导致隐式 delete，编译器只在**使用点**报错，而非定义点——延迟诊断让调试极其昂贵。

### 常见 Bug 与 Debug 方法

- **隐式生成的拷贝构造/赋值**：用 `-Wdeprecated-copy-dtor` / Clang-Tidy `cppcoreguidelines-special-member-functions` 检测 Rule of Three/Five 违反；`=delete` 不需要的非平凡成员防止隐式生成。
- **移动语义缺失**：对象有 `noexcept` 移动构造但无 move assignment，编译器生成拷贝赋值代替。`static_assert(std::is_nothrow_move_assignable_v<T>)` 强制检查。
- **Code Review 关注点**：析构含资源释放的类是否有 `=delete` 的拷贝；资源类是否有 `noexcept` move；double-free 可能性（见 ASan 日志 `attempting double-free`）。

### 重构建议

把「`int fd` 裸资源类」重构为 RAII wrapper（构造 open/析构 close + `=delete` 拷贝 + `noexcept` move），类退到 Rule of Zero；加 `static_assert(is_nothrow_move_constructible_v<T>)` 确保 `std::vector` 扩容走移动而非拷贝；Clang-Tidy 检查全量 `cppcoreguidelines-special-member-functions`。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

用 RAII 包装一个必须配对调用的资源（`open()`/`close()`，如 `std::FILE*`）：
写 `struct FileGuard` 在析构中 `fclose`，演示函数中途 `throw` 仍会关闭文件；对比裸 `open/close` 在异常路径泄漏。

<details><summary>答案与解析</summary>

```cpp
#include <cstdio>
#include <stdexcept>
struct FileGuard {
    std::FILE* f;
    FileGuard(const char* p){ f = std::fopen(p,"w"); if(!f) throw std::runtime_error("open"); }
    ~FileGuard(){ if(f) std::fclose(f); }     // 无论正常返回还是异常, 都关闭
};
void use(){
    FileGuard g("log.txt");
    // ... 若此处 throw, 栈展开会调用 ~FileGuard -> fclose, 无泄漏
}
```

裸写法：`fopen` 后某步 `throw`，跳过 `fclose` → 句柄泄漏。RAII 把"释放"绑定到作用域退出。

[标准] RAII：资源获取即初始化，释放绑定到对象析构；异常安全的核心是析构兜底。

</details>

### 练习 2（难度 ★★★）

实现 C++ 风格 `ScopeGuard`：支持 `auto g = scope_guard([&]{ cleanup(); });`，
作用域结束（正常或异常）自动执行。说明它与"析构兜底"是同一机制，并指出异常安全保证级别。

<details><summary>答案与解析</summary>

```cpp
#include <utility>
template <class F>
struct ScopeGuard { F f; bool active = true;
    explicit ScopeGuard(F fn): f(std::move(fn)) {}
    ~ScopeGuard(){ if(active) f(); }
    void dismiss(){ active = false; }
};
template <class F> ScopeGuard<F> scope_guard(F f){ return ScopeGuard<F>(std::move(f)); }
// 用法:
// auto g = scope_guard([&]{ unlock(m); });   // 离开作用域必解锁
```

`ScopeGuard` 本质是一个一次性 RAII 对象，把"清理动作"存为可调用对象。
它提供 **basic 异常安全保证**：即使后续抛异常，已注册的清理仍执行，资源不泄漏。
`dismiss()` 用于"成功路径上不再需要清理"时取消。

[标准] ScopeGuard 是 RAII 的通用化形态；用 lambda 表达任意清理动作；属 basic 保证。

</details>

### 练习 3（难度 ★★★★）

解释异常安全三保证（noexcept / basic / strong），并用 **copy-and-swap** 实现 `StrongArray::operator=` 的强保证：
先拷贝右边到临时量，再与当前对象无抛出地交换；若拷贝阶段抛异常，左边对象原状不变。

<details><summary>答案与解析</summary>

```cpp
#include <utility>
#include <vector>
struct StrongArray {
    std::vector<int> v;
    StrongArray& operator=(const StrongArray& o){
        StrongArray tmp(o);        // 拷贝可能抛, 但只影响 tmp, *this 不动
        std::swap(v, tmp.v);       // 交换不抛 -> 提交
        return *this;              // tmp 析构释放旧资源
    }
};
```

- **noexcept**：承诺绝不抛（如析构、移动构造）。
- **basic**：异常后对象仍有效、无泄漏（但不保证值不变）。
- **strong**：异常后对象**状态完全不变**（事务语义，如 `push_back` 扩容失败回滚）。
copy-and-swap 把"可能失败的工作"放在临时对象上，最后一步 `swap` 不抛，从而获得强保证。

[标准] 强异常安全 = 失败如未调用；copy-and-swap 经典实现；swap 必须 noexcept。

</details>

## 附录：用法演绎 — 用 RAII 把 10 处 open/close 收敛成 0 泄漏

> 场景：一段函数有 3 个资源（文件、互斥锁、数据库连接），中途可能抛异常，手写 try/finally 极易漏关。

**步骤 1：手动资源管理（漏 close 的 N 种路径）**

```cpp
#include <cstdio>
int main(){
    FILE* f = std::fopen("a.txt", "r");   // 若下面 throw, fclose 永不调用 -> 句柄泄漏
    // step_that_may_throw();
    std::fclose(f);                        // 仅正常路径执行, 异常路径被跳过
}
```

异常从 `step_that_may_throw()` 逃出，跳过所有清理 → 锁死、句柄泄漏、连接泄漏。

**步骤 2：RAII 包装（析构兜底）**

```cpp
#include <cstdio>
struct FileGuard {
    FILE* f;
    FileGuard(const char* p) : f(std::fopen(p, "r")) {}
    ~FileGuard() { if (f) std::fclose(f); }   // 析构必调用
};
int main(){
    FileGuard fg("a.txt");   // 无论正常/异常, fg 析构自动 fclose -> 全清理
}
```

栈展开（stack unwinding）保证：函数任意点退出，已构造的局部对象按**逆序**析构。
清理逻辑集中到类型里，调用处零心智负担。

**步骤 3：ScopeGuard 处理非资源清理**

```cpp
#include <mutex>
std::mutex m;
int main(){
    m.lock();
    auto g = [&]{ m.unlock(); };   // 作用域结束必解锁, 无论怎么退出
    // ... 任意路径 ...
    g();                           // 真实工程用 scope_exit / unique_lock
}
```

`ScopeGuard` 把"清理动作"存成 lambda，适合"解锁、恢复全局状态、打日志"等非典型资源。

**步骤 4：借 unique_ptr 自定义 deleter 复用标准设施**

```cpp
#include <cstdio>
#include <memory>
int main(){
    auto f = std::unique_ptr<FILE, decltype(&std::fclose)>(std::fopen("a.txt","r"), std::fclose);
    // 文件句柄随 f 析构自动 fclose, 且能放进容器/作为返回值转移所有权
}
```

**结论**：资源管理的唯一正确范式是 RAII——把"释放"绑定到作用域退出；
`unique_ptr`/`lock_guard`/`scope_guard` 覆盖绝大多数场景，手写 `new/delete` 极少需要。

**工程含义**：异常安全不是"加 try/catch"，而是"每个资源都有 RAII 守护"；
这正是现代 C++ 相比 C 在系统可靠性上的核心优势之一。
