# MIS-MEM-013（misconception）

## 正面

【误解】MIS-MEM-013 裸资源管理靠"记得释放"：认为 new 后自己 delete 就能管好资源
触发说法：new 完记得 delete 就行

## 背面

为什么错：RAII 把释放绑到析构，由语言在作用域结束（含异常栈展开）保证调用；靠人'记得'在异常/提前 return 路径会漏删 → 泄漏 [except.ctor]
反例 1：实测：裸路径在 leak_path 后 g_live 留 1（未释放），同场景 RAII 对象析构后 g_live 归 0（见 ATOM-MEM-RAII-001 / EV-MEM-009）
关联原子：ATOM-MEM-RAII-001
