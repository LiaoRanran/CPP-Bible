#include <cstdlib>
int main(){
  int* p = (int*)malloc(40);
  delete p; // <<PLANTED-DEFECT>> malloc / delete 不匹配
  return 0;
}

