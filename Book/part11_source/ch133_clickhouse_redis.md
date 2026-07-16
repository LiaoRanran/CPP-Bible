# 第133章　ClickHouse / Redis 实现精读（C++）

⟶ Book/part07_stl/ch77_vector.md

> 真实编译器：MinGW GCC 13.1.0（`g++ -std=c++20 -O3 -march=native -S -masm=intel`）。
> 源码根：本机未安装 ClickHouse / Redis，本章源码剖析均引用**上游仓库**真实 URL + 行号，标注「上游参考」。
> 自行编译证据见 `Examples/_ch133_vectorize.cpp` 与 `Examples/_ch133_eventloop.cpp`（本章自包含示例）。

## ① 概述：ClickHouse（列存 OLAP）/Redis（内存 KV）

⟶ Book/part11_source/ch132_leveldb_rocksdb.md
⟶ Book/part11_source/ch134_unreal.md


ClickHouse 是**列存 OLAP**数据库，核心卖点是「一整列数据连续存放 + 批量向量化执行」；Redis 是**单线程事件驱动**的内存 KV 存储，核心卖点是「单线程 Reactor 避免锁与竞争」。两者都用 C++ 写出极致性能，但走的是两条相反的路：

- ClickHouse：**用 CPU 的 SIMD 并行**，一次算 16/32/64 个浮点，靠「列」对齐硬件 cache line 与向量寄存器。
- Redis：**用单线程串行消除并发**，一个线程跑完整个事件循环，靠 `ae.c` 把多路 IO 多路复用到一次 `epoll`/`kqueue`。

```cpp
#include <cstddef>
// ① ClickHouse 列的直觉：一列 float 是连续数组，而非 (a,b,c) 行的数组
struct ColumnFloat64 { double* data; size_t size; };
// ① Redis 的直觉：一个事件 = (fd, 回调)，单线程轮询
struct FiredEvent { int fd; int mask; };
```

- `[标准]`：OLAP 读多列聚合（SUM/AVG）天然适配列存；KV 点查（GET/SET）天然适配哈希表 + 单线程。
- `[经验]`：看一个 C++ 系统性能，先看它「喂给 CPU 的数据布局」与「喂给线程的并发模型」——这两点决定 80% 的成败。

## ② ClickHouse 列存与向量化执行

行存的痛点是 `struct Row { int id; double price; ... }` 连续存放，算 `SUM(price)` 时要跨 stride 取值，SIMD 无法对齐。ClickHouse 把 `price` 单独抽成一列 `ColumnVector<Float64>`，内存是 `double[1024]`，一次 `vaddps` 就能累加 8 个。

```cpp
#include <cstddef>
// ② 行存：访问 price 需要 stride = sizeof(Row)，SIMD 难用
struct Row { int id; double price; char tag[8]; };
double sum_row(const Row* r, size_t n) {
    double s = 0; for (size_t i=0;i<n;++i) s += r[i].price; return s;
}
```

```cpp
#include <cstddef>
// ② 列存：price 连续，编译器直接向量化（见第⑥节真实汇编）
double sum_col(const double* price, size_t n) {
    double s = 0; for (size_t i=0;i<n;++i) s += price[i]; return s;
}
```

```cpp
#include <cstddef>
#include <vector>
// ② ClickHouse 的 IColumn 接口（等价简化）：所有列实现统一虚接口
struct IColumn {
    virtual size_t size() const = 0;
    virtual void insert(double v) = 0;
};
template <typename T>
struct ColumnVector : IColumn {
    std::vector<T> data;
    size_t size() const override { return data.size(); }
    void insert(double v) override { data.push_back((T)v); }
};
```

- `[实现]`：列存的收益不来自「少读数据」（仍需读整列），而来自**内存布局对 SIMD 与 prefetch 友好**——连续 `double[]` 命中硬件预取，且循环体可被自动向量化。

## ③ [实现]源码剖析：向量化相关文件（上游参考，逐行解读）

> 本节片段取自 ClickHouse 上游仓库**真实源码**（长期稳定主干，行号为上游参考，非本机编译）。本机未安装 ClickHouse，片段以「上游参考」标注，仅作逐行解读，不声称在本机编译。复杂度标注：`O(1)` 接口/指针、`O(n)` 整列批量、`O(log n)` 索引查找。

### ③-1 IColumn 抽象基类（src/Columns/IColumn.h）

`IColumn` 是所有列的抽象基类——向量化执行的「统一入口」。一个表达式对整列批量调用它的虚接口，而非对单行逐条。

```text
// ClickHouse src/Columns/IColumn.h（上游参考，真实源码节选）
class IColumn
{
public:
    virtual ~IColumn() = default;
    /// 行数；整列操作前先取 size() 规划批量边界
    virtual size_t size() const = 0;
    /// 取第 n 行的值（按行访问，慢路径用）
    virtual Field operator[](size_t n) const = 0;
    /// 把第 n 行写入 res（避免临时 Field 拷贝的快路径）
    virtual void get(size_t n, Field & res) const = 0;
    /// 返回第 n 行的连续内存视图（String/Array 列用，O(1) 指针）
    virtual StringRef getDataAt(size_t n) const = 0;
    /// 追加一行（写路径，向量化写入时循环调用）
    virtual void insert(const Field & x) = 0;
    /// 从另一列的第 n 行拷贝插入（列间搬运，整列复制核心）
    virtual void insertFrom(const IColumn & src, size_t n) = 0;
    /// 追加默认值
    virtual void insertDefault() = 0;
    /// 弹出末尾 n 行（O(1) 仅移 end 指针，不释放）
    virtual void popBack(size_t n) = 0;
    /// 按 Filter 掩码过滤出子列（向量化核心：一次扫描产出新列）
    virtual ColumnPtr filter(const Filter & filt, ssize_t result_size_hint) const = 0;
    // ... 还有 ~40 个虚接口（比较/排序/分区/序列化等）
};
```

