int main(){
  int r = 1 << 40; // <<PLANTED-DEFECT>> 移位量超出 int 位宽（UB）
  (void)r;
  return 0;
}

