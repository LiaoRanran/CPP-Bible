// sample_B044
// defect_type: resource_leak
// severity: medium
// planted: true
// expected_verdict: catch
// expected_detectors: asan
// (authoritative annotation in sample_B044.json)

#include <cstdio>
int* make(){ int* p = new int(7); return p; /*DEFECT: leak: caller never frees */ }
int main(){
  int* q = make();
  std::printf("%d\n", *q);
  return 0;
}