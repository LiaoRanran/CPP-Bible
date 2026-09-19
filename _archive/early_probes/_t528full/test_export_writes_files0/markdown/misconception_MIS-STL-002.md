# MIS-STL-002（misconception）

## 正面

【误解】MIS-STL-002 vector<bool> 的 operator[] 返回 bool&
触发说法：auto& b = vb[0]; 拿到的是 bool 的引用

## 背面

为什么错：vector<bool> 是位压缩特化，operator[] 返回代理对象（proxy reference），不是 bool&
反例 1：后果：不能取址、不能绑 bool&、不能喂给 span<bool>；需要真 bool 用 vector<char> 或 deque<bool>
