# MIS-HIST-003（misconception）

## 正面

【误解】MIS-HIST-003 auto_ptr 被移除是因为它有 bug / 实现得不好
触发说法：auto_ptr 有缺陷所以被弃用

## 背面

为什么错：拷贝构造签名 auto_ptr(auto_ptr&) 不满足 CopyConstructible 却仍能从非 const 对象拷贝——这是 C++98 **没有移动语义**时表达所有权的合理工程妥协，不是实现失误
反例 1：C++11 引入移动语义后，同一需求有了正确语法（std::move + = delete），auto_ptr 才被 unique_ptr 取代
关联原子：ATOM-HIST-AUTOPTR-001
