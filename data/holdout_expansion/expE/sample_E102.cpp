// sample_E102
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E102.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex m, gate;
static std::condition_variable cv;
static bool done = false;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void waiter(){
  wait_go();
  std::unique_lock<std::mutex> lk(m);
  std::lock_guard<std::mutex> keep(gate);    // 关键：第二把锁，超时路径也不释放
  /*DEFECT: wait_for 超时返回后不重新检查谓词就往下走；
     而 gate 被一直持有，需要 gate 的线程永远拿不到它 ⇒ 死锁 */
  cv.wait_for(lk, std::chrono::milliseconds(50), []{ return done; });
  done = true;
}
static void helper(){
  wait_go();
  /*DEFECT: helper 必须拿到 gate 才能推进，被 waiter 永久持有 ⇒ 阻塞 */
  std::lock_guard<std::mutex> g(gate);
  std::lock_guard<std::mutex> lk(m);
  done = true;
  cv.notify_all();
}
int main(){
  std::thread a(waiter), b(helper);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
