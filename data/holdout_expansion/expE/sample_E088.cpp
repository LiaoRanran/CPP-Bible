// sample_E088
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E088.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m, space_lock;
static std::condition_variable cv;
static int free_slots = 0;
static std::atomic<bool> go{false}, producer_ready{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void producer(){
  wait_go();
  std::unique_lock<std::mutex> lk(m);
  std::lock_guard<std::mutex> keep(space_lock);   // 关键：第二把锁，wait 不会释放它
  producer_ready.store(true, std::memory_order_release);
  /*DEFECT: 持 space_lock 等「有空位」，而空位只能由拿到 space_lock 的 consumer 释放
     ⇒ cv.wait 只释放 m，space_lock 仍在手上 ⇒ 死锁 */
  cv.wait(lk, []{ return free_slots > 0; });
  --free_slots;
  std::printf("E088 produced\n");
}
static void consumer(){
  wait_go();
  while(!producer_ready.load(std::memory_order_acquire)){}   // 确保 producer 已持住 space_lock
  /*DEFECT: consumer 必须拿到 space_lock 才能腾出空位，而 space_lock 被 producer 永久持有 */
  std::lock_guard<std::mutex> s(space_lock);
  free_slots += 2;
  cv.notify_all();
}
int main(){
  std::thread a(producer), b(consumer);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
