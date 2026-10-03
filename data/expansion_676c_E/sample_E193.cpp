// sample_E193
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E193.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool req = false;
static int handled = 0;
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  while (!req) cv.wait(lk);
  handled = 1;
  /*DEFECT: 处理完成后在锁内把 req 清零（当作「消费掉」），而另一个线程可能正在
             同一次 notify_all 的唤醒里检查谓词 ⇒ 谓词被过早清零，
             后续等待者再也等不到（通知丢失） */
  req = false;
}
static void toggler(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  for (int i = 0; i < 2; ++i){
    {
      std::lock_guard<std::mutex> lk(m);
      req = true;
    }
    cv.notify_all();
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
  }
}
int main(){
  std::thread a(waiter), b(toggler);
  a.join(); b.join();
  std::printf("E193 handled=%d\n", handled);
  return 0;
}
