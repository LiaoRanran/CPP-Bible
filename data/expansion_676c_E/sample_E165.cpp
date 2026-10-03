// sample_E165
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E165.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex l1, l2;
static int data[32] = {0};
static std::atomic<int> stage{0};
static void low2(){
  std::lock_guard<std::mutex> a(l1);
  std::lock_guard<std::mutex> b(l2);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 低优先级线程持双锁做长耗时处理 */
  for (int k = 0; k < 200000; ++k)
    for (int i = 0; i < 32; ++i) data[i] ^= k;
  stage.store(2, std::memory_order_release);
}
static void high1(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程按 l2->l1 顺序取锁，与低优先级相反 */
  std::lock_guard<std::mutex> b(l2);
  std::lock_guard<std::mutex> a(l1);
  data[0] = 1;
  stage.store(3, std::memory_order_release);
}
static void mid2(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 中优先级线程抢占低优先级持锁者，放大反转 */
  while (stage.load(std::memory_order_acquire) < 2) std::this_thread::yield();
}
int main(){
  std::thread x(low2), y(high1), z(mid2);
  x.join(); y.join(); z.join();
  std::printf("E165 d0=%d\n", data[0]);
  return 0;
}
