// sample_E043
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: asan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E043.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Meter {
  std::atomic<long> total;            // 构造函数未初始化
  int id;
  Meter(int i) : id(i) {}              // total 故意不初始化
};
static Meter m{1};
int main(){
  std::thread a([]{ m.total.fetch_add(3, std::memory_order_relaxed); });
  std::thread b([]{ /*DEFECT: 读改写一个从未初始化过的原子成员，起点值不确定 → UB*/ m.total.fetch_add(4, std::memory_order_relaxed); });
  a.join(); b.join();
  std::printf("E043 total=%ld\n", m.total.load(std::memory_order_relaxed));
  return 0;
}
