// 文件：Examples/_ch156_main.cpp
// 行号：2
// 构建A（无 LTO）：g++ -O2 -c ... 然后链接 → objdump -d -M intel
// 构建B（有 LTO）：g++ -O2 -flto -c ... 然后 -flto 链接 → objdump -d -M intel
extern int compute(int);
int main(int argc, char**) { return compute(argc); }