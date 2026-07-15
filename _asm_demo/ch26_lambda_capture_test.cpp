// ASM-26-lambda-capture : GCC 15.3.0 真机实证 —— lambda 捕获形式的指令代价与闭包对象布局
// 编译: g++ -std=c++26 -O2 ch26_lambda_capture_test.cpp -o ch26_lambda_capture_test.exe
// 反汇编: objdump.exe -d -M intel -C ch26_lambda_capture_test.exe
//
// 设计要点：用不透明指针 int* p (来自 [[gnu::noinline]] get_field()) 让被捕获的"指针值"在编译期未知，
// 从而逼出"按引用捕获"真实存在的二次解引用（先取闭包内指针、再取 int）；
// 与"按值捕获值"的单一加载形成对照。若 p 指向局部且值可证明不变，GCC 会把引用捕获也折叠为直接加载
// （即"按引用捕获在目标可证明不变时零开销"），本实验专门取"目标未知"的嵌入式典型场景。
#include <cstdio>

[[gnu::noinline]] int* get_field();          // 不透明：返回的 int* 对优化器未知
[[gnu::noinline]] void bump(int*);            // 不透明：经指针修改，强制闭包实时重读
[[gnu::noinline]] int sink(int v) { return v; }   // 强制闭包调用结果实体化

int main() {
    int* p = get_field();                     // p 的值编译期未知
    int& r = *p;                              // r 引用不透明位置

    auto f0 = []{ return 42; };               // 无捕获
    auto f1 = [val = *p]{ return val; };      // 按值捕获"值"(4B 闭包, 快照于捕获时刻)
    bump(p);                                  // 不透明别名写：*p 改变，f1 快照不受影响
    auto f2 = [&r]{ return r; };              // 按引用捕获(8B 闭包, 存 int* = p)

    int y = 0;
    y += sink(f0());   // 42 常量折叠
    y += sink(f1());   // 快照值(捕获时刻的 *p)：1 次加载
    y += sink(f2());   // 实时值(经未知指针, *p 已被 bump 改写)：2 次加载

    // 闭包对象真实布局(sizeof 编译期常量，运行期打印核对)
    std::printf("%d %zu %zu %zu\n",
                y, sizeof(f0), sizeof(f1), sizeof(f2));
    return 0;
}

// get_field 定义(不透明，noinline 使 main 侧无法看穿返回的地址)
[[gnu::noinline]] int* get_field() { static int g = 7; return &g; }
// bump 定义(不透明，使 main 侧无法证明 *p 在 f2 调用前未变)
[[gnu::noinline]] void bump(int* q) { *q += 100; }
