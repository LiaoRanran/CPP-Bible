#!/usr/bin/env python3
"""learning_path.py - 学习路径生成器
扫描所有交叉引用,构建DAG,生成DOT图+JSON依赖表

Usage:
  python3 tools/learning_path.py --format json    # 依赖表
  python3 tools/learning_path.py --format dot     # Graphviz源
  python3 tools/learning_path.py --format stats   # 统计
"""
import os, re, sys, json
from collections import defaultdict, Counter

# 交叉引用模式: ⟶ Book/partXX/chYY_name.md
XREF_RE = re.compile(r'⟶\s*Book/([\w/]+)\.md')

# 章号→主题
TOPIC_HINTS = {
    '01': 'C++历史', '02': 'C++标准化', '03': 'C++98/03', '04': 'C++11', '05': 'C++14',
    '06': 'C++17', '07': 'C++20', '08': 'C++23', '09': 'C++26', '10': '版本矩阵',
    '11': 'C生态', '12': '工具链', '13': '打包', '14': '调试', '15': 'CMake',
    '16': 'IDE', '17': '交叉编译', '18': 'Sanitizer', '19': '构建系统',
    '20': '基本语法', '21': 'const', '22': 'auto', '23': '类型系统', '24': 'enum',
    '25': 'union', '26': 'lambda', '27': '属性', '28': '生命周期', '29': '友元',
    '30': '作用域', '31': '运算符重载', '32': '初始化',
    '37': 'new/delete', '38': 'allocator', '39': 'RAII', '40': '异常安全',
    '41': '智能指针', '42': 'move', '43': '内存模型', '44': '内存池',
    '45': 'OOP', '46': '封装继承', '47': '虚函数', '48': 'RTTI', '49': '虚继承',
    '50': '多继承', '51': 'CRTP', '52': 'EBO',
    '60': '模板基础', '61': '模板重载', '62': '特化', '63': '可变参数', '64': '模板元',
    '65': 'type_traits', '66': 'SFINAE', '67': 'Concepts', '68': '折叠', '69': 'constexpr',
    '70': 'tag dispatch', '71': 'Policy',
    '76': 'STL架构', '77': 'vector', '78': 'deque', '79': 'list', '80': 'array',
    '81': 'string', '82': 'span', '83': 'map', '84': 'set', '85': 'unordered',
    '86': '适配器', '87': 'bitset', '88': 'tuple', '89': 'optional/variant',
    '90': 'ranges', '91': 'filesystem', '92': 'chrono', '93': 'thread', '94': 'stop_token',
    '95': '算法总览', '96': '排序', '97': '搜索', '98': '数值', '99': '集合', '100': 'heap',
    '101': '线程', '102': '线程管理', '103': 'TLS', '104': 'mutex', '105': 'cv',
    '106': 'call_once', '107': 'atomic', '108': 'memory_order', '109': 'fence',
    '110': 'lock-free', '111': 'ABA', '112': 'future', '113': '协程', '114': '并行',
    '115': 'move', '116': '完美转发', '117': 'copy elision', '118': 'modules',
    '119': 'ranges深入', '120': '协程应用', '121': 'contracts', '122': 'pmr', '123': 'ct',
    '124': 'source location', '125': 'std::format', '126': 'msstl', '127': 'llvm',
    '128': 'boost', '129': 'qt', '130': 'chromium', '131': 'fmt', '132': 'cppreference',
    '133': 'clickhouse', '134': 'unreal',
    '135': '模式总论', '136': '创建型', '137': '结构型', '138': '行为型',
    '139': 'CRTP模式', '140': 'Policy', '141': 'DI', '142': 'ECS', '143': 'DOD',
    '144': '代码风格', '145': '命名API', '146': '错误处理', '147': '代码审查',
    '148': 'Git', '149': 'CI/CD', '150': '测试', '151': '基准测试',
    '152': '性能模型', '153': 'CPU微架构', '154': 'Cache', '155': 'SIMD',
    '156': '编译器优化', '157': 'Compiler Explorer', '158': '反模式',
    '159': '线程池', '160': '内存池', '161': '日志', '162': 'JSON', '163': '网络', '164': '框架',
    '165': '路线图',
}

def get_chapter_num(path):
    m = re.search(r'ch(\d{2,3})', os.path.basename(path))
    if m:
        return m.group(1)
    return '?'

def get_topic(num):
    return TOPIC_HINTS.get(num, '?')

def build_graph():
    """扫描所有章,返回 {chapter: [dep1, dep2, ...]} 依赖表。"""
    graph = defaultdict(set)
    indegree = Counter()
    chapters = set()

    for r,d,f in os.walk('Book/'):
        if '_legacy' in r: continue
        for ff in f:
            if not ff.endswith('.md'): continue
            path = r+'/'+ff
            text = open(path, encoding='utf-8').read()
            num = get_chapter_num(path)
            chapters.add((num, os.path.basename(path)))

            for m in XREF_RE.finditer(text):
                dep_path = m.group(1)
                dep_num = get_chapter_num(dep_path + '.md')
                if dep_num != '?':
                    graph[num].add(dep_num)
                    indegree[dep_num] += 1

    return graph, indegree, chapters

def format_stats():
    g, indeg, chapters = build_graph()
    print(f'Total chapters: {len(chapters)}')
    print(f'Edges (xrefs): {sum(len(v) for v in g.values())}')
    print(f'Avg deps/chapter: {sum(len(v) for v in g.values())/max(len(chapters),1):.1f}')

    # Most depended-on (high indegree = foundational)
    print(f'\n=== TOP 10 most-depended-on (foundation chapters) ===')
    for num, deg in indeg.most_common(10):
        print(f'  ch{num} ({get_topic(num)}): {deg} deps')

    # Most dependent-on-others (advanced)
    outdeg = {n: len(d) for n, d in g.items()}
    print(f'\n=== TOP 10 most-dependent (advanced chapters) ===')
    for num, deg in sorted(outdeg.items(), key=lambda x: -x[1])[:10]:
        print(f'  ch{num} ({get_topic(num)}): depends on {deg}')

def format_json():
    g, indeg, chapters = build_graph()
    out = {
        'chapters': sorted([n for n, _ in chapters]),
        'edges': [{'from': n, 'to': t} for n, deps in g.items() for t in deps],
        'indegree': dict(indeg),
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))

def format_dot():
    g, indeg, chapters = build_graph()
    print('digraph learning_path {')
    print('  rankdir=LR; node [shape=box, style=filled, fillcolor=lightblue];')
    # Group by part
    by_part = defaultdict(list)
    for num, _ in chapters:
        part = 'part' + num[:2] if num != '?' else 'unknown'
        by_part[part].append(num)
    for part, nums in by_part.items():
        print(f'  subgraph cluster_{part} {{ label="{part}";')
        for n in sorted(nums):
            print(f'    "ch{n}" [label="ch{n}\\n{get_topic(n)}"];')
        print('  }')
    for n, deps in g.items():
        for t in deps:
            print(f'  "ch{n}" -> "ch{t}";')
    print('}')

if __name__ == '__main__':
    fmt = 'stats'
    if '--format' in sys.argv:
        fmt = sys.argv[sys.argv.index('--format') + 1]
    if fmt == 'json':
        format_json()
    elif fmt == 'dot':
        format_dot()
    else:
        format_stats()
