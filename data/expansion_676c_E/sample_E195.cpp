// sample_E195
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E195.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool stop = false;              // 无锁写
static int counter = 0;                // 无锁写
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  /*DEFECT: 谓词 stop 由两个通知者无锁写，这里锁内读 ⇒ 数据竞争 */
  while (!stop) cv.wait(lk);
  std::printf("E195 counter=%d\n", counter);   // counter 也是无锁写的非原子变量
}
static void notifier(int id){
  /*DEFECT: counter / stop 都不加锁修改 */
  for (int i = 0; i < 50000; ++i) counter += id;
  stop = true;
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(notifier, 1), c(notifier, 2);
  a.join(); b.join(); c.join();
  std::printf("E195 final=%d\n", counter);
  return 0;
}
