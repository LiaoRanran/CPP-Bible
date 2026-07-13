// _ch127_gvn.cpp : 展示 GVN / SCCP 的常量传播与冗余消除
int compute(int x) {
    int a = x * 2;          // 若 x 已知常量则折叠
    int b = x * 2;          // 与 a 同值 -> GVN 复用
    int c = (x + 1) * (x + 1);
    return a + b + c;
}

int caller() {
    return compute(7);      // 常量 7 进入 -> SCCP 全程折叠为常量
}
