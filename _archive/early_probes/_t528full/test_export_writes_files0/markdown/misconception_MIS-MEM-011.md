# MIS-MEM-011（misconception）

## 正面

【误解】MIS-MEM-011 unique_ptr 可以像普通对象一样按值传参
触发说法：函数签名直接写 unique_ptr<T> 收值

## 背面

为什么错：unique_ptr 不可拷贝，按值传参必须 std::move；调用点忘了 move 就是编译错误（这是优点）
反例 1：只读场景应传 T& 或 T*，不涉及所有权就别传智能指针
关联原子：ATOM-HIST-AUTOPTR-001
