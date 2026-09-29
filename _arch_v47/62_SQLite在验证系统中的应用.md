# 方向 62：SQLite 在验证系统中的应用

## 核心结论

1. **对阙疑的 append-only 判决账本，正确的配置是 `journal_mode=WAL` + `synchronous=FULL`，而且这个组合恰好有一个反直觉的安全性质：在 WAL 模式下，COMMIT 时的 fsync 失败只会损失持久性，不会损坏数据库**。SQLite 官方 howtocorrupt 页逐字：*"SQLite in WAL mode is far more forgiving of out-of-order writes than in the default rollback journal modes. In WAL mode, the only time that a failed sync operation can cause database corruption is during a checkpoint operation. A sync failure during a COMMIT might result in loss of durability but not in a corrupt database file. Hence, one line of defense against database corruption due to failed sync operations is to use SQLite in WAL mode and to checkpoint as infrequently as possible."* **对"账本"这种数据结构，"丢一条"和"整库损坏"是两个严重程度差几个量级的事故；WAL 把最坏情况从后者降级为前者。这一条本身就足以构成选 WAL 的理由，与性能无关。** 同时官方明确要求：*"For maximum reliability and for robustness against database corruption, SQLite should always be run with its default synchronous setting of FULL."*——**不要为了快而降到 NORMAL。**

2. **有一个必须立刻处理的硬约束：WAL-reset bug 存在于 SQLite 3.7.0 到 3.51.2 的所有版本，修复版本是 3.51.3（2026-03-13）**。官方逐字：*"When there are two or more database connections in separate threads or processes, both open on the same WAL-mode database, and if both connections try to write or run checkpoint at the same time, then there is a race condition that might corrupt the database file. This is the WAL-reset bug. It existed in all versions of SQLite from 3.7.0 through 3.51.2."* **触发条件与阙疑的架构高度相关**：阙疑有"内核 `gate_engine.py`"和"独立对账器"两个组件，如果它们**同时打开同一个 SQLite 文件并写入**（例如内核追加判决、对账器写审计记录），就正好落在 bug 的触发条件上。**行动要求：`python -c "import sqlite3; print(sqlite3.sqlite_version)"` 检查版本，若 < 3.51.3 则要么升级，要么严格保证"任何时刻只有一个写进程"，要么把对账器改成只读连接。** 这是本方向唯一一条"不做就可能丢数据"的发现。

3. **SQLite 的容量上限与阙疑的规模差了 8 个数量级，性能上限也不是约束；真正的约束是"单写者"这一条，而它对单人项目完全无害**。容量逐字：最大数据库 **4294967294 页**，在最大页大小 **65536 字节**下约 **281 TB（2.8×10¹⁴ 字节）**；默认页大小 **4096 字节**（对应约 **17.5 TB**）。阙疑的账本按每条判决 4 KB 估算，452 条约 **1.8 MB**——**占 17.5 TB 的 1.0×10⁻⁸**。写并发方面，SQLite 同一时刻只允许一个写事务（WAL 下读不阻塞写、写不阻塞读，但**写者之间仍然串行**）。**阙疑是单人、离线、批量追加判决的场景，写并发需求为零。** 所以"SQLite 只能单写者"这条被广泛引用的缺点，在阙疑这里根本不构成缺点。

---

## 精确数字与案例

### 一、WAL 的精确语义（官方逐字）

来源：sqlite.org/wal.html。

**引入时间**：*"Beginning with version 3.7.0 (2010-07-21), a new 'Write-Ahead Log' option (hereafter referred to as 'WAL') is available."*

**优点（逐字四条）**：
1. *"WAL is significantly faster in most scenarios."*
2. *"WAL provides more concurrency as readers do not block writers and a writer does not block readers. Reading and writing can proceed concurrently."*
3. *"Disk I/O operations tends to be more sequential using WAL."*
4. *"WAL uses many fewer fsync() operations and is thus less vulnerable to problems on systems where the fsync() system call is broken."*

**缺点（逐字八条，我只列与阙疑相关的）**：
- *"All processes using a database must be on the same host computer; WAL does not work over a network filesystem."* —— **阙疑是单机，无影响。**
- *"It is not possible to change the page_size after entering WAL mode"* —— 若阙疑要改页大小，必须先在 rollback journal 模式下改。
- *"WAL might be very slightly slower (perhaps 1% or 2% slower) than the traditional rollback-journal approach in applications that do mostly reads and seldom write."* —— **注意这条**：阙疑的读远多于写（判决写入是低频的，复算与查询是高频的）。但"1%–2%"这个量级在阙疑的绝对时间尺度（毫秒）上是不可测的。
- *"There is an additional quasi-persistent '-wal' file and '-shm' shared memory file associated with each database"* —— **阙疑若把账本当作"可分发文件"，必须同时打包 `.db`、`.db-wal`、`.db-shm` 三个文件，或者在分发前做一次 checkpoint 并关闭连接。这是一个真实的工程陷阱**（见行动 2）。
- *"WAL works best with smaller transactions. WAL does not work well for very large transactions. For transactions larger than about 100 megabytes, traditional rollback journal modes will likely be faster. For transactions in excess of a gigabyte, WAL mode may fail with an I/O or disk-full error."* —— **阙疑的单条判决远小于 100 MB，无影响。**（另注：*"Beginning with version 3.11.0 (2016-02-15), WAL mode works as efficiently with large transactions as does rollback mode."*）

**激活方式（逐字）**：默认是 `journal_mode=DELETE`，转换用 `PRAGMA journal_mode=WAL;`。转换成功时 pragma 返回字符串 `"wal"`；失败（例如 VFS 不支持共享内存）则返回原来的模式。**并且**：*"Unlike the other journaling modes, PRAGMA journal_mode=WAL is persistent. If a process sets WAL mode, then closes and reopens the database, the database will come back in WAL mode."*、*"The WAL journal mode will be set on all connections to the same database file if it is set on any one connection."* —— **这意味着 WAL 是一次性设置，不需要每次连接都设；但也意味着它会被"意外地"带到其他地方。**

**Checkpoint 机制（逐字要点）**：
- 默认自动 checkpoint 阈值：**1000 页**（约 4 MB）；*"By default, SQLite will automatically checkpoint whenever a COMMIT occurs that causes the WAL file to be 1000 pages or more in size, or when the last database connection on a database file closes."*
- 三种 checkpoint 类型：**PASSIVE**（默认，不干扰其他连接，可能跑不完）、**FULL**、**RESTART**（后两者只能通过 `sqlite3_wal_checkpoint_v2()` 发起）。
- *"The checkpoint does not normally truncate the WAL file (unless the journal_size_limit pragma is set). Instead, it merely causes SQLite to start overwriting the WAL file from the beginning."* —— **这是一个常见误解：checkpoint 不等于把 WAL 文件变小。**
- *"a long-running read transaction can prevent a checkpointer from making progress."* —— **阙疑若有一个长时间运行的只读复算事务，会阻塞 checkpoint 推进，导致 WAL 文件持续增长。** 这是一个值得在代码里防范的模式（不要在复算期间持有长事务）。
- *"the wal-index rarely exceeds 32 KiB in size and is never synced"* —— **`.shm` 文件通常不超过 32 KiB，且从不同步到磁盘**（所以它是纯缓存，丢了可以重建）。