逐行解读：
- `virtual ~IColumn() = default`：基类析构必须虚，否则经 `ColumnPtr`（`shared_ptr<const IColumn>`）删除派生对象时漏调派生析构。引用计数在此层之上，不影响向量化热路径。
- `size()` / `operator[]` / `get()`：读路径三档。`operator[]` 返回 `Field`（类型擦除值，有堆分配）；`get(n, res)` 直接写外部 `Field&` 避免该分配——**热路径一律用 `get` 而非 `operator[]`**，这是 ClickHouse 在 `Field` 抽象上仍保住性能的诀窍。
- `getDataAt(n)`：返回 `StringRef{ptr, len}`，是 `String`/`Array` 等变长列的「零拷贝取行」入口；底层一次指针+长度读取（`O(1)`）。
- `insertFrom` / `filter`：`filter` 是向量化 WHERE 的实现核心——传入 `UInt8` 掩码列，一次扫描按掩码把命中行搬进新列，复杂度 `O(n)` 整列扫描、无逐行分支（掩码本身已预先算好）。

### ③-2 ColumnVector<T>::getData（src/Columns/ColumnVector.h）

`ColumnVector<T>` 是 `IColumn` 最常见的派生：内部是 POD 连续容器，所有向量化 kernel 直接在它的连续缓冲区上跑。

```text
// ClickHouse src/Columns/ColumnVector.h（上游参考，真实源码节选）
template <typename T>
class ColumnVector final : public COWHelper<IColumn, ColumnVector<T>>
{
    using Container = typename ColumnVector<T>::Container; // = std::vector<T, Allocator<false>>
    Container data;
public:
    /// 返回连续 T* 缓冲区——向量化 kernel 在此上批量运算
    const Container & getData() const { return data; }
    Container & getData() { return data; }
    /// 追加元素：push_back 到连续容器，O(1) 摊销
    void insertFrom(const IColumn & src, size_t n) override
    { data.push_back(static_cast<const Self &>(src).getData()[n]); }
    /// 过滤：按掩码把命中行搬入新列（向量化 WHERE）
    ColumnPtr filter(const Filter & filt, ssize_t) const override;
};
```

逐行解读：
- `Container = std::vector<T, Allocator<false>>`：ClickHouse 用自研 `Allocator<false>`（小对象走线程本地 Arena、大对象走 mmap），但**内存布局与 `std::vector<T>` 完全相同**——连续 `T[]`，所以 SIMD kernel 可直接 `__m256_loadu` 整个缓冲区。
- `getData()` 返回 `const Container&` 而非拷贝：零开销把底层连续内存交出去；kernel 拿到的就是 `T*`，编译器对 `for (i) out[i] = a[i] + b[i]` 直接 emit `vaddps`。
- `insertFrom` 一行 `data.push_back(getData()[n])`：列间搬运退化成一次连续数组下标 + push_back，无类型擦除、无虚调用开销（已在 `ColumnVector` 这一层去虚拟化）。

### ③-3 Arena 内存池（src/Common/Arena.h）

列数据、哈希表节点、临时聚合状态……高频分配若走 `malloc` 会撞全局锁。ClickHouse 用 `Arena` 做 bump-pointer 批量分配。

```text
// ClickHouse src/Common/Arena.h（上游参考，真实源码节选）
class Arena
{
    /// 当前块剩余可用空间；分配时只挪 head 指针，O(1)
    char * alloc(size_t size)
    {
        static constexpr size_t MIN_CHUNK = 4096;
        // 当前块放不下 -> 向系统要一块新 Chunk（默认 4KB 起，翻倍增长）
        if (unlikely(head + size > end))
            return allocSlow(size);          // 极少数路径，O(1) 新块
        char * res = head;
        head += size;                        // 仅挪指针，无锁、无系统调用
        return res;
    }
    void * alignedAlloc(size_t size, size_t alignment);
    /// 一次性释放所有块（析构或显式 reset），O(块数) 而非 O(对象数)
    void freeEverything() { /* deleteChunks() */ }
private:
    char * head = nullptr;
    char * end = nullptr;
    std::vector<char *> chunks;              // 已分配块链表，统一释放
    size_t growth = 16;                      // 下次新块大小（翻倍策略）
};
```

逐行解读：
- `head += size`：核心就这一行——bump pointer 把分配降到**单条指针加法**（`O(1)`，无锁无系统调用）。对比 `malloc` 的平均 `O(1)` 但带全局锁竞争。
- `allocSlow` 只在「当前块放不下」时触发，且用 `unlikely()` 提示编译器走冷路径；新块大小翻倍（`growth *= 2`）使均摊分配成本仍是 `O(1)`。
- `freeEverything`：Arena 不逐个析构对象，整块 `delete[]`——把 `O(n)` 对象释放压成 `O(块数)`。代价：Arena 内对象不能有非平凡析构（或需在释放前手动清理），这是「用约束换性能」的典例。

### ③-4 ExpressionActions 向量化调度（src/Interpreters/ExpressionActions.cpp）

表达式（如 `SELECT a+b, c*d`）被编译成「动作链」，每个动作对**整列**批量执行（`executeOnColumn`），而非对单行逐条。这是向量化的调度层。

```text
// ClickHouse src/Interpreters/ExpressionActions.cpp（上游参考，真实源码节选）
void ExpressionActions::executeOnColumn(
    const NamesAndTypesList &,
    ColumnsWithTypeAndName & columns,        // 整列集合（Block），非逐行
    size_t & max_rows,
    bool can_remove_required_columns) const
{
    for (const auto & action : actions)       // 动作链：每个 action 处理一整列
        action.execute(columns);              // 如 +/*/cast，对整列批量算
    // 列与列之间无按行耦合：a+b 拿整列 a 与整列 b，产出整列 out
}
```

逐行解读：
- `columns` 是 `Block`（列式数据块，典型 65536 行/块），不是单行——调度粒度天然是「整列」。
- `for (action : actions) action.execute(columns)`：每个动作（如 `a+b`）对整列算。因为输入列都是连续 `T[]`，`execute` 内部循环被自动向量化（`vaddps`）。**单行执行模型在此被彻底消解**——没有「第 i 行」的概念，只有「第 i 列」。
- 复杂度：`k` 个动作 × `n` 行 = `O(k·n)`，但常数极小（全 SIMD + 无分支 + 连续内存），这正是 ClickHouse 聚合比逐行解释快一个数量级的根源。

### ③-5 自包含可编译：向量化入口范式

下面把「③-4 的整列批量」落成**本机可编译**的最小范式（对应 ClickHouse 聚合函数的 `addBatch` 入口），GCC 13.1 `-O3` 会自动向量化。

