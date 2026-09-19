# MIS-MEM-020（misconception）

## 正面

【误解】MIS-MEM-020 Rule of Zero 是什么都不写（误解为不管理资源）
触发说法：Rule of Zero 就是类的特殊成员函数什么都不用管

## 背面

为什么错：Rule of Zero 的前提是**成员都是 RAII 类型**（unique_ptr/vector/string 等）：实测 EV-MEM-023，成员形状驱动隐式规则——unique_ptr 成员让移动隐式生成、拷贝被删、析构正确（allocs=1 dtors=1 frees=1）；正确性来自成员类型组合，不是'不写'本身
反例 1：成员含裸资源（raw pointer/文件句柄）时'什么都不写'恰是 MIS-MEM-019 的 double-free 灾难：Rule of Zero 的完整表述是'不需要自定义任何一个特殊成员函数（因为成员是 RAII 类型），就一个都别写'——判据是成员形状，前提不满足就回退 Rule of Three/Five（见 ATOM-MEM-RAII-002）
关联原子：ATOM-MEM-RAII-002 ATOM-MEM-UNIQUE-001
