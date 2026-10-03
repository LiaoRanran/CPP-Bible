// sample_E185
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E185.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool done = false;
static long attempts = 0;              // 非原子，被两条路径并发访问
static std::atomic<int> waiting{0};
static void waiter(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  /*DEFECT: wait_for 超时后进入重试分支，而重试分支在释放锁的情况下自增非原子
     attempts（与 slow 线程对同一变量的写并发）⇒ 数据竞争 */
  if (!cv.wait_for(lk, std::chrono::milliseconds(20), []{ return done; })){
    lk.unlock();
    for (int i = 0; i < 100000; ++i) ++attempts;
    lk.lock();
  }
  std::printf("E185 attempts=%ld done=%d\n", attempts, (int)done);
}
static void slow(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  for (int i = 0; i < 100000; ++i) ++attempts;      // 无锁写非原子变量
  std::this_thread::sleep_for(std::chrono::milliseconds(30));
  {
    std::lock_guard<std::mutex> lk(m);
    done = true;
  }
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(slow);
  a.join(); b.join();
  return 0;
}
