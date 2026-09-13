# MIS-MEM-022（misconception）

## 正面

【误解】MIS-MEM-022 std::string 总是分配堆内存（不知道 SSO）
触发说法：每次构造 string 都要 new 一块内存

## 背面

为什么错：实测 EV-MEM-029：len≤15 的字符串构造零堆分配（SSO：短串存对象内部 32 字节缓冲），len=16 才首次落堆（本机 libstdc++ 阈值 15）
反例 1：实测 EV-MEM-030：短字符串拷贝 allocs=0（只搬对象内缓冲；赋值走同一实现路径），长字符串同操作 allocs=1——'总是分配'与'总是慢'一起被推翻（见 ATOM-MEM-PERF-002）
关联原子：ATOM-MEM-PERF-002 ATOM-MEM-NEW-001
