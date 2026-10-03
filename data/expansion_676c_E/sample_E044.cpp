// sample_E044
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E044.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> owner{-1};
static int resource = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void claim(int id){
  wait_go();
  int expected = -1;
  if (owner.compare_exchange_weak(expected, id, std::memory_order_acq_rel)){
    resource = id;                     // 正常路径
    return;
  }
  /*DEFECT: CAS 失败后 expected 已被写成当前值，但这里仍把它当成「我拿到的资源编号」使用（未重新检查成功标志）*/
  resource = expected + 1000;
  std::printf("E044 loser saw=%d\n", expected);
}
int main(){
  std::thread a(claim, 1), b(claim, 2);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E044 resource=%d\n", resource);
  return 0;
}
