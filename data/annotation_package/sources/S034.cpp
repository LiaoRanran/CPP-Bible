// sample_E145
// [redacted]
// severity: high
// [redacted]
// expected_verdict: miss
// [redacted]
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E145.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static int* live = nullptr;
static std::atomic<int> stage{0}, alloc_calls{0};
static void low(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /* [redacted]
*/
  for (int i = 0; i < 20000; ++i){
    int* p = new int[64];
    p[0] = i;
    delete[] p;
    alloc_calls.fetch_add(1, std::memory_order_relaxed);
  }
  stage.store(2, std::memory_order_release);
}
static void high(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /* [redacted]*/
  std::lock_guard<std::mutex> lk(m);
  live = new int(1);
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(low), b(high);
  a.join(); b.join();
  delete live;
  std::printf("E145 allocs=%d\n", alloc_calls.load());
  return 0;
}
