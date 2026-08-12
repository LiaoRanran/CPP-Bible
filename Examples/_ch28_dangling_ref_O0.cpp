// ch28 真实汇编证据源（-O0 对照）：返回局部地址 -> 悬垂（GCC 15.3.0 -masm=intel）
// 完整产物见 Examples/_ch28_dangling_ref_O0.asm
// 对照 -O2 版（Examples/_ch28_dangling_ref.asm）：-O2 把 UB 武器化为返回 0（nullptr），
// 而 -O0 朴素地返回即将失效的栈地址 [rsp+N]，更易看清"悬垂"本质。
// 编译：g++ -std=c++23 -O0 -S -masm=intel _ch28_dangling_ref_O0.cpp -o _ch28_dangling_ref_O0.asm
int* bad_ptr()  __attribute__((used));
int* good_ptr() __attribute__((used));

int* bad_ptr() {
    int x = 5;
    return &x;   // -O0：朴素返回 &x（栈地址，悬垂）；-O2：被优化为 0
}

int* good_ptr() {
    static int x = 5;
    return &x;   // 静态存储期，地址稳定
}
