# MIS-CONC-008（misconception）

## 正面

【误解】MIS-CONC-008 线程对象既不 join 也不 detach，只是警告一下
触发说法：忘了 join 顶多资源泄漏

## 背面

为什么错：可汇合（joinable）的 thread 析构时调用 std::terminate → 程序直接终止
