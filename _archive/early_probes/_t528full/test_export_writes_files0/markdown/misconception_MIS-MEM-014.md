# MIS-MEM-014（misconception）

## 正面

【误解】MIS-MEM-014 delete 放在函数尾就够：没意识到异常/提前 return 会跳过 delete
触发说法：在函数最后 delete 就安全了

## 背面

为什么错：函数在 new 与尾部 delete 之间抛异常或提前 return，尾部 delete 不可达 → 泄漏；只有析构（RAII）在栈展开时必然调用 [except.ctor]
反例 1：实测：safe_path 抛异常后 RAII 析构仍调用（g_live 归 0），裸路径 g_live 留 1（见 ATOM-MEM-RAII-001 / EV-MEM-009）
关联原子：ATOM-MEM-RAII-001
