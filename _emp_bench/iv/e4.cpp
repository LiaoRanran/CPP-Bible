#include <atomic>
#include <cstdint>
std::atomic<std::uint32_t> g_tick{0};
static_assert(std::atomic<std::uint32_t>::is_always_lock_free);
std::uint32_t now(){ return g_tick.load(std::memory_order_acquire); }
int main(){ g_tick.fetch_add(1,std::memory_order_relaxed); return (int)now()-1; }
