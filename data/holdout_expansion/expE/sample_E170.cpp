// sample_E170
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E170.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex key_lock;
static unsigned char key[32] = {0};
static std::atomic<int> stage{0};
static void sign(){
  std::lock_guard<std::mutex> lk(key_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做多轮签名运算（CPU 密集，真实实现里还可能触发换页） */
  for (int round = 0; round < 5000; ++round)
    for (int i = 0; i < 32; ++i) key[i] = (unsigned char)((key[i] * 31 + round) & 0xFF);
  stage.store(2, std::memory_order_release);
}
static void handshake(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 握手线程（高优先级）必须等锁才能读密钥 */
  std::lock_guard<std::mutex> lk(key_lock);
  std::printf("E170 key0=%d\n", key[0]);
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(sign), b(handshake);
  a.join(); b.join();
  return 0;
}
