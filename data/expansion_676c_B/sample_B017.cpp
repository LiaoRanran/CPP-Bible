// sample_B017
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B017.json)

#include <thread>
#include <cstdio>
int g = 0;
void w(){ for (int i = 0; i < 2000000; i++) g = i; /*DEFECT: data race: write */ }
void w2(){ for (int i = 0; i < 2000000; i++) g = -i; /* racy write (also unsynchronized) */ }
int main(){
  std::thread a(w), b(w2);
  a.join(); b.join();
  std::printf("%d\n", g);
  return 0;
}