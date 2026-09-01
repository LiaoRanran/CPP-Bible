// a1_add.cpp — A1 导论示例：一个最简单的加法函数，用于观察编译器生成的汇编
// 编译: g++ -std=c++23 -O2 -c -o a1_add.o a1_add.cpp
// 反汇编: objdump -d -M intel a1_add.o
int add(int a, int b) {
    return a + b;
}

int main() {
    volatile int x = add(2, 3);
    return x;
}
