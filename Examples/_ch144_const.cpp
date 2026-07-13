// ch144 ⑥ const 正确性：const 成员函数可作用于 const 对象，且支持重载
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch144_const.cpp -o _ch144_const_O2.asm
#include <string>

class Account {
    long balance_ = 0;
public:
    void deposit(long n) { balance_ += n; }     // 修改对象：非 const
    long balance() const { return balance_; }   // ✅ const 成员，可读不可写
    long&       balance_ref()       { return balance_; }       // 非 const 版
    const long& balance_ref() const { return balance_; }       // ✅ const 重载
};
