// sample_E196
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E196.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool state_changed = false;
static int version = 0;                // 非原子版本号
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: wait 内部谓词正确，但醒来后解锁再读 version */
  if (!cv.wait_for(lk, std::chrono::milliseconds(50), []{ return state_changed; })){}
  lk.unlock();
  /*DEFECT: 无锁读非原子 version，而 updater 仍在锁内持续 ++version ⇒ 数据竞争 */
  long s = 0;
  for (int i = 0; i < 400000; ++i) s += version;
  std::printf("E196 sum=%ld\n", s);
}
static void updater(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  for (int i = 0; i < 400000; ++i){
    {
      std::lock_guard<std::mutex> lk(m);
      ++version;                          // 写始终在锁内
      state_changed = true;
    }
    cv.notify_all();
  }
}
int main(){
  std::thread a(waiter), b(updater);
  waiting.store(1, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
