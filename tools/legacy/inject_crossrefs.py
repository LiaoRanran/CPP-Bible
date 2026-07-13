#!/usr/bin/env python3
"""自动交叉引用注入：为裸章添加⟶链接（基于knowledge_graph依赖拓扑）"""
import os, re, json

kg = json.load(open('knowledge_graph.json', encoding='utf-8'))
# Build part → chapter file map
part_map = {}
for root, dirs, files in os.walk('Book/'):
    for f in sorted(files):
        if not f.endswith('.md') or '_legacy' in root: continue
        part = os.path.basename(root)
        part_map.setdefault(part, []).append(f)

# Build part → prerequisite parts map
prereq_map = {}
for p in kg['parts']:
    prereq_map[p['id']] = p.get('prereq', [])

# For each chapter with 0 cross-refs, add 3-5 ⟶ links in ①学习目标 or ②前置知识 section
fixed = 0
for part_dir in sorted(os.listdir('Book/')):
    if not part_dir.startswith('part') or '_legacy' in part_dir: continue
    part_path = f'Book/{part_dir}'
    chapters = sorted([c for c in os.listdir(part_path) if c.endswith('.md')])
    
    for ch in chapters:
        fpath = f'{part_path}/{ch}'
        text = open(fpath, encoding='utf-8').read()
        
        # Skip if already has cross-refs
        if re.findall(r'⟶\s*Book/', text):
            continue
        
        # Get prerequisite parts
        prereqs = prereq_map.get(part_dir, [])
        
        # Build 3-5 link suggestions
        links = []
        for pr in prereqs:
            if pr in part_map and part_map[pr]:
                target = part_map[pr][0]  # first chapter in prereq part
                links.append(f'⟶ Book/{pr}/{target}')
        
        # Add next/prev chapter links
        ch_num = re.match(r'ch(\d+)', ch)
        if ch_num:
            n = int(ch_num.group(1))
            for ch2 in chapters:
                ch2_num = re.match(r'ch(\d+)', ch2)
                if ch2_num:
                    n2 = int(ch2_num.group(1))
                    if n2 == n+1 or n2 == n-1:
                        links.append(f'⟶ Book/{part_dir}/{ch2}')
        
        # Inject into ① or ② section
        # Find a good insertion point: after the first ## ① or ## ② heading
        insert_pos = None
        for m in re.finditer(r'^## [①②③]\b.*$', text, re.MULTILINE):
            end = m.end()
            next_nl = text.find('\n', end)
            if next_nl > 0:
                insert_pos = next_nl + 1
                break
        
        if not links or not insert_pos:
            continue
        
        link_text = '\n' + '\n'.join(links[:5]) + '\n\n'
        new_text = text[:insert_pos] + link_text + text[insert_pos:]
        
        open(fpath, 'w', encoding='utf-8').write(new_text)
        fixed += 1
        print(f'[OK] {ch}: {len(links[:5])} links')

print(f'\nInjected cross-refs to {fixed} chapters')
