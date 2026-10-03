// sample_B006
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B006.json)

#include <thread>
#include <cstdio>
int flag = 0;
void w(){ for (int i = 0; i < 2000000; i++) flag = 1; /*DEFECT: data race: concurrent write to flag */ }
void r(){ for (int i = 0; i < 2000000; i++) (void)flag; /* racy read of flag (also unsynchronized) */ }
int main(){
  std::thread a(w), b(r);
  a.join(); b.join();
  std::printf("%d\n", flag);
  return 0;
}