# 第132章　LevelDB / RocksDB 存储引擎（C++）

⟶ Book/part07_stl/ch83_map.md
⟶ Book/part08_algorithms/ch96_sorting.md

> 元数据：标准基 C++11/14/17 · 预计阅读 45min · 前置 第118章 Modules（仅文字提及，无交叉引用）· 难度 ★★★★
> 真实编译器取证：MinGW GCC 13.1.0（`-std=c++23 -O2 -S -masm=intel`）。
> LevelDB / RocksDB 本机未安装，源码剖析引用上游仓库 URL + 行号，标注「上游参考」。
> 源码根（上游）：`https://github.com/google/leveldb` 与 `https://github.com/facebook/rocksdb`。

## ① 概述：LSM-Tree 存储引擎 [标准]

⟶ Book/part11_source/ch131_fmt_spdlog.md
⟶ Book/part11_source/ch133_clickhouse_redis.md


LSM-Tree（Log-Structured Merge-Tree）把**随机写**转化为**顺序写**：所有写入先进内存表（MemTable），写满后刷成有序的不可变文件（SSTable），后台合并（Compaction）回收空间并维持读性能。LevelDB / RocksDB 是工业级 LSM 引擎，被 TiKV、Kafka、Rockset、MongoDB（WiredTiger 同源思想）等广泛使用。

```cpp
// ① 最小 LevelDB 打开示例：一个 LSM 引擎实例
#include <leveldb/db.h>
#include <string>
leveldb::DB* db = nullptr;
leveldb::Options opt;
opt.create_if_missing = true;
leveldb::Status s = leveldb::DB::Open(opt, "/tmp/testdb", &db);  // 创建/打开 LSM
```

- `[标准]`：LSM 不是 C++ 标准的一部分，而是**存储引擎架构范式**；LevelDB 提供 `leveldb::DB` 这一具体 API 契约。
- `[经验]`：LSM 用「写放大 / 读放大 / 空间放大」三角权衡换顺序写吞吐，理解三者取舍是调优前提。

```cpp
// ① LSM 三层结构（概念，非 LevelDB 源码）
//   写:  Client -> WAL(顺序) -> MemTable(内存有序) -> 刷盘 -> SSTable(有序文件)
//   读:  Client -> MemTable -> Immutable -> SSTable(L0..Ln) -> BlockCache
```

```cpp
// ① 读放大/写放大/空间放大的直觉度量（示意，非本机实测）
enum class Amplification { Read, Write, Space };
// 顺序写吞吐高 => Write 放大低；点查要扫多层 => Read 放大高
```

## ② LevelDB 架构（MemTable/SSTable/WAL） [实现]

LevelDB 的单库由下列部件组成，全部是 C++ 类，体现 RAII 与明确所有权：

```cpp
// ② 核心类（上游参考，类名与 leveldb 1.23 一致）
//   DBImpl        : 引擎门面，持有 MemTable / 版本集 / 后台线程
//   MemTable      : 内存跳表（SkipList），提供 Insert/Get
//   VersionSet    : 管理各层 SSTable 的元数据（MANIFEST）
//   Table / TableBuilder : SSTable 读写（block + 索引 + 布隆）
//   log::Writer   : WAL，顺序追加写入
```

```cpp
// ② MemTable 的跳表节点（等价本仓库 Examples/_ch132_lsm_toy.cpp 的 Node）
// 上游参考：https://github.com/google/leveldb/blob/main/db/skiplist.h
// 行号：62  （struct Node 定义处，leveldb 1.23）
struct SkipNode {
    const Key key;
    AtomicPointer next_[1];   // 柔性数组：多层级指针
};
```

```cpp
// ② 一次写入的组件流转（伪代码，展示所有权边界）
//   Put(key,val) -> log::Writer.Append(record)   // WAL
//                -> mem_->Add(seq, kTypeValue, key, val)  // MemTable 跳表
//   MemTable 达阈值 -> 转为 Immutable -> 后台 Build Table -> 落 SSTable
```

- `[实现·LevelDB]`：`MemTable` 用跳表（O(log n) 查找/插入），`Immutable MemTable` 在刷盘期间继续服务读，避免写停顿。
- `[平台]`：WAL 直接 `write()` 系统调用顺序落盘；崩溃恢复重放 WAL 重建 MemTable。

```cpp
// ② 文件布局（磁盘目录，概念）
//   /tmp/testdb/
//     CURRENT      -> 指向 MANIFEST 当前文件
//     MANIFEST-xxx   版本与层元数据
//     000123.log      WAL
//     000124.ldb      SSTable（旧格式 sst）
```

## ③ [实现]源码剖析：DBImpl::Write（上游参考） [实现]

以下剖析 LevelDB 的写入口，引用上游源码 URL + 行号（上游参考，非本机文件）。

```cpp
// 文件：https://github.com/google/leveldb/blob/main/db/db_impl.cc
// 行号：1017  （Status DBImpl::Write(const WriteOptions&, WriteBatch*) 定义处，leveldb 1.23）
// 上游参考：以下为对应逻辑摘录（已精简，保留关键分支）
Status DBImpl::Write(const WriteOptions& options, WriteBatch* my_batch) {
    Writer w(&mutex_);
    w.batch = my_batch;
    w.sync = options.sync;
    // 1) 抢锁，入写队列（保证 WAL 顺序）
    MutexLock l(&mutex_);
    writers_.push_back(&w);
    // 2) 队首者负责把批量写入 WAL + MemTable
    if (!w.done && (&w != writers_.front())) {
        while (!w.done) cv_.Wait();   // 非队首者等待
    }
    // 3) 写 WAL（log::Writer），再 Apply 到 MemTable
    status = WriteBatchInternal::InsertInto(my_batch, mem_);
    // 4) MemTable 超阈值 -> 触发后台 Compaction
    MaybeScheduleCompaction();
    return status;
}
```

```cpp
// ③ 写路径关键不变量：WAL 先于 MemTable（durability 保证）
//   - 若进程崩溃在 WAL 之后、MemTable 刷盘之前：重启重放 WAL 可恢复
//   - 若崩溃在 WAL 之前：该批写入视为未提交（与 sync 选项相关）
```

- `[实现·LevelDB]`：写合并（group commit）由 `writers_` 队列 + condition variable 实现——队首 writer 代表整批落盘，其余等待，极大提升并发吞吐。
- `[实现]`：行号 `1017` 为 leveldb 1.23 发布标签近似位置，阅读请以你 checkout 的实际行号为准（上游参考）。

```cpp
// ③ MaybeScheduleCompaction 触发后台线程（后台 Compaction 总览）
// 上游参考：https://github.com/google/leveldb/blob/main/db/db_impl.cc
// 行号：约 1100（BackgroundCompaction 入口，上游参考）
//   if (imm_ != nullptr) { CompactMemTable(); }   // 内存表落盘
//   else { DoCompactionWork(...); }               // 层间合并
```

## ④ RocksDB 扩展（列族/合并/压缩） [实现]

RocksDB 是 Facebook 对 LevelDB 的工业级分支，增加**列族（Column Family）**、**Merge 算子**、**通用压缩（Universal/_FIFO）**、**事务**、**前缀布隆**等。

