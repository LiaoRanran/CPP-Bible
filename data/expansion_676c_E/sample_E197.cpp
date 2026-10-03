// sample_E197
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E197.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static bool job_ready = false;
static std::atomic<int> picked{0}, waiting{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  waiting.store(1, std::memory_order_release);
  while (!job_ready) cv.wait(lk);
  picked.store(1, std::memory_order_release);
}
static void dispatcher(){
  while (waiting.load(std::memory_order_acquire) == 0){}
  /*DEFECT: 谓词在锁外写 + notify 也在锁外：
             两步之间 worker 可能正在 wait（或还没进入 wait）⇒ 通知永久丢失，
             worker 永久阻塞；且锁外写谓词与 worker 锁内读构成数据竞争 */
  job_ready = true;
  cv.notify_all();
}
int main(){
  std::thread a(worker), b(dispatcher);
  a.join(); b.join();
  std::printf("E197 picked=%d\n", picked.load());
  return 0;
}
