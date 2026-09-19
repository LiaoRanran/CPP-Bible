#!/usr/bin/env python3
"""Re-verify ONLY the failed blocks recorded in compile_report.json.

Much faster than a full recompile: recompiles just the specific block
indices that previously failed, then classifies each remaining failure.
Results are written incrementally to tools/reverify_result.json so the
run survives session-boundary interruptions.
"""
import json
import os
import sys

sys.path.insert(0, 'tools')
import compile_all as ca  # noqa: E402
import compile_classify as cc  # noqa: E402

REPORT = 'tools/compile_report.json'
OUT = 'tools/reverify_result.json'


def main():
    d = json.load(open(REPORT, encoding='utf-8'))
    entries = d['failures']
    total_prev = sum(len(e['failures']) for e in entries)
    print(f're-verifying {total_prev} previously-failed blocks '
          f'across {len(entries)} chapters', flush=True)

    fixed = 0
    still = 0
    remaining = []      # per (file, block, error, class)
    cls_counter = {}

    for e in entries:
        path = e['path']
        try:
            txt = open(path, encoding='utf-8').read()
        except FileNotFoundError:
            continue
        blocks = ca.extract_blocks(txt)
        chap_remain = []
        for fr in e['failures']:
            idx = fr['block']            # 1-based
            if idx - 1 >= len(blocks):
                continue
            block = blocks[idx - 1]
            err = ca.compile_block(block)
            if err is None:
                fixed += 1
            else:
                still += 1
                klass = cc.classify(err)
                kname = klass[0] if isinstance(klass, tuple) else klass
                cls_counter[kname] = cls_counter.get(kname, 0) + 1
                chap_remain.append({
                    'block': idx, 'error': err[:200], 'class': kname,
                })
        if chap_remain:
            remaining.append({'file': os.path.basename(path),
                              'path': path, 'failures': chap_remain})
        # incremental checkpoint
        json.dump({'prev_failed': total_prev, 'fixed': fixed,
                   'still_failing': still, 'by_class': cls_counter,
                   'remaining': remaining},
                  open(OUT, 'w', encoding='utf-8'),
                  indent=2, ensure_ascii=False)
        print(f'  {os.path.basename(path):34s} '
              f'{len(e["failures"])} -> {len(chap_remain)} remain', flush=True)

    print('\n=== RE-VERIFY SUMMARY ===', flush=True)
    print(f'previously failed blocks : {total_prev}', flush=True)
    print(f'now fixed                : {fixed}', flush=True)
    print(f'still failing            : {still}', flush=True)
    print(f'by class                 : {cls_counter}', flush=True)


if __name__ == '__main__':
    main()
