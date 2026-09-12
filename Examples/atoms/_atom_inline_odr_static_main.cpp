// ATOM-LANG-INLINE-001 机制判别对照夹具 · main（同实验组：可选 argv[1] 作输出前缀）
#include <cstdio>

int sa_value();
int sb_value();

int main(int argc, char** argv) {
    const char* p = (argc > 1) ? argv[1] : "";
    std::printf("%ssa=%d\n", p, sa_value());
    std::printf("%ssb=%d\n", p, sb_value());
    return 0;
}
