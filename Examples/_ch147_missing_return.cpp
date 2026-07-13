// _ch147_missing_return.cpp —— 缺少返回值
// 取证命令:
//   g++ -std=c++23 -Wall -Wextra _ch147_missing_return.cpp -o /tmp/t
int g(bool b) {
    if (b) return 1;
    // 控制流可能到达函数末尾而未返回值 -> -Wreturn-type
}

int main() {
    return g(true);
}
