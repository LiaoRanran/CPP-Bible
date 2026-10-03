// sample_E178
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E178.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool submitted = false;
static std::atomic<int> got{0};
static void submitter(){
  /*DEFECT: 谓词 submitted 在锁外被读改写（waiter 在锁内读，这里在锁外写）：
     通知与谓词更新都没有与「等待者进入阻塞」这一动作建立任何同步关系，
     通知可以从「检查谓词」与「真正阻塞」之间的窗口里整个漏过去 ⇒ 永久阻塞 */
  submitted = true;
  cv.notify_all();
  std::printf("E178 submitted\n");
}
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  while (!submitted) cv.wait(lk);
  got.store(1, std::memory_order_release);
}
int main(){
  std::thread a(submitter), b(waiter);
  a.join(); b.join();
  std::printf("E178 got=%d\n", got.load());
  return 0;
}
