// sample_E151
// defect_type: lock_priority_inversion
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E151.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <chrono>
#include <cstdio>
static std::mutex conn_lock;
static int session = 0;
static std::atomic<int> stage{0};
static void net_io(){
  std::lock_guard<std::mutex> lk(conn_lock);
  stage.store(1, std::memory_order_release);
  /*DEFECT: 持锁做网络往返等待（真实项目里就是持锁 recv） */
  std::this_thread::sleep_for(std::chrono::milliseconds(200));
  session = 1;
  stage.store(2, std::memory_order_release);
}
static void heartbeat(){
  while (stage.load(std::memory_order_acquire) < 1){}
  /*DEFECT: 心跳（高优先级）线程必须等这把锁 */
  std::lock_guard<std::mutex> lk(conn_lock);
  session = 2;
  stage.store(3, std::memory_order_release);
}
int main(){
  std::thread a(net_io), b(heartbeat);
  a.join(); b.join();
  std::printf("E151 session=%d\n", session);
  return 0;
}
