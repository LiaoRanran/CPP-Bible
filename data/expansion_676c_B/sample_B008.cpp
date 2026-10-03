// sample_B008
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B008.json)

#include <thread>
#include <cstdio>
double d = 0.0;
void f(){ for (int i = 0; i < 2000000; i++) d += 1.0; /*DEFECT: data race on double d */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%f\n", d);
  return 0;
}