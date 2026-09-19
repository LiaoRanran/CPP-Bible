# MIS-MEM-018（misconception）

## 正面

【误解】MIS-MEM-018 T&& 就是右值引用（混淆推导语境下的万能引用）
触发说法：T&& 就是右值引用，模板参数和普通声明没区别

## 背面

为什么错：实测 EV-MEM-021：推导语境的模板 T&& 传**左值**时推 T=int&，T&& 经引用折叠成 int&（左值引用）；只有传右值才推 T=int、T&& 才是右值引用——T&& 是否为右值引用取决于实参，不是写死的
反例 1：T&& 只有在**推导语境**（[temp.deduct.call] 特判）下才是万能引用：auto&& 同理、const T&& 不是（无左值特判，实测只接右值 T=int）；非推导语境下的 T&&（如 std::move 的返回类型）就是普通右值引用（见 ATOM-MEM-VALUE-002 / EV-MEM-021）
关联原子：ATOM-MEM-VALUE-002 ATOM-MEM-VALUE-001
