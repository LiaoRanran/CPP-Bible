// sample_E173
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E173.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool ready = false;
static int shared_total = 0;           // 非原子，且 wait 后不加锁就读
static std::atomic<int> waiting{0};
static void reader(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: wait 不带谓词：被唤醒时 ready 仍可能是 false，读者不该继续 */
  cv.wait(lk);
  lk.unlock();
  /*DEFECT: 解锁后无锁读非原子 shared_total，与 writer 的无锁写并发 ⇒ 数据竞争 */
  long t = 0;
  for (int i = 0; i < 300000; ++i) t += shared_total;
  std::printf("E173 total=%ld\n", t);
}
static void writer(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  /*DEFECT: 通知早于数据就绪 —— 读者会在数据还没写完时醒来 */
  cv.notify_all();
  for (int i = 0; i < 300000; ++i) shared_total += i;   // 无锁写非原子变量
  std::lock_guard<std::mutex> lk(m);
  ready = true;
  cv.notify_all();
}
int main(){
  std::thread a(reader), b(writer);
  a.join(); b.join();
  return 0;
}
