#include <atomic>
#include <cstdint>
std::atomic<__int128> g{0};
// 双字 CAS 经由 GCC __atomic 内建；声明为 volatile 防止被完全优化掉
extern "C" int dcas_probe(__int128 expected, __int128 desired) {
    return __atomic_compare_exchange(&g, &expected, &desired, 0,
        __ATOMIC_ACQ_REL, __ATOMIC_ACQUIRE);
}