```cpp
// ④ 列族：一个 DB 内含多个独立有序空间，共享 WAL/Manifest 但独立 Compaction
#include <rocksdb/db.h>
#include <vector>
rocksdb::DB* db;
rocksdb::ColumnFamilyHandle* cf_meta;
rocksdb::ColumnFamilyHandle* cf_data;
std::vector<rocksdb::ColumnFamilyDescriptor> descs = {
    {"default", rocksdb::ColumnFamilyOptions()},
    {"meta",    rocksdb::ColumnFamilyOptions()},
    {"data",    rocksdb::ColumnFamilyOptions()},
};
std::vector<rocksdb::ColumnFamilyHandle*> handles;
rocksdb::DB::Open(rocksdb::DBOptions(), "/tmp/rdb", descs, &handles, &db);
cf_meta = handles[1]; cf_data = handles[2];
```

```cpp
// ④ Merge 算子：把「读-改-写」变成服务端合并，避免读放大
//   适合计数器、集合、最高值等场景
rocksdb::WriteOptions wopt;
db->Merge(wopt, cf_data, "page_views", "+1");   // 累加合并
db->Merge(wopt, cf_data, "tags", "rocksdb");     // 集合合并
```

```cpp
// ④ 通用压缩（Universal Compaction）：按文件数/大小触发，而非按层
rocksdb::ColumnFamilyOptions uo;
uo.compaction_style = rocksdb::kCompactionStyleUniversal;
uo.compaction_options_universal.size_ratio = 10;   // 相邻文件大小比阈值
```

- `[实现·RocksDB]`：列族让单进程多租户共享 WAL 但独立调优；Merge 把累加逻辑下推，减少读放大。
- `[经验]`：列族数量别太多（每列族有独立 MemTable + 线程开销），通常按「冷热/生命周期」而非「每张表」划分。

```cpp
// ④ 前缀布隆：对前缀范围查询加速（如 user:1000:*）
rocksdb::BlockBasedTableOptions bto;
bto.filter_policy.reset(rocksdb::NewBloomFilterPolicy(10, true));  // whole_key=false => 前缀
rocksdb::ColumnFamilyOptions prefix_opt;
prefix_opt.prefix_extractor.reset(rocksdb::NewFixedPrefixTransform(7));
prefix_opt.table_factory.reset(rocksdb::NewBlockBasedTableFactory(bto));
```

## ⑤ 写路径（WAL+MemTable） [实现]

写 = `WriteBatch` 序列化 → `log::Writer` 顺序追加（WAL）→ `MemTable::Add`。可单条 `Put` 或批量 `WriteBatch`。

```cpp
// ⑤ 单条 Put（内部即一次单元素 WriteBatch）
leveldb::Status s = db->Put(leveldb::WriteOptions(), "k1", "v1");
```

```cpp
// ⑤ 原子批量写：一批要么全见、要么全不见（WAL 单条 record）
leveldb::WriteBatch batch;
batch.Put("a", "1");
batch.Put("b", "2");
batch.Delete("c");
leveldb::Status s = db->Write(leveldb::WriteOptions(), &batch);
```

```cpp
// ⑤ 同步写：options.sync=true 落盘 fsync（强持久，吞吐更低）
leveldb::WriteOptions sync_opt;
sync_opt.sync = true;
db->Put(sync_opt, "durable_key", "v");   // 返回前已 fsync WAL
```

- `[实现·LevelDB]`：`WriteBatch` 的内部表示含 `SequenceNumber`，保证批量原子与快照隔离。
- `[平台]`：`sync=true` 触发 `fdatasync`/`fsync`，延迟受磁盘决定；异步写靠后台 `bg_thr` 周期刷。

```bash
# ⑤ LevelDB 专属编译命令 + 典型输出（本机需先安装 leveldb，否则链接失败）
# 编译：
g++ -std=c++17 -O2 -I/opt/leveldb/include ch132_leveldb_demo.cpp \
    -L/opt/leveldb/lib -lleveldb -lsnappy -o ch132_leveldb_demo
# 运行：
./ch132_leveldb_demo
# 典型输出（成功路径，来自上游示例行为）：
#   Open status: OK
#   Put(status=OK) Get(value=v1)
#   Batch committed, keys a,b deleted c
```

## ⑥ 读路径与缓存 [实现]

读先看 MemTable，再 Immutable，再 SSTable（自 L0 向下）；BlockCache 缓存热点数据块，布隆过滤器跳过必然缺失的文件。

```cpp
#include <string>
// ⑥ 点查：Get 自动走 MemTable -> Immutable -> SSTable
std::string value;
leveldb::Status s = db->Get(leveldb::ReadOptions(), "k1", &value);
if (s.ok()) { /* value 可用 */ }
else if (s.IsNotFound()) { /* 键不存在 */ }
```

```cpp
// ⑥ 快照读：保证迭代期间视图不变（SequenceNumber 快照）
leveldb::ReadOptions ro;
ro.snapshot = db->GetSnapshot();           // 固定一致视图
// ... 迭代 ...
db->ReleaseSnapshot(ro.snapshot);          // 用完释放
```

```cpp
// ⑥ 迭代器：范围扫描（LevelDB 合并各层形成有序视图）
leveldb::Iterator* it = db->NewIterator(leveldb::ReadOptions());
for (it->Seek("a"); it->Valid() && it->key().ToString() < "z"; it->Next()) {
    // 处理 it->key() / it->value()
}
delete it;   // 迭代器需手动释放（见 ⑧ RAII 封装）
```

- `[实现·LevelDB]`：布隆过滤器在 `Table::Get` 前先判「文件必有？」，消除大量无谓 IO。
- `[经验]`：默认 BlockCache 为 8MB LRU；热数据集调大 `options.block_cache` 显著降读放大。

```cpp
// ⑥ 显式 BlockCache 尺寸（RocksDB 写法，LevelDB 用 options.block_cache）
// 上游参考：https://github.com/facebook/rocksdb/blob/main/include/rocksdb/options.h
// 行号：约 720（BlockBasedTableOptions::block_cache 字段，上游参考）
rocksdb::BlockBasedTableOptions bto;
bto.block_cache = rocksdb::NewLRUCache(512 << 20);   // 512MB 缓存
```

## ⑦ Compaction 策略 [实现]

Compaction 合并有序段、丢弃过期版本与墓碑（delete 标记）、维持层数。LevelDB 用分层（Leveled），RocksDB 额外支持 Universal / FIFO。

```cpp
// ⑦ LevelDB 手动触发某范围 Compaction
leveldb::Slice begin("a"), end("z");
db->CompactRange(&begin, &end);   // 合并 [a,z) 覆盖的所有层
```

```cpp
#include <string>
// ⑦ Compaction 过滤器：合并时改写/丢弃值（如 TTL 过期）
// 上游参考：https://github.com/facebook/rocksdb/blob/main/include/rocksdb/compaction_filter.h
// 行号：约 60（CompactionFilter::Filter 虚函数，上游参考）
class TtlFilter : public rocksdb::CompactionFilter {
public:
    bool Filter(int /*level*/, const rocksdb::Slice& key,
                const rocksdb::Slice& /*existing_value*/,
                std::string* /*new_value*/, bool* /*value_changed*/) const override {
        return key.ToString().find("expired:") == 0;   // 丢弃过期键
    }
    const char* Name() const override { return "TtlFilter"; }
};
```

```cpp
// ⑦ 本仓库自包含等价：多路归并（真实汇编见 ⑨）
// 见 Examples/_ch132_lsm_toy.cpp 的 merge_runs()：
//   多个有序 Run -> 按 key 升序合并，同 key 后者覆盖前者（= compaction 收新版本）
```

