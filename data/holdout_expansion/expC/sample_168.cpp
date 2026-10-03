int main(){
  int n = 20;
  int a[10] = {0};
  for (int i = 0; i < n; ++i) a[i] = i; // <<PLANTED-DEFECT>> 当 n>=10 时越界写
  return 0;
}

