// sample_E188
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E188.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m1, m2;              // 两把锁
static std::condition_variable cv;
static bool flag = false;              // 谓词：约定由 m1 保护
static std::atomic<int> waiting{0};
static void waiter(){
  /*DEFECT: cv.wait 必须配「保护谓词的那把锁」。这里用 m2 去 wait，
             而 flag 的读写都在 m1 下 ⇒ 谓词读与写不同步（数据竞争 + 丢失唤醒） */
  std::unique_lock<std::mutex> lk2(m2);
  waiting.store(1, std::memory_order_release);
  while (!flag) cv.wait(lk2);
  std::printf("E188 flag=%d\n", (int)flag);
}
static void setter(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  {
    std::lock_guard<std::mutex> lk1(m1);
    flag = true;
  }
  cv.notify_all();                     // 通知发了，但等待者在 m2 上，谓词不同步
}
int main(){
  std::thread a(waiter), b(setter);
  a.join(); b.join();
  return 0;
}