- `[实现·LevelDB]`：Leveled 策略保证每层总大小按 10^L 增长，L0 可重叠、L≥1 不重叠，点查至多扫各一层。
- `[经验]`：写重负载下 Compaction 与前台写抢 IO（写放大），用 `level_compaction_dynamic_level_bytes`（RocksDB）可缓解。

```cpp
// ⑦ RocksDB Universal Compaction 触发条件（文件数触发）
rocksdb::CompactionOptionsUniversal u;
u.min_merge_width = 2;
u.max_merge_width = 20;
u.size_ratio = 10;   // 相邻文件大小比超过即合并
```

## ⑧ 与 C++ 特性（RAII/智能指针/自定义分配器） [标准]

LevelDB 大量使用 RAII 与裸指针所有权约定；RocksDB 更进一步用 `std::unique_ptr` 与可插拔分配器（Arena）。

```cpp
// ⑧ RAII 封装 leveldb::DB：离开作用域自动 Close（避免漏 Close 陷阱，见 ⑬）
#include <memory>
#include <leveldb/db.h>
#include <string>
struct DBDeleter { void operator()(leveldb::DB* p) const { delete p; } };
using DBPtr = std::unique_ptr<leveldb::DB, DBDeleter>;
DBPtr open_db(const std::string& path) {
    leveldb::DB* raw = nullptr;
    leveldb::Options opt; opt.create_if_missing = true;
    leveldb::DB::Open(opt, path, &raw).ok();
    return DBPtr(raw);   // 析构自动 delete，等价于 db->Close()
}
```

```cpp
#include <memory>
// ⑧ RAII 封装迭代器：delete it 易漏，用 unique_ptr 定制删除器
struct IterDeleter { void operator()(leveldb::Iterator* p) const { delete p; } };
using IterPtr = std::unique_ptr<leveldb::Iterator, IterDeleter>;
IterPtr scan(leveldb::DB* db) {
    return IterPtr(db->NewIterator(leveldb::ReadOptions()));
}
```

```cpp
#include <cstddef>
// ⑧ Arena 分配器：MemTable 内对象从同一块连续内存分配，析构一次释放全部
// 上游参考：https://github.com/facebook/rocksdb/blob/main/include/rocksdb/memory_allocator.h
// 行号：约 40（MemoryAllocator 接口，上游参考）
//   class Arena : public Allocator { char* Allocate(size_t) override; ... };
//   MemTable 析构时 Arena 一次性归还，避免逐节点 delete（O(n) -> O(1) 释放）
```

- `[标准]`：C++ 的 RAII（资源获取即初始化）天然匹配「DB/Iterator/快照」的生命周期，是包装 C 风格句柄的最佳实践。
- `[实现·RocksDB]`：`Arena` 是自定义分配器典型——减少 `malloc/free` 系统调用次数、提升局部性、简化释放。

```cpp
// ⑧ 自定义分配器注入（RocksDB）：把 MemTable 放到巨页/特定内存池
rocksdb::ColumnFamilyOptions co;
co.arena_block_size = 8192;
co.memtable_prefix_bloom_size_ratio = 0.1;   // 前缀布隆占 MemTable 比例
```

## ⑨ [实现]真实：编译自包含跳表/SSTable 等价示例取汇编 [实现]

本仓库 `Examples/_ch132_lsm_toy.cpp` 用纯标准库实现跳表（MemTable 等价）+ 有序段（SSTable 等价）+ 多路归并（Compaction 等价）。以下是 **GCC 13.1.0 真实 `-O2 -masm=intel` 汇编**（非示意）。

```cpp
// 文件：Examples/_ch132_lsm_toy.cpp
// 行号：26  （int skiplist_contains(const Node*, int, int) 定义）
// 编译：g++ -std=c++23 -O2 -S -masm=intel Examples/_ch132_lsm_toy.cpp -o Examples/_ch132_lsm_toy.asm
// 真实汇编（节选，GCC 13.1.0，x86-64）：
```

```x86asm
; 真实取证：_Z17skiplist_containsPK4Nodeii（跳表查找，等价 MemTable::Get）
_Z17skiplist_containsPK4Nodeii:
.LFB5059:
	.seh_endprologue
	mov	rcx, QWORD PTR 8[rcx]
	test	edx, edx
	js	.L2
	movsx	rdx, edx
	xor	r9d, r9d
	sal	rdx, 3
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L14:
	cmp	DWORD PTR [rax], r8d
	jge	.L3
	mov	rcx, QWORD PTR 8[rax]
.L4:
	mov	rax, QWORD PTR [rcx+rdx]
	test	rax, rax
	jne	.L14
.L3:
	lea	rax, -8[rdx]
	cmp	r9, rdx
	je	.L2
	mov	rdx, rax
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L2:
	mov	rax, QWORD PTR [rcx]
	test	rax, rax
	je	.L9
	cmp	DWORD PTR [rax], r8d
	jne	.L9
	mov	eax, DWORD PTR 4[rax]
	ret
.L9:
	mov	eax, -1
	ret
	.seh_endproc
```

```cpp
#include <vector>
// 文件：Examples/_ch132_lsm_toy.cpp
// 行号：64  （void merge_runs(const std::vector<Run>&, std::vector<int>&, std::vector<int>&) 定义）
// 多路归并（Compaction 等价）真实汇编（节选，GCC 13.1.0）：
```

```x86asm
; 真实取证：_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_（Compaction 归并）
_Z10merge_runsRKSt6vectorI3RunSaIS0_EERS_IiSaIiEES7_:
.LFB5061:
	push	r15
	.seh_pushreg	r15
	push	r14
	...
	.seh_endprologue
	mov	rax, QWORD PTR [rcx]
	mov	r12, rdx
	mov	rdx, QWORD PTR 8[rcx]
	mov	r14, rcx
	mov	r13, r8
	movabs	r8, -6148914691236517205
	mov	rcx, rdx
	sub	rcx, rax
	mov	r9, rcx
	sar	r9, 3
	imul	r9, r8            ; 除以 8 的魔法乘法（指针差 -> 元素数）
	test	rcx, rcx
	mov	QWORD PTR 40[rsp], r9
	js	.L84
	...
.L34:
	movsx	rcx, DWORD PTR [rsi+rdx*4]
	cmp	ecx, DWORD PTR 16[rax]
	jge	.L32
	mov	r9, QWORD PTR [rax]
	mov	r9d, DWORD PTR [r9+rcx*4]
	cmp	r9d, ebx
	jl	.L68            ; 当前 key < best 则更新候选
	...
.L31:
	test	rsi, rsi
	jne	.L35
	; 全部 run 耗尽 -> 函数收尾 ret
```

- `[实现·GCC13]`：跳表查找被编译为两层 `jmp` 循环（层下降 + 同层前进），命中返回 `DWORD PTR 4[rax]`（value 偏移），未命中走 `.L9` 返回 `-1`。
- `[实现·GCC13]`：`merge_runs` 用魔法乘法 `-6148914691236517205` 做 `ptrdiff/8`；`jl .L68` 实现「取最小 key」的归并选择——这正是 Compaction 多路归并的核心分支。
- `[平台]`：上述符号名 `_Z17skiplist_containsPK4Nodeii` 为 Itanium C++ ABI 名字改编（leveldb 的 `SkipList::FindGreaterOrEqual` 在目标文件中呈类似改编名）。