**WAL 模式下仍会返回 SQLITE_BUSY 的三种情况（逐字）**：
1. 另一连接以 exclusive locking mode 打开了数据库；
2. 最后一个连接正在关闭并清理 WAL 与共享内存文件时；
3. 最后一个连接崩溃后，第一个新连接正在做恢复，此时第三个连接会被拒绝。

**只读访问 WAL 数据库**：*"Older versions of SQLite could not read a WAL-mode database that was read-only... This constraint was relaxed beginning with SQLite version 3.22.0 (2018-01-22)."* 满足以下任一条件即可只读打开：(1) `-shm` 与 `-wal` 文件已存在且可读；(2) 数据库所在目录可写（以便创建这两个文件）；(3) 用 `immutable` 查询参数打开。**官方还建议**：*"it is good practice to convert the database to PRAGMA journal_mode=DELETE prior to burning an SQLite database image onto read-only media."* —— **如果阙疑要发布"只读的账本快照"（例如作为论文附录或 artifact 分发），应当在发布前转回 DELETE 模式。**

### 二、原子提交的精确步骤与 fsync 次数

来源：sqlite.org/atomiccommit.html。这是理解"账本为什么安全"的基础。

**单文件提交的完整步骤（逐字顺序）**：

| 步骤 | 动作 | 关键引文 |
|---|---|---|
| 3.2 | 获取共享锁（读锁） | *"the shared lock is on the operating system disk cache, not on the disk itself... the lock will instantly vanish if the operating system crashes or if there is a power loss."* |
| 3.4 | 获取 reserved 锁 | *"there can only be a single reserved lock on the database file."* |
| 3.5 | 创建回滚日志，写入**将被修改页的原始内容** | *"SQLite first creates a separate rollback journal file and writes into the rollback journal the original content of the database pages that are to be altered."* |
| 3.6 | 在用户空间修改数据库页 | 每个连接有自己的私有副本 |
| **3.7** | **刷新回滚日志到非易失存储（两次 fsync）** | *"On most platforms two separate flush (or fsync()) operations are required. The first flush writes out the base rollback journal content. Then the header of the rollback journal is modified to show the number of pages in the rollback journal. Then the header is flushed to disk."* |
| 3.8 | 获取 pending → exclusive 锁 | pending 锁允许已有共享锁的进程继续读，但阻止新的共享锁建立 |
| 3.9 | 将变更写入数据库文件 | — |
| **3.10** | **刷新数据库变更到非易失存储（第三次 fsync）** | *"Another flush must occur to make sure that all the database changes are written into nonvolatile storage."* |
| **3.11** | **删除回滚日志 —— 这就是提交的时刻** | *"After the database changes are all safely on the mass storage device, the rollback journal file is deleted. This is the instant where the transaction commits."* |
| 3.12 | 释放排他锁 | — |

**fsync 次数**：FULL 同步下**三次**（回滚日志内容、回滚日志头、数据库文件）；降到 NORMAL 时**只刷一次**（*"if the synchronous setting is lowered to 'normal', SQLite only flushes the rollback journal once, after the page count has been written."*）。

**性能归属（逐字）**：*"because of the inherent slowness of writing to disk or flash memory, this step [3.10] together with the rollback journal file flush in section 3.7 above takes up most of the time required to complete a transaction commit in SQLite."* 以及 *"Profiling indicates that for most systems and in most circumstances SQLite spends most of its time doing disk I/O."* —— **结论：阙疑写一条判决的延迟几乎完全由 fsync 决定，与数据库大小、记录条数无关。这是"452 条还是 452 万条，单条写入延迟都一样"的严格理由。**

**热日志（hot journal）的五条件与两道防线（这是恢复正确性的核心）**：

热日志需同时满足：回滚日志存在、非空、主库上无 reserved 锁、头部格式良好（特别是未被清零）、不包含 super-journal 名字（或该 super-journal 存在）。

两道防御垃圾数据的机制：
1. **头部记录页数（初始为 0）**：*"This number is initially zero. So during an attempt to rollback an incomplete (and possibly corrupt) rollback journal, the process doing the rollback will see that the journal contains zero pages and will thus make no changes to the database."*
2. **每页 32 位校验和**：*"SQLite also uses a 32-bit checksum on every page of data in the rollback journal... If an incorrect checksum is seen, the rollback is abandoned."* 并且明确：*"the checksums in the rollback journal are not necessary if the synchronous setting is FULL. We only depend on the checksums when synchronous is lowered to NORMAL."* —— **这解释了为什么降到 NORMAL 会引入新风险：此时正确性依赖 32 位校验和（碰撞概率 2⁻³²），而 FULL 下不依赖。**

**SQLite 对文件系统的假设（逐字，这一节对"账本能不能放在各种存储介质上"至关重要）**：
- *"SQLite has traditionally assumed that a sector write is not atomic. However, SQLite does always assume that a sector write is linear."*
- *"SQLite assumes that the operating system will buffer writes and that a write request will return before data has actually been stored... SQLite further assumes that write operations will be reordered by the operating system."*
- *"SQLite assumes that the flush or fsync will not return until all pending write operations for the file that is being flushed have completed."*
- *"SQLite assumes that a file deletion is atomic from the point of view of a user process."*
- *"SQLite assumes that the data it reads is exactly the same data that it previously wrote."*、*"SQLite does not add any redundancy to the database file for the purpose of detecting corruption or I/O errors."* —— **这一条极为重要：SQLite 不做端到端校验（见方向 66），所以阙疑必须在应用层自己做哈希链校验。**
- **powersafe overwrite**：*"By default, SQLite assumes that an operating system call to write a range of bytes will not damage or alter any bytes outside of that range even if a power loss or OS crash occurs during that write."*（该假设自 **3.7.9，2011-11-01** 起成立）

**版本与扇区大小**：*"Prior to SQLite version 3.3.14, a sector size of 512 bytes was assumed in all cases."*；*"there has recently been a push to increase the sector size of disks to 4096 bytes."*

### 三、损坏的完整分类，以及哪几类对阙疑是真实风险

来源：sqlite.org/howtocorrupt.html。该页开头就给出强度声明，逐字：

> *"An SQLite database is highly resistant to corruption. If an application crash, or an operating-system crash, or even a power failure occurs in the middle of a transaction, the partially written transaction should be automatically rolled back the next time the database file is accessed. The recovery process is fully automatic and does not require any action on the part of the user or the application."*