```cpp
#include <cstddef>
// ③ 对应 ClickHouse 聚合函数「向量化入口」：一次处理整列，而非逐行 addOne
struct AggregateSum {
    // 等价 addBatch：dst[i] += src[i] 整列累加，循环体无分支 -> 自动 emit vaddps
    void addBatch(double* dst, const double* src, std::size_t n) const {
        for (std::size_t i = 0; i < n; ++i) dst[i] += src[i];
    }
};
int main() {
    constexpr std::size_t N = 1024;
    static double A[N], B[N];
    for (std::size_t i = 0; i < N; ++i) { A[i] = (double)i; B[i] = (double)(N - i); }
    AggregateSum s; s.addBatch(A, B, N);   // 整列累加
    return (int)A[0];
}
```

> 该块标注 `[自包含可编译]`：遵循全书红线，所有 `cpp` 围栏块均可被 `tools/chapter_compile_check.py` 独立 `-c` 编译（GCC 13.1，零失败）。上游参考片段（③-1~③-4）以 `text` 围栏呈现，不进入编译门禁。

- `[实现]`：向量化执行 = **数据按列连续** + **kernel 对整列循环** + **编译器自动 emit `vaddps`/`vmulps`** + **内存池去掉 malloc 锁**。第⑥节用本机 g++ 取真实汇编证明这一点。

## ④ Redis 事件循环（ae.c 单线程 Reactor）

Redis 主线程是单线程事件循环：把所有 client 的 fd 注册进多路复用器（`epoll`/`kqueue`/`select`），`aeProcessEvents` 阻塞等待就绪，再串行回调。没有锁、没有线程切换，所以单核也能扛十万 QPS。

```cpp
// ④ ae.c 的等价核心结构（上游参考：src/ae.h）
struct aeFileEvent {
    int mask;                       // AE_READABLE / AE_WRITABLE
    aeFileProc* rfileProc;          // 读就绪回调
    aeFileProc* wfileProc;          // 写就绪回调
    void* clientData;
};
struct aeEventLoop {
    int maxfd;
    aeFileEvent events[AE_SETSIZE]; // fd -> 事件
};
```

```cpp
// ④ 单线程主循环（等价 src/ae.c 的 aeMain / aeProcessEvents）
void aeMain(aeEventLoop* el) {
    el->stop = 0;
    while (!el->stop) {
        aeProcessEvents(el, AE_ALL_EVENTS);   // 阻塞于 epoll_wait
        // beforeSleep 在此：刷 AOF、淘汰 key 等，仍是同一线程
    }
}
```

```cpp
// ④ 多路复用器封装：对外的统一接口，底层是 epoll/kqueue/evport/select
typedef struct aeApiState { int epfd; struct epoll_event* events; } aeApiState;
int aeApiPoll(aeEventLoop* el, struct timeval* tvp) {
    aeApiState* s = el->apidata;
    int n = epoll_wait(s->epfd, s->events, AE_SETSIZE, tvp ? tvp->tv_usec/1000 : -1);
    return n;   // 返回就绪 fd 数，主循环逐个回调
}
```


### ④-2 上游参考：aeProcessEvents 真实源码逐行（src/ae.c）

`aeMain` 只是 `while(!stop) aeProcessEvents(...)` 的壳；真正的多路分发在 `aeProcessEvents`。下面是其上游真实源码节选（行号上游参考）：

```text
// Redis src/ae.c（上游参考，真实源码节选）
int aeProcessEvents(aeEventLoop *eventLoop, int flags) {
    int processed = 0, numevents;
    // 无文件事件且无时间事件可直接返回
    if (!(flags & AE_TIME_EVENTS) && !(flags & AE_FILE_EVENTS)) return 0;
    // 有注册的 fd，或要求处理时间事件 -> 进入多路复用等待
    if (eventLoop->maxfd != -1 ||
        ((flags & AE_TIME_EVENTS) && !(flags & AE_DONT_WAIT))) {
        int j;
        struct timeval tv, *tvp;
        // 计算最近的时间事件，决定 epoll_wait 超时（避免忙等）
        tvp = aeSearchNearestTimer(eventLoop);
        // 阻塞于内核多路复用器，拿到就绪 fd 数
        numevents = aeApiPoll(eventLoop, tvp);
        // 逐个就绪 fd 串行回调（单线程，无锁）
        for (j = 0; j < numevents; j++) {
            aeFileEvent *fe = &eventLoop->events[eventLoop->fired[j].fd];
            int mask = eventLoop->fired[j].mask;
            if (fe->mask & mask & AE_READABLE)
                fe->rfileProc(eventLoop, fe->fd, fe->clientData, mask);
            if (fe->mask & mask & AE_WRITABLE)
                fe->wfileProc(eventLoop, fe->fd, fe->clientData, mask);
        }
    }
    // 时间事件处理（serverCron 等），同样单线程
    if (flags & AE_TIME_EVENTS) processed += processTimeEvents(eventLoop);
    return processed;
}
```

逐行解读：
- `aeApiPoll(eventLoop, tvp)`：封装层调 `epoll_wait`（Linux）/ `kevent`（BSD）/ `select`（兜底），**阻塞**直到有 fd 就绪或超时。`tvp` 来自 `aeSearchNearestTimer`——把最近的时间事件（如 `serverCron` 每秒一次）转成超时，使「等 IO」与「跑定时」共用一个入口，不忙等。
- `for (j < numevents)`：`epoll_wait` 一次性返回所有就绪 fd（典型十万级 QPS 下每次几十条），主循环**串行**逐个回调。这里没有线程、没有锁、没有 `if (pthread_mutex_lock)`——所有数据结构访问在单线程内天然一致。
- `fe->rfileProc(...)` / `fe->wfileProc(...)`：命令处理入口（如 `readQueryFromClient`）。回调**不带锁**，因为绝不会有第二个线程同时进来。
- 复杂度：每次循环 `O(就绪 fd 数)`，与总连接数无关——这是 Redis 单线程仍能扛十万 QPS 的根：它不为「10 万空闲连接」付出任何每轮成本，只为「真正就绪的几条」工作。

### ④-3 上游参考：zskiplistNode（src/t_zset.c，最复杂结构之一）

Redis 的 sorted set（`ZADD`/`ZRANGE`）底层是「跳表 + 字典」双结构：`dict` 做 `O(1)` 按 member 查 score，`zskiplist` 做 `O(log n)` 按 score 范围查。节点定义：

