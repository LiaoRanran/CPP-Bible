// 文件：Examples/_ch159_priority.cpp
// 行号：1
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 Examples/_ch159_priority.cpp -o Examples/_ch159_priority.exe
// 说明：带优先级的任务队列（std::priority_queue + 大顶堆按 level 排序）。
#include <cstdio>
#include <queue>
#include <string>

struct Task {
    int level;          // 越小优先级越高
    std::string name;
    bool operator<(const Task& o) const { return level > o.level; }
};

int main() {
    std::priority_queue<Task> pq;
    pq.push({3, "low"});
    pq.push({1, "high"});
    pq.push({2, "mid"});
    while (!pq.empty()) {
        Task t = pq.top();
        pq.pop();
        std::printf("run %s (level %d)\n", t.name.c_str(), t.level);
    }
}
