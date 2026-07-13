// 工业案例 C1：批量报文长度缓冲（复用容量，避免反复扩容）
#include <vector>
#include <iostream>

class PktLenBuffer {
    std::vector<unsigned short> lens;
public:
    PktLenBuffer() { lens.reserve(4096); }   // 预分配峰值容量
    void on_batch(const unsigned short* ps, size_t n) {
        lens.clear();                          // 清空但保留容量（不释放）
        lens.insert(lens.end(), ps, ps + n);  // 批量尾插
    }
    size_t total() const {
        size_t s = 0; for (auto x : lens) s += x; return s;
    }
    size_t capacity_kept() const { return lens.capacity(); }  // 始终 ~4096
};
int main() {
    PktLenBuffer b;
    unsigned short batch[] = {64, 128, 256, 512};
    b.on_batch(batch, 4);
    std::cout << "total=" << b.total() << " cap=" << b.capacity_kept() << "\n"; // 960 4096
    return 0;
}