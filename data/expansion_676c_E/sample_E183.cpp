// sample_E183
// defect_type: condition_variable
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E183.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex m;
static std::condition_variable cv;
static int permits = 0;
static std::atomic<int> consumed{0};
static void worker(){
  std::unique_lock<std::mutex> lk(m);
  while (permits <= 0) cv.wait(lk);
  --permits;                          // 谓词写法正确
  consumed.fetch_add(1, std::memory_order_release);
}
static void issuer(){
  for (int i = 0; i < 3; ++i){
    {
      std::lock_guard<std::mutex> lk(m);
      ++permits;
    }
    /*DEFECT: 条件变量不是「计数信号量」：三次 notify 并不携带「三份许可」的语义，
             两次通知之间若谓词已被消费，第三次 notify 就是空通知（丢失许可） */
    cv.notify_all();
  }
}
int main(){
  std::thread a(worker), b(issuer);
  a.join(); b.join();
  std::printf("E183 consumed=%d permits=%d\n", consumed.load(), permits);
  return 0;
}
