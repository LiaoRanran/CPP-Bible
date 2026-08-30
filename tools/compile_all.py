#!/usr/bin/env python3
"""compile_all.py — Batch Compile All Chapters (enhanced v3)

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

v3 changes (2026-08-10, P0-2 CI 加固):
  - `--parallel`: group chapters by their `Book/partNN_*` directory and
    compile one part per worker process (ProcessPoolExecutor).  g++ is a
    subprocess-bound bottleneck, so multiprocessing scales nearly linearly
    with part count.  Default stays single-process so `--resume` incremental
    checkpoint semantics are unchanged (parallel mode always runs fresh).
  - GCC resolution: default to project-standard mingw1530 GCC 15.3.0
    (consistent with chapter_compile_check.py); fall back to PATH `g++`
    only when mingw1530 is absent.

Options:
  --quick        only first 3 cpp blocks per chapter (smoke test)
  --main-only    only compile blocks containing 'int main'
  --gcc PATH     path to g++ (default: mingw1530 15.3.0, else PATH g++)
  --json PATH    write full failure report (default tools/compile_report.json)
  --parallel     compile parts concurrently (one process per part)
  --workers N    max concurrent part-workers (default: part count, capped cpu)
  --only PATH [PATH...]  only compile the listed chapter file(s) (scoped run)
  --changed      only compile Book/*.md changed vs git base (incremental;
                 auto-falls back to full when nothing changed)
  --base REF     git base ref for --changed (default: origin/master, else HEAD~1)
"""

import os, re, sys, subprocess, tempfile, shutil, json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

# --- GCC resolution (hardened) -------------------------------------------
_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
from toolchain import resolve_gpp as _resolve_gpp  # noqa: E402


def resolve_gcc(explicit=None):
    if explicit:
        return os.path.normpath(explicit)
    # Project standard is GCC 15.3.0 (mingw1530). Path resolution now lives in
    # tools/toolchain.py (single source of truth = repo-root toolchain.toml):
    # prefer-list probing -> PATH fallback. To retarget a machine or CI image,
    # edit toolchain.toml instead of this file.
    return _resolve_gpp()


GCC = resolve_gcc(sys.argv[sys.argv.index('--gcc') + 1]
                  if '--gcc' in sys.argv else None)
FLAGS = '-std=c++23 -O0 -fsyntax-only'
QUICK = '--quick' in sys.argv
MAIN_ONLY = '--main-only' in sys.argv
PARALLEL = '--parallel' in sys.argv
WORKERS = None
if '--workers' in sys.argv:
    try:
        WORKERS = int(sys.argv[sys.argv.index('--workers') + 1])
    except Exception:
        WORKERS = None
OUT_JSON = 'tools/compile_report.json'
if '--json' in sys.argv:
    OUT_JSON = sys.argv[sys.argv.index('--json') + 1]

# --- incremental / scoped selection (T2) ---------------------------------
CHANGED = '--changed' in sys.argv
BASE = None
if '--base' in sys.argv:
    try:
        BASE = sys.argv[sys.argv.index('--base') + 1]
    except Exception:
        BASE = None
ONLY = []
if '--only' in sys.argv:
    i = sys.argv.index('--only') + 1
    while i < len(sys.argv) and not sys.argv[i].startswith('--'):
        ONLY.append(sys.argv[i])
        i += 1


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


