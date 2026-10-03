// sample_E147
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E147.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex a, b;
static int data[16] = {0};
static std::atomic<int> stage{0};
static void low(){
  std::lock_guard<std::mutex> la(a);
  std::lock_guard<std::mutex> lb(b);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 低优先级线程同时持有两把锁做长耗时变换：
     任何一把被高优先级线程需要时，持锁者都无法被及时抢占让出 */
  for (int round = 0; round < 3000; ++round)
    for (int i = 0; i < 16; ++i) data[i] = data[i] * 3 + round;
  stage.store(2, std::memory_order_release);
}
static void high_a(){
  while (stage.load(std::memory_order_acquire) < 1){}
  std::lock_guard<std::mutex> la(a);
  data[0] += 1;
  stage.store(3, std::memory_order_release);
}
static void high_b(){
  while (stage.load(std::memory_order_acquire) < 1){}
  std::lock_guard<std::mutex> lb(b);
  data[1] += 1;
}
int main(){
  std::thread x(low), y(high_a), z(high_b);
  x.join(); y.join(); z.join();
  std::printf("E147 d0=%d\n", data[0]);
  return 0;
}
