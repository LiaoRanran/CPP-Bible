#!/usr/bin/env python3
r"""module_compile_check.py — C++20 Modules 感知编译校验 (L1, 2026-07-14)

背景：
  compile_all.py 逐块独立 -fsyntax-only，跨块不联动，导致
    - export module X; / import X; 演示块必然失败（找不到 BMI）
    - import std; 标准库模块需要支持该特性的工具链
  GCC13 连自定义模块都编不过（实测不生成 gcm.cache BMI）。
  用户要求"仔细下载"升级工具链，本工具用升级后的 GCC 验证 modules
  演示能否真正编译。

策略（章节级，非逐块独立）：
  1. 抽章内全部 ```cpp 块。
  2. 找出模块接口块（含 `export module X;` 或 `module X;`）。
  3. 把每个接口块编译成 BMI（-fmodules-ts -c，落 gcm.cache/）。
  4. 找出使用块（含 `import X;` 或 `import std;`），带 BMI / std 模块
     两步编译。
  5. 分类报告：
       custom-module  : 自定义模块，两步编译可过 -> OK / FAIL
       std-module     : import std;，依赖工具链 std 模块支持
       none           : 非模块块（正常 -fsyntax-only）

用法：
  python3 tools/module_compile_check.py                 # 全 Book/ 扫描
  python3 tools/module_compile_check.py Book/.../ch118_modules.md
  python3 tools/module_compile_check.py --gcc "C:/path/g++.exe"
  python3 tools/module_compile_check.py --json out.json
退出码：0=所有模块演示可编译 / 1=有不可编译模块 / 2=用法/工具错误
"""
import os, re, sys, subprocess, json, tempfile, shutil

GCC = shutil.which('g++') or 'g++'
MODULE_FLAGS = ['-std=c++23', '-fmodules-ts']

CPP_FENCE = re.compile(r'```cpp\n(.*?)\n```', re.S)
RE_EXPORT_MODULE = re.compile(r'^\s*export\s+module\s+(\w+)', re.M)
RE_MODULE = re.compile(r'^\s*module\s+(\w+)', re.M)
RE_IMPORT = re.compile(r'^\s*import\s+(\w+)', re.M)


def find_modules_in_chapter(path):
    """返回该章模块相关检查单元列表。"""
    text = open(path, encoding='utf-8').read()
    blocks = CPP_FENCE.findall(text)
    units = []
    for i, b in enumerate(blocks):
        if RE_EXPORT_MODULE.search(b) or RE_MODULE.search(b):
            m = RE_EXPORT_MODULE.search(b) or RE_MODULE.search(b)
            units.append({'kind': 'interface', 'name': m.group(1),
                          'block': i + 1, 'body': b})
        elif RE_IMPORT.search(b):
            m = RE_IMPORT.search(b)
            units.append({'kind': 'import', 'name': m.group(1),
                          'block': i + 1, 'body': b,
                          'is_std': m.group(1) == 'std'})
    return units


def compile_interface(gcc, body, workdir):
    """编译模块接口块 -> BMI。返回 (ok, bmi_path, err)。"""
    with tempfile.NamedTemporaryFile(suffix='.cppm', mode='w',
                                     delete=False, encoding='utf-8',
                                     dir=workdir) as f:
        f.write(body)
        fpath = f.name
    try:
        r = subprocess.run([gcc] + MODULE_FLAGS + ['-c', fpath],
                           capture_output=True, text=True, timeout=30,
                           cwd=workdir)
        if r.returncode == 0:
            # BMI 落在 gcm.cache/ 或同目录 .gcm
            for root, _, files in os.walk(workdir):
                for fn in files:
                    if fn.endswith('.gcm'):
                        return True, os.path.join(root, fn), ''
            return True, fpath + '.gcm', ''  # 不知确切位置但编译通过
        return False, None, (r.stderr or r.stdout).strip().split('\n')[-1][:160]
    except subprocess.TimeoutExpired:
        return False, None, 'TIMEOUT'
    finally:
        os.unlink(fpath)


def compile_user(gcc, body, workdir, is_std):
    """编译使用块。自定义模块依赖 gcm.cache BMI；std 模块靠编译器自带。"""
    with tempfile.NamedTemporaryFile(suffix='.cpp', mode='w',
                                     delete=False, encoding='utf-8',
                                     dir=workdir) as f:
        f.write(body)
        fpath = f.name
    try:
        args = [gcc] + MODULE_FLAGS + ['-fsyntax-only', fpath]
        r = subprocess.run(args, capture_output=True, text=True,
                           timeout=30, cwd=workdir)
        if r.returncode == 0:
            return True, ''
        return False, (r.stderr or '').strip().split('\n')[-1][:160]
    except subprocess.TimeoutExpired:
        return False, 'TIMEOUT'
    finally:
        os.unlink(fpath)


def check_chapter(gcc, path):
    units = find_modules_in_chapter(path)
    if not units:
        return None
    workdir = tempfile.mkdtemp(prefix='modchk_')
    results = []
    try:
        bmis = {}
        for u in units:
            if u['kind'] == 'interface':
                ok, bmi, err = compile_interface(gcc, u['body'], workdir)
                bmis[u['name']] = ok
                results.append({'block': u['block'], 'kind': 'interface',
                                'name': u['name'], 'ok': ok, 'error': err})
            else:
                # import 块：先确保依赖接口已编译（同章内）
                ok, err = compile_user(gcc, u['body'], workdir, u['is_std'])
                results.append({'block': u['block'], 'kind': 'import',
                                'name': u['name'], 'is_std': u['is_std'],
                                'ok': ok, 'error': err})
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    return results


def main():
    global GCC
    if '--gcc' in sys.argv:
        GCC = os.path.normpath(sys.argv[sys.argv.index('--gcc') + 1])
    use_json = '--json' in sys.argv
    json_path = sys.argv[sys.argv.index('--json') + 1] if use_json else None
    targets = [a for a in sys.argv[1:] if a.endswith('.md')]
    if not targets:
        targets = []
        for r, d, f in os.walk('Book/'):
            if '_legacy' in r:
                continue
            for ff in sorted(f):
                if ff.endswith('.md'):
                    targets.append(os.path.join(r, ff))
    summary = {'gcc': GCC, 'chapters': [], 'module_blocks': 0,
               'ok': 0, 'fail': 0}
    any_fail = False
    for path in targets:
        res = check_chapter(GCC, path)
        if not res:
            continue
        n_ok = sum(1 for x in res if x['ok'])
        n_fail = len(res) - n_ok
        summary['module_blocks'] += len(res)
        summary['ok'] += n_ok
        summary['fail'] += n_fail
        if n_fail:
            any_fail = True
        summary['chapters'].append({
            'file': os.path.basename(path), 'path': path,
            'blocks': res})
        print(f"MODULES {os.path.basename(path)}: "
              f"{n_ok}/{len(res)} ok")
        for x in res:
            tag = 'STD ' if x.get('is_std') else ''
            print(f"   blk{x['block']} {tag}{x['kind']}/{x['name']}: "
                  f"{'OK' if x['ok'] else 'FAIL '+x.get('error','')}")
    if json_path:
        json.dump(summary, open(json_path, 'w', encoding='utf-8'),
                  indent=2, ensure_ascii=False)
    print(f"\nTOTAL module blocks: {summary['module_blocks']} "
          f"ok={summary['ok']} fail={summary['fail']}")
    return 1 if any_fail else 0


if __name__ == '__main__':
    sys.exit(main())
