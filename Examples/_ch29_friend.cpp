// ch29 真机实证：friend 的标准演化 / 不继承不传递 / 类内 friend 的 ADL 陷阱
// g++ -std=c++23 -O2 -Wall -Wextra _ch29_friend.cpp -o _ch29_friend.exe

#include <cstdio>

// ── ⑭ C++11 起：模板参数可作友元（[temp.param]）——真机验证 ──────────────
template <typename T>
struct Passkey {
    friend T;                                   // C++11 新语法：friend T;
    static int token;
};
template <typename T> int Passkey<T>::token = 7;
struct Client { void use() { std::printf("[evolve] token=%d（Client 是友元，可读私有）\n", Passkey<Client>::token); } };

// ── ⑮ friend 不继承、不传递——真机验证 ───────────────────────────────────
struct Base {
    friend void touch_base(Base&);
private:
    int secret = 42;
};
struct Derived : Base {
private:
    int extra = 7;          // 派生类新增私有：Base 的友元不可见（friend 不继承）
};
void touch_base(Base& b) { b.secret = 43; }

// ── ⑯ 类内定义 friend ≠ 成员函数：只能经 ADL 找到——真机验证 ─────────────
struct X {
    friend void poke(X&) { std::printf("[adl] poke via ADL\n"); }  // 隐式 inline
private:
    int v = 1;
};

int main() {
    // ⑭
    Client c;
    c.use();
    // ⑮ 友元只授权给 Base：可经派生对象访问 Base 子对象私有，
    //   但访问 Derived::extra 是编译错误（取消注释即验证）：
    //   void bad(Base& b) { b.extra = 1; }   // ✗ error: 'int Derived::extra' is private
    Derived d;
    touch_base(d);
    std::printf("[inherit] touch_base 经 Base 子对象改写成功（Derived::extra 仍不可见）\n");
    // ⑯ 全局限定调用会失败（取消注释即验证）：
    //   ::poke(x);   // ✗ error: 'poke' not declared —— friend 不是成员、不注入全局作用域
    X x;
    poke(x);        // OK：ADL——实参类型 X 参与查找
    return 0;
}
