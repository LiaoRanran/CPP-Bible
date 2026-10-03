// sample_E156
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E156.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;                  // 无 PI：等待者优先级不会被继承给持锁者
static int sample = 0;
static std::atomic<int> stage{0};
static void rt_consumer(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 实时（高优先级）消费者等一把普通 mutex：
     持锁者若被中优先级线程压制，实时线程的截止期必然被错过 */
  std::lock_guard<std::mutex> lk(m);
  sample = sample + 1;
  stage.store(3, std::memory_order_release);
}
static void normal_producer(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 普通（非实时）线程持锁做长耗时处理 */
  for (long i = 0; i < 4000000; ++i) sample += (int)(i & 3);
  stage.store(2, std::memory_order_release);
}
int main(){
  std::thread a(rt_consumer), b(normal_producer);
  a.join(); b.join();
  std::printf("E156 sample=%d\n", sample);
  return 0;
}
