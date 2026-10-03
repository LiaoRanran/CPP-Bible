// sample_B075
// defect_type: type_punning
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B075.json)

#include <cstdio>
int main(){
  int i = 42;
  short* sp = (short*)&i; /*DEFECT: int->short strict-aliasing pun (UB); aligned, no trap */
  short s = *sp;
  std::printf("%d\n", (int)s);
  return 0;
}