> *"Though SQLite is resistant to database corruption, it is not immune."*

> *"SQLite is very carefully tested... Among the many tests that are carried out for every SQLite version are tests that simulate power failures, I/O errors, and out-of-memory (OOM) errors to verify that no database corruption occurs during any of these events. SQLite is also field-proven with approximately **two billion active deployments** with no serious problems."*

**官方列出的八类原因**：① 流氓线程/进程覆写文件；② 文件锁问题；③ 未执行 sync；④ 磁盘与闪存故障；⑤ 内存损坏；⑥ 其他操作系统问题；⑦ SQLite 配置错误；⑧ SQLite 自身缺陷。

**对阙疑逐类判定（这是本节的核心）**：

| 类别 | 官方要点（逐字摘要） | 阙疑风险 |
|---|---|---|
| ③ **fsync 谎言** | *"Unfortunately, most consumer-grade mass storage devices lie about syncing. Disk drives will report that content is safely on persistent media as soon as it reaches the track buffer and before actually being written to oxide."*；*"USB flash memory sticks seem to be especially pernicious liars regarding sync requests... Pulling out the memory stick while the LED is still flashing will frequently result in database corruption."*；*"SQLite must believe whatever the operating system and hardware tell it about the status of sync requests. There is no way for SQLite to detect that either is lying and that writes might be occurring out-of-order."* | **高**——如果阙疑在 U 盘/移动硬盘上跑账本，这是最现实的风险。**但 WAL 模式把它降级为"丢持久性"而非"损坏"。** |
| ④ **非断电安全的闪存控制器** | *"in some flash memory controllers the wear-leveling logic can cause random filesystem damage if power is interrupted during a write... could result in an SQLite database being corrupted even though the database was not even in use at the time of the power loss."* | **中**——嵌入式方向尤须注意；这是硬件层面的，软件无法防。 |
| ② **NFS / 网络文件系统锁缺陷** | *"This is especially true of network filesystems and NFS in particular. If SQLite is used on a filesystem where the locking primitives contain bugs, and if two or more threads or processes try to access the same database at the same time, then database corruption might result."* | **高（如果阙疑把账本放在网盘/同步盘里）**。官方 WAL 页也明确 WAL 不能跨网络文件系统。**结论：账本必须放在本地磁盘，不要放 OneDrive/坚果云/NFS。** |
| ② **`close()` 取消 POSIX 咨询锁** | *"the close() system call will cancel all POSIX advisory locks on the same file for all threads and all file descriptors in the process."*；*"To avoid corruptions, developers should be careful to never use close() on an SQLite database file while one or more database connections are open, even in other threads."* | **中**——Python 的 `sqlite3` 通常不会这样，但如果阙疑用 `os.close()` 或 `open()/close()` 混用就会中招。 |
| ② **跨 fork() 携带连接** | *"Do not open an SQLite database connection, then fork(), then try to use that database connection in the child process. All kinds of locking problems will result and you can easily end up with a corrupt database."* | **中**——如果阙疑用 `multiprocessing` 做并行复算，必须**在每个子进程里重新打开连接**，不能继承。 |
| ② **多份 SQLite 库被链入同一应用** | *"if multiple copies of SQLite is linked into the same application, then there will be multiple instances of this global list... A close() operation on one connection might unknowingly clear the locks on a different database connection, leading to database corruption."* | **低**——Python 只有一个 `sqlite3` 模块。 |
| ⑤ **应用内存损坏** | *"SQLite is a C-library that runs in the same address space as the application... stray pointers, buffer overruns, heap corruption... can corrupt internal SQLite data structure and ultimately result in a corrupt database file."* | **低**（Python 层），**但如果阙疑写 C++ 扩展则升高**。 |
| ⑦ **配置错误** | *"Setting PRAGMA synchronous=OFF can cause the database to go corrupt if there is an operating-system crash or power failure"*；*"Using PRAGMA journal_mode=OFF or PRAGMA journal_mode=MEMORY and taking an application crash in the middle of a write transaction"*；*"Setting PRAGMA writable_schema=ON and then changing the database schema using DML statements can render the database completely unreadable"* | **高（如果阙疑为了快而调这些参数）**。**明确禁止：`synchronous=OFF`、`journal_mode=OFF/MEMORY`、`writable_schema=ON`。** |
| ⑧ **WAL-reset bug** | 见核心结论 2 | **高**——见行动 1 |
| ⑧ **模式切换 + VACUUM** | *"Repeatedly switching an SQLite database in and out of WAL mode and running the VACUUM command in between switches, in one process or thread, can cause another process or thread that has the database file open to miss the fact that the database has changed."* | **低**——阙疑不需要频繁切换模式或 VACUUM。**但如果做了，必须独占访问。** |
| ⑧ **WAL 共享内存锁的 I/O 错误** | *"If the operating system returns an I/O error while attempting to obtain a certain lock on shared memory in WAL mode then SQLite might fail to reset its cache, which could lead to database corruption if subsequent writes are attempted."* | **低**——需要底层 I/O 错误。 |
| ② **硬链接 / 软链接 / unlink / rename 使用中的数据库** | *"If a single database file has multiple links (either hard or soft links) then that is just another way of saying that the file has multiple names... if one process crashes, the other process will be unable to recover the transaction in progress because it will be looking in the wrong place for the appropriate journal."* | **中**——如果阙疑用符号链接指向账本（例如 `data/ledger.db -> /mnt/backup/ledger.db`），有风险。 |

**新防护**：*"Beginning with SQLite version 3.51.0 (2025-11-04), SQLite implements additional defenses to try to avoid problems caused by locks that are broken by close(). These new defenses help when the database is in WAL mode and is being accessed from multiple processes. But they are not a cure-all."*

### 四、PRAGMA 清单：阙疑该设什么

基于以上官方文档，给出**逐条带理由**的清单。**"必须"= 不设就有真实风险；"建议"= 有收益；"禁止"= 设了会引入风险。**

