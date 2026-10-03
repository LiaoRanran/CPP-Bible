// sample_E081
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E081.json)

#include <mutex>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex sock_lock, sess_lock;
static std::atomic<int> held{0};
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void send_path(){
  wait_go();
  std::lock_guard<std::mutex> s(sock_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 发送路径 sock->session */
  std::lock_guard<std::mutex> q(sess_lock);
  std::printf("E081 sent\n");
}
static void cleanup_path(){
  wait_go();
  std::lock_guard<std::mutex> q(sess_lock);
  held.fetch_add(1, std::memory_order_release);
  while (held.load(std::memory_order_acquire) < 2){}
  /*DEFECT: 清理路径 session->sock，与发送路径相反 ⇒ 死锁 */
  std::lock_guard<std::mutex> s(sock_lock);
  std::printf("E081 cleaned\n");
}
int main(){
  std::thread a(send_path), b(cleanup_path);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
