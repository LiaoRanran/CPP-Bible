// sample_B057
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: miss
// expected_detectors: asan
// (authoritative annotation in sample_B057.json)

#include <cstdio>
int main(){
  FILE* f = std::fopen("676c_w.txt", "w");
  std::fprintf(f, "x");
  /*DEFECT: resource leak: fopen for write not closed */
  return 0;
}