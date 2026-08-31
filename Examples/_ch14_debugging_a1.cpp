// 文件：Examples/_ch14_asm.cpp
// 行号：4
// ⑫ 调试符号演示：g++ -g -O0 -S 会在汇编里写入 .loc 行号指令
int add_debug(int a, int b) {
    int s = a + b;            // 行4：这一行对应汇编 .loc 1 4 9
    return s;
}

int main() {
    volatile int r = add_debug(2, 3);
    (void)r;
    return 0;
}