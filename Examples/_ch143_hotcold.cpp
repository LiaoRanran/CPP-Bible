#include <vector>
#include <string>

// ⑥ 冷热分离：把每帧都要访问的热字段，与很少访问的冷字段拆开
struct EntityHot {           // 每帧遍历：紧凑、缓存友好
    int   id;
    bool  active;
    float x, y;
};

struct EntityCold {          // 偶尔访问：可以放指针间接引用，不污染热循环
    std::vector<int> inventory;
    std::string      name;
    int              questState;
};

// 热循环只触碰 EntityHot 数组，冷数据按需经索引查表
float sum_hot(const EntityHot* e, int n) {
    float s = 0.0f;
    for (int i = 0; i < n; ++i)
        if (e[i].active) s += e[i].x + e[i].y;
    return s;
}
