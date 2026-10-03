// sample_E100
// defect_type: deadlock
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// thread_count: 2
// timeout_seconds: 5
// (authoritative annotation in sample_E100.json)

#include <mutex>
#include <condition_variable>
#include <atomic>
#include <thread>
#include <cstdio>
static std::mutex conn, resp;
static std::condition_variable cv_conn, cv_resp;
static bool resp_ready = false, conn_released = false;
static std::atomic<bool> go{false};
static void wait_go(){ while(!go.load(std::memory_order_acquire)){} }
static void request(){
  wait_go();
  std::unique_lock<std::mutex> c(conn);
  /*DEFECT: 持 conn 等 resp_ready；resp_ready 需由应答线程在拿到 conn 后设置 ⇒ 死锁 */
  cv_conn.wait(c, []{ return resp_ready; });
  conn_released = true;
  cv_resp.notify_all();
}
static void respond(){
  wait_go();
  std::unique_lock<std::mutex> r(resp);
  /*DEFECT: 持 resp 等 conn_released，与上面互为因果循环 */
  cv_resp.wait(r, []{ return conn_released; });
  resp_ready = true;
  cv_conn.notify_all();
}
int main(){
  std::thread a(request), b(respond);
  go.store(true, std::memory_order_release);
  a.join(); b.join();
  return 0;
}
