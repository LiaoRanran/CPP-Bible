// sample_E168
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E168.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static int page[4096];
static std::atomic<int> stage{0};
static void touch_pages(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁逐页「换入」：真实系统里这是不可中断的缺页处理，
     持锁页错误会让锁被占用毫秒级 ⇒ 实时线程必然错过截止期 */
  for (int p = 0; p < 4096; p += 64){
    page[p] = p;
    if (p % 512 == 0) std::this_thread::sleep_for(std::chrono::microseconds(200));
  }
  stage.store(2, std::memory_order_release);
}
static void rt_read(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 实时读线程等锁 */
  std::lock_guard<std::mutex> lk(m);
  int s = 0;
  for (int p = 0; p < 4096; p += 512) s += page[p];
  std::printf("E168 s=%d\n", s);
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(touch_pages), b(rt_read);
  a.join(); b.join();
  return 0;
}