| PRAGMA | 值 | 级别 | 理由 |
|---|---|---|---|
| `journal_mode` | `WAL` | **必须** | 把 fsync 失败的最坏情况从"损坏"降级为"丢持久性"（howtocorrupt 逐字） |
| `synchronous` | `FULL` | **必须** | 官方：*"For maximum reliability and for robustness against database corruption, SQLite should always be run with its default synchronous setting of FULL."* |
| `foreign_keys` | `ON` | **建议** | 默认是 OFF；阙疑的 `deps` 表有外键，开启可防悬空引用 |
| `busy_timeout` | `5000`（毫秒） | **必须** | WAL 下仍有三种情况返回 SQLITE_BUSY；不设 timeout 会直接抛异常 |
| `wal_autocheckpoint` | `1000`（默认） | **建议** | 默认值约 4 MB；**若要"尽量少 checkpoint"（howtocorrupt 的建议），可调大，但代价是 WAL 文件更大、崩溃后恢复更久** |
| `journal_size_limit` | `67108864`（64 MB） | **建议** | 不设则 checkpoint **不会截断** WAL 文件；设了才会 |
| `integrity_check` | 定期执行 | **必须** | 见下节 |
| `locking_mode` | `NORMAL`（默认） | **建议** | 若设为 `EXCLUSIVE` 则其他连接全部 SQLITE_BUSY；单进程场景可考虑 `EXCLUSIVE` 以省去共享内存，但会牺牲灵活性 |
| `cache_size` | 按需（负值 = KiB） | 建议 | 阙疑数据量小，默认 2 MB 足够 |
| `page_size` | 默认 `4096` | **建议不动** | **注意：进入 WAL 模式后无法再改**（WAL 页逐字） |
| `mmap_size` | `0` | **建议** | QNX 上 mmap 有已知缺陷（howtocorrupt 6.2）；虽非 QNX，但关闭 mmap 可减少一类风险 |
| `synchronous=OFF` | — | **禁止** | howtocorrupt 逐字列出 |
| `journal_mode=OFF` / `MEMORY` | — | **禁止** | 同上 |
| `writable_schema=ON` | — | **禁止** | 同上；官方：*"can render the database completely unreadable"* |

**一个 Python 侧的注意事项**：`sqlite3` 模块的默认 `isolation_level` 是 `""`（隐式开启事务），这意味着 `execute("INSERT ...")` 会**自动开始一个事务但不自动提交**。对 append-only 账本，应当**显式**写 `BEGIN IMMEDIATE; ... COMMIT;`，因为 `BEGIN IMMEDIATE` 立即获取 reserved 锁，避免在提交时才失败。同时 `isolation_level=None` 可关闭 Python 的隐式事务管理，改由代码显式控制。

### 五、损坏检测与修复

**检测**：
- `PRAGMA integrity_check;` —— 完整校验，返回错误列表或 `ok`。**注意**：*"Pragma integrity_check will return at most N errors before the analysis quits, with N defaulting to 100."*（来自中文二手转述 cnblogs，**我未从 sqlite.org 官方页面逐字核验这个默认值 100**）。
- `PRAGMA quick_check;` —— 更快但不完整。
- `PRAGMA foreign_key_check;` —— 只查外键违反。
- `PRAGMA integrity_check(N)` —— 限制返回错误数。

**修复**：官方提供 `.recover` 命令（CLI），它逐页扫描并尽可能抢救数据（来源：多个中文技术博客转述，**我未从 sqlite.org 官方 `.recover` 文档逐字核验**）。

**对阙疑的最优策略：不做"修复"，做"重建"。** 理由是一个结构性事实：**阙疑的账本是可复算的——452 条判决的每一条都应当能从知识卡 + 规则 + 证据重新推导出来**。所以损坏的正确响应不是 `.recover`，而是：
1. 用 `PRAGMA integrity_check` 检测到损坏；
2. 从**最新的完整备份**恢复；
3. 用**哈希链校验**确定哪些判决丢失或损坏；
4. **用内核重新计算**这些判决，追加回去。

**这个策略的代价远低于通用修复**，因为阙疑有通用数据库没有的东西：**可复算性**。这也正是阙疑卖点的工程价值所在——它不只是论文里的漂亮话，它直接决定了灾难恢复的成本。**这一条应当写进论文。**

**Fossil 的对照做法**（见下节）值得注意：Fossil 有 `rebuild` 命令，它把除 `blob` 表以外的所有表都销毁并从 `blob` 表重建。**这是"只保留不可变的原始数据、其余皆为派生缓存"这一设计的直接收益。**

### 六、真实案例：Fossil SCM 用 SQLite 做 append-only 内容寻址存储

来源：fossil-scm.org 的《Fossil is not Relational》文档。**Fossil 是一个把 SQLite 用作"append-only artifact 仓库"的成熟案例，已经用了 20 年以上**（其仓库文件本身就是一个 SQLite 数据库）。它对阙疑有三条直接可借鉴的设计。

**（1）不可变性 + 内容寻址**。逐字：*"It is **immutable**. An artifact is identified by its unique hash value. Any modification to an artifact changes that hash, thereby changing its identity."*

**（2）"not relational" 的真正含义**：不可变的 artifact 才是数据模型的本体，SQLite 的关系表只是**派生的、可销毁重建的缓存**。逐字：
- *"how does one perform SQL queries against its plain-text format? In short: One Does Not Simply Query the Artifacts."*
- *"Crosslinking, as its colloquially known, is a one-way processing step which transforms an immutable artifact's state into something database-friendly."*
- *"any tables in a Fossil repository file except for the `blob` table. Most, but not all, of these tables are transient caches... and can safely be destroyed and rebuilt from the collection of artifacts with no loss of state to the repository. All of them, except for `blob` and `delta`, can be destroyed with no loss of SCM-relevant data."*
- *"Noting, however, that all database tables are effectively internal APIs, with no API stability guarantees and subject to change at any time."*

**（3）schema 设计**：`blob` 表的四个字段逐字：
- `uuid`：*"the hash code of the blob's contents."*
- `rid`：*"a unique integer key for this record. This is how the blob table is mapped to other (transient) tables, but the RIDs are specific to one given copy of a repository and must not be used for cross-repository referencing."* —— **这是一个重要的设计决策：内部用整数 RID 做外键（快），对外用哈希 UUID 做引用（可跨仓库）**。阙疑的 `deps` 表可以照抄这个双键设计。
- `size`：*"the size, in bytes, of the blob's contents, or -1 for 'phantom' blobs (those which Fossil knows should exist because it's seen them referenced somewhere, but for which it has not been given any content)."* —— **"phantom blob"（已知应存在但内容未获得）这个概念对阙疑很有用**：账本里引用了某张知识卡的某个版本，但该版本内容缺失时，可以记为一个 phantom，而不是拒绝整条记录。
- `content`：*"the blob's raw content bytes, with the caveat that Fossil is free to store it in an 'alternate representation.'"*

**delta 编码**：*"the `content` field often holds a zlib-compressed delta from a previous version of the blob's content (a separate entry in the `blob` table), and an auxiliary table named `delta` maps such blobs to their previous versions, such that Fossil can reconstruct the real content from them by applying the delta to its previous version (and such deltas may be chained). Thus extraction of the content from this field cannot be performed via vanilla SQL, and requires a Fossil-specific function."*

**校验机制（两层）**：
- **Z 行**：*"The `Z` line is a hash of all of the content of this artifact which precedes the `Z` line. Thus any change to the content of an artifact changes both the artifact's identity (its hash) and its `Z` value, making it impossible to inject modified artifacts into an existing artifact tree."*
- **R 行**：*"The `R` line is yet another consistency-checking hash... an internal consistency check/line of defense against modification of file content referenced by the artifact."*
- **提交前重新解析**：*"Every artifact which is internally created is re-parsed for validity before it is committed to the database, making it impossible that Fossil can inject an invalid artifact into the repository."*

