// ch28 真实汇编证据源：返回局部地址 -> 悬垂（GCC 15.3.0 -O2 -masm=intel）
// 完整产物见 Examples/_ch28_dangling_ref.asm
// 注：引用版 int& bad(){ int x; return x; } 在 GCC 15 已升级为硬错误；
//     指针版语义等价——都返回"即将随栈帧回退而消失"的地址。
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch28_dangling_ref.cpp -o _ch28_dangling_ref.asm
int* bad_ptr()  __attribute__((used));   // 返回局部地址 -> 悬垂（UB）
int* good_ptr() __attribute__((used));   // 返回静态地址 -> 安全

int* bad_ptr() {
    int x = 5;
    return &x;   // 警告（-Wreturn-local-addr）：返回局部变量 x 的地址 -> 悬垂
}

int* good_ptr() {
    static int x = 5;
    return &x;   // 静态存储期，地址稳定 -> 安全
}
