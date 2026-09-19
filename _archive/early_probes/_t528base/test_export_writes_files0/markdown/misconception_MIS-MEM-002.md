# MIS-MEM-002（misconception）

## 正面

【误解】MIS-MEM-002 移动后源对象为空，可以当空容器用
触发说法：移动完 size() 一定是 0

## 背面

为什么错：标准只说源对象处于有效但未指定状态，清空是实现细节而非保证 [lib.types.movedfrom]
反例 1：std::string 的小字符串优化（SSO）下移动后源可能仍保留内容；实测需 volatile 读回才观测得到
关联原子：ATOM-MEM-MOVE-002
