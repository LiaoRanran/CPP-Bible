// _ch14_asm.cpp — 调试符号演示（g++ -g -S 取证）
// 编译：g++ -std=c++23 -g -O0 -S _ch14_asm.cpp -o _ch14_asm.asm
int add_debug(int a, int b) {
    int s = a + b;            // 行号会写进 .loc 调试指令
    return s;
}

int main() {
    volatile int r = add_debug(2, 3);
    (void)r;
    return 0;
}
