#!/usr/bin/env python3
"""fast_compile.py - 快速批量编译（并行）
v1: 并行+分类（pass/fail/timeout）

Usage: python3 tools/fast_compile.py [N] [--full]
  N: 并行worker数 (default 8)
  --full: 编译所有cpp块（默认每个文件仅前3块）
"""
import os, re, sys, subprocess, tempfile, shutil
from concurrent.futures import ProcessPoolExecutor

GCC = shutil.which('g++') or shutil.which('g++.exe') or 'g++'
FLAGS = ['-std=c++23', '-O0', '-fsyntax-only', '-w']
WORKERS = 8
FULL = '--full' in sys.argv
OUTPUT = '/tmp/cppbible_compile.log'

def extract_blocks(text, max_blocks=3):
    blocks = []
    in_block = False
    current = []
    for line in text.split('\n'):
        if line.strip().startswith('```cpp'):
            in_block = True
            current = []
        elif line.strip() == '```' and in_block:
            in_block = False
            blocks.append('\n'.join(current))
            if max_blocks and len(blocks) >= max_blocks:
                break
        elif in_block:
            current.append(line)
    return blocks

def compile_one(args):
    chapter, idx, block = args
    if not block.strip():
        return (chapter, idx, 'empty', '')

    if 'int main' not in block and 'int __main_' not in block:
        if any(kw in block for kw in ['template<', 'struct ', 'class ', 'namespace ']):
            block = f'struct Wrap {{\n{block}\n}};\nint main(){{return 0;}}'

    with tempfile.NamedTemporaryFile(suffix='.cpp', mode='w', delete=False, encoding='utf-8') as f:
        f.write(block)
        fpath = f.name

    try:
        result = subprocess.run(
            [GCC] + FLAGS + [fpath],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return (chapter, idx, 'pass', '')
        else:
            err = result.stderr.strip().split('\n')[-1][:200] if result.stderr else 'unknown'
            return (chapter, idx, 'fail', err)
    except subprocess.TimeoutExpired:
        return (chapter, idx, 'timeout', '>5s')
    except Exception as e:
        return (chapter, idx, 'error', str(e)[:200])
    finally:
        try: os.unlink(fpath)
        except: pass

def collect_chapters(limit=3):
    items = []
    for r,d,f in os.walk('Book/'):
        if '_legacy' in r: continue
        for ff in sorted(f):
            if not ff.endswith('.md'): continue
            path = r+'/'+ff
            text = open(path, encoding='utf-8').read()
            blocks = extract_blocks(text, max_blocks=None if FULL else limit)
            for i, b in enumerate(blocks):
                items.append((os.path.basename(path), i+1, b))
    return items

def main():
    global WORKERS
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        WORKERS = int(sys.argv[1])

    items = collect_chapters(50 if FULL else 3)
    print(f'Compiling {len(items)} cpp blocks with {WORKERS} workers...')
    print(f'Compiler: {GCC}')

    pass_n = fail_n = timeout_n = 0
    fails = []

    with ProcessPoolExecutor(max_workers=WORKERS) as ex:
        for result in ex.map(compile_one, items, chunksize=10):
            chap, idx, status, err = result
            if status == 'pass':
                pass_n += 1
            elif status == 'fail':
                fail_n += 1
                fails.append((chap, idx, err))
            elif status == 'timeout':
                timeout_n += 1
                fails.append((chap, idx, 'TIMEOUT'))

    print(f'\n=== Compile Summary ===')
    print(f'Total: {len(items)}')
    print(f'Pass:  {pass_n}  ({100*pass_n/max(len(items),1):.1f}%)')
    print(f'Fail:  {fail_n}  ({100*fail_n/max(len(items),1):.1f}%)')
    print(f'Time:  {timeout_n}')

    if fails:
        print(f'\n=== First 30 failures ===')
        for chap, idx, err in fails[:30]:
            print(f'  {chap} #{idx}: {err[:150]}')

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(f'PASS={pass_n}\nFAIL={fail_n}\nTIMEOUT={timeout_n}\nTOTAL={len(items)}\n')
        for chap, idx, err in fails:
            f.write(f'FAIL {chap} #{idx}: {err}\n')
    print(f'\nReport: {OUTPUT}')

if __name__ == '__main__':
    main()
