// C++23 <print> — 编译期支持但本 MinGW 构建【链接失败】的证据文件 (GCC 15.3.0, -std=c++26 -O2)
// 现象：<print> 头存在、语法支持，但 libstdc++ 未导出 __open_terminal / __write_to_terminal，链接报
//   undefined reference to `std::__open_terminal(_iobuf*)'
//   undefined reference to `std::__write_to_terminal(void*, std::span<char, ...>)'
// 该书 Book/part01_history/ch08_cpp23.md 附录 G 据此说明：std::print 在 GCC15.3 该 MinGW 构建下
// 不可用，改用 std::format（已验证可编译+链接）等价展示。
#include <print>

int main() {
    std::print("result = {}\n", 42);
    return 0;
}
