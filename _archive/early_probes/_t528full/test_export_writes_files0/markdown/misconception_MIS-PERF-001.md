# MIS-PERF-001（misconception）

## 正面

【误解】MIS-PERF-001 std::endl 和 \n 是一样的，只是写法不同
触发说法：endl 就是换行的标准写法

## 背面

为什么错：std::endl 除了写 \n 还强制 flush → 每次都触发系统调用；热路径吞吐差距可达量级
