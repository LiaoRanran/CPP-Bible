// Examples/_ch136_singleton_o0.cpp
// 用 -O0 + nm 观察 C++ 名字改编（mangled name），证明 instance() 在目标文件中的符号。
struct Logger {
    static Logger& instance();
    int x = 0;
};
Logger& Logger::instance() {
    static Logger inst;
    return inst;
}
int use() { return Logger::instance().x; }
