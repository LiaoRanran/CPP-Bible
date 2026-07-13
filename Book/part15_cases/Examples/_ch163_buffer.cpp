// _ch163_buffer.cpp  [跨平台, 纯 C++23, 无套接字依赖]
// 编译: g++ -std=c++23 -O2 _ch163_buffer.cpp -o _ch163_buffer.exe
// 作用: 单生产者/单消费者环形缓冲区——网络读写的"应用层缓冲"核心结构（⑩）。
#include <iostream>
#include <cstddef>

template <size_t N>
struct RingBuffer {
    char buf[N];
    size_t head = 0, tail = 0;
    size_t available() const { return (tail + N - head) % N; }
    size_t free_space() const { return N - 1 - available(); }
    void push(char c) { buf[tail] = c; tail = (tail + 1) % N; }
    char pop() { char c = buf[head]; head = (head + 1) % N; return c; }
};

int main() {
    RingBuffer<8> rb;
    for (char c : {'a', 'b', 'c'}) rb.push(c);
    std::cout << "[buffer] 可读字节=" << rb.available() << "\n";
    while (rb.available()) std::cout << "[buffer] pop=" << rb.pop() << "\n";
    return 0;
}
