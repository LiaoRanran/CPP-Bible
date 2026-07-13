#!/usr/bin/env python3
"""修复ch82-94新章中引用INDEX规划编号但实际文件名不同的断链"""
import re, os

REPAIR_MAP = {
    'ch41_allocator.md':          'ch38_allocator.md',
    'ch38_new_delete.md':         'ch37_new_delete.md',
    'ch49_exception_safety.md':   'ch40_exception_safety.md',
    'ch47_raii.md':               'ch39_raii_rule.md',
    'ch27_lambda.md':             'ch26_lambda.md',
    'ch44_cache_false_sharing.md':'ch43_cache_locality.md',
    'ch104_mutex.md':             'ch93_thread_async.md',
    'ch114_executor.md':          'ch93_thread_async.md',
    'ch102_concurrency_model.md': 'ch107_atomic.md',
    'ch105_condition_variable.md':'ch93_thread_async.md',
    'ch103_thread.md':            'ch93_thread_async.md',
    'ch157_ce.md':                'ch157_compiler_explorer.md',
    'ch158_perf_antipattern.md':  'ch158_perf_antipatterns.md',
}

fixed = 0
for root, dirs, files in os.walk('Book'):
    for f in sorted(files):
        if not f.endswith('.md'): continue
        path = os.path.join(root, f)
        text = open(path, encoding='utf-8').read()
        orig = text
        for wrong, right in REPAIR_MAP.items():
            text = text.replace(f'/{wrong}', f'/{right}')
        if text != orig:
            open(path, 'w', encoding='utf-8').write(text)
            fixed += 1
            print(f'[OK] {f}: {sum(1 for a,b in zip(orig.splitlines(),text.splitlines()) if a!=b)} lines changed')

print(f'\nFixed {fixed} files')
