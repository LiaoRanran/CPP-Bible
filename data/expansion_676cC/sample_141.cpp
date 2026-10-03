int main(){
  int a = 10;
  int r = a / 0; // <<PLANTED-DEFECT>> 整数除以零（UB）
  (void)r;
  return 0;
}

