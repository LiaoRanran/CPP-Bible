# MIS-CONC-009（misconception）

## 正面

【误解】MIS-CONC-009 stop_token 能主动把线程停下来
触发说法：request_stop() 之后线程就会停

## 背面

为什么错：停止是**协作**的：request_stop 只置位，线程须主动检查 stop_requested() 并返回
反例 1：线程从不检查 → jthread 析构时 join 永久阻塞；阻塞系统调用须用 stop_callback 唤醒
