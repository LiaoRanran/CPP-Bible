#include <cstdio>
int main(){
  FILE* fp = fopen("sample_056tmp.dat", "w");
  if (!fp) return 1;
  // <<PLANTED-DEFECT>> 文件句柄未 fclose 即返回 -> 句柄泄漏
  return 0;
}

