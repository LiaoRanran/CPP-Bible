// sample_E189
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 3
// timeout_seconds: 5
// (authoritative annotation in sample_E189.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex a, b, c;
static std::condition_variable cv;
static bool event = false;
static int payload = 0;                // 非原子
static std::atomic<int> woke{0};
static void waiter(int id, std::mutex* m){
  /*DEFECT: 同一个条件变量被三把不同的 mutex 搭配使用：
             谓词 event/payload 的同步边界与 wait 的释放/重加锁边界不一致 ⇒ 数据竞争 */
  std::unique_lock<std::mutex> lk(*m);
  while (!event) cv.wait(lk);
  payload += id;                       // 非原子读改写
  woke.fetch_add(1, std::memory_order_release);
}
static void setter(){
  while (woke.load(std::memory_order_acquire) > 100) break;
  {
    std::lock_guard<std::mutex> lk(a);
    event = true;
    payload = 100;
  }
  cv.notify_all();
}
int main(){
  std::thread x(waiter, 1, &a), y(waiter, 2, &b), z(waiter, 3, &c), w(setter);
  x.join(); y.join(); z.join(); w.join();
  std::printf("E189 woke=%d payload=%d\n", woke.load(), payload);
  return 0;
}