**删除合规：shunning**。这是"append-only 与删除权冲突"的成熟答案。逐字：*"Fossil offers only one option for modifying history: 'shunning' is the forceful removal of an artifact from the `blob` table and the creation of a db record stating that the shunned hash may no longer be synced into this repository. Shunning effectively leaves a hole in the SCM history, and is only intended to be used for removal of illegal, dangerous, or private information which should never have been added to the repository."* —— **注意 Fossil 的诚实：shunning 是"在历史上留一个洞"，而不是"假装它从未存在"。这正是方向 64 要讨论的 GDPR 遗忘权与 append-only 的冲突的工程答案。**

**哈希算法迁移**：*"There are exceptionally rare cases, namely the switch from SHA1 to SHA3-256 ushered in with Fossil 2.0, which can lead to true incompatibility. e.g. a Fossil 1.x client cannot use a repository database which contains SHA3 hashes, regardless of a rebuild."* —— **对阙疑的教训：哈希算法是一个"一旦选定就近乎不可迁移"的决定。**（阙疑用 SHA-256，与 RFC 6962 一致，是正确的选择。）

**注意：Fossil 文档没有给出任何性能或体积数字**（该页唯一的定性表述是 *"reference the `blob` table via its RID field, as that's far more efficient than using hashes (`blob.uuid`) as foreign keys."*）。

### 七、容量与性能上限的数字，以及一个必须避开的陷阱

**容量上限**（sqlite.org/limits.html 逐字）：
- 最大数据库：*"The maximum size of a database file is 4294967294 pages. At the maximum page size of 65536 bytes, this translates into a maximum database size of approximately 2.8e+14 bytes (281 terabytes, or 256 tebibytes, or 281474 gigabytes, or 262143 gibibytes)."*
- 最大页数：*"The largest possible setting for SQLITE_MAX_PAGE_COUNT is 4294967294 (2³²−2). Since version 3.45.0 (2024-01-15), 4294967294 is also the default value."*
- 默认页大小 **4096 字节**；页大小范围 **512–65536**（2 的幂）。
- 最大行数：*"The theoretical maximum number of rows in a table is 2⁶⁴... This limit is unreachable since the maximum database size of 281 terabytes will be reached first. A 281 terabytes database can hold no more than approximately 2e+13 rows."*
- 最大列数：`SQLITE_MAX_COLUMN` 默认 **2000**，可编译到 **32767**。
- 最大 SQL 语句长度：默认 **1,000,000,000 字节**。
- 最大 ATTACH 数据库数：默认 **10**，硬上限 **125**。
- 单条 SQL 的最大宿主参数编号：**32766**（3.32.0 之后；之前为 999）。
- *"versions of SQLite since about release 3.5.8 (2008-04-16) have well-defined limits, and those limits are tested as part of the test suite."*

**阙疑对照**：452 条 × 4 KB ≈ **1.8 MB**。占默认页大小下 17.5 TB 上限的 **1.0×10⁻⁸**；占 281 TB 上限的 **6.4×10⁻⁹**。**容量完全不是约束。唯一可能有意义的上限是 `SQLITE_MAX_VARIABLE_NUMBER`（32766）——如果阙疑用 `executemany` 一次性插入大批记录，参数个数可能触顶。批量插入时应分批（例如每批 1000 条）。**

**性能数字的陷阱（必须诚实标注）**：SQLite 官方的 *Database Speed Comparison* 页面（sqlite.org/speed.html）**开篇就声明已作废**，逐字：*"Note: This document is very very old. It describes a speed comparison between archaic versions of SQLite, MySQL and PostgreSQL. The numbers here have become meaningless. This page has been retained only as an historical artifact."*

该页测试的是 **SQLite 2.7.6 / PostgreSQL 7.1.3 / MySQL 3.23.41**，硬件是 **1.6 GHz Athlon + 1 GB 内存 + IDE 硬盘**，操作系统 **RedHat Linux 7.2**。其中与"批量提交 vs 逐条提交"最相关的两个数字（**仅作历史参照，不可引用**）：
- Test 1（1000 条 INSERT，每条独立事务）：SQLite 2.7.6 同步 **13.061 s**（≈ 77 条/秒）vs 不同步 **0.223 s**（≈ 4,484 条/秒）。
- Test 2（25000 条 INSERT 放在一个事务里）：SQLite 2.7.6 同步 **0.914 s**（≈ 27,352 条/秒）。

**结论（这部分是可用的）**：逐条提交与批量提交之间差 **350 倍**以上，而这个差异**完全由 fsync 次数决定**，与 SQLite 版本无关。**阙疑若一次追加多条判决，必须放在同一个事务里。** 但**绝对数字（77 条/秒、27,352 条/秒）不可引用**——它们是 2002 年左右的硬件与 SQLite 2.x。

**关于"85 到 96,000 条/秒"这个广为流传的数字**：我在中文技术站点（kzen.dev、duoke360.com）看到 *"一个C应用程序的批量插入性能可以从每秒85次插入到每秒96,000次插入不等"*，这似乎是某条 Stack Overflow 答案的转述。**我未能核验其原始出处、硬件与 SQLite 版本，因此本方向不采用这个数字。** 若阙疑要用，必须自己实测（见行动 3）。

---

## 对阙疑的 3 条具体行动

1. **立刻检查 SQLite 版本，并据此决定是否升级（本周内，2026-10 前）**。执行：
```bash
python -c "import sqlite3; print('sqlite3 module:', sqlite3.version); print('sqlite lib   :', sqlite3.sqlite_version)"
```
- 若 `sqlite_version` **< 3.51.3**：**必须**满足以下之一——(a) 升级 Python 或自行编译带新版 SQLite 的 Python；(b) 严格保证"任何时刻只有一个进程持有写连接"（把对账器改成 `file:ledger.db?mode=ro` 的只读连接）；(c) 在代码里用文件锁（`fcntl.flock` / `msvcrt.locking`）串行化所有写操作。**推荐 (b)**——因为对账器本来就不需要写。
- 若 **≥ 3.51.3**：可以放宽到"允许多个进程写"，但仍应避免"同时写 + 同时 checkpoint"。
- **同时**：在 `_arch_v47/` 之外的代码目录下加一个启动自检函数 `assert_sqlite_version()`，把版本号写进每条判决的 `payload_json`（作为环境元数据的一部分），这样**论文的 artifact 能证明结果是在哪个 SQLite 版本上产生的**。**时间点：2026-10 底前。**

2. **写一份 `db/SCHEMA.md` + `db/init.sql`，把本方向的 PRAGMA 清单固化成可执行代码，并加一条"分发前处理"流程（2026-11 前）**。`init.sql` 的开头逐字建议如下：

