// sample_B072
// defect_type: type_punning
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B072.json)

#include <cstdio>
int main(){
  float f = 1.0f;
  int i = *(int*)&f; /*DEFECT: strict-aliasing punning (UB); no runtime trap */
  std::printf("%d\n", i);
  return 0;
}