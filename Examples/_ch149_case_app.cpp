// 见 Examples/_ch149_case_app.cpp
// ⑰ GitHub Actions 真实案例中的被构建程序
#include <cstdio>
int main(int argc, char** argv) {
    std::printf("args=%d first=%s\n", argc, argc > 1 ? argv[1] : "(none)");
    return 0;
}