```sql
-- 阙疑判决账本：初始化。参见 research/19_sqlite_config.md
PRAGMA journal_mode = WAL;          -- howtocorrupt: WAL 下 COMMIT 时 sync 失败只丢持久性，不损坏
PRAGMA synchronous = FULL;          -- 官方要求：max reliability 必须 FULL
PRAGMA foreign_keys = ON;           -- 默认 OFF，必须显式开启
PRAGMA busy_timeout = 5000;         -- WAL 下仍有三种 SQLITE_BUSY 情况
PRAGMA journal_size_limit = 67108864;  -- 64 MiB；不设则 checkpoint 不截断 WAL
PRAGMA mmap_size = 0;               -- 规避 mmap 相关的一类风险
-- 禁止项（写入注释以防后来者修改）：
-- PRAGMA synchronous = OFF;   -- 会损坏
-- PRAGMA journal_mode = OFF;  -- 会损坏
-- PRAGMA journal_mode = MEMORY; -- 会损坏
-- PRAGMA writable_schema = ON; -- 可使数据库完全不可读
```

**并且必须加一个"分发前"脚本** `db/prepare_release.py`，做三件事：(a) `PRAGMA wal_checkpoint(TRUNCATE)` 把 WAL 合并回主库；(b) 关闭所有连接；(c) 断言目录下**只有** `ledger.db` 一个文件（没有 `-wal` / `-shm` 残留）。**理由**：WAL 页逐字警告 *"There is an additional quasi-persistent '-wal' file and '-shm' shared memory file associated with each database"* —— 如果阙疑把 `.db` 单独作为 artifact 上传而漏了 `-wal`，**下载者会看到一个丢失了最近事务的旧数据库，而且不会报错**。这是最容易发生、也最难被发现的 artifact 缺陷。**时间点：2026-11 前，与第一次 artifact 打包同步。**

3. **把"灾难恢复 = 重算而非修复"写成一份可执行的恢复流程，并做一次演练，时间点 2027-06 前**。具体做法：(a) 在 `db/` 下写 `recover.py`，流程为：`PRAGMA integrity_check` → 若失败则从备份恢复 → 逐条重算哈希链定位第一处断点 → 报告断点后的所有判决为"待重算" → 调用内核重算并追加；(b) **做一次真实演练**：故意损坏数据库的一个字节（例如用 `dd` 覆写中间 512 字节），运行 `recover.py`，记录恢复耗时与恢复结果，把结果写进 `exp/recovery_drill.csv`（字段 `damage_offset, damage_size, integrity_check_result, detected_at_seq, recovered_count, elapsed_s`）；(c) 在论文里写一段逐字建议的文本："本系统的灾难恢复不依赖通用数据库修复工具。由于判决是可复算的，恢复流程为：检测 → 回退到最近完整备份 → 用哈希链定位断点 → 用内核重算断点后的判决并重新追加。这使得恢复的正确性可以独立验证（对账器可对恢复后的账本重新做完整校验），而不需要信任任何修复工具的语义。" **(c) 这一段是本方向最有论文价值的产出**——它把"可复算"从一句宣传语变成一个可测量的工程性质（恢复耗时、恢复完整率）。同时建议：**把 `integrity_check` 排进常规流程**（例如每次追加判决前跑 `PRAGMA quick_check`，每周跑一次完整 `PRAGMA integrity_check`），并把结果写进账本的元数据表，这样"我们检查过完整性"本身也是可审计的。

---

## 盲区（诚实标注）

- **`PRAGMA integrity_check` 默认最多返回 100 个错误的这个数字，我未从官方页面核验**。它来自中文博客（cnblogs 的"检查sqlite数据库完整性"，2016-10-12），转述原文为 *"Pragma integrity_check will return at most N errors before the analysis quits, with N defaulting to 100."* —— 这句话看起来像官方文档的英文原文，但**我没有打开 sqlite.org/pragma.html 的对应段落逐字确认**。若阙疑要引用这个数字，必须回到官方页面。
- **`.recover` 命令的具体行为、能恢复什么、恢复上限，我完全没有核验**。相关的中文来源（raybyte.cn、quant67.com、docs.pingcode.com）都是二手汇编，且我没有从 sqlite.org 官方 CLI 文档确认 `.recover` 的存在与语义。**我在正文里把它写成"官方提供"是不严谨的——更准确的表述是"SQLite CLI 据称提供 .recover 命令，我未核验"。**
- **WAL-reset bug 的修复版本 3.51.3（2026-03-13）**：我拿到的是 howtocorrupt 页面的逐字表述（*"It existed in all versions of SQLite from 3.7.0 through 3.51.2."*）与 WAL 页面提到的 *"WAL-reset bug 修复：3.51.3（2026-03-13）"*。**我未打开 sqlite.org 的 release log 核验 3.51.3 的确切发布日期与 release note 原文。** 行动 1 要求阙疑自己检查版本——**这是必须做的，不能只依赖本调研。**
- **SQLite 官方 speed 页的所有数字已作废**（官方自己声明 *"The numbers here have become meaningless"*）。我在正文里只用了它的**比值**（逐条提交 vs 批量提交差 350 倍以上），**没有用任何绝对数字**。**"85 到 96,000 条/秒"这个广为流传的数字我未核验出处，本方向不采用。** 阙疑若需要真实的写入吞吐数字，**必须自己实测**（行动 3 可以顺便覆盖）。
- **Fossil 的 `blob` 表设计我拿到了逐字文档，但没有任何性能或体积数字**（该文档明确不含）。如果阙疑要引用 Fossil 作为"SQLite 做 append-only 存储可行"的证据，**能引用的只有"它已经这样用了 20 年以上"这个事实，不能引用任何数字**。
- **RFC 3161（时间戳权威）我只拿到了标题与摘要**（rfc-editor.org/info/rfc3161/，逐字：*"This document describes the format of a request sent to a Time Stamping Authority (TSA) and of the response that is..."*）。**具体的请求/响应格式、验证成本、以及公开 TSA 服务的可用性与费用我完全未核验。** 阙疑若要把"外部锚定"写进设计（方向 64 会进一步讨论），需要自己补 RFC 3161 的正文与至少一个可用 TSA 的实测。
- **immudb 我只拿到了存在性证据**（GitHub codenotary/immudb、immudb.io 逐字：*"immudb is a database with built-in cryptographic proof and verification. It tracks changes to sensitive data, and the..."*），**其架构细节（Merkle 树的实现方式）、性能数字、与 SQLite 的关系（它是否基于 SQLite 存储引擎）我都没有核验**。中文来源（CSDN 的 immudb 系列）是 AI 生成特征明显的汇编内容，我未采用。
- **一个未验证的关键假设**：我在核心结论 2 里推断"阙疑的内核与对账器可能同时打开同一个数据库并写入"。**这个推断我没有依据**——我没有看过阙疑的实际代码。**如果实际情况是"对账器只读"或"内核与对账器不共享同一个 DB 文件"，那么 WAL-reset bug 的风险就低得多。** 阙疑必须自己确认这一点，再决定行动的紧迫程度。
- **另一个未验证的假设**：我按"每条判决 4 KB"估算账本体积（1.8 MB）。**这个数字是我拍的，没有依据。** 如果阙疑的 `payload_json` 里嵌入了完整的证据快照（例如整段代码、编译输出），单条可能达到几十 KB 到几 MB，452 条的总量可能到几百 MB 到 1 GB 量级。**这会影响备份策略与 WAL 文件大小，但不影响容量上限的结论（仍差 4–5 个数量级）。**
- **样本偏差**：本方向的中文搜索结果中，`runebook.dev`（多个 SQLite 页面）、`raybyte.cn`、`quant67.com`、`kzen.dev`、`duoke360.com`、CSDN 的 SQLite 系列**大量是 AI 生成或机器翻译的汇编内容**（runebook.dev 是文档镜像站，其"中文翻译"由机器生成）。**我在正文中只使用 sqlite.org 的官方页面作为逐字来源**，中文来源仅用于"某主题存在"的存在性证据，且已逐条标注。
- **一个方法论层面的提醒**：SQLite 官方文档是本方向唯一权威且高质量的来源，**这与其他方向（尤其是中文搜索为主的方向）形成鲜明对比**。阙疑在写作时应当**优先引用 sqlite.org 的一手页面**，而不是任何二手汇编。**如果一篇文档没有给出版本号与日期，就不要引用它。**

