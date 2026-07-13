// _ch145_noexcept2.cpp —— noexcept 的终止语义（g++ -O2 -S 取证）
// 含 throw 的 noexcept 函数：编译器把 throw 替换为直接调用 std::terminate
void sink() noexcept { throw 1; }

// 普通（可能抛）函数：保留真正的异常抛出与展开路径
void boom() { throw 2; }

int main() { sink(); return 0; }
