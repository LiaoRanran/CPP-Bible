// sample_E057
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E057.json)

#include <atomic>
#include <thread>
#include <cstdio>
static int plain = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void bump_via_fake_atomic(){
  wait_go();
  /*DEFECT: 把普通 int 的地址强转成 std::atomic<int>* 并当原子变量自增：
     实际是对非原子对象做「假装原子」的 RMW，两线程间是真实数据竞争 + 违反对象类型规则（UB）*/
  std::atomic<int>* fake = reinterpret_cast<std::atomic<int>*>(&plain);
  fake->fetch_add(1, std::memory_order_relaxed);
}
int main(){
  std::thread a(bump_via_fake_atomic), b(bump_via_fake_atomic);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E057 plain=%d\n", plain);
  return 0;
}