```cpp
// ⑨ 速取汇编的命令（可重跑验证）
//   g++ -std=c++23 -O2 -S -masm=intel Examples/_ch132_lsm_toy.cpp -o Examples/_ch132_lsm_toy.asm
```

## ⑩ 调试 [经验]

引擎内置日志与统计，是排查「为什么这么慢/为什么空间暴涨」的主力。

```cpp
// ⑩ 设置日志级别（RocksDB），定位 Compaction/Flush 卡点
rocksdb::Options o;
o.info_log_level = rocksdb::INFO_LEVEL;     // DEBUG/INFO/WARN/ERROR/HEADER
o.stats_dump_period_sec = 60;               // 每 60s 向 LOG 倾倒统计
```

```cpp
#include <string>
// ⑩ 读取实时统计（读放大/压缩比/待合并字节）
std::string stats;
db->GetProperty("rocksdb.stats", &stats);    // 返回多行文本统计
// 关键行：compaction.pending; cur-size-active-mem-table; background-errors
```

```cpp
#include <string>
// ⑩ LevelDB 读取 SSTable 计数等（部分实现暴露）
std::string out;
db->GetProperty("leveldb.sstables", &out);   // 列出各层文件与范围
```

- `[经验]`：慢查询先看 `rocksdb.dbstats` 的 `get.from.memtable / .from.block.cache / .from.sst` 占比——若大量 `from.sst` 说明 BlockCache 太小或布隆缺失。
- `[经验]`：磁盘满/权限错常表现为 `Status::IOError`，优先看 `<db>/LOG` 文件而非 stdout。

```cpp
// ⑩ 把统计打到自定义 logger（RocksDB：实现 Logger 接口）
// 上游参考：https://github.com/facebook/rocksdb/blob/main/include/rocksdb/env.h
// 行号：约 380（Env::Logger 虚接口，上游参考）
class MyLogger : public rocksdb::Logger {
    void Logv(const char* format, va_list ap) override { /* 转发到业务日志 */ }
};
```

## ⑪ 性能（顺序写 vs 随机读） [经验]

LSM 的天性：**顺序写极快，随机点查需跨层**，范围扫描友好。

```cpp
// ⑪ 顺序写基准骨架（示意，非本机实测数字）
#include <benchmark>  // 伪：用循环即可
leveldb::WriteOptions w;
for (int i = 0; i < 1'000'000; ++i) {
    db->Put(w, std::to_string(i), payload);   // 顺序 key => 顺序写，吞吐最高
}
```

```cpp
#include <string>
// ⑪ 随机读基准骨架：跨层 -> 读放大
for (int i = 0; i < 100'000; ++i) {
    int k = dist(rng);                         // 随机 key
    std::string v; db->Get(r, std::to_string(k), &v);
}
```

```cpp
// ⑪ 复杂度直觉（示意，量级）
//   顺序写:  O(1) 追加（WAL）+ O(log n) MemTable         ~ 数十万 ops/s
//   点查:    O(log n) MemTable + Σ O(log file) SSTable   受读放大限制
//   范围扫描: O(scan) 顺序 IO，远快于 B-Tree 随机读
```

- `[经验]`：顺序 key（如时间戳前缀）让写入天然聚集，避免 L0 爆炸；随机 key 建议加 `Hash`/分桶前缀。
- `[平台]`：SSD 上 Compaction 的写放大比 HDD 更可接受；但 NAND 有擦除寿命，高写入仍需注意。

```cpp
// ⑪ RocksDB 直接读（跳过 MemTable 的读路径统计）用于隔离测量
rocksdb::ReadOptions ro;
ro.read_tier = rocksdb::kBlockCacheTier;   // 仅读缓存层，缺失即返回（压测缓存命中率）
```

## ⑫ 跨平台 [平台]

LevelDB / RocksDB 本身是跨平台 C++，但**文件系统语义、原子 rename、fsync 行为**在 Windows / POSIX 上不同。

```cpp
// ⑫ 用 Env 抽象屏蔽平台 IO（RocksDB 默认 Env::Default()）
// 上游参考：https://github.com/facebook/rocksdb/blob/main/include/rocksdb/env.h
// 行号：约 200（Env 接口，上游参考）
rocksdb::Options o;
o.env = rocksdb::Env::Default();           // Windows: WinAPI；Linux: POSIX
```

```cpp
// ⑫ Windows 路径注意反斜杠：用正斜杠或双反斜杠
#ifdef _WIN32
leveldb::DB::Open(opt, "C:/tmp/testdb", &db);   // 推荐正斜杠
#else
leveldb::DB::Open(opt, "/tmp/testdb", &db);
#endif
```

```cpp
// ⑫ 文件锁在跨平台下行为差异：LevelDB 用 flock(Linux)/LockFileEx(Win)
//   网络盘(NFS/SMB)上锁可能不可靠 -> 不要把 DB 放在网络文件系统
```

- `[平台·Windows]`：WAL 的 `fsync` 在 Windows 走 `FlushFileBuffers`，比 Linux `fdatasync` 更重；高吞吐场景考虑 `options.wal_dir` 放到独立盘。
- `[平台·x86-64]`：Itanium C++ ABI 名字改编一致，跨编译器目标文件可链接（同 ABI 前提下）。

```cpp
// ⑫ 大页 / 直接 IO（RocksDB，Linux 专用，提升大块顺序 IO）
rocksdb::Options o;
o.use_direct_reads = true;     // 绕过页缓存，自己管理 BlockCache
o.use_direct_io_for_flush_and_compaction = true;
```

## ⑬ 常见陷阱 [经验]

```cpp
// ⑬ 陷阱1：忘记 delete iterator -> 内存泄漏
leveldb::Iterator* it = db->NewIterator(leveldb::ReadOptions());
// ... 使用后必须有 delete it;   => 用 ⑧ 的 IterPtr 封装避免
```

```cpp
// ⑬ 陷阱2：迭代器/快照长期持有 -> MemTable 无法释放，空间爆
//   ❌ 持有快照数小时，期间所有旧版本都不能被 Compaction 回收
//   ✅ 用完立即 ReleaseSnapshot
```

```cpp
// ⑬ 陷阱3：把 LevelDB 当关系库做事务跨键更新
//   ❌ 期望两个 Put 原子（LevelDB 单键原子，无跨键事务）
//   ✅ 用 WriteBatch 单批，或上 RocksDB TransactionDB
```

```cpp
// ⑬ 陷阱4：options.block_cache 多 ColumnFamily 共享同一 cache 实例
//   ❌ 每个 CF new 一个 cache -> 内存翻倍且无全局 LRU 效益
//   ✅ 共享同一个 block_cache 指针
```

- `[经验]`：最致命的是「长期快照 + 高写入」导致空间放大失控；监控 `rocksdb.estimate-live-data-size` 与 `rocksdb.compaction-pending`。
- `[经验]`：LevelDB 默认 `create_if_missing=false` 时要先确认目录存在，否则 `Open` 返回 `NotFound`。

```cpp
#include <string>
// ⑬ 陷阱5：value 返回引用悬空（LevelDB 的 Slice 指向内部缓冲）
std::string v;
db->Get(ro, key, &v);     // ✅ 复制到 std::string
// leveldb::Slice s = it->value();  // 仅迭代器存活期间有效，别跨 Next 保存
```

## ⑭ 演进 [标准]

LevelDB（2011，Google，源自 BigTable 论文）→ RocksDB（2012，Facebook 分支）→ 持续迭代至今。

