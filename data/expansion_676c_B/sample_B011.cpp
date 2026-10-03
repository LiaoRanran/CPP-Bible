// sample_B011
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B011.json)

#include <thread>
#include <cstdio>
bool done = false;
void w(){ for (int i = 0; i < 2000000; i++) done = true; /*DEFECT: data race on bool done */ }
void r(){ for (int i = 0; i < 2000000; i++) (void)done; /* racy read of done (also unsynchronized) */ }
int main(){
  std::thread a(w), b(r);
  a.join(); b.join();
  std::printf("%d\n", (int)done);
  return 0;
}