def compile_block(block, gcc=GCC):
    """Compile a single block as-written. Return error string or None."""
    if not block.strip():
        return None
    with tempfile.NamedTemporaryFile(suffix='.cpp', mode='w',
                                     delete=False, encoding='utf-8') as f:
        f.write(block)
        fpath = f.name
    try:
        result = subprocess.run(
            [gcc] + FLAGS.split() + [fpath],
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
        print(f'ERROR: g++ not found at {gcc}')
        sys.exit(1)
    finally:
        os.unlink(fpath)


def compile_chapter(path, quick=QUICK, main_only=MAIN_ONLY, gcc=GCC):
    """Compile all (or filtered) cpp blocks in one chapter file.

    Returns dict: {path, passed, failed, failures:[...], blocks_checked}.
    """
    try:
        text = open(path, encoding='utf-8').read()
    except Exception as e:
        return {'path': path, 'error': str(e), 'passed': 0, 'failed': 0,
                'failures': [], 'blocks_checked': 0}
    blocks = extract_blocks(text, max_blocks=3 if quick else None)
    if not blocks:
        return {'path': path, 'passed': 1, 'failed': 0,
                'failures': [], 'blocks_checked': 0}
    chap_failures = []
    blocks_checked = 0
    for i, block in enumerate(blocks):
        if main_only and not block_has_main(block):
            continue
        blocks_checked += 1
        err = compile_block(block, gcc=gcc)
        if err is not None:
            chap_failures.append({'block': i + 1, 'error': err,
                                  'has_main': block_has_main(block)})
    return {
        'path': path,
        'passed': 1 if not chap_failures else 0,
        'failed': 1 if chap_failures else 0,
        'failures': chap_failures,
        'blocks_checked': blocks_checked,
    }


def compile_part(arg):
    """Worker: compile every chapter in one part directory.

    arg = {'paths':[...], 'quick':bool, 'main_only':bool, 'gcc':str}
    Returns list of per-chapter result dicts (see compile_chapter).
    Top-level so it is picklable for ProcessPoolExecutor on Windows/spawn.
    """
    paths = arg['paths']
    quick = arg['quick']
    main_only = arg['main_only']
    gcc = arg['gcc']
    return [compile_chapter(p, quick=quick, main_only=main_only, gcc=gcc)
            for p in paths]


def group_by_part(paths):
    """Group chapter paths by their Book/*part*/ parent directory."""
    groups = {}
    for p in paths:
        parent = os.path.dirname(p)
        groups.setdefault(parent, []).append(p)
    return groups


def collect_chapters(book_root):
    paths = []
    for r, d, f in os.walk(book_root):
        if '_legacy' in r:
            continue
        for ff in sorted(f):
            # 只收集正式章节 chNN_*.md，跳过 SUMMARY/GLOSSARY/PREREQUISITES/
            # MANIFEST 等索引文件，统一"章节数=147"口径（见审计报告 §5.4）
            if ff.endswith('.md') and re.match(r'^ch\d+_', ff):
                paths.append(os.path.join(r, ff))
    return paths


def _resolve_base():
    """Pick a sensible git base ref for --changed: prefer origin/master/main,
    fall back to HEAD~1. Returns a rev-parse-able ref string."""
    for ref in ("origin/master", "origin/main", "HEAD~1"):
        try:
            subprocess.check_output(["git", "rev-parse", "--verify", ref],
                                    stderr=subprocess.DEVNULL)
            return ref
        except Exception:
            continue
    return "HEAD~1"


def collect_changed(book_root, base=None):
    """Return set of changed Book/*.md paths (forward-slashed) for incremental
    compile. Union of:
      * committed changes since <base> (CI push / PR),
      * unstaged worktree edits (local pre-commit check),
      * staged (--cached) edits.
    Only Book/**/*.md is retained. Returns empty set if git is unavailable or
    nothing relevant changed (caller falls back to a full run)."""
    base = base or _resolve_base()
    results = set()
    # committed changes since base
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", f"{base}..HEAD"],
            text=True, stderr=subprocess.DEVNULL)
        results |= {l.strip() for l in out.splitlines() if l.strip()}
    except Exception:
        pass
    # unstaged + staged worktree edits
    for extra in (["git", "diff", "--name-only"],
                  ["git", "diff", "--cached", "--name-only"]):
        try:
            out = subprocess.check_output(extra, text=True, stderr=subprocess.DEVNULL)
            results |= {l.strip() for l in out.splitlines() if l.strip()}
        except Exception:
            pass
    return {p for p in results if p.startswith("Book/") and p.endswith(".md")}


def dump_report(total_chapters, passed_chapters, failed_chapters,
                total_blocks, failed_blocks, all_failures,
                processed_paths=None, partial=True):
    """Write the (possibly partial) report to OUT_JSON.

    Called after every chapter in sequential mode so a long run interrupted
    at a session boundary still leaves a recoverable, valid JSON covering
    all chapters processed up to that point.
    """
    report = {
        'gcc': GCC,
        'flags': FLAGS,
        'main_only': MAIN_ONLY,
        'partial': partial,
        'total_chapters': total_chapters,
        'passed_chapters': passed_chapters,
        'failed_chapters': failed_chapters,
        'total_blocks_checked': total_blocks,
        'failed_blocks': failed_blocks,
        'failures': all_failures,
        'processed_paths': sorted(processed_paths) if processed_paths else [],
    }
    with open(OUT_JSON, 'w', encoding='utf-8', newline="\n") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def _merge_chapter_results(chap_results):
    """Aggregate a list of per-chapter dicts into summary counters."""
    total_chapters = passed_chapters = failed_chapters = 0
    total_blocks = failed_blocks = 0
    all_failures = []
    processed = []
    for cr in chap_results:
        processed.append(cr['path'])
        total_chapters += 1
        total_blocks += cr.get('blocks_checked', 0)
        if cr.get('failed'):
            failed_chapters += 1
            failed_blocks += len(cr.get('failures', []))
            all_failures.append({
                'file': os.path.basename(cr['path']),
                'path': cr['path'],
                'failures': cr.get('failures', []),
            })
        else:
            passed_chapters += 1
    return (total_chapters, passed_chapters, failed_chapters,
            total_blocks, failed_blocks, all_failures, processed)