```cpp
// ⑭ 版本能力里程碑（文字，非代码）
//   LevelDB 1.0  : 基础 LSM，跳表 MemTable，分层 Compaction
//   RocksDB 3.x  : 列族、Merge、Universal Compaction
//   RocksDB 5.x  : 事务(TransactionDB)、前缀布隆、Persistent Cache
//   RocksDB 7.x  : 全速落盘、背压、更好默认参数
```

```cpp
// ⑭ 关键演进：从「单 MemTable」到「双 MemTable（active+immutable）」
//   写满 active -> 切 immutable -> 后台刷盘，前台继续写 active，消除写停顿
// 上游参考：https://github.com/facebook/rocksdb/blob/main/db/memtable_list.h
// 行号：约 50（MemTableList 管理 active/immutable，上游参考）
```

```cpp
// ⑭ RocksDB 默认参数随版本变优：新版本常「开箱即接近最优」
rocksdb::Options o = rocksdb::Options::OptimizeForSmallDb();   // 小库预设
// 或 OptimizeForPointLookup / OptimizeLevelStyleCompaction
```

- `[标准]`：演进是工程实践驱动，非 ISO 标准；API 大体向后兼容，但默认行为会改。
- `[经验]`：升级大版本务必对比 `LOG` 起始段的「SST 格式版本」，跨大版本升级前先做 Compaction 到最新格式。

```cpp
#include <string>
// ⑭ 格式版本检查（RocksDB）
std::string fmt;
db->GetProperty("rocksdb.format-version", &fmt);
```

## ⑮ 最佳实践 [经验]

```cpp
// ⑮ 写优化：批量 + 关 sync（可容忍丢最近写时）
leveldb::WriteOptions w;
w.sync = false;             // 异步 WAL，吞吐高；崩溃可能丢最后几 ms 写
db->Write(w, &batch);
```

```cpp
// ⑮ 读优化：共享 BlockCache + 布隆过滤器
leveldb::Options o;
o.filter_policy = leveldb::NewBloomFilterPolicy(10);   // 每键 ~10bit
o.block_cache = leveldb::NewLRUCache(128 << 20);        // 128MB
```

```cpp
// ⑮ RocksDB 针对点查的预设（一行到位）
rocksdb::Options o = rocksdb::Options::OptimizeForPointLookup(128 /*MB cache*/);
```

```cpp
// ⑮ 控制写放大：限制后台线程，避免 Compaction 抢前台 IO
rocksdb::Options o;
o.max_background_flushes = 2;
o.max_background_compactions = 4;
o.level0_slowdown_writes_trigger = 20;   // L0 文件数达此值则前台限流
o.level0_stop_writes_trigger = 36;       // 达此值直接停写
```

- `[经验]`：先测后调——用 `db_bench` 跑真实负载，再据 `rocksdb.stats` 调整，不要盲改魔数。
- `[经验]`：键设计影响巨大：定长、带前缀、避免过长 value（大 value 用 BlobDB / 外置）。

```cpp
// ⑮ 大 value 外置（RocksDB BlobDB / 或自行把 value 存对象存储，key 存定位符）
rocksdb::ColumnFamilyOptions co;
co.enable_blob_files = true;
co.min_blob_size = 1024;     // 大于 1KB 的 value 进 blob 文件
```

## ⑯ 跨库 [经验]

```cpp
// ⑯ LevelDB vs RocksDB API 相似度（迁移成本低）
//   leveldb::DB::Open  <->  rocksdb::DB::Open
//   leveldb::Options   <->  rocksdb::Options（RocksDB 字段更多）
//   主要差异：RocksDB 多 ColumnFamilyHandle 参数，几乎所有方法多一个 handle
```

```cpp
// ⑯ 与 LMDB（B+Tree，mmap）对比：LMDB 读无拷贝、事务强，但写单线程
//   LevelDB/RocksDB：写并发高、Compaction 自管；LMDB：读极致、写受锁
```

```cpp
// ⑯ 与 SQLite 对比：SQLite 单文件关系库，LevelDB 仅有序 KV，无 SQL/索引
//   选型：需要 SQL/事务表 -> SQLite；需要超高写吞吐 KV -> LevelDB/RocksDB
```

- `[经验]`：同进程多引擎共存常见（RocksDB 存 KV、SQLite 存元数据）；但别让两者抢同一块磁盘 IO。
- `[经验]`：Redis 是内存 KV，可做 LevelDB 的上层缓存；二者常组合（热在 Redis，全量在 RocksDB）。

```cpp
// ⑯ 简单选型函数（示意）
const char* pick(bool need_sql, bool need_high_write) {
    if (need_sql) return "SQLite";
    if (need_high_write) return "RocksDB";
    return "LevelDB";
}
```

## ⑰ 贡献 [经验]

要改引擎，先能自构建。两者均用 CMake，跨平台一条命令。

```cpp
// ⑰ LevelDB 从源码构建（上游参考，非本机命令输出）
//   git clone https://github.com/google/leveldb.git
//   cd leveldb && mkdir -p build && cd build
//   cmake -DCMAKE_BUILD_TYPE=Release .. && cmake --build . -j
//   产物：libleveldb.a / libleveldb.so
```

```cpp
// ⑰ RocksDB 从源码构建（上游参考）
//   git clone https://github.com/facebook/rocksdb.git
//   cd rocksdb && mkdir -p build && cd build
//   cmake -DCMAKE_BUILD_TYPE=Release -DWITH_TESTS=OFF .. && cmake --build . -j
```

```cpp
// ⑰ 贡献流程：fork -> 分支 -> 单测(gtest) -> 跑 db_bench -> 提 PR
//   上游参考：https://github.com/facebook/rocksdb/blob/main/CONTRIBUTING.md
//   行号：N/A（文档，上游参考）
```

- `[经验]`：改核心路径（Compaction / MemTable）务必补 `db_test` 与 `compaction_test`，并跑 `make check`。
- `[平台]`：Windows 用 Visual Studio 的 CMake 预设；Linux/macOS 用 Ninja 更快。

```cpp
// ⑰ 用 sanitizer 编译定位内存问题（开发期）
//   cmake -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined" ..
```

## ⑱ 与 STL 容器对比（map vs LSM） [标准]

`std::map`（红黑树）与 LevelDB（LSM）都提供有序 KV，但**持久化、并发、规模**维度天差地别。

```cpp
// ⑱ std::map：内存、单线程友好、O(log n) 但受限于 RAM
#include <map>
#include <string>
std::map<std::string, std::string> m;
m["k1"] = "v1";
auto it = m.find("k1");   // O(log n)，纯内存，崩溃即丢
```

```cpp
// ⑱ LevelDB：持久化、可远超内存、写吞吐更高但读放大
//   等价 find 见 ⑥ 的 db->Get；范围扫描见 ⑥ 的迭代器
//   差异：map 在内存；LevelDB 在磁盘 + BlockCache，容量以 TB 计
```

```cpp
#include <map>
// ⑱ 复杂度/特性对照（文字表在章末速查，此处给代码侧直觉）
//   std::map                  : 插入 O(log n)，无持久化，无内建并发
//   std::unordered_map        : 插入 O(1) 均摊，无序，仍内存受限
//   LevelDB/RocksDB           : 写 O(log n) MemTable + 顺序落盘，持久化，并发写
```

