# MIS-UB-008（misconception）

## 正面

【误解】MIS-UB-008 reinterpret_cast 做类型双关读是常规操作
触发说法：强转指针再解引用就能重新解释位模式

## 背面

为什么错：reinterpret_cast 的类型双关读违反严格别名规则 [basic.lval] → UB；优化器可重排读写顺序
反例 1：正确做法是 std::bit_cast（C++20）或 memcpy（两者都是定义良好的位重解释）
关联原子：ATOM-UB-GRAY-001
