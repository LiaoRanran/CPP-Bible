// C++23 <mdspan> — 本 MinGW 构建【头缺失·编译失败】的证据文件 (GCC 15.3.0, -std=c++26 -O2)
// 现象：libstdc++ 未提供 <mdspan> 头，编译报
//   fatal error: mdspan: No such file or directory
// 该书 Book/part01_history/ch08_cpp23.md 附录 G 据此说明：std::mdspan 在 GCC15.3 该 MinGW 构建下
// 不可用（__cpp_lib_mdspan 宏 <undef> 同源），多维偏移计算可用手写下标等价表达（见 ch82_span）。
#include <mdspan>
#include <cstdio>

int main() {
    int data[6]{};
    std::mdspan<int, std::extents<unsigned, 2, 3>> a(data);
    a[1, 2] = 5;                 // 期望写入 data[1*3+2] = data[5]
    std::printf("%d\n", a[1, 2]);
    return 0;
}