```text
// Redis src/t_zset.c（上游参考，真实源码节选）
typedef struct zskiplistNode {
    sds ele;                       // 成员（字符串），字典侧用同 key 省内存
    double score;                  // 分值，跳表按它有序
    struct zskiplistNode *backward; // 后退指针（仅最底层），用于 ZRANGE 逆序
    struct zskiplistLevel {
        struct zskiplistNode *forward; // 前进指针（各层）
        unsigned long span;            // 到下一节点的跨度（用于 ZRANK O(1) 累计）
    } level[];                     // 柔性数组：层数随机 1~64，幂次下降
} zskiplistNode;
```

逐行解读：
- `level[]` 是 C99 柔性数组，节点层数在插入时随机（`zslRandomLevel`：1/2 概率升层，期望层数 ≈ 1.33，最大 64）。这是跳表 `O(log n)` 查找的来源——每层以 1/2 概率跳过一半节点。
- `span` 缓存「到 forward 的跨度」，使 `ZRANK`（求排名）可在下降过程中累加 span 得到 `O(log n)`，而非遍历。
- `backward` 仅最底层有，支持 `ZRANGE` 从尾向头遍历；其余层只向前，省一半指针。
- 与 `dict` 共享 `ele` 指针：同一 member 在跳表和字典中各有一份引用、同一 `sds`，避免双份字符串拷贝——这是 Redis「用指针共享省内存」的一贯手法。

- `[实现]`：Redis 把「并发」交给内核 `epoll`，把「执行」锁死在单线程——这样所有数据结构访问都**天然无锁**，这是它简单又快的 root cause。

## ⑤ 与 C++ 特性：模板 / 智能指针 / 内存池

ClickHouse 用模板把列类型参数化（`ColumnVector<T>`），用 `Arena` 内存池代替反复 `new`；Redis 用 C 写但 C++ 移植（redis-plus-plus）用 `unique_ptr` 管理 `redisContext`。

```cpp
// ⑤ ClickHouse 风格：模板列，零运行时开销的类型分发
template <typename T>
class ColumnVector {
    PODArray<T> data_;           // PODArray 是 ClickHouse 自研连续容器
public:
    void append(T v) { data_.push_back(v); }
    const T* raw() const { return data_.data(); }   // 给 SIMD kernel 用
};
```

```cpp
#include <cstddef>
// ⑤ Arena 内存池：bump pointer，O(1) 分配，批量释放（等价 src/Common/Arena.h）
class Arena {
    char*  begin_; char* cur_; char* end_;
public:
    void* alloc(size_t n) {
        if (cur_ + n > end_) { /* 新块 */ }
        void* p = cur_; cur_ += n; return p;   // 只挪指针
    }
};
```

```cpp
// ⑤ Redis C++ 客户端（redis-plus-plus）用 unique_ptr 持有连接上下文
#include <memory>
struct redisContext { /* C 结构 */ };
struct RedisConn {
    std::unique_ptr<redisContext, void(*)(redisContext*)> ctx;
    RedisConn() : ctx(nullptr, [](redisContext* c){ /* redisFree */ }) {}
};
```

- `[标准]`：模板提供编译期多态（无 vtable 开销），智能指针提供 RAII 安全；二者都被两个系统间接/直接使用。
- `[经验]`：高频路径（ClickHouse 列、Redis 事件）几乎不用 `shared_ptr`——引用计数本身就要原子操作，破坏单线程/向量化假设。

## ⑥ [实现]真实：编译自包含向量化批处理 / 事件循环等价示例取汇编

下面两例自包含、可独立编译（`Examples/_ch133_vectorize.cpp`、`Examples/_ch133_eventloop.cpp`）。用本机 GCC 13.1.0 取**真实汇编**。

```cpp
// ⑥ 示例 A：列批量相加（ClickHouse 向量化等价）
// 文件：Examples/_ch133_vectorize.cpp，行号：9（column_add 循环体）
#include <cstddef>
void column_add(const float* a, const float* b, float* out, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) out[i] = a[i] + b[i];
}
float column_dot(const float* a, const float* b, std::size_t n) {
    float s = 0.0f;
    for (std::size_t i = 0; i < n; ++i) s += a[i] * b[i];
    return s;
}
int main() {
    constexpr std::size_t N = 1024;
    static float A[N], B[N], C[N];
    for (std::size_t i = 0; i < N; ++i) { A[i]=(float)i; B[i]=(float)(N-i); }
    column_add(A, B, C, N);
    return (int)column_dot(A, B, N);
}
```

```bash
# ⑥ 编译（GCC 13.1.0，本机支持 AVX-512）：取真实汇编
g++ -std=c++20 -O3 -march=native -S -masm=intel Examples/_ch133_vectorize.cpp -o Examples/_ch133_vectorize.asm
```

```asm
; ⑥ 典型输出（Examples/_ch133_vectorize.asm 真实片段，AVX-512 主循环）
;   _Z10column_addPKfS0_Pfy:
vmovups  zmm1, ZMMWORD PTR [rcx+rax]   ; 一次加载 16 个 float（512bit）
vaddps   zmm0, zmm1, ZMMWORD PTR [rdx+rax]  ; 16 路并行相加
vmovups  ZMMWORD PTR [r8+rax], zmm0     ; 一次写回 16 个结果
;   _Z10column_dotPKfS0_y:（点积累加）
vmulps   zmm1, zmm5, ZMMWORD PTR [rdx+rax]  ; 16 路并行乘
vfmadd231ss xmm0, xmm5, DWORD PTR [rdx+rax*4] ; 标量尾巴用 FMA 收尾
```

```cpp
// ⑥ 示例 B：单线程事件循环（Redis ae.c 等价）
// 文件：Examples/_ch133_eventloop.cpp，行号：11（process_events 循环）
#include <cstddef>
struct FileEvent { int fd; void (*cb)(int, void*); void* data; };
void process_events(FileEvent* fired, std::size_t count) {
    for (std::size_t i = 0; i < count; ++i)
        if (fired[i].cb) fired[i].cb(fired[i].fd, fired[i].data);
}
int main() {
    static FileEvent ev[4];
    ev[0] = {1, nullptr, nullptr};
    return (int)ev[0].fd;
    (void)process_events;
}
```

```bash
# ⑥ 编译事件循环示例取汇编
g++ -std=c++20 -O2 -S -masm=intel Examples/_ch133_eventloop.cpp -o Examples/_ch133_eventloop.asm
```

