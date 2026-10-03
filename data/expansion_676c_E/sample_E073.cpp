// sample_E073
// defect_type: atomic_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E073.json)

#include <atomic>
#include <thread>
#include <cstdio>
#include <csignal>
static std::atomic<long> tick{0};
static volatile int sig_seen = 0;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
extern "C" void on_alarm(int){ sig_seen = 1; }   // 类信号处理：只碰 sig_seen
static void counter(){
  wait_go();
  /*DEFECT: 把「中断/信号上下文会做的事」搬进普通线程却用非 lock-free 原子做长自增：
     atomic 自增只在 lock-free 时才保证异步上下文安全，本类含非原子后备实现 → 潜在死锁（不保证可重入）*/
  for (int i = 0; i < 100000; ++i) tick.fetch_add(1, std::memory_order_relaxed);
}
int main(){
  std::signal(SIGINT, on_alarm);
  std::thread a(counter);
  go.store(true, std::memory_order_release);
  a.join();
  std::printf("E073 tick=%ld sig=%d\n", tick.load(), sig_seen);
  return 0;
}