---

## 来源

1. Write-Ahead Logging — https://sqlite.org/wal.html — 逐字引文："Beginning with version 3.7.0 (2010-07-21), a new 'Write-Ahead Log' option (hereafter referred to as 'WAL') is available."；优点四条（"WAL is significantly faster in most scenarios."、"readers do not block writers and a writer does not block readers"、"Disk I/O operations tends to be more sequential"、"WAL uses many fewer fsync() operations"）；缺点八条（含 "WAL might be very slightly slower (perhaps 1% or 2% slower)"、"For transactions larger than about 100 megabytes, traditional rollback journal modes will likely be faster. For transactions in excess of a gigabyte, WAL mode may fail with an I/O or disk-full error."）；"Unlike the other journaling modes, PRAGMA journal_mode=WAL is persistent."；"By default, SQLite will automatically checkpoint whenever a COMMIT occurs that causes the WAL file to be 1000 pages or more in size"；"There are three subtypes of checkpoints that vary in their aggressiveness: PASSIVE, FULL, and RESTART."；"The checkpoint does not normally truncate the WAL file (unless the journal_size_limit pragma is set)."；"a long-running read transaction can prevent a checkpointer from making progress."；"the wal-index rarely exceeds 32 KiB in size and is never synced"；"the checkpoint is the only operation to issue an I/O barrier or sync operation"；"This constraint was relaxed beginning with SQLite version 3.22.0 (2018-01-22)."；"it is good practice to convert the database to PRAGMA journal_mode=DELETE prior to burning an SQLite database image onto read-only media." — SQLite 官方文档 — 抓取于 2026-09-29
2. How To Corrupt An SQLite Database File — https://sqlite.org/howtocorrupt.html — 逐字引文："An SQLite database is highly resistant to corruption. If an application crash, or an operating-system crash, or even a power failure occurs in the middle of a transaction, the partially written transaction should be automatically rolled back..."；"Though SQLite is resistant to database corruption, it is not immune."；"SQLite is also field-proven with approximately two billion active deployments with no serious problems."；"However, SQLite in WAL mode is far more forgiving of out-of-order writes than in the default rollback journal modes. In WAL mode, the only time that a failed sync operation can cause database corruption is during a checkpoint operation. A sync failure during a COMMIT might result in loss of durability but not in a corrupt database file. Hence, one line of defense against database corruption due to failed sync operations is to use SQLite in WAL mode and to checkpoint as infrequently as possible."；"This is the WAL-reset bug. It existed in all versions of SQLite from 3.7.0 through 3.51.2."；"Unfortunately, most consumer-grade mass storage devices lie about syncing."；"USB flash memory sticks seem to be especially pernicious liars regarding sync requests."；"There is no way for SQLite to detect that either is lying and that writes might be occurring out-of-order."；"This is especially true of network filesystems and NFS in particular."；"the close() system call will cancel all POSIX advisory locks on the same file for all threads and all file descriptors in the process."；"Do not open an SQLite database connection, then fork(), then try to use that database connection in the child process."；"For maximum reliability and for robustness against database corruption, SQLite should always be run with its default synchronous setting of FULL."；"Setting PRAGMA synchronous=OFF can cause the database to go corrupt if there is an operating-system crash or power failure"；"Setting PRAGMA writable_schema=ON and then changing the database schema using DML statements can render the database completely unreadable"；"Beginning with SQLite version 3.51.0 (2025-11-04), SQLite implements additional defenses..." — SQLite 官方文档 — 页面标注 2026-04-13
3. Atomic Commit In SQLite — https://sqlite.org/atomiccommit.html — 逐字引文：步骤 3.2–3.12 的完整序列；"On most platforms two separate flush (or fsync()) operations are required."；"Another flush must occur to make sure that all the database changes are written into nonvolatile storage."；"After the database changes are all safely on the mass storage device, the rollback journal file is deleted. This is the instant where the transaction commits."；"if the synchronous setting is lowered to 'normal', SQLite only flushes the rollback journal once, after the page count has been written."；"because of the inherent slowness of writing to disk or flash memory, this step together with the rollback journal file flush in section 3.7 above takes up most of the time required to complete a transaction commit in SQLite."；"SQLite also uses a 32-bit checksum on every page of data in the rollback journal... If an incorrect checksum is seen, the rollback is abandoned."；"the checksums in the rollback journal are not necessary if the synchronous setting is FULL. We only depend on the checksums when synchronous is lowered to NORMAL."；"SQLite has traditionally assumed that a sector write is not atomic. However, SQLite does always assume that a sector write is linear."；"SQLite does not add any redundancy to the database file for the purpose of detecting corruption or I/O errors."；"Prior to version 3.7.9 (2011-11-01), SQLite did not assume powersafe overwrite."；"Profiling indicates that for most systems and in most circumstances SQLite spends most of its time doing disk I/O." — SQLite 官方文档 — 抓取于 2026-09-29
4. Implementation Limits For SQLite — https://sqlite.org/limits.html — 逐字引文："The maximum size of a database file is 4294967294 pages. At the maximum page size of 65536 bytes, this translates into a maximum database size of approximately 2.8e+14 bytes (281 terabytes, or 256 tebibytes, or 281474 gigabytes, or 262143 gibibytes)."；"The largest possible setting for SQLITE_MAX_PAGE_COUNT is 4294967294 (2³²−2). Since version 3.45.0 (2024-01-15), 4294967294 is also the default value."；"The theoretical maximum number of rows in a table is 2⁶⁴ (18446744073709551616 or about 1.8e+19). This limit is unreachable since the maximum database size of 281 terabytes will be reached first."；"The maximum number of bytes in the text of an SQL statement is limited to SQLITE_MAX_SQL_LENGTH which defaults to 1,000,000,000."；"The number of simultaneously attached databases is limited to SQLITE_MAX_ATTACHED which is set to 10 by default. The maximum number of attached databases cannot be increased above 125."；"versions of SQLite since about release 3.5.8 (2008-04-16) have well-defined limits, and those limits are tested as part of the test suite." — SQLite 官方文档 — 页面标注 2026-07-10
5. Fossil is not Relational — https://www.fossil-scm.org/home/doc/trunk/www/fossil-is-not-relational.md — 逐字引文："It is immutable. An artifact is identified by its unique hash value. Any modification to an artifact changes that hash, thereby changing its identity."；"how does one perform SQL queries against its plain-text format? In short: One Does Not Simply Query the Artifacts."；"Crosslinking, as its colloquially known, is a one-way processing step which transforms an immutable artifact's state into something database-friendly."；"All of them, except for `blob` and `delta`, can be destroyed with no loss of SCM-relevant data."；"all database tables are effectively internal APIs, with no API stability guarantees and subject to change at any time."；blob 表字段 `uuid`/`rid`/`size`/`content` 的逐字定义（含 "phantom" blobs）；"the `content` field often holds a zlib-compressed delta from a previous version of the blob's content"；"The `Z` line is a hash of all of the content of this artifact which precedes the `Z` line."；"The `R` line is yet another consistency-checking hash"；"Every artifact which is internally created is re-parsed for validity before it is committed to the database"；"Fossil offers only one option for modifying history: 'shunning' is the forceful removal of an artifact from the `blob` table and the creation of a db record stating that the shunned hash may no longer be synced into this repository. Shunning effectively leaves a hole in the SCM history"；"the switch from SHA1 to SHA3-256 ushered in with Fossil 2.0, which can lead to true incompatibility" — Fossil SCM 官方文档 — 抓取于 2026-09-29（页面标注 2026-08-28）
6. Database Speed Comparison — https://sqlite.org/speed.html — 逐字引文（**官方声明已作废**）："Note: This document is very very old. It describes a speed comparison between archaic versions of SQLite, MySQL and PostgreSQL. The numbers here have become meaningless. This page has been retained only as an historical artifact."；测试环境 "a 1.6GHz Athlon with 1GB or memory and an IDE disk drive... RedHat Linux 7.2"；Test 1（1000 INSERTs）"SQLite 2.7.6: 13.061 / SQLite 2.7.6 (nosync): 0.223"；Test 2（25000 INSERTs in a transaction）"SQLite 2.7.6: 0.914 / SQLite 2.7.6 (nosync): 0.757"；"SQLite works best if you group multiple operations together into a single transaction." — SQLite 官方文档（**历史页面，数字已作废，本方向仅用其比值**）
7. File Locking And Concurrency In SQLite Version 3 — https://sqlite.org/lockingv3.html — "SQLite Version 3.0.0 introduced a new locking and journaling mechanism designed to improve concurrency over..." — SQLite 官方文档 — 页面标注 2025-05-31（**未打开正文**）
8. Pragma statements supported by SQLite — https://sqlite.org/pragma.html — SQLite 官方 PRAGMA 参考页 — 页面标注 2026-06-04（**未逐条打开核验**）
9. SQLite Documentation Search: synchronous = NORMAL — https://sqlite.org/search?q=synchronous+%3D+NORMAL — 逐字："For maximum database safety following a power loss, the setting of PRAGMA synchronous =FULL is recommended." — SQLite 官方文档搜索页 — 抓取于 2026-09-29
10. RFC 3161: Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP) — https://www.rfc-editor.org/info/rfc3161/ — 逐字："This document describes the format of a request sent to a Time Stamping Authority (TSA) and of the response that is..." — IETF — 抓取于 2026-09-29（**正文未获取**）
11. Sigstore Timestamp Authority — https://github.com/sigstore/timestamp-authority — "A timestamp authority creates signed timestamps using public key infrastructure. The operator of the timestamp authority must secure the signing key material to prevent unauthorized timestamp signing."；"If you trust an external timestamp authority, fetch the timestamp from Rekor, verify the signed timestamp, and verify..." — Sigstore 项目 — 抓取于 2026-09-29
12. codenotary/immudb（GitHub）— https://github.com/codenotary/immudb 与 https://immudb.io/ — 逐字："immudb is a database with built-in cryptographic proof and verification. It tracks changes to sensitive data, and the..." — Codenotary — 页面标注 2026-09-04（**架构与性能细节未核验**）
13. The Write Stuff: Concurrent Write Transactions in SQLite — https://oldmoe.blog/2024/07/08/the-write-stuff-concurrent-write-transactions-in-sqlite/ — "Versatile as it is, SQLite still suffers from one major drawback. Which is write concurrency." — oldmoe.blog — 2024-07-08（**未打开正文**）
14. SQLite WAL Concurrency and Locking — https://tarrragon.github.io/blog/backend/01-database/vendors/sqlite/wal-concurrency-locking/ — 关于 SQLite 单文件/嵌入式与 WAL 并发的实现层分析 — tarragon — 2026-05-21（**未打开正文**）
15. 检查sqlite数据库完整性 — https://www.cnblogs.com/huahuahu/p/jian-chasqlite-shu-ju-ku-wan-zheng-xing.html — 逐字："Pragma integrity_check will return at most N errors before the analysis quits, with N defaulting to 100."（**二手转述，未从官方页面核验**） — 博客园 — 2016-10-12
16. SQLite数据库损坏及其修复探究 — https://www.cnblogs.com/ZhaoxiCheung/p/15861066.html — "SQLite 数据库具有很强的抗损坏能力。在执行事务时如果发生应用程序崩溃、操作系统崩溃甚至电源故障，那么..."（**二手汇编，仅作存在性证据**） — 博客园 — 2022-06-21
17. 提高SQLite的INSERT-per-second性能 — https://kzen.dev/zh/51171386 — "一个C应用程序的批量插入性能可以从每秒85次插入到每秒96,000次插入不等"（**Stack Overflow 答案的镜像转述，原始出处与硬件/版本未核验，本方向不采用该数字**） — kzen.dev — 2009-10-27
18. 警惕 SQLite 文件损坏：WAL 模式与多进程并发的安全替代方案 — https://runebook.dev/zh/docs/sqlite/howtocorrupt — sqlite.org/howtocorrupt.html 的机器翻译镜像（**仅作存在性证据，本方向所有 howtocorrupt 引文均以官方英文页面为准**） — runebook.dev — 2025-12-09
