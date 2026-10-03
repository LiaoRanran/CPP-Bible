// sample_E194
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E194.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool quit_req = false;          // 谓词：无锁读写
static std::atomic<int> loops{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: 谓词 quit_req 由 notifier 无锁写，这里在锁内读：
             两者构成数据竞争（编译器可把读提升到循环外 ⇒ 永久阻塞或虚假通过） */
  while (!quit_req) cv.wait(lk);
  loops.fetch_add(1, std::memory_order_release);
}
static void notifier(){
  for (int i = 0; i < 100000; ++i) loops.fetch_add(1, std::memory_order_relaxed);
  /*DEFECT: 谓词完全不加锁修改 */
  quit_req = true;
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(notifier);
  a.join(); b.join();
  std::printf("E194 loops=%d\n", loops.load());
  return 0;
}