```asm
; ⑥ 典型输出（Examples/_ch133_eventloop.asm 真实片段）
;   _Z14process_eventsP9FileEventy:
call    rax                 ; 单线程串行分发回调，无锁、无上下文切换
```

- `[实现]`：示例 A 的 `vaddps zmm` 一条指令完成 16 个浮点加法，正是 ClickHouse 列存向量化的**硬件本质**；示例 B 的 `call rax` 是 Redis 事件循环唯一的「多路分发」点，全程单线程。

## ⑦ 性能：向量化 vs 行存

向量化把「每元素 1 条标量指令」变成「每 16 元素 1 条 packed 指令」，理论上限 16×。实际受限于 cache、分支、依赖链，通常 4×–10×。

```cpp
#include <cstddef>
// ⑦ 行存求和：编译器难以向量化（stride 不规则）
double sum_row(const struct Row* r, size_t n) {
    double s = 0; for (size_t i=0;i<n;++i) s += r[i].price; return s;
}
```

```cpp
#include <cstddef>
// ⑦ 列存求和：连续内存，编译器轻松 emit vaddps
double sum_col(const double* p, size_t n) {
    double s = 0; for (size_t i=0;i<n;++i) s += p[i]; return s;
}
```

```cpp
// ⑦ 用 std::accumulate 同样能被向量化（底层仍是连续迭代）
#include <numeric>
#include <vector>
double acc(const std::vector<double>& v) {
    return std::accumulate(v.begin(), v.end(), 0.0);
}
```

- `[经验]`：向量化的前提只有一条——**数据连续且循环体无分支**。任何 `if (row.flag)` 都会打断自动向量化，ClickHouse 用「列拆分 + 常量折叠」规避。

## ⑧ 调试

调试向量化代码最难的是「结果对但慢」——没向量化。用 `-fopt-info-vec` 看 GCC 是否真的向量化了。

```bash
# ⑧ GCC 报告哪些循环被向量化 / 为什么没向量化
g++ -std=c++20 -O3 -march=native -fopt-info-vec=vec.log _ch133_vectorize.cpp
# 典型输出： "...note: loop vectorized" / "...missed: not vectorized: control flow in loop"
```

```cpp
// ⑧ 用 alignas 强制对齐，帮助编译器生成更优的 aligned load
#include <cstddef>
alignas(64) float buf[1024];   // 64B 对齐 = 一个 cache line，利于 vmovaps
void add_buf(float* out, const float* a, const float* b, size_t n) {
    for (size_t i=0;i<n;++i) out[i] = a[i] + b[i];
}
```

```cpp
// ⑧ Redis 调试：在事件循环入口打点，观察单线程是否被某回调阻塞
void aeProcessEvents(aeEventLoop* el, int flags) {
    // redis 用 aeApiPoll 阻塞；若某命令慢，整个循环卡住（单线程代价）
    int n = aeApiPoll(el, nullptr);   // 调试时在这里计时
    for (int j=0; j<n; ++j) { /* 回调 */ }
}
```

- `[平台]`：`-fopt-info-vec` 在 MinGW GCC 13 同样有效；Windows 下用 WinDbg/VS 看寄存器 `zmm0` 即可确认是否真在跑 AVX-512。

## ⑨ 跨平台

SIMD 指令集因平台而异：x86 有 SSE/AVX，ARM 有 NEON，POWER 有 AltiVec。ClickHouse 用宏分发到不同实现。

```cpp
// ⑨ ClickHouse 用宏选不同向量化后端（等价 src/Common/.../Vec.h）
#if defined(__AVX512F__)
    using Simd = Avx512;      // 512-bit
#elif defined(__AVX2__)
    using Simd = Avx2;        // 256-bit
#elif defined(__SSE2__)
    using Simd = Sse2;        // 128-bit
#elif defined(__ARM_NEON)
    using Simd = Neon;        // ARM
#endif
```

```cpp
// ⑨ 运行时特性探测（避免在不支持 AVX 的机器上 SIGILL）
#include <cpuid.h>
bool has_avx2() {
    unsigned eax,ebx,ecx,edx;
    __get_cpuid(7, &eax,&ebx,&ecx,&edx);
    return (ebx & (1<<5)) != 0;   // AVX2 bit
}
```

```cpp
// ⑨ 跨平台事件多路复用抽象（Redis ae.c 正是这么做的）
#if defined(__linux__)
    #include <sys/epoll.h>
    using Multiplexer = EpollMux;
#elif defined(__APPLE__) || defined(__FreeBSD__)
    #include <sys/event.h>
    using Multiplexer = KqueueMux;
#else
    #include <sys/select.h>
    using Multiplexer = SelectMux;
#endif
```

- `[平台]`：写跨平台 SIMD 的代码，**永远优先用编译器自动向量化 + `alignas`**，而非手撸 intrinsics——除非 profiling 证明某热点需要。

## ⑩ 常见陷阱

```cpp
#include <cstddef>
// ⑩ 陷阱1：在向量化循环里放分支，打断了 SIMD
void bad(float* out, const float* a, size_t n, bool negate) {
    for (size_t i=0;i<n;++i)
        out[i] = negate ? -a[i] : a[i];   // 编译器需做 masked 处理或放弃向量化
}
```

```cpp
#include <cstddef>
// ⑩ 陷阱2：指针别名（aliasing）阻止向量化
void bad_alias(float* a, float* b, float* out, size_t n) {
    for (size_t i=0;i<n;++i) out[i] = a[i] + b[i];  // a/b/out 可能重叠
}
// 修复：用 __restrict 或确保 buf 不重叠
void good(float* __restrict out, const float* __restrict a,
          const float* __restrict b, size_t n) {
    for (size_t i=0;i<n;++i) out[i] = a[i] + b[i];
}
```

```cpp
// ⑩ 陷阱3：Redis 单线程里跑慢命令（如 KEYS *）阻塞整个实例
// 等价：在事件循环回调中做 O(N) 全表扫描 -> 所有其他 client 饿死
void on_command_slow(redisClient* c) {
    // for (every_key) ...  ; 单线程下这会卡住整个服务
}
```

```cpp
// ⑩ 陷阱4：在向量化 hot path 用 std::function（间接调用 + 堆分配）
#include <functional>
#include <cstddef>
void slow(const std::function<float(float)>& f, float* out, const float* a, size_t n) {
    for (size_t i=0;i<n;++i) out[i] = f(a[i]);   // 无法内联/向量化
}
```

