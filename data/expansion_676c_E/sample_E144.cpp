// sample_E144
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E144.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <vector>
#include <algorithm>
#include <cstdio>
static std::mutex m;
static std::vector<int> data{5, 3, 9, 1, 7, 2};
static std::atomic<int> stage{0};
static void low_rt(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 低优先级线程持锁做 O(n log n) 排序 + 反复重排：锁被长时间占用 */
  for (int round = 0; round < 2000; ++round){
    std::sort(data.begin(), data.end());
    if (data[0] == 999) break;
  }
  stage.store(2, std::memory_order_release);
}
static void high_rt(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程必须等锁；无 PI（优先级继承）机制 */
  std::lock_guard<std::mutex> lk(m);
  data.push_back(42);
  stage.store(3, std::memory_order_release);
}
static void mid_rt(){
  while (stage.load(std::memory_order_acquire) < 1){}
  while (stage.load(std::memory_order_acquire) < 2) std::this_thread::yield();
}
int main(){
  std::thread a(low_rt), b(high_rt), c(mid_rt);
  a.join(); b.join(); c.join();
  std::printf("E144 n=%zu\n", data.size());
  return 0;
}
