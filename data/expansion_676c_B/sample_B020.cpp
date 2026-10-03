// sample_B020
// defect_type: data_race
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: tsan
// (authoritative annotation in sample_B020.json)

#include <thread>
#include <cstdio>
struct S { int x; int y; };
S s;
void w(){ for (int i = 0; i < 2000000; i++) s.y = i; /*DEFECT: data race on s.y */ }
void r(){ for (int i = 0; i < 2000000; i++) (void)s.y; /* racy read of s.y */ }
int main(){
  std::thread a(w), b(r);
  a.join(); b.join();
  std::printf("%d\n", s.y);
  return 0;
}