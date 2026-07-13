#include <queue>
#include <vector>

void pq_push(std::priority_queue<int>& pq, int x) {
    pq.push(x);
}

int pq_top_pop(std::priority_queue<int>& pq) {
    int t = pq.top();
    pq.pop();
    return t;
}
