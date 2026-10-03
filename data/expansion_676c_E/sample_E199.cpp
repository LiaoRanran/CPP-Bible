// sample_E199
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 1
// timeout_seconds: 5
// (authoritative annotation in sample_E199.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::recursive_mutex m;
static std::condition_variable_any cv;
static bool flag = false;
static std::atomic<bool> resume{false};
static void recursive_worker(){
  std::unique_lock<std::recursive_mutex> lk(m);
  lk.lock();                           // 递归计数 = 2
  resume.store(true, std::memory_order_release);
  /*DEFECT: condition_variable_any 配 recursive_mutex：wait 只解锁一层，
             m 仍被本线程持有（计数 1）⇒ 谓词只能由需要完整锁的线程来改，
             而那把锁永远拿不到 ⇒ 永久阻塞 */
  cv.wait(lk, []{ return flag; });
  std::printf("E199 resumed\n");
}
static void setter(){
  while (!resume.load(std::memory_order_acquire)){}
  std::lock_guard<std::recursive_mutex> g(m);
  flag = true;
  cv.notify_all();
}
int main(){
  std::thread a(recursive_worker), b(setter);
  a.join(); b.join();
  return 0;
}
