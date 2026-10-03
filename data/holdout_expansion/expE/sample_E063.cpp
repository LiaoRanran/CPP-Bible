// sample_E063
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E063.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> state{0};
static std::atomic<int> expected_shadow{0};
static int swaps = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void swap_role(int id){
  wait_go();
  int expected = state.load(std::memory_order_relaxed);
  expected_shadow.store(expected, std::memory_order_relaxed);
  /*DEFECT: expected 是被其它线程间接影响的共享计算结果：CAS 的比较基准在「读」与「比较」之间不是稳定快照，
     角色交换的互斥语义不成立 */
  if (state.compare_exchange_strong(expected, id, std::memory_order_acq_rel))
    swaps++;
}
int main(){
  std::thread a(swap_role, 1), b(swap_role, 2);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E063 swaps=%d state=%d\n", swaps, state.load());
  return 0;
}
