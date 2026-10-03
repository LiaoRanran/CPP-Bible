int main(){
  int n = 4;
  int sum = 0;
  for (int i = 0; i <= n; ++i) sum += i; // <<PLANTED-DEFECT>> 边界 off-by-one：多算一项（结果错但无越界）
  (void)sum;
  return 0;
}

