// sample_B074
// defect_type: type_punning
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B074.json)

#include <cstdio>
union U { int i; float f; };
int main(){
  U u; u.i = 7;
  float x = u.f; /*DEFECT: union punning inactive member (UB in C++); no runtime trap */
  std::printf("%f\n", x);
  return 0;
}