// sample_E191
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E191.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv_a, cv_b;
static bool slot_free = false;
static std::atomic<int> woke_a{0}, woke_b{0};
static void consumer_a(){
  std::unique_lock<std::mutex> lk(m);
  while (!slot_free) cv_a.wait(lk);
  woke_a.store(1, std::memory_order_release);
}
static void consumer_b(){
  /*DEFECT: 两个条件变量共用同一个谓词 slot_free，但生产者只通知 cv_a，
             于是 cv_b 上的等待者永远收不到通知 ⇒ 永久阻塞（时序相关） */
  std::unique_lock<std::mutex> lk(m);
  while (!slot_free) cv_b.wait(lk);
  woke_b.store(1, std::memory_order_release);
}
static void producer(){
  std::this_thread::sleep_for(std::chrono::milliseconds(3));
  {
    std::lock_guard<std::mutex> lk(m);
    slot_free = true;
  }
  cv_a.notify_all();                   // DEFECT: 忘了通知 cv_b
}
int main(){
  std::thread a(consumer_a), b(consumer_b), c(producer);
  a.join(); b.join(); c.join();
  std::printf("E191 woke_a=%d woke_b=%d\n", woke_a.load(), woke_b.load());
  return 0;
}