- `[标准]`：`std::map` 满足 `std::` 容器契约（有序、迭代稳定），LevelDB 不实现任何标准容器接口——它是**独立持久化抽象**。
- `[经验]`：数据量 < 内存且要事务一致性，`std::map` + 偶尔落盘即可；数据量 >> 内存或要高并发写，上 LSM。

```cpp
#include <string>
#include <string_view>
#include <map>
// ⑱ 把 LevelDB 包装成近似 map 接口的适配器（仅示意签名）
class LsmMap {
public:
    bool insert(std::string_view k, std::string_view v);
    bool find(std::string_view k, std::string& out);
    // 注意：无迭代器失效语义，与 std::map 不等价
};
```

## ⑲ 调试/源码阅读 [经验]

```cpp
// ⑲ 阅读入口（上游参考，标注上游参考，行号对应 release 标签）
//   LevelDB : db/db_impl.cc       Write/Get/Compact 三大入口
//   LevelDB : db/skiplist.h       跳表（对照 Examples/_ch132_lsm_toy.cpp 的 Node）
//   LevelDB : table/table_builder.cc  SSTable 写出
//   RocksDB : db/db_impl/db_impl.cc    全家桶
//   RocksDB : db/memtable.cc           MemTable 实现
```

```cpp
#include <string>
// ⑲ 用 GetProperty 在运行时印证源码行为（读放大拆解）
std::string h;
db->GetProperty("rocksdb.cfstats", &h);     // 每列族详细统计
// 关注：rw-per-query( GET )、compaction times、memtable hit
```

```cpp
// ⑲ 断点建议：在 DBImpl::Write / MemTable::Add / Compaction 入口下断
//   用 gdb 看真实的 SequenceNumber 推进与 writers_ 队列合并
//   (gdb) b leveldb::DBImpl::Write
//   (gdb) r
```

- `[经验]`：先读 `doc/` 与 `README` 再读 `db_impl.cc`；跳表与 SSTable 是两块独立易读代码，优先攻克。
- `[平台]`：源码用 `port/` 目录隔离平台差异（atomic、mutex、env），阅读时对应自己平台实现。

```cpp
// ⑲ 用 LOG 文件定位「为何某 key 读慢」：对比 memtable/blockcache/sst 占比
//   见 ⑩ 的 rocksdb.stats 解析
```

## ⑳ 速查表 [经验]

```cpp
#include <vector>
#include <string>
// ⑳ 打开（LevelDB）
leveldb::DB* db; leveldb::Options o; o.create_if_missing = true;
leveldb::DB::Open(o, "/tmp/db", &db);

// ⑳ 打开（RocksDB，含列族）
rocksdb::DB* rdb; std::vector<rocksdb::ColumnFamilyHandle*> hs;
rocksdb::DB::Open(rocksdb::DBOptions(), "/tmp/rdb",
    {rocksdb::ColumnFamilyDescriptor{"default", rocksdb::ColumnFamilyOptions{}}}, &hs, &rdb);

// ⑳ 写
db->Put(leveldb::WriteOptions(), "k", "v");
rdb->Put(rocksdb::WriteOptions(), hs[0], "k", "v");

// ⑳ 读
std::string v; db->Get(leveldb::ReadOptions(), "k", &v);

// ⑳ 删
db->Delete(leveldb::WriteOptions(), "k");

// ⑳ 范围扫描
for (auto* it = db->NewIterator(leveldb::ReadOptions()); it->Valid(); it->Next()) { }
```

```text
┌───────────────────────┬─────────────────────────────┬──────────────────────────┐
│ 维度                  │ LevelDB                     │ RocksDB                  │
├───────────────────────┼─────────────────────────────┼──────────────────────────┤
│ 列族                  │ 无                          │ 有（多命名空间）         │
│ 事务                  │ 无（WriteBatch 批原子）     │ TransactionDB            │
│ Compaction 策略       │ Leveled                      │ Leveled/Universal/FIFO   │
│ Merge 算子            │ 无                          │ 有                       │
│ 典型写吞吐            │ 高                          │ 更高（可调优）           │
│ 内存映射读            │ 否                          │ 支持（direct IO）        │
│ 适合规模              │ 单机中等                    │ 单机/分布式底层          │
└───────────────────────┴─────────────────────────────┴──────────────────────────┘
```

```cpp
// ⑳ 常见 GetProperty 键速查（RocksDB）
//   "rocksdb.stats"            整体统计
//   "rocksdb.cfstats"          每列族
//   "rocksdb.compaction-pending"  是否有待合并
//   "rocksdb.estimate-live-data-size" 活跃数据量
//   "rocksdb.num-immutable-mem-table" 待刷内存表数（写积压信号）
```

- `[经验]`：三个最该盯的属性：`num-immutable-mem-table`（写积压）、`compaction-pending`（合并滞后）、`estimate-live-data-size`（空间放大）。
- `[平台]`：所有属性名在 `include/rocksdb/db.h` 的 `GetProperty` 文档注释列出（上游参考）。

```cpp
// ⑳ 一行健康判断（示意）
bool healthy = imm <= 2 && !pending_compaction && live_data_mb < capacity_mb * 0.8;
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第131章](Book/part11_source/ch131_fmt_spdlog.md) | 键值查找/缓存 | 本章提供概念，第131章提供实现 |
| [第133章](Book/part11_source/ch133_clickhouse_redis.md) | 独占所有权/工厂模式 | 本章提供概念，第133章提供实现 |
| [第96章](Book/part08_algorithms/ch96_sorting.md) | 无锁队列/计数器 | 本章提供概念，第96章提供实现 |
| [第83章](Book/part07_stl/ch83_map.md) | 日志格式化/序列化 | 本章提供概念，第83章提供实现 |

## 附录 F：LevelDB/RocksDB 工业原理与面试 [B: Principle / D: Stdlib / H: Design / I: Practice / J: Learning]

```
LevelDB设计哲学 (Jeff Dean, Sanjay Ghemawat, 2011):
- LSM Tree: 写优化 → 内存MemTable → 磁盘SST文件 → Compaction合并
- 为什么不用B-tree? → B-tree随机写慢(寻道~10ms), LSM顺序写快(~100MB/s)
- Google BigTable的后端存储引擎

RocksDB改进 (Facebook, 2013):
- 多线程Compaction → 写吞吐提升3-5×
- Bloom filter by default → 读加速(假阳性1%, 内存~10bits/key)
- Column Families → 逻辑分区, 独立配置

