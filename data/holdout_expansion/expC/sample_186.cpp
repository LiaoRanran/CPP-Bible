int main(){
  int input = 2;
  int* p = new int[8];
  if (input > 0) { return 0; } // <<PLANTED-DEFECT>> 特定分支提前返回 -> 泄漏
  delete[] p;
  return 0;
}

