// ch144 ④ 同一头文件包含两次，守卫确保 Widget 只定义一次
// 预处理展开：g++ -std=c++23 -E _ch144_guard_main.cpp -o _ch144_guard.i
#include "_ch144_guard.h"
#include "_ch144_guard.h"   // ✅ 第二次包含被 #ifndef 挡掉

int main() {
    Widget w{42, 7};
    return w.id + w.value;
}