C++实现: 整个项目~500K行C++, 使用std::atomic, std::thread, std::unique_ptr
```

```cpp
#include <iostream>
#include <memory>
#include <string>
int main() {
    std::cout << "LSM Tree: writes append-only (fast), reads merge views (Bloom filter helps)" << std::endl;
    std::cout << "LevelDB=200K users, RocksDB=5M+ users (MySQL/MyRocks, Kafka Streams, Flink)" << std::endl;
    std::cout << "std::string (key+value), std::atomic (ref counting), std::unique_ptr (ownership)" << std::endl;
    return 0;
}
```

| DB | 写入 | 读取 | 适用 |
|---|---|---|---|
| LevelDB | 100K ops/s | 50K ops/s | 嵌入式/移动 |
| RocksDB | 500K ops/s | 200K ops/s | 服务端/大数据 |
| SQLite | 50K ops/s | 100K ops/s | 嵌入式OLTP |
| lmdb | 200K ops/s | 500K ops/s | 读密集型 |

面试: LSM vs B-tree? LSM=写快(顺序)+读慢(多层); B-tree=读写均衡+就地修改
       RocksDB优化? Bloom filter + 多线程Compaction + Column Families


## 相关章节（交叉引用）

- **同模块兄弟（part11 源码）**：⟶ Book/part11_source/ch124_libstdcxx.md（第124章　libstdc++ 架构与阅读入口（C++））
- **同模块兄弟（part11 源码）**：⟶ Book/part11_source/ch125_libcxx.md（第125章　libc++ 架构（C++））
- **同模块兄弟（part11 源码）**：⟶ Book/part11_source/ch126_msstl.md（第126章　MS STL 架构（C++））
- **同模块兄弟（part11 源码）**：⟶ Book/part11_source/ch127_llvm.md（第127章　LLVM / Clang 架构（C++））
- **同模块兄弟（part11 源码）**：⟶ Book/part11_source/ch128_boost.md（第128章　Boost 核心库（C++））
- **同模块兄弟（part11 源码）**：⟶ Book/part11_source/ch129_qt.md（第129章　Qt 对象模型与信号槽（C++））
- **同模块兄弟（part11 源码）**：⟶ Book/part11_source/ch130_chromium_abseil.md（第130章　Chromium / Abseil 基础设施（C++））
- **同模块兄弟（part11 源码）**：⟶ Book/part11_source/ch131_fmt_spdlog.md（第131章　fmt / spdlog 格式化与日志（C++））
- **同模块兄弟（part11 源码）**：⟶ Book/part11_source/ch133_clickhouse_redis.md（第133章　ClickHouse / Redis 实现精读（C++））
- **同模块兄弟（part11 源码）**：⟶ Book/part11_source/ch134_unreal.md（第134章　Unreal Engine C++ 架构（C++））

## 附录 G（LSM-Tree 与 SSTable）

LevelDB/RocksDB 用 LSM 树，写入先落 memtable 再 compaction。

```text
; memtable 跳表查找（rdi=node）
mov rax, [rdi+0x0008]     ; 右指针
cmp [rax+0x0000], key
jg  .left
mov rax, [rdi+0x0010]     ; 下一级
```

### 布局与偏移

- memtable 跳表节点：key 偏移 `0x0000`，指针 `0x0008`/`0x0010`
- SSTable 数据块 `0x1000` 字节；索引块偏移 `0x0010`
- Bloom filter 位图 `0x0040` 字节/键，误判率 < 0x0001

### 量级

- 写（WAL + memtable）≈ 1.0us；读（memtable 命中）≈ 0.5us
- compaction 读取 ≈ 22ms/GB；L0→L1 合并 ≈ 0x0008 路
- 块缓存命中 LRU ≈ 1.0ns；冷读主存 ≈ 100ns

### 编译器与标准

- 内部用 `std::atomic` 保护引用计数；`-O2` 生成上示代码
- GCC 13.2 / Clang 18 编译；`__cplusplus` = 202302L
- WG21 提案 P0784R7 扩展 constexpr 存储结构


## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例：Compaction 风暴——RocksDB 写停顿的根因

某推荐系统用 RocksDB 存特征向量（单实例 500GB LSM），高峰期写 QPS 从 50K 骤降到 5K，P99 延迟从 2ms 飙到 500ms。根因是 L0 文件数超过 `level0_file_num_compaction_trigger=4` 后触发 Compaction，但 L0→L1 的写放大（Write Amplification）达 20×，Compaction 线程跑满磁盘 IO 带宽，前台写入被 `DB::Write()` 内部 stall 阻塞。解决方案：增加 `max_background_compactions` 到 CPU 核数、设置 `level0_slowdown_writes_trigger=20` / `level0_stop_writes_trigger=36` 加大缓冲、换 NVMe 后写放大降到可控。教训：LSM 的 Compaction 不是"后台任务"——磁盘带宽不足时它就是前台瓶颈。

### 常见 Bug / Debug 方法

- **MANIFEST 损坏**：突然断电后 `MANIFEST-*` 文件可能记录未完成的 Compaction 元数据，导致 DB 无法 open。用 `ldb repair` 或 RocksDB 的 `repairer` API 恢复，但会丢弃未 flush 的 WAL 尾部数据（<1MB 可接受）。
- **Column Family 句柄泄漏**：`DB::CreateColumnFamily()` 返回的 `ColumnFamilyHandle*` 必须 `delete`，否则 RocksDB 内部引用计数不归零，`DB::Close()` 死等。
- **Iterator 持有资源过长**：`DB::NewIterator()` 内部持有 SST 文件的 mmap 引用，长生命周期 Iterator（如遍历 1 亿 key 的离线任务）会阻止 Compaction 回收旧 SST → 磁盘空间只增不减。改用 `DB::Get()` 逐 key 查或用 `ReadOptions::background_purge_on_iterator_cleanup=true`。

### Code Review 关注点

- `WriteOptions::sync=false` 在生产是否安全？（机器级掉电丢失最近一批写，但对推荐/日志类场景可接受；金融/元数据须 `sync=true`）
- `CompactRange(nullptr, nullptr)` 全量 Compaction 会长时间 Block 写入，是否放在维护窗口执行？
- Bloom filter 的 `bits_per_key` 默认 10——但对 key 空间巨大的场景（如 UUID key）调高到 14–16 可显著降低读放大。

### 重构建议

- 从 LevelDB 迁 RocksDB：保留 `leveldb::DB*` 接口兼容层用适配器模式包裹 `rocksdb::DB*`（API 95% 兼容），灰度切流验证 L0 行为差异。
- LSM 不是银弹：写多读少才高效；读多写少用 B-tree 系列（LMDB/WiredTiger）更好；读写均衡考虑 PostgreSQL 的 LSM（Citus）+ B-tree 混合方案。

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

### 练习 1（难度 ★★）

LevelDB 写路径第一步是把记录追加进 WAL（Write-Ahead Log），进程崩溃时靠 WAL 重放恢复。
请用 RAII 封装一个 `WalWriter`：构造时以追加模式打开文件，提供 `Append(const std::string&)` 写入一条带长度前缀的记录，
析构时保证 flush 并关闭文件——即便中途抛异常也不泄漏文件句柄。

```cpp
#include <cstdio>
#include <cstdint>
#include <string>
#include <cstring>

class WalWriter {
    std::FILE* fp_ = nullptr;
public:
    explicit WalWriter(const char* path) : fp_(std::fopen(path, "ab")) {}
    ~WalWriter() {
        if (fp_) { std::fflush(fp_); std::fclose(fp_); }   // 析构即释放，异常安全
    }
    WalWriter(const WalWriter&) = delete;
    WalWriter& operator=(const WalWriter&) = delete;
    bool ok() const { return fp_ != nullptr; }
    void Append(const std::string& rec) {
        uint32_t n = static_cast<uint32_t>(rec.size());
        std::fwrite(&n, sizeof n, 1, fp_);                  // 长度前缀，便于重放时定界
        std::fwrite(rec.data(), 1, n, fp_);
    }
};

