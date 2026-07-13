#include <cstddef>
#include <cstdlib>

struct MallocAlloc {
    static void* alloc(std::size_t n) { return std::malloc(n); }
    static void  dealloc(void* p) { std::free(p); }
};
struct NewAlloc {
    static void* alloc(std::size_t n) { return ::operator new(n); }
    static void  dealloc(void* p) { ::operator delete(p); }
};

template <typename T, typename AllocPolicy>
class PodVector {
    T* data = nullptr; std::size_t n = 0;
public:
    void push_back(const T& v) {
        data = static_cast<T*>(AllocPolicy::alloc((n + 1) * sizeof(T)));
        data[n++] = v;
    }
    std::size_t size() const { return n; }
    ~PodVector() { if (data) AllocPolicy::dealloc(data); }
};

int main() {
    PodVector<int, MallocAlloc> a;
    PodVector<int, NewAlloc> b;
    a.push_back(1); b.push_back(2);
    return (int)a.size() + (int)b.size();
}