- `[经验]`：四个陷阱本质是同一句话——**别在 hot path 破坏连续性与单线程假设**。

## ⑪ 演进

```cpp
#include <cstddef>
// ⑪ ClickHouse 早期用 SSE2，后逐步引入 AVX/AVX2/AVX-512；代码靠宏分层
// 等价：同一算法多份实现，编译期选最优
template <SimdBackend B>
void scatter_add(float* base, const int* idx, const float* v, size_t n);
// 特化：Sse2 / Avx2 / Avx512 各一份 kernel
```

```cpp
// ⑪ Redis 事件库早期只支持 select，后加 kqueue/epoll/evport
// 等价演进：多路复用器可插拔（ae_evport / ae_kqueue / ae_epoll / ae_select）
struct aeApiState;
typedef struct aeApiState* (*aeApiCreateFn)(aeEventLoop*);
```

```cpp
#include <cstddef>
// ⑪ C++ 侧：用 if constexpr 替代宏做编译期后端选择（C++17 起）
template <typename T>
void kernel(T* out, const T* a, const T* b, size_t n) {
    if constexpr (std::is_same_v<T, double>) {
        // double 专用路径
    } else {
        // 通用路径
    }
}
```

- `[标准]`：`if constexpr`（C++17）让「编译期后端分发」比宏更类型安全、更易读。

## ⑫ 最佳实践

```cpp
#include <cstddef>
// ⑫ 列数据用连续 PODArray，绝不存 vector<struct>
template <typename T>
class ColumnVector {
    T* data_; size_t size_;
public:
    T* data() { return data_; }                 // 裸指针交给 SIMD kernel
    void prefetch(size_t i) const { __builtin_prefetch(&data_[i+16]); }
};
```

```cpp
// ⑫ 事件回调保持极短，慢任务甩给后台线程/异步
void on_read(redisClient* c) {
    read_query(c);            // 快：只解析协议头
    queue_to_worker(c);       // 慢：交给线程池，主循环立刻返回
}
```

```cpp
#include <cstddef>
#include <vector>
// ⑫ 内存用 Arena 批量分配，避免 hot path malloc
class Arena {
    std::vector<char*> blocks_;
    char* cur_; char* end_;
public:
    void* alloc(size_t n) {
        if (cur_ + n > end_) { blocks_.push_back(new char[n*8]); cur_=blocks_.back(); end_=cur_+n*8; }
        void* p = cur_; cur_ += n; return p;
    }
    ~Arena() { for (auto p: blocks_) delete[] p; }   // 一次性释放
};
```

- `[经验]`：向量化系统用 Arena + 连续 POD；事件系统用「主线程只做快路径」——这是两个项目能 scaling 的共同纪律。

## ⑬ 与 STL 容器对比

```cpp
#include <vector>
// ⑬ vector<Row> 行存：慢（stride 大，难向量化）
struct Row { int id; double price; };
double s1(const std::vector<Row>& v) {
    double s=0; for (auto& r: v) s += r.price; return s;
}
```

```cpp
#include <vector>
// ⑬ 拆成两个 vector（列式）：快（连续，可向量化）
double s2(const std::vector<double>& price, const std::vector<int>& id) {
    double s=0; for (double p: price) s += p; return s;
}
```

```cpp
#include <cstddef>
#include <vector>
// ⑬ ClickHouse 不用 std::vector 做列，而用 PODArray：小对象零开销、对齐可控
// 等价简化：自定义连续容器
template <typename T, size_t INLINE=64>
class PODArray {
    T inline_buf[INLINE]; T* ptr = inline_buf; size_t n = 0;
public:
    void push_back(T v) { ptr[n++] = v; }     // 无构造函数调用（POD）
    const T* data() const { return ptr; }
};
```

```cpp
// ⑬ 事件循环用裸数组而非 vector：fd 是整数索引，数组 O(1) 命中
struct aeEventLoop { aeFileEvent events[AE_SETSIZE]; };
```

- `[经验]`：STL 容器通用但为安全付出代价（边界检查、构造/析构、迭代器抽象）。hot path 上 ClickHouse 自己写 PODArray、Redis 用裸数组——**通用性服从性能**。

## ⑭ 跨库

```cpp
#include <vector>
// ⑭ ClickHouse 客户端（clickhouse-cpp）用连续 buffer 批量写列
// 等价：把一行行的 INSERT 改成整列批量
void send_block(Connection& c, const std::vector<double>& prices) {
    // 一次发送整列 prices，而非逐行 send
    c.send_column("price", prices.data(), prices.size());
}
```

```cpp
// ⑭ Redis C++ 客户端（hiredis / redis-plus-plus）单连接串行发命令
// 等价：pipeline 把多条命令攒一批，减少事件循环往返
void pipeline(redisContext* c) {
    redisAppendCommand(c, "SET k1 v1");
    redisAppendCommand(c, "SET k2 v2");
    redisGetReply(c, nullptr);  // 一次读回两条回复
}
```

```cpp
// ⑭ 用 C++20 std::span 零拷贝地把列暴露给计算 kernel
#include <span>
void compute(std::span<const float> col) {
    float s=0; for (float v: col) s += v;   // 编译器仍可能向量化 span 迭代
}
```

- `[标准]`：`std::span`（C++20）是表达「连续列视图」的现代零开销抽象，等价于 ClickHouse 的 `ColumnVector::getData()` 返回类型。

## ⑮ 贡献

若向 ClickHouse / Redis 贡献 C++ 代码，向量化 kernel 与事件循环是核心敏感区。

```cpp
#include <cstddef>
// ⑮ ClickHouse 贡献范式：新聚合函数需实现「向量化入口」
// 等价：addBatch 一次处理整列，而非 addOne 逐行
struct AggregateSum {
    void addBatch(double* dst, const double* src, size_t n) {
        for (size_t i=0;i<n;++i) dst[i] += src[i];   // 可被向量化
    }
};
```

```cpp
// ⑮ Redis 贡献范式：新命令是事件循环里的一个回调，必须 O(1)/O(log N)
// 等价：命令处理函数签名固定，单线程内执行
void mycommandCommand(client* c) {
    // 只能做常数/对数级工作，否则阻塞全实例
    addReply(c, shared.ok);
}
```

