#include <iostream>
#include <new>
#include <cassert>
#include <cstdlib>
#include <cstdint>

// 计数器必须是 volatile：这样 operator new 内部就有"可观测副作用"，
// 否则 -O2 会把成对的 new/delete 整体消除，计数结果全为 0。
static volatile long long g_alloc = 0;
static volatile long long g_align_alloc = 0;

// 对齐分配的可移植包装：Windows（MSVC/MinGW）提供 _aligned_malloc/_aligned_free，
// POSIX（glibc）提供手动对齐分配（std::malloc + 指针运算，无 C11/POSIX 特性宏依赖）。
#if defined(_WIN32)
  #include <malloc.h>
  static void* aligned_alloc_impl(std::size_t align, std::size_t size) {
      return _aligned_malloc(size, static_cast<std::size_t>(align));
  }
  static void aligned_free_impl(void* p) { _aligned_free(p); }
#else
  static void* aligned_alloc_impl(std::size_t align, std::size_t size) {
      if (align < sizeof(void*)) align = sizeof(void*);
      void* raw = std::malloc(size + align - 1 + sizeof(void*));
      if (!raw) return nullptr;
      std::uintptr_t base = reinterpret_cast<std::uintptr_t>(raw) + sizeof(void*);
      std::uintptr_t aligned = (base + align - 1) & ~(std::uintptr_t)(align - 1);
      *reinterpret_cast<void**>(aligned - sizeof(void*)) = raw;
      return reinterpret_cast<void*>(aligned);
  }
  static void aligned_free_impl(void* p) {
      if (p) std::free(*reinterpret_cast<void**>(
          reinterpret_cast<std::uintptr_t>(p) - sizeof(void*)));
  }
#endif

void* operator new(std::size_t n) {
    g_alloc = g_alloc + 1;
    void* p = std::malloc(n ? n : 1);
    if (!p) throw std::bad_alloc();
    return p;
}
void* operator new[](std::size_t n) {
    g_alloc = g_alloc + 1;
    void* p = std::malloc(n ? n : 1);
    if (!p) throw std::bad_alloc();
    return p;
}
void* operator new(std::size_t n, std::align_val_t a) {
    g_align_alloc = g_align_alloc + 1;
    void* p = aligned_alloc_impl(static_cast<std::size_t>(a), n ? n : 1);
    if (!p) throw std::bad_alloc();
    return p;
}
void operator delete(void* p) noexcept { std::free(p); }
void operator delete[](void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
void operator delete[](void* p, std::size_t) noexcept { std::free(p); }
void operator delete(void* p, std::align_val_t) noexcept { aligned_free_impl(p); }
void operator delete(void* p, std::size_t, std::align_val_t) noexcept { aligned_free_impl(p); }

struct Node { long long v[4]; };
struct alignas(64) Node64 { long long v[4]; };

int main() {
    constexpr int K = 64;

    // 1) 逐对象 new：K 次 operator new
    long long a0 = g_alloc;
    Node* ps[K];
    for (int i = 0; i < K; ++i) ps[i] = new Node;
    long long single_calls = g_alloc - a0;
    for (int i = 0; i < K; ++i) delete ps[i];

    // 2) 批量 new[]：整段只有 1 次 operator new[]
    long long a1 = g_alloc;
    Node* arr = new Node[K];
    long long bulk_calls = g_alloc - a1;
    arr[0].v[0] = 7;
    delete[] arr;

    // 3) placement new：零次堆分配，只在既有缓冲区上构造
    alignas(Node) unsigned char buf[sizeof(Node)];
    long long a2 = g_alloc;
    Node* pp = ::new (static_cast<void*>(buf)) Node;
    long long place_calls = g_alloc - a2;
    pp->v[0] = 42;
    pp->~Node();

    // 4) nothrow new：失败返回空指针而非抛异常
    Node* pn = new (std::nothrow) Node;

    // 5) 对齐 new：过对齐类型走 operator new(size_t, align_val_t)
    long long b0 = g_align_alloc;
    Node64* p64 = new Node64;
    long long align_calls = g_align_alloc - b0;
    std::uintptr_t addr = reinterpret_cast<std::uintptr_t>(p64);

    std::cout << "single new  calls (K=64) : " << single_calls << std::endl;
    std::cout << "bulk new[]  calls        : " << bulk_calls << std::endl;
    std::cout << "placement   calls        : " << place_calls << std::endl;
    std::cout << "aligned-new calls        : " << align_calls << std::endl;
    std::cout << "nothrow new non-null?    : " << (pn != nullptr ? "yes" : "no") << std::endl;
    std::cout << "Node64 addr % 64         : " << (addr % 64) << std::endl;

    // 功能正确性断言（不断言时间 / 倍数 / 精确 sizeof）
    assert(single_calls == K);          // 逐对象分配 = K 次
    assert(bulk_calls == 1);            // 批量分配 = 1 次
    assert(bulk_calls < single_calls);  // 稳定语义：批量分配次数更少
    assert(place_calls == 0);           // placement new 不碰堆
    assert(align_calls == 1);           // 过对齐类型走对齐重载
    assert(addr % 64 == 0);             // 对齐承诺必须兑现
    assert(pn != nullptr);

    delete pn;
    delete p64;
    std::cout << "all assertions passed" << std::endl;
    return 0;
}