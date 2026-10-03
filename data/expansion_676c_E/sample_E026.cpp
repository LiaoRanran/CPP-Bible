// sample_E026
// defect_type: memory_order
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E026.json)

#include <atomic>
#include <thread>
#include <cstdio>
static std::atomic<int> idx{0};
static int arr[4] = {0, 1, 2, 3};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void bump(){
  wait_go();
  int expected = 0;
  /*DEFECT: CAS 成功序用 relaxed：随后对 arr 的两次写入不在任何 release 语义内，读线程可见性无保证*/
  if (idx.compare_exchange_weak(expected, 1, std::memory_order_relaxed)){
    arr[0] = 100;
    arr[1] = 200;
  }
}
static void peek(){
  wait_go();
  while (idx.load(std::memory_order_acquire) < 1){}
  std::printf("E026 arr0=%d arr1=%d\n", arr[0], arr[1]);
}
int main(){
  std::thread a(bump), b(peek);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
