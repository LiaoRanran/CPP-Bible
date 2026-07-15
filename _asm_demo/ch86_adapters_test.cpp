#include <stack>
#include <queue>

// 批 L7：stack/queue 纯委托零开销（stack 底层 vector，queue 底层 deque）
int main() {
    std::stack<int> st;
    st.push(1); st.push(2);
    volatile int t = st.top();      // = c.back()
    (void)t;
    std::queue<int> q;
    q.push(1); q.push(2);
    volatile int f = q.front();     // = c.front()
    (void)f;
    volatile int b = q.back();      // = c.back()
    (void)b;
    return 0;
}
