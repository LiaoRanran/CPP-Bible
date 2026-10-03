// sample_B094
// defect_type: other_ub
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B094.json)

#include <cstdio>
int main(){
  int i = 0;
  int a[3];
  a[i++] = i++ + i++; /*DEFECT: unsequenced modification/access (UB); wunsequenced N/A here -> blind spot */
  std::printf("%d\n", a[0]);
  return 0;
}