def main():
    RESUME = '--resume' in sys.argv
    book = 'Book/'
    all_paths = collect_chapters(book)

    # --- incremental / scoped selection (T2) ---------------------------
    if ONLY:
        targets = [p for p in ONLY if os.path.exists(p)]
        partial_run = True
    elif CHANGED:
        changed = {c.replace('\\', '/') for c in collect_changed(book, BASE)}
        targets = [p for p in all_paths if p.replace('\\', '/') in changed]
        if not targets:
            print("[*] --changed: 无章节变更，回退全量编译。")
            targets = all_paths
            partial_run = False
        else:
            print(f"[*] --changed: 仅编译 {len(targets)} 个变更章节 (partial)。")
            partial_run = True
    else:
        targets = all_paths
        partial_run = False
    paths = targets

    if PARALLEL:
        # --- parallel-by-part branch (no resume; always fresh) -----------
        groups = group_by_part(paths)
        part_args = [{'paths': pl, 'quick': QUICK, 'main_only': MAIN_ONLY,
                      'gcc': GCC} for pl in groups.values()]
        workers = WORKERS or min(len(part_args), (os.cpu_count() or 4))
        workers = max(workers, 1)
        print(f"[*] --parallel: {len(groups)} parts, {workers} workers")
        chap_results = []
        with ProcessPoolExecutor(max_workers=workers) as ex:
            for part_res in ex.map(compile_part, part_args):
                chap_results.extend(part_res)
        (total_chapters, passed_chapters, failed_chapters,
         total_blocks, failed_blocks, all_failures, processed) = \
            _merge_chapter_results(chap_results)
        dump_report(total_chapters, passed_chapters, failed_chapters,
                    total_blocks, failed_blocks, all_failures,
                    processed_paths=processed, partial=partial_run)
    else:
        # --- sequential branch (preserves --resume checkpoint) -----------
        total_chapters = passed_chapters = failed_chapters = 0
        total_blocks = failed_blocks = 0
        all_failures = []
        done_paths = set()

        if (not partial_run) and RESUME and os.path.exists(OUT_JSON):
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

        for path in paths:
            if RESUME and path in done_paths:
                continue
            cr = compile_chapter(path)
            total_chapters += 1
            total_blocks += cr['blocks_checked']
            failed_blocks += len(cr['failures'])
            if cr['failed']:
                failed_chapters += 1
                all_failures.append({
                    'file': os.path.basename(path),
                    'path': path,
                    'failures': cr['failures'],
                })
                print(f'FAIL {os.path.basename(path)} '
                      f'({len(cr["failures"])} fails):')
                for fr in cr['failures'][:3]:
                    print(f"  block #{fr['block']}: {fr['error']}")
            else:
                passed_chapters += 1

            done_paths.add(path)
            # Incremental checkpoint: survives session-boundary kills.
            dump_report(total_chapters, passed_chapters,
                        failed_chapters, total_blocks,
                        failed_blocks, all_failures, done_paths,
                        partial=True)

    # Final report: mark complete (partial=False) for sequential path.
    if not PARALLEL:
        report = {
            'gcc': GCC,
            'flags': FLAGS,
            'main_only': MAIN_ONLY,
            'partial': partial_run,
            'total_chapters': total_chapters,
            'passed_chapters': passed_chapters,
            'failed_chapters': failed_chapters,
            'total_blocks_checked': total_blocks,
            'failed_blocks': failed_blocks,
            'failures': all_failures,
            'processed_paths': sorted(done_paths),
        }
        with open(OUT_JSON, 'w', encoding='utf-8', newline="\n") as f:
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
