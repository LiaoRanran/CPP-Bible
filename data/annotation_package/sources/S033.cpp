// sample_E154
// [redacted]
// severity: high
// [redacted]
// expected_verdict: miss
// [redacted]
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E154.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex rpc_lock;
static int rpc_result = 0;
static std::atomic<int> stage{0};
static void do_rpc(){
  std::lock_guard<std::mutex> lk(rpc_lock);
  stage.store(1, std::memory_order_release);
  /* [redacted]*/
  std::this_thread::sleep_for(std::chrono::milliseconds(180));
  rpc_result = 1;
  stage.store(2, std::memory_order_release);
}
static void urgent_rpc(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /* [redacted]*/
  std::lock_guard<std::mutex> lk(rpc_lock);
  rpc_result = 2;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(do_rpc), b(urgent_rpc);
  a.join(); b.join();
  std::printf("E154 rpc=%d\n", rpc_result);
  return 0;
}
