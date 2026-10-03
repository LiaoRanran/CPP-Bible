int main(){
  int flag = 0;
  int* p = new int[4];
  if (flag) { delete[] p; }
  int v = p[0]; // <<PLANTED-DEFECT>> flag 为真时 p 已释放 -> 释放后使用
  (void)v;
  return 0;
}

