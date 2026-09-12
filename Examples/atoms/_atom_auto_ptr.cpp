// 受控实验 ATOM-HIST-AUTOPTR（演化类）：auto_ptr 的"拷贝"其实是转移所有权
//
// 历史语境（C++98）：语言没有移动语义，"把所有权交出去"只能借用**拷贝构造**的语法来表达。
// 于是在 C++98 里这是**合理的工程妥协**；但它违反了容器对元素的隐含约定——"拷贝后两个对象等价"。
//
// 观测设计（三项，全部确定性、不依赖 UB）：
//   ① 编译期（最先测，不成立则整个对照无效）：
//      auto_ptr **可拷贝构造** / unique_ptr **禁止拷贝构造**（static_assert 双向锁定）。
//      —— 这是"语言特性为语义护航"的机器证据：C++11 用 `= delete` 把错误用法变成编译错误。
//   ② 运行时：auto_ptr 拷贝构造后**源被清空**（"拷贝"= 转移）。
//   ③ 运行时：**拷贝整个 vector<auto_ptr>** 后源容器元素全部变空
//      —— 这就是"容器里的灾难"的最小可复现形态（不需要触发排序内部的未指定拷贝次数）。
//
// 复现（C++17 起 std::auto_ptr 已从标准移除，故钉 -std=c++14；deprecation 警告用 -Wno- 静音，
//       但**不掩盖**它已弃用这一事实）：
//   g++ -std=c++14 -Wno-deprecated-declarations -O2 Examples/_atom_auto_ptr.cpp -o build/_replay_autoptr.exe && ./build/_replay_autoptr.exe
//   g++ -std=c++14 -Wno-deprecated-declarations -O2 -S -masm=intel Examples/_atom_auto_ptr.cpp -o Examples/_atom_auto_ptr.asm

#include <cstdio>
#include <memory>
#include <type_traits>
#include <utility>
#include <vector>

int main() {
    // ①（编译期）语言是否为语义护航——三条断言精确刻画两者差异。
    //    注意首版这里我写错了（以为 auto_ptr 满足 CopyConstructible），被编译器的 static_assert
    //    当场打回：**auto_ptr 的"拷贝构造"签名是 `auto_ptr(auto_ptr&)`——收非 const 左值引用**，
    //    因此按标准它连 CopyConstructible 都不满足（那要求 `T(const T&)`）。
    //    也就是说：它既**不是**一个合格的可拷贝类型（容器要求 CopyConstructible），
    //    又**能**在不带 const 的对象上"拷贝"（语法上看着完全正常）——两个条件叠加才酿成灾难。
    static_assert(!std::is_copy_constructible<std::auto_ptr<int>>::value,
                  "auto_ptr 的拷贝构造收非 const 左值引用 ⇒ 不满足 CopyConstructible");
    static_assert(std::is_constructible<std::auto_ptr<int>, std::auto_ptr<int>&>::value,
                  "但它能从**非 const** 对象'拷贝'——这正是当年的语法陷阱");
    static_assert(!std::is_copy_constructible<std::unique_ptr<int>>::value,
                  "unique_ptr 禁止拷贝");
    static_assert(std::is_move_constructible<std::unique_ptr<int>>::value,
                  "unique_ptr 只能移动");

    // ② 拷贝即转移：拷完之后源被清空
    std::auto_ptr<int> a(new int(42));
    std::auto_ptr<int> b(a);                       // 语法上是"拷贝"，语义上是"偷走"
    std::printf("auto_ptr 拷贝后源为空=%s 目标值=%d\n",
                (a.get() == nullptr) ? "是" : "否", *b);

    // ③ 容器语义冲突：把元素从容器里"读出来"这一步就会把它偷空
    //    （当年 sort/reverse 等算法内部会拷贝元素，于是元素在排序过程中互相偷空。）
    std::vector<std::auto_ptr<int>> v;
    v.push_back(std::auto_ptr<int>(new int(7)));
    std::auto_ptr<int> stolen(v[0]);               // 语法上"读"，实际偷
    std::printf("从容器读元素后源为空=%s 偷到值=%d\n",
                (v[0].get() == nullptr) ? "是" : "否", *stolen);

    // ④ 同一个"把所有权交出去"的需求，unique_ptr 用**移动**表达：源同样变空，
    //    但**必须显式写 std::move** —— 语言把"我在转移所有权"这个意图写进了语法；
    //    auto_ptr 则把同一件事伪装成拷贝（②的写法里没有任何"我在转移"的痕迹）。
    std::unique_ptr<int> u(new int(9));
    std::unique_ptr<int> u2 = std::move(u);
    std::printf("unique_ptr 移动后源为空=%s 目标值=%d\n",
                (u.get() == nullptr) ? "是" : "否", *u2);
    //@ auto_ptr 拷贝后源为空=是 目标值=42
    //@ 从容器读元素后源为空=是 偷到值=7
    //@ unique_ptr 移动后源为空=是 目标值=9
    return 0;
}
