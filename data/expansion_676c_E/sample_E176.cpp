// sample_E176
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E176.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool flag = false;
static std::atomic<int> woke{0};
static void waiter(int id){
  std::unique_lock<std::mutex> lk(m);
  if (id == 0){
    while (!flag) cv.wait(lk);
    woke.fetch_add(1, std::memory_order_release);
  } else {
    /*DEFECT: 第二个等待者用 notify_one 语义去「预留」通知，但它自己并不在等：
       通知被投递到系统选择的某个等待者，可能正好唤醒 id==0 之外的路径，
       而真正需要唤醒的等待者再无通知 ⇒ 永久阻塞 */
    while (!flag) cv.wait(lk);
    woke.fetch_add(1, std::memory_order_release);
  }
}
static void setter(){
  std::this_thread::sleep_for(std::chrono::milliseconds(2));
  {
    std::lock_guard<std::mutex> lk(m);
    flag = true;
  }
  /*DEFECT: 有两个等待者却只 notify_one()：若一次通知未能唤醒全部依赖该谓词的等待者，
     剩余等待者永久阻塞 */
  cv.notify_one();
}
int main(){
  std::thread a(waiter, 0), b(waiter, 1), c(setter);
  a.join(); b.join(); c.join();
  std::printf("E176 woke=%d\n", woke.load());
  return 0;
}
