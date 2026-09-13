# MIS-STL-007（misconception）

## 正面

【误解】MIS-STL-007 std::string 的拷贝是写时复制（COW），很便宜
触发说法：string 拷贝不复制字符，反正 COW

## 背面

为什么错：C++11 起禁止 COW（要求迭代器和引用在拷贝后仍有效且 operator[] 返回可写引用）→ 拷贝必深拷贝
反例 1：SSO 让**短字符串**拷贝便宜，长字符串拷贝是真实开销；该用 move/引用时别依赖 COW
