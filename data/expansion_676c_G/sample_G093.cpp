// sample_G093
// defect_type: heap_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: leethomason/tinyxml2#1065 (https://github.com/leethomason/tinyxml2/issues/1065) [tinyxml2]
// (authoritative annotation in sample_G093.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// tinyxml2#1065: DynArray::EnsureCapacity 整数溢出 → 小分配大拷贝
template <typename T, int INITIAL_SIZE = 16>
class DynArray {
    T*     _mem;
    int    _size;
    int    _allocated;

public:
    DynArray() : _mem(new T[INITIAL_SIZE]), _size(0), _allocated(INITIAL_SIZE) {}
    ~DynArray() { delete[] _mem; }

    /* DEFECT */ // 镜像 issue 引用的 EnsureCapacity: cap*2 无运行时保护(release 无 TIXMLASSERT)
    void EnsureCapacity(size_t cap) {
        if (cap <= (size_t)_allocated) return;
        const size_t newAllocated = cap * 2;                 // 溢出 → 极小值
        T* newMem = new T[newAllocated > 0 ? newAllocated : 1];
        std::memcpy(newMem, _mem, sizeof(T) * (size_t)_size);   // 大 memcpy → 堆越界写
        delete[] _mem;
        _mem = newMem;
        _allocated = (int)newAllocated;
    }

    void Push(const T& v) {
        EnsureCapacity((size_t)_size + 1);   // 常规增长
        _mem[_size++] = v;
    }
};

int main() {
    DynArray<int> arr;
    for (int i = 0; i < 16; ++i) arr.Push(i);      // 填满 16 个元素(_size=16)
    // crafted XML 触发的巨大 cap: 2^63 → cap*2 回绕为 0 → 分配 1 元素
    arr.EnsureCapacity(0x8000000000000000ull);
    std::printf("capacity grown\n");
    return 0;
}