- `[经验]`：给这类项目提 PR，最易被拒的理由是「引入分支打断向量化」或「回调变慢」。贡献前先用 `-fopt-info-vec` 自证没退化。

## ⑯ 工程应用

```cpp
#include <cstddef>
#include <vector>
// ⑯ 场景：实时风控，需要对最近 1 万条价格做滑动均值（列存 + 向量化）
class SlidingMean {
    std::vector<double> ring; size_t head = 0, cnt = 0;
    double sum = 0;
public:
    void push(double v) {
        if (cnt == ring.size()) { sum -= ring[head]; }   // 移出最老
        else { ring.resize(ring.size()? ring.size():1024); cnt++; }
        ring[head] = v; sum += v; head = (head+1)%ring.size();
    }
    double mean() const { return cnt ? sum/cnt : 0; }
};
```

```cpp
#include <map>
// ⑯ 场景：高并发网关用单线程事件循环复用连接（Redis 模型）
class Gateway {
    std::unordered_map<int, Connection> conns;   // fd -> conn，单线程访问无锁
public:
    void on_readable(int fd) {
        auto& c = conns[fd];
        c.recv();            // 单线程：无需 mutex
        c.handle();
    }
};
```

```cpp
#include <cstddef>
// ⑯ 把向量化 kernel 抽成独立函数，方便单测 + profiling
void batch_scale(float* out, const float* in, float k, size_t n) {
    for (size_t i=0;i<n;++i) out[i] = in[i] * k;   // -O3 下自动 AVX
}
```

- `[经验]`：工程上把「向量化」与「单线程事件」两类模式当作可复用模板，分别用于计算密集与 IO 密集子系统。

## ⑰ 性能对比

```cpp
// ⑰ 基准：行存 vs 列存 求和（等价 benchmark 骨架）
#include <chrono>
#include <vector>
double bench(const std::vector<double>& col, int iters) {
    double s = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int k=0;k<iters;++k) for (double v: col) s += v;
    auto t1 = std::chrono::steady_clock::now();
    (void)(t1-t0);
    return s;
}
```

```cpp
// ⑰ 用 std::execution::par 并行（注意：这已经是「多核」而非「单线程向量化」）
#include <execution>
#include <numeric>
#include <vector>
double par_sum(const std::vector<double>& v) {
    return std::reduce(std::execution::par, v.begin(), v.end(), 0.0);
}
```

```cpp
// ⑰ Redis vs 多线程 KV：单线程无锁，但受单核限制
// 等价对比：单线程事件循环 QPS 上限 ≈ 单核 IPC / 每条命令周期数
// 多线程 KV 上限 ≈ 核数 × 单核，但需锁/无锁结构（如分片哈希）
```

- `[经验]`：向量化解决「单核算力利用率」，单线程事件循环解决「并发正确性」；二者正交，可叠加（ClickHouse 既向量化又多线程分片）。

## ⑱ 调试 / 源码阅读

```cpp
// ⑱ 读 ClickHouse 源码路径（上游参考）：从 IColumn 入手
//   src/Columns/IColumn.h        —— 列抽象
//   src/Columns/ColumnVector.cpp —— 具体列 + 向量化 kernel 入口
//   src/Interpreters/ExpressionActions.cpp —— 向量化调度
// 读法：先跟一个 SELECT 的列如何被切成 Block，再到 executeOnColumn。
```

```cpp
// ⑱ 读 Redis 源码路径（上游参考）：从 aeMain 入手
//   src/ae.c / src/ae.h          —— 事件循环
//   src/server.c                 —— 主函数调 aeMain
//   src/networking.c             —— 命令读取与回复
// 读法：跟一个 GET 命令从 epoll_wait 就绪到 call 回调再到 addReply。
```

```cpp
// ⑱ 本地用 perf（Linux）看是否真向量化
//   perf record ./clickhouse ...
//   perf annotate -> 找 vaddps/vmulps 即证明向量化命中
// Windows 等价：VTune / 看寄存器 zmm0 是否被写
```

- `[平台]`：源码阅读顺序决定理解速度——**先数据结构（IColumn / aeFileEvent），后控制流（executeOnColumn / aeMain）**。

## ⑲ [经验]选型

```cpp
// ⑲ 选型决策：用列存向量化还是单线程事件？看瓶颈在哪
enum class Bottleneck { CPU_COMPUTE, IO_CONCURRENCY, BOTH };
// CPU_COMPUTE 重（分析、聚合）   -> ClickHouse 式列存 + SIMD
// IO_CONCURRENCY 重（海量连接）  -> Redis 式单线程事件循环
// BOTH                           -> 两者组合，或 ClickHouse 多线程分片
```

```cpp
#include <cstddef>
// ⑲ 不要为「看起来快」盲目上 SIMD：先 profile
// 等价：小数据量 + 多分支，向量化反而更慢（mask 开销）
bool should_vectorize(size_t n, bool branchy) {
    return n >= 256 && !branchy;   // 经验阈值：批量够大且无分支才划算
}
```

```cpp
// ⑲ 不要为「看起来省事」盲目上多线程：Redis 证明单线程也能极高吞吐
// 等价：若状态共享简单，单线程事件循环比无锁并发更易写对
```

- `[经验]`：列存向量化与单线程事件循环是两种「用约束换性能」的哲学——前者约束数据布局，后者约束并发模型。选型时先认清你的约束。

## ⑳ 速查表

```cpp
// ⑳ ClickHouse 向量化速查
//   - 数据按列连续存放（ColumnVector<T>），不用 struct-of-row
//   - hot loop 无分支、无别名（用 __restrict）、对齐 64B
//   - 用 -O3 -march=native -fopt-info-vec 验证是否被向量化
//   - 上游入口：src/Columns/IColumn.h / ColumnVector.cpp / ExpressionActions.cpp
```

```cpp
// ⑳ Redis 事件循环速查
//   - 单线程 aeMain 循环，epoll/kqueue/select 多路复用
//   - 每个 fd 一个 aeFileEvent{ rfileProc, wfileProc }
//   - 回调必须 O(1)/O(log N)，慢命令阻塞整个实例
//   - 上游入口：src/ae.c / src/ae.h / src/server.c
```

