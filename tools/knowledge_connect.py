#!/usr/bin/env python3
"""knowledge_connect.py — Generate cross-chapter usage scenario tables for all chapters.
Scans existing ⟶ links, generates "联合使用场景" appendix at chapter end.
B-phase: turns reference manual into learning system."""

import os, re

# Topic-to-scenario mapping based on chapter keywords
SCENARIOS = {
    'thread': '多线程服务器',
    'mutex': '线程安全数据结构',
    'atomic': '无锁队列/计数器',
    'vector': '动态数组/缓冲区',
    'string': '文本处理/协议解析',
    'map': '键值查找/缓存',
    'unique_ptr': '独占所有权/工厂模式',
    'shared_ptr': '共享所有权/图结构',
    'move': '高性能容器/零拷贝传输',
    'template': '泛型库/编译期计算',
    'lambda': 'STL算法回调/异步任务',
    'RAII': '资源管理/事务回滚',
    'exception': '错误恢复/不可恢复错误',
    'sort': '数据处理管道/排行榜',
    'search': '索引查找/路由表',
    'virtual': '多态插件/框架扩展',
    'CRTP': '静态多态/编译期接口',
    'concept': '模板约束/类型安全API',
    'coroutine': '异步IO/生成器',
    'format': '日志格式化/序列化',
    'filesystem': '文件扫描/配置加载',
    'chrono': '计时器/性能测量',
    'network': 'TCP服务器/HTTP客户端',
    'json': '配置解析/API响应',
    'pool': '高性能分配/资源复用',
    'allocator': '内存管理/PMR定制',
    'benchmark': '性能基准/回归检测',
    'profiling': '热路径识别/优化目标',
    'SIMD': '向量化计算/图像处理',
    'cache': '数据局部性/缓存友好设计',
}

def get_scenario(chapter_text, chapter_name):
    """Guess usage scenarios from chapter content."""
    scenarios = set()
    lower = chapter_text.lower() + chapter_name.lower()
    for keyword, scenario in SCENARIOS.items():
        if keyword.lower() in lower:
            scenarios.add(scenario)
    if not scenarios:
        scenarios.add('通用C++开发')
    return scenarios

def main():
    # Phase 1: Build chapter map (ch_num → {title, path, xrefs})
    chapters = {}
    for r,d,f in os.walk('Book/'):
        if '_legacy' in r: continue
        for ff in sorted(f):
            if not ff.endswith('.md'): continue
            path = r+'/'+ff
            m = re.match(r'ch(\d+)', ff)
            if not m: continue
            num = int(m.group(1))
            text = open(path, encoding='utf-8').read()
            title = text.split('\n')[0].strip('# ').strip()
            # Extract cross-references
            xrefs = re.findall(r'⟶\s*Book/([^\n]+)', text)
            chapters[num] = {
                'file': ff, 'path': path, 'title': title,
                'xrefs': xrefs, 'text': text
            }

    # Phase 2: Generate connection tables
    count = 0
    for num, info in chapters.items():
        scenarios = get_scenario(info['text'], info['file'])
        
        # Resolve xrefs to chapter numbers and titles
        resolved = []
        for xref in info['xrefs']:
            fn = xref.split('/')[-1]
            m = re.match(r'ch(\d+)', fn)
            if m:
                target_num = int(m.group(1))
                if target_num in chapters:
                    resolved.append((target_num, chapters[target_num]['title'][:50]))
        
        if not resolved: continue
        
        # Take top 5 most relevant (closest in number = related topic area)
        resolved.sort(key=lambda x: abs(x[0] - num))
        top = resolved[:5]
        
        # Build table
        table = '\n\n## 联合使用场景\n\n| 关联章节 | 场景 | 组合方式 |\n|---|---|---|\n'
        for i, (tn, ttitle) in enumerate(top):
            scenario = list(scenarios)[i % len(scenarios)]
            table += f'| [第{tn}章]({chapters[tn]["path"].replace("Book/","")}) | {scenario} | 本章提供概念，第{tn}章提供实现 |\n'
        
        # Append
        current = open(info['path'], encoding='utf-8').read()
        if '## 联合使用场景' not in current:
            current += table
            open(info['path'], 'w', encoding='utf-8').write(current)
            count += 1

    print(f'Generated usage scenarios for {count}/{len(chapters)} chapters')

if __name__ == '__main__':
    main()
