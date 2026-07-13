#!/usr/bin/env python3
"""compile_all.py — Batch Compile All Chapters (enhanced v2)

Extracts ```cpp blocks from all chapters and compiles them with
    g++ -std=c++23 -O0 -fsyntax-only
to surface real errors (dead code / syntax errors / missing includes).

Design decision (2026-07-11):
  A chapter contains two kinds of cpp blocks:
    (a) complete programs the author wrote with `int main` -> MUST compile;
    (b) illustrative fragments (class def, global snippet, multi-fence
        examples) that are intentionally NOT standalone -> expected to fail
        when compiled in isolation.
  Compiling every block standalone produces massive false negatives that
  drown real bugs.  `--main-only` restricts verification to (a), giving a
  clean, actionable signal.  The full run (no flag) is still available for
  the complete inventory.

Options:
  --quick        only first 3 cpp blocks per chapter (smoke test)
  --main-only    only compile blocks containing 'int main'
  --gcc PATH     path to g++ (default: shutil.which('g++'))
  --json PATH    write full failure report (default tools/compile_report.json)
"""

import os, re, sys, subprocess, tempfile, shutil, json

GCC = shutil.which('g++') or 'g++'
FLAGS = '-std=c++23 -O0 -fsyntax-only'
QUICK = '--quick' in sys.argv
MAIN_ONLY = '--main-only' in sys.argv
if '--gcc' in sys.argv:
    GCC = sys.argv[sys.argv.index('--gcc') + 1]
# Normalize so that a unix-style path passed via --gcc (/c/Qt/...) is
# accepted by Windows subprocess (which needs C:\Qt\...).
GCC = os.path.normpath(GCC)
OUT_JSON = 'tools/compile_report.json'
if '--json' in sys.argv:
    OUT_JSON = sys.argv[sys.argv.index('--json') + 1]


def extract_blocks(text, max_blocks=None):
    """Extract all ```cpp blocks from markdown text."""
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


def block_has_main(block):
    return 'int main' in block


def compile_block(block):
    """Compile a single block as-written. Return error string or None."""
    if not block.strip():
        return None
    with tempfile.NamedTemporaryFile(suffix='.cpp', mode='w',
                                     delete=False, encoding='utf-8') as f:
        f.write(block)
        fpath = f.name
    try:
        result = subprocess.run(
            [GCC] + FLAGS.split() + [fpath],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            # pick the most informative error line
            msg = ''
            for e in result.stderr.strip().split('\n'):
                if 'error:' in e:
                    msg = e.split('error:')[-1].strip()[:160]
                    break
            if not msg:
                msg = (result.stderr.strip().split('\n')[0] or 'unknown')[:160]
            return msg
        return None
    except subprocess.TimeoutExpired:
        return 'TIMEOUT(>10s)'
    except FileNotFoundError:
        print(f'ERROR: g++ not found at {GCC}')
        sys.exit(1)
    finally:
        os.unlink(fpath)


def dump_report(total_chapters, passed_chapters, failed_chapters,
                total_blocks, failed_blocks, all_failures,
                processed_paths=None):
    """Write the current (possibly partial) report to OUT_JSON.

    Called after every chapter so that a long run interrupted at a
    session boundary still leaves a recoverable, valid JSON covering
    all chapters processed up to that point.
    """
    report = {
        'gcc': GCC,
        'flags': FLAGS,
        'main_only': MAIN_ONLY,
        'partial': True,
        'total_chapters': total_chapters,
        'passed_chapters': passed_chapters,
        'failed_chapters': failed_chapters,
        'total_blocks_checked': total_blocks,
        'failed_blocks': failed_blocks,
        'failures': all_failures,
        'processed_paths': sorted(processed_paths) if processed_paths else [],
    }
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def main():
    RESUME = '--resume' in sys.argv
    total_chapters = passed_chapters = failed_chapters = 0
    total_blocks = failed_blocks = 0
    all_failures = []
    done_paths = set()

    if RESUME and os.path.exists(OUT_JSON):
        try:
            prev = json.load(open(OUT_JSON, encoding='utf-8'))
            total_chapters = prev.get('total_chapters', 0)
            passed_chapters = prev.get('passed_chapters', 0)
            failed_chapters = prev.get('failed_chapters', 0)
            total_blocks = prev.get('total_blocks_checked', 0)
            failed_blocks = prev.get('failed_blocks', 0)
            all_failures = prev.get('failures', [])
            done_paths = set(prev.get('processed_paths', []))
            if not done_paths:
                done_paths = {e['path'] for e in all_failures}
            print(f'RESUME: carried {total_chapters} chapters '
                  f'({failed_chapters} failed) from previous run')
        except Exception as e:
            print('RESUME load failed, starting fresh:', e)

    for r, d, f in os.walk('Book/'):
        if '_legacy' in r:
            continue
        for ff in sorted(f):
            if not ff.endswith('.md'):
                continue
            path = r + '/' + ff
            if RESUME and path in done_paths:
                continue
            text = open(path, encoding='utf-8').read()
            blocks = extract_blocks(text, max_blocks=3 if QUICK else None)
            if not blocks:
                continue

            total_chapters += 1
            chap_failures = []
            for i, block in enumerate(blocks):
                if MAIN_ONLY and not block_has_main(block):
                    continue
                total_blocks += 1
                err = compile_block(block)
                if err is not None:
                    failed_blocks += 1
                    chap_failures.append({
                        'block': i + 1,
                        'error': err,
                        'has_main': block_has_main(block),
                    })
            if chap_failures:
                failed_chapters += 1
                all_failures.append({
                    'file': os.path.basename(path),
                    'path': path,
                    'failures': chap_failures,
                })
                print(f'FAIL {os.path.basename(path)} '
                      f'({len(chap_failures)} fails):')
                for fr in chap_failures[:3]:
                    print(f"  block #{fr['block']}: {fr['error']}")
            else:
                passed_chapters += 1

            done_paths.add(path)
            # Incremental checkpoint: survives session-boundary kills.
            dump_report(total_chapters, passed_chapters,
                        failed_chapters, total_blocks,
                        failed_blocks, all_failures, done_paths)

    # Final report: mark complete (partial=False).
    report = {
        'gcc': GCC,
        'flags': FLAGS,
        'main_only': MAIN_ONLY,
        'partial': False,
        'total_chapters': total_chapters,
        'passed_chapters': passed_chapters,
        'failed_chapters': failed_chapters,
        'total_blocks_checked': total_blocks,
        'failed_blocks': failed_blocks,
        'failures': all_failures,
        'processed_paths': sorted(done_paths),
    }
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print('\n--- Compile Summary ---')
    print(f'Chapters : {total_chapters} '
          f'(pass {passed_chapters} / fail {failed_chapters})')
    print(f'Blocks   : {total_blocks} checked, {failed_blocks} failed')
    print(f'Report   : {OUT_JSON}')
    if failed_chapters == 0:
        print('All (checked) blocks compile! ✅')


if __name__ == '__main__':
    main()
