// sample_B079
// defect_type: type_punning
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B079.json)

#include <cstdio>
int main(){
  int i = 0x40490FDB;
  float f = *(float*)&i; /*DEFECT: int->float punning (UB); same 4-byte alignment, no trap */
  std::printf("%f\n", f);
  return 0;
}