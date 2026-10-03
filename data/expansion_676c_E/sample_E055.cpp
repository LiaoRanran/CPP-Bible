// sample_E055
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E055.json)

#include <atomic>
#include <thread>
#include <cstdio>
struct Gate {
  std::atomic_flag f;                  // 未在构造函数中 ATOMIC_FLAG_INIT
  int payload;
  Gate() : payload(0) {}
};
static Gate g;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void guard(int id){
  wait_go();
  /*DEFECT: atomic_flag 从未 ATOMIC_FLAG_INIT：其状态不确定就进入自旋，行为未定义*/
  while (g.f.test_and_set(std::memory_order_acquire)){}
  g.payload = id;
  g.f.clear(std::memory_order_release);
}
int main(){
  std::thread a(guard, 1), b(guard, 2);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E055 payload=%d\n", g.payload);
  return 0;
}
