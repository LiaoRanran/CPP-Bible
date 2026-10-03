// sample_E053
// defect_type: atomic_ub
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E053.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<bool> shutdown_req{false};
static int shutdowns = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void requester(){
  wait_go();
  /*DEFECT: exchange 的旧值（是否已有请求在途）被丢弃：并发两个请求者时后到者无法察觉信号已被消费*/
  shutdown_req.exchange(true, std::memory_order_acq_rel);
  shutdowns = shutdowns + 1;
}
int main(){
  std::thread a(requester), b(requester);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  std::printf("E053 req=%d count=%d\n", (int)shutdown_req.load(), shutdowns);
  return 0;
}
