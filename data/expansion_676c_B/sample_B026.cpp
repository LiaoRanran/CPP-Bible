// sample_B026
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B026.json)

#include <cstdio>
int main(){
  volatile int a = 2000000000;
  a *= 2; /*DEFECT: signed overflow via *= */
  std::printf("%d\n", (int)a);
  return 0;
}