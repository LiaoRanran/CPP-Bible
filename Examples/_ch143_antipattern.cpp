// ⑯ 反模式：链表逐节点跳转，内存随机散布，预取器几乎失效
struct Node { int val; Node* next; };

int sum_list(const Node* head) {
    int s = 0;
    for (const Node* p = head; p; p = p->next)
        s += p->val;          // 每次 next 都是一次随机内存访问
    return s;
}

// DOD 替代：用索引数组（或 SoA）保持连续遍历
int sum_array(const int* v, int n) {
    int s = 0;
    for (int i = 0; i < n; ++i)
        s += v[i];            // 顺序访问，可预取、可向量化
    return s;
}
