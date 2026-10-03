// sample_E148
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E148.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <string>
#include <cstdio>
static std::mutex m;
static std::string blob;
static std::atomic<int> stage{0};
static void low(){
  std::lock_guard<std::mutex> lk(m);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做大量字符串构造/拼接（持锁耗时操作） */
  for (int i = 0; i < 20000; ++i) blob += "x";
  stage.store(2, std::memory_order_release);
}
static void high(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 高优先级线程等锁读取 blob */
  std::lock_guard<std::mutex> lk(m);
  std::printf("E148 len=%zu\n", blob.size());
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(low), b(high);
  a.join(); b.join();
  return 0;
}