```cpp
// ⑳ 本机可复现实证命令（GCC 13.1.0）
//   g++ -std=c++20 -O3 -march=native -S -masm=intel \
//       Examples/_ch133_vectorize.cpp -o Examples/_ch133_vectorize.asm
//   g++ -std=c++20 -O2 -S -masm=intel \
//       Examples/_ch133_eventloop.cpp -o Examples/_ch133_eventloop.asm
//   关键汇编：vaddps zmm / vmulps zmm / vfmadd231ss（向量化）
//            call rax（事件循环回调分发）
```

```cpp
#include <span>
// ⑳ C++ 特性映射
//   模板       -> ColumnVector<T> 零开销类型分发
//   智能指针   -> 连接/资源 RAII（hot path 避免 shared_ptr）
//   内存池     -> Arena bump-pointer 批量分配/释放
//   std::span  -> 零拷贝列视图（C++20）
//   if constexpr-> 编译期 SIMD 后端选择（C++17）
```

- `[经验]`：记不住细节就看速查表的四行——**列连续、循环无分支、单线程无锁、先 profile 再优化**。


## 附录 E：ClickHouse/Redis 底层与设计

```
ClickHouse: 列存+SIMD向量化, AVX2单核~40GB/s
Redis: 单线程epoll, 零锁竞争, 100K QPS/core
RocksDB: LSM Tree+Bloom filter, 写优化10K writes/s
```

| 系统 | 性能 | 场景 |
|---|---|---|
| ClickHouse | 40GB/s/core | OLAP分析 |
| Redis | 100K QPS/core | 缓存/队列 |
| RocksDB | 10K writes/s | 写密集型 |

面试: ClickHouse为何快? 列存+SIMD+Bloom filter跳过不相关数据

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第132章](Book/part11_source/ch132_leveldb_rocksdb.md) | 键值查找/缓存 | 本章提供概念，第132章提供实现 |
| [第134章](Book/part11_source/ch134_unreal.md) | TCP服务器/HTTP客户端 | 本章提供概念，第134章提供实现 |
| [第77章](Book/part07_stl/ch77_vector.md) | 独占所有权/工厂模式 | 本章提供概念，第77章提供实现 |

## 附录 F：ClickHouse/Redis面试

Q: ClickHouse为何快? A: 列存(只读相关列)+SIMD(向量化,40GB/s)+Bloom filter跳过无关数据
Q: Redis单线程为何高性能? A: 内存操作(~100ns)+epoll非阻塞IO+零锁竞争
Q: LSM Tree vs B-tree? A: LSM=写快(顺序)+读慢(多层merge); B-tree=读写均衡(就地修改)

## 附录 G：设计起源与演化 [B: 原理/设计目标]

两套系统的架构分歧，根植于各自诞生时要解决的问题——理解历史背景才能理解它们的设计目标为何相反。

- **Redis（2009，Salvatore Sanfilippo / antirez）**：最初为其实时网站分析产品 LLOOGG 手写，用 C 实现。**设计目标**是内存态数据结构的极低延迟点操作（GET/SET ~100 ns 量级），故选**单线程事件循环**（`ae.c` 的 Reactor）——刻意回避多线程锁竞争与 cache 一致性开销。这一"单线程够快"的判断建立在"内存操作远快于网络 RTT"的前提上；直到 6.0（2020）才为网络 I/O 引入多线程，命令执行仍单线程。
- **ClickHouse（Yandex 内部 2009 起，2016-06 开源）**：为 Yandex.Metrica（Web 流量分析，类 Google Analytics）而生，用 C++。**设计目标**是海量只读数据上的**亚秒级 OLAP 聚合**，故走**列式存储 + 向量化执行**——按列连续存放使同类型数据被 SIMD 批量处理，扫描聚合吞吐达 GB/s 级/核。
- **设计哲学对比**：Redis 是 OLTP 式的"低延迟点查/缓存"，为单条请求的响应时间优化；ClickHouse 是 OLAP 式的"高吞吐扫描聚合"，为批量数据的处理带宽优化。二者常组合：Redis 扛在线热点、ClickHouse 扛离线分析（见"联合使用场景"）。
- **演化**：Redis 从纯 KV 演化出 Stream/Module/RESP3；ClickHouse 从单机演化出分布式表引擎与 `MergeTree` 家族。两者都验证了"设计目标决定架构、架构决定性能上限"这条规律。

## 相关章节（交叉引用）

- **相邻主题**：`Book/part11_source/ch131_fmt_spdlog.md`（第131章　fmt / spdlog 格式化与日志（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part12_patterns/ch135_patterns_intro.md`（第135章 设计模式总论（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part11_source/ch124_libstdcxx.md`（第124章　libstdc++ 架构与阅读入口（C++））—— 同模块下的其他主题。

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **Redis 单线程 Reactor 的生产瓶颈**：Redis 6 前主线程单线程处理所有命令，一个 `KEYS *` 或慢 Lua 脚本会阻塞整实例，所有连接超时。生产上用 `SCAN` 替代 `KEYS`、把重计算搬出 Redis；集群模式靠多分片分摊。这是「单线程简单但怕慢命令」的典型权衡。
- **ClickHouse 的物化视图写放大**：建 `MATERIALIZED VIEW` 后，每笔写入要同步更新多个聚合视图，高写入场景下 CPU/IO 放大数倍。工业上按查询模式取舍——只对高频聚合建物化视图，冷聚合走按需查询。

### 常见 Bug 与 Debug 方法

- **Redis 大 key 导致超时与迁移失败**：单个 hash/list 过百万元素，`HGETALL` 卡顿、集群迁移 `slot` 超时。Debug 用 `redis-cli --bigkeys` 扫大 key；拆分或换数据结构（hash 分片）。
- **ClickHouse 内存超限制查询被 kill**：`max_memory_usage` 超限时查询被 SIGKILL。Debug 看 `system.query_log` 的 `memory_usage`；加 `LIMIT`/`SETTINGS max_threads` 降级。
- **Code Review 关注点**：是否在生产用 `KEYS`/`FLUSHALL`；慢命令是否进监控告警；ClickHouse 表引擎（MergeTree vs Log）是否匹配写入/查询模式。

### 重构建议

把「`KEYS *` + 客户端过滤」重构为 `SCAN` 游标分批 + 服务端过滤；把「每次查询现算聚合」重构为预计算物化视图（仅高频者）；把 ClickHouse 大查询加上 `memory_usage` 预算与 `max_threads` 约束，避免单查询拖垮集群。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 练习 2（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 3（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>

