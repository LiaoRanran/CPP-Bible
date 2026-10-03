// sample_E160
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E160.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex stat_lock;
static long stat[8] = {0};
static std::atomic<int> stage{0};
static void sampler(){
  std::lock_guard<std::mutex> lk(stat_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做长时间采样聚合 */
  for (int k = 0; k < 300000; ++k)
    for (int i = 0; i < 8; ++i) stat[i] += (k + i) & 7;
  stage.store(2, std::memory_order_release);
}
static void fast_path(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 快路径（高优先级）直接写统计数组，不取锁：与持锁的采样线程并发访问同一内存 ⇒ 数据竞争 */
  for (int k = 0; k < 300000; ++k) stat[3] += k & 1;
  while (stage.load(std::memory_order_acquire) < 2){}
}
static void reader(){
  while (stage.load(std::memory_order_acquire) < 1){}
  std::lock_guard<std::mutex> lk(stat_lock);
  std::printf("E160 stat3=%ld\n", stat[3]);
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(sampler), b(fast_path), c(reader);
  a.join(); b.join(); c.join();
  return 0;
}
