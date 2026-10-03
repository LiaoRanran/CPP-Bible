// sample_B078
// defect_type: type_punning
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B078.json)

#include <cstdio>
struct RGB { int r, g, b; };
struct BGR { int b, g, r; };
int main(){
  RGB c{1, 2,3};
  BGR* p = (BGR*)&c; /*DEFECT: reinterpret between layout-incompatible structs (UB); aligned */
  int x = p->r;
  std::printf("%d\n", x);
  return 0;
}