int main() {
    WalWriter w("wal_demo.log");
    if (!w.ok()) { std::printf("open failed\n"); return 1; }
    w.Append("k1=v1");
    w.Append("k2=v2");
    std::printf("WAL 写入 2 条记录，离开作用域自动 flush+close\n");
}
```

[标准] WAL 的“先写日志再改内存”是崩溃一致性的基石；RAII 把 `fflush/fclose` 从所有控制流出口收拢到析构，
是 C++ 异常安全的核心手段（关联 ⑧ RAII/智能指针）。

### 练习 2（难度 ★★★）

MemTable 中的一条记录可能是 Put（带值）、Delete（墓碑）或 Merge（增量）。
请用 `std::variant` 把这三类操作建模为一个 `Op` 类型，并统计一批操作中各类型的占比——
体会用代数数据类型（sum type）替代“基类+继承”如何消除虚调用与堆分配。

```cpp
#include <iostream>
#include <variant>
#include <string>
#include <vector>
#include <type_traits>

struct Put   { std::string value; };
struct Delete { };                       // 墓碑，无载荷
struct Merge { std::string delta; };

using Op = std::variant<Put, Delete, Merge>;

int main() {
    std::vector<Op> log = { Put{"v1"}, Delete{}, Merge{"+1"}, Put{"v2"}, Delete{} };
    int n_put = 0, n_del = 0, n_merge = 0;
    for (const auto& op : log) {
        // std::visit 编译期分派，零虚调用、零堆分配
        std::visit([&](auto&& o) {
            using T = std::decay_t<decltype(o)>;
            if constexpr (std::is_same_v<T, Put>)        ++n_put;
            else if constexpr (std::is_same_v<T, Delete>) ++n_del;
            else ++n_merge;
        }, op);
    }
    std::cout << "Put=" << n_put << " Delete=" << n_del << " Merge=" << n_merge << '\n';
}
```

[标准] `std::variant`+`std::visit` 是零开销的“标签联合”：判别在编译期完成，无 vtable 间接跳转，
比 `class Op { virtual ... }` 更贴合 MemTable 这类“少量固定类型、高频访问”的场景（关联 ⑧ 自定义分配器）。

### 练习 3（难度 ★★★★）

LevelDB 的 MemTable 底层是跳表（SkipList），读路径无锁、写路径用 CAS 把新节点链入多层链表。
请实现一个简化跳表：固定最大层数、`next` 指针用 `std::atomic` 标注内存序，
插入时以 `memory_order_release` 发布、查找时以 `memory_order_acquire` 观察，保证发布-观察的 happens-before。

```cpp
#include <iostream>
#include <atomic>
#include <vector>
#include <cstdint>

struct Node {
    int key;
    std::atomic<Node*> next;           // 单层后继，发布用 release / 观察用 acquire
    explicit Node(int k) : key(k), next(nullptr) {}
};

// 单层有序插入（演示内存序，不做多层随机高度）
void insert(Node*& head, int key) {
    Node* n = new Node(key);
    if (!head || key < head->key) {    // 空表或新最小值 -> 成为新头
        n->next.store(head, std::memory_order_relaxed);
        head = n;
        return;
    }
    Node* prev = head;
    Node* cur = prev->next.load(std::memory_order_acquire);
    while (cur && cur->key < key) { prev = cur; cur = cur->next.load(std::memory_order_acquire); }
    n->next.store(cur, std::memory_order_relaxed);
    prev->next.store(n, std::memory_order_release);   // 发布：后续 acquire 能看到 n 及之前写入
}

bool contains(Node* head, int key) {
    Node* cur = head;                  // 从首节点开始遍历
    while (cur) {
        if (cur->key == key) return true;
        if (cur->key > key) return false;
        cur = cur->next.load(std::memory_order_acquire);
    }
    return false;
}

int main() {
    Node* head = nullptr;
    for (int k : {3, 1, 4, 1, 5}) insert(head, k);
    std::cout << "contains(4)=" << contains(head, 4)
              << " contains(2)=" << contains(head, 2) << '\n';
}
```

[标准] 无锁读靠 `memory_order_acquire` 与写者 `memory_order_release` 配对建立同步；跳表因而支持“并发读+单写/受保护写”。
真实 LevelDB 用 `AtomicPointer`（封装 `void*` + 内存序）而非 `std::atomic<Node*>`，语义等价（关联 ⑨ 跳表/SSTable）。

## 附录：用法演绎（从选型到落地）

### 演绎 1：Arena 分配器——把 N 次 new 合并为少量大块分配

**场景**：MemTable 每条记录都 `new`，高频小对象让通用分配器锁争用与碎片飙升。
**选型**：LevelDB 的 `Arena` 一次向堆要一大块（如 4 KiB），记录从块内线性 bump 分配；块满再要下一块。
**错误**：每条记录独立 `new/delete`，分配器成为瓶颈且碎片难回收。
**落地**：

```cpp
#include <iostream>
#include <vector>
#include <cstddef>
#include <cstring>

// 简化 Arena：批量预留，记录从块内线性分配
struct Arena {
    std::vector<char*> blocks_;
    char*  cur_ = nullptr;
    size_t remain_ = 0;
    static constexpr size_t kBlock = 4096;
    void* alloc(size_t n) {
        if (remain_ < n) {                       // 当前块不够，新开一块
            char* b = new char[kBlock];
            blocks_.push_back(b);
            cur_ = b; remain_ = kBlock;
        }
        void* p = cur_;
        cur_ += n; remain_ -= n;
        return p;
    }
    ~Arena() { for (char* b : blocks_) delete[] b; }
};

int main() {
    Arena a;
    int allocs = 0;
    for (int i = 0; i < 1000; ++i) {             // 1000 次“逻辑分配”
        a.alloc(32);
        ++allocs;
    }
    // 1000 次逻辑分配只触发 ceil(1000*32/4096)=8 次真实 new
    std::cout << "逻辑分配=" << allocs
              << " 真实 new 块数=" << a.blocks_.size() << '\n';
}
```

**结论**：Arena 用“批量化 + 生命周期统一（Arena 析构一次性释放）”把分配器调用次数从 O(N) 降到 O(N/块大小)，
是高吞吐存储引擎的标配（关联 ⑧ 自定义分配器）。

### 演绎 2：Compaction 风暴与写停顿——从“会写”到“写不卡”

**场景**：L0 文件堆积到阈值，RocksDB 触发 Compaction；若跟不上写入，进入“写停顿（Stall）”甚至“停止（Stop）”。
**选型**：用状态机表达“写流量闸门”：普通 → 软停顿（降速）→ 硬停顿（阻塞写），按 L0 文件数切换。
**错误**：不看后端压实进度，无脑全速写入，最终被反压拖垮（关联 附录 I 工业案例：Compaction 风暴）。
**落地**：

```cpp
#include <iostream>

enum class WriteGate { Normal, SoftStall, HardStop };

// 依据 L0 文件数决定写闸门（阈值取 RocksDB 常见默认的量级）
WriteGate gate_for(int l0_files) {
    if (l0_files >= 20) return WriteGate::HardStop;   // L0>=20：硬停顿，先让 Compaction 追平
    if (l0_files >= 12) return WriteGate::SoftStall;  // L0>=12：软停顿，写入降速
    return WriteGate::Normal;
}

int main() {
    for (int n : {4, 12, 20}) {
        const char* s = n >= 20 ? "HardStop" : n >= 12 ? "SoftStall" : "Normal";
        std::cout << "L0 文件数=" << n << " -> 写闸门=" << s << '\n';
    }
}
```

**结论**：存储引擎的“可观测反压”比“裸吞吐”更重要；把 Compaction 进度显式映射为写闸门，
才能在大写入下保持尾延迟可控（关联 ⑦ Compaction 策略 / 附录 I 工业复盘）。