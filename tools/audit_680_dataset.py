# -*- coding: utf-8 -*-
"""680 批次 · 数据集标注质量深度审计（只读）。

红线：不修改任何样本、JSON 标注、检测器；只读 + 报告。
输入：
  data/676m_sample_manifest_corrected.json      1147 全集（expansion 1042 + 原始 105）
  data/blindspot_676g_detection_matrix.json     1147×8 实际判定矩阵（含 or_verdict_all8）
  data/677b_clone_families.json                 克隆家族（1137）
  逐样本标注 data/holdout_expansion/exp*/sample_*.json（1042，SCHEMA §1 定义的权威记录）
输出：
  data/680_审计不合格样本清单.json
"""
import collections
import glob
import json
import os
import random
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def p(*a):
    return os.path.join(ROOT, *a)


SEED, FRAC = 6801, 0.20
MARKERS = ['<<PLANTED-DEFECT>>', 'PLANTED-DEFECT', '<<DEFECT>>', '/* DEFECT */', 'DEFECT:', '// BUG', 'BUG:',
           '// DEFECT', '//DEFECT', '❌']
REQ_MANIFEST = ['uid', 'sample_id', 'source_batch', 'defect_type', 'planted', 'expected_verdict', 'input_mode',
                'run_mode']
REQ_SAMPLE = ['sample_id', 'defect_type', 'defect_location', 'severity', 'planted', 'expected_verdict', 'notes']
EMBEDDED = {'volatile_misuse', 'register_ub', 'interrupt_safety'}
CONCURRENCY = {'data_race', 'deadlock', 'memory_order', 'atomic_ub', 'condition_variable'}
PLATFORM_TOKENS = ['pthread', 'std::thread', 'volatile', 'atomic', 'sigaction', 'signal(', 'mmap', 'unistd.h',
                   'windows.h', 'msvc', 'setarch', 'memory_order', 'alignas']


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def read_lines(path):
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            return f.read().splitlines()
    except OSError:
        return None


def loc_dir(rec):
    if rec['source_batch'].startswith('exp'):
        return p('data', 'holdout_expansion', rec['source_batch'])
    return p(rec['dir']) if rec.get('dir') else ''


def loc_files(rec):
    d = loc_dir(rec)
    return [os.path.join(d, fn) for fn in (rec.get('files') or [])]


def short_id(batch, sid):
    m = re.match(r'sample_(\d+)$', sid)
    if batch.startswith('exp') and m:
        return batch[3] + m.group(1)
    return sid


def main():
    man = load(p('data', '676m_sample_manifest_corrected.json'))
    mat = load(p('data', 'blindspot_676g_detection_matrix.json'))
    fam = load(p('data', '677b_clone_families.json'))
    S = man['samples']
    by_uid = {r['uid']: r for r in mat['samples']}
    voc = man.get('vocabulary')
    vocab = set(voc if isinstance(voc, list) else (voc or {}).keys()) if voc else set()
    issues = []

    def issue(uid, batch, dim, sev, reason, **ev):
        issues.append({'uid': uid, 'source_batch': batch, 'dimension': dim, 'severity': sev,
                       'reason': reason, 'evidence': ev})

    # 逐样本 JSON 索引：按 (batch, sample_id) 键（expA/expC 共用 sample_XXX 命名空间，uid 才唯一）
    json_index = {}
    for f in glob.glob(p('data', 'holdout_expansion', 'exp*', 'sample_*.json')):
        batch = os.path.basename(os.path.dirname(f))
        try:
            jd = load(f)
        except Exception as e:  # noqa: BLE001
            issue(os.path.basename(f), batch, 'B1', 'high', f'JSON 不可解析: {e}')
            continue
        json_index[(batch, jd.get('sample_id'))] = (f, jd)
    def jget(rec):
        return json_index.get((rec['source_batch'], rec['sample_id']))

    # ---------- B1 完整性 ----------
    b1 = collections.Counter()
    for rec in S:
        for k in REQ_MANIFEST:
            if k not in rec or rec[k] in (None, ''):
                b1['manifest_missing'] += 1
                issue(rec['uid'], rec['source_batch'], 'B1', 'high', f'manifest 必填字段缺失: {k}')
        inline = rec['input_mode'] == 'code_materialized'
        if inline:
            b1['inline_no_disk'] += 1
            continue
        cands = loc_files(rec)
        exist = [c for c in cands if os.path.isfile(c)]
        if not cands:
            b1['no_files_declared'] += 1
            issue(rec['uid'], rec['source_batch'], 'B1', 'medium', '未声明源文件且非内联模式')
            continue
        if not exist:
            b1['source_file_missing'] += 1
            issue(rec['uid'], rec['source_batch'], 'B1', 'high', '源文件缺失',
                  dir=loc_dir(rec), files=rec.get('files'))
            continue
        if rec['source_batch'].startswith('exp'):
            j = jget(rec)
            if not j:
                b1['json_missing'] += 1
                issue(rec['uid'], rec['source_batch'], 'B1', 'high', '逐样本 JSON 缺失')
                continue
            fpath, jd = j
            for kk in REQ_SAMPLE:
                if kk not in jd or jd[kk] in (None, ''):
                    b1['json_field_missing'] += 1
                    issue(rec['uid'], rec['source_batch'], 'B1', 'high', f'逐样本 JSON 必填字段缺失: {kk}')
            loc = jd.get('defect_location') or {}
            ln = loc.get('line')
            df = loc.get('file')
            if df and not os.path.isfile(os.path.join(os.path.dirname(fpath), df)):
                b1['locfile_missing'] += 1
                issue(rec['uid'], rec['source_batch'], 'B1', 'medium', 'defect_location.file 不存在', file=df)
            elif isinstance(ln, int):
                tgt = os.path.join(os.path.dirname(fpath), df) if df else exist[0]
                ls = read_lines(tgt) or []
                if not (1 <= ln <= len(ls)):
                    b1['line_out_of_range'] += 1
                    issue(rec['uid'], rec['source_batch'], 'B1', 'high',
                          'defect_location.line 超出行范围', line=ln, n_lines=len(ls))

    # ---------- B2 真实性抽样 ----------
    rng = random.Random(SEED)
    n_take = max(1, round(len(S) * FRAC))
    sel = rng.sample(S, n_take)
    b2 = collections.Counter()
    marker_by_batch = collections.Counter()
    sampled_by_batch = collections.Counter()
    fails, reviews = [], []
    for rec in sel:
        sampled_by_batch[rec['source_batch']] += 1
        if rec['input_mode'] == 'code_materialized':
            b2['N/A_inline'] += 1
            continue
        exist = [c for c in loc_files(rec) if os.path.isfile(c)]
        if not exist:
            b2['FAIL'] += 1
            fails.append({'uid': rec['uid'], 'reason': 'missing_file'})
            continue
        j = jget(rec)
        jd = j[1] if j else {}
        ln = (jd.get('defect_location') or {}).get('line')
        all_markers, near = [], False
        for c in exist:
            ls = read_lines(c) or []
            ml = [i + 1 for i, t in enumerate(ls) if any(mk in t for mk in MARKERS)]
            all_markers.extend(ml)
            if isinstance(ln, int) and any(abs(x - ln) <= 3 for x in ml):
                near = True
        if all_markers:
            marker_by_batch[rec['source_batch']] += 1
        if not all_markers:
            b2['REVIEW'] += 1
            reviews.append({'uid': rec['uid'], 'reason': 'no_defect_marker'})
        elif isinstance(ln, int) and not near:
            b2['REVIEW'] += 1
            reviews.append({'uid': rec['uid'], 'reason': f'line{ln}_far_from_markers{all_markers[:3]}'})
        else:
            b2['PASS'] += 1
    for x in fails:
        issue(x['uid'], '?', 'B2', 'high', '抽样真实性: ' + x['reason'])
    for x in reviews:
        issue(x['uid'], '?', 'B2', 'medium', '抽样真实性(待人工复核): ' + x['reason'])
    b2['marker_coverage_by_batch'] = dict(marker_by_batch)
    b2['sampled_by_batch'] = dict(sampled_by_batch)

    # ---------- B3 词表一致性 ----------
    dt_json = collections.Counter()
    seen_files = set()
    for _, (fpath2, jd) in json_index.items():
        if fpath2 in seen_files:
            continue
        seen_files.add(fpath2)
        dt_json[jd.get('defect_type')] += 1
    dt_man = collections.Counter(r.get('defect_type') for r in S)
    oov_json = {k: v for k, v in dt_json.items() if vocab and k not in vocab}
    orig = [r for r in S if not r['source_batch'].startswith('exp')]
    oov_orig = {k: v for k, v in collections.Counter(r['defect_type'] for r in orig).items()
                if vocab and k not in vocab}
    b3 = {'vocab_size': len(vocab), 'n_distinct_json_1042': len(dt_json), 'n_distinct_manifest_1147': len(dt_man),
          'oov_json_1042': oov_json, 'oov_originals_105': oov_orig, 'dist_json': dict(dt_json.most_common())}
    for k, v in oov_json.items():
        issue(f'(json×{v})', 'exp', 'B3', 'medium', f'defect_type 不在 34 项闭集: {k}')
    for k, v in oov_orig.items():
        issue(f'(originals×{v})', 'holdout/corpus', 'B3', 'low', f'原始样本沿用 legacy 标签: {k}')

    # ---------- B3b 跨源标签一致性（manifest vs 权威 JSON vs matrix） ----------
    xs = collections.Counter()
    xsf = collections.Counter()
    xs_rows = []
    for rec in S:
        if not rec['source_batch'].startswith('exp'):
            continue
        j = jget(rec)
        if not j:
            continue
        jd = j[1]
        m = by_uid.get(rec['uid']) or {}
        bad = []
        if jd.get('defect_type') != rec.get('defect_type'):
            bad.append(('defect_type', rec.get('defect_type'), jd.get('defect_type')))
        if jd.get('expected_verdict') != rec.get('expected_verdict'):
            bad.append(('expected_verdict', rec.get('expected_verdict'), jd.get('expected_verdict')))
        if bool(jd.get('planted')) != bool(rec.get('planted')):
            bad.append(('planted', rec.get('planted'), jd.get('planted')))
        if m and m.get('defect_type') != jd.get('defect_type'):
            bad.append(('matrix_defect_type', m.get('defect_type'), jd.get('defect_type')))
        if bad:
            xs[rec['source_batch']] += 1
            for fld, _a, _b in bad:
                xsf[fld] += 1
            xs_rows.append({'uid': rec['uid'], 'diffs': bad})
    b3['cross_source_mismatch_by_batch'] = dict(xs)
    b3['cross_source_mismatch_by_field'] = dict(xsf)
    b3['cross_source_rows'] = xs_rows[:300]
    if xs_rows:
        issue(f'(cross-source×{len(xs_rows)})', 'exp', 'B3b', 'high',
              'manifest/matrix 与权威逐样本 JSON 标签不一致（建议以 JSON 重derive）')
    b3['expA_manifest_type_dist'] = dict(collections.Counter(r['defect_type'] for r in S if r['source_batch'] == 'expA'))
    b3['expA_json_type_dist'] = dict(collections.Counter(d['defect_type'] for k, (_, d) in json_index.items() if k[0] == 'expA'))

    # ---------- B4 平台依赖 ----------
    b4 = collections.Counter()
    plat_by_type = collections.Counter()
    plat_no_note = []
    for rec in S:
        j = jget(rec)
        jd = j[1] if j else {}
        has_note = bool(jd.get('platform_notes'))
        dep = bool(jd.get('platform_dependent'))
        if dep or has_note:
            b4['declared'] += 1
            plat_by_type[rec['defect_type']] += 1
            if dep and not has_note:
                b4['declared_but_no_note'] += 1
                plat_no_note.append(rec['uid'])
        if rec['input_mode'] == 'code_materialized':
            b4['inline_skipped'] += 1
            continue
        text = ''
        for c in loc_files(rec):
            ls = read_lines(c)
            if ls:
                text += '\n'.join(ls)
        tok = [t for t in PLATFORM_TOKENS if t in text]
        if tok:
            b4['has_platform_token'] += 1
        if tok and not (dep or has_note):
            b4['token_no_note'] += 1
            if rec['defect_type'] in EMBEDDED | CONCURRENCY:
                b4['embedded_concurrency_token_no_note'] += 1
                plat_no_note.append(rec['uid'])
    b4['note_coverage_pct_of_1147'] = round(100.0 * b4['declared'] / len(S), 2)
    b4['top_platform_types'] = dict(plat_by_type.most_common(12))
    for uid in plat_no_note:
        issue(uid, '?', 'B4', 'low', '平台依赖迹象但无 platform_notes')

    # ---------- B5 检测器复现一致性（matrix 内部：expected vs actual） ----------
    b5 = collections.Counter()
    mism = []
    for rec in S:
        m = by_uid.get(rec['uid'])
        if not m:
            b5['no_matrix_row'] += 1
            continue
        exp, act = m.get('expected_verdict'), m.get('or_verdict_all8')
        if exp == act:
            b5['consistent'] += 1
        else:
            b5['inconsistent'] += 1
            b5[f'{exp}->{act}'] += 1
            mism.append({'uid': rec['uid'], 'batch': rec['source_batch'], 'defect_type': m.get('defect_type'),
                         'expected': exp, 'actual': act, 'hung': m.get('hung_flag'), 'kind': f'{exp}->{act}'})
    b5['inconsistent_pct'] = round(100.0 * b5['inconsistent'] / len(S), 2)
    b5['by_batch'] = dict(collections.Counter(x['batch'] for x in mism).most_common())
    b5['catch2miss_by_type'] = dict(collections.Counter(x['defect_type'] for x in mism
                                                        if x['kind'] == 'catch->miss').most_common())
    b5['catch2miss_hung'] = sum(1 for x in mism if x['kind'] == 'catch->miss' and x['hung'])
    b5['catch2miss_nonhung'] = sum(1 for x in mism if x['kind'] == 'catch->miss' and not x['hung'])
    b5['catch2miss_nonhung_ids'] = [x['uid'] for x in mism if x['kind'] == 'catch->miss' and not x['hung']]
    for x in mism:
        sev = 'high' if x['kind'] == 'catch->miss' else 'medium'
        issue(x['uid'], x['batch'], 'B5', sev, f"expected/actual 不一致 {x['kind']}",
              defect_type=x['defect_type'], hung=x['hung'])

    # ---------- B6 克隆家族标注质量 ----------
    idx = {}
    for rec in S:
        idx[rec['sample_id']] = rec
        idx[short_id(rec['source_batch'], rec['sample_id'])] = rec
    rows = []
    for f in fam.get('families', []):
        members = f.get('members') or []
        recs = [idx[m] for m in members if m in idx]
        if not recs:
            continue
        dts = collections.Counter(r['defect_type'] for r in recs)
        evs = collections.Counter(r['expected_verdict'] for r in recs)
        acts = collections.Counter((by_uid.get(r['uid']) or {}).get('or_verdict_all8') for r in recs)
        score = (len(dts) - 1) * 10 + (len(evs) - 1) * 5 + (len([k for k in acts if k]) - 1)
        rows.append({'family_id': f['family_id'], 'size': len(members), 'mapped': len(recs),
                     'n_distinct_defect_type': len(dts), 'defect_type_dist': dict(dts),
                     'expected_dist': dict(evs), 'actual_dist': {str(k): v for k, v in acts.items()},
                     'score': score, 'members': members[:25]})
    rows.sort(key=lambda x: (-x['score'], -x['size']))
    b6 = {'n_families': len(fam.get('families', [])),
          'n_multimember': sum(1 for f in fam.get('families', []) if len(f.get('members') or []) > 1),
          'n_mixed_defect_type': sum(1 for x in rows if x['n_distinct_defect_type'] > 1),
          'n_mixed_expected': sum(1 for x in rows if len(x['expected_dist']) > 1),
          'worst10': rows[:10]}
    for x in rows[:10]:
        if x['n_distinct_defect_type'] > 1:
            issue(x['family_id'], 'family', 'B6', 'medium',
                  f"家族内 defect_type 不一致 ({x['n_distinct_defect_type']} 种)",
                  size=x['size'], dist=x['defect_type_dist'])

    # ---------- 输出 ----------
    out = {'schema': 'queyi-680-audit/v1', 'generated_at': '2026-10-07', 'seed': SEED, 'sample_frac': FRAC,
           'n_universe': len(S), 'n_sampled_B2': len(sel),
           'B1': dict(b1), 'B2': dict(b2), 'B2_fail': fails, 'B2_review': reviews,
           'B3': b3, 'B4': dict(b4), 'B5': dict(b5), 'B5_mismatches': mism, 'B6': b6,
           'n_issues': len(issues), 'issues': issues}
    with open(p('data', '680_审计不合格样本清单.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print('WROTE data/680_审计不合格样本清单.json', len(issues), 'issues')
    print('== B1', json.dumps(out['B1'], ensure_ascii=False))
    print('== B2', json.dumps(out['B2'], ensure_ascii=False)[:400])
    print('== B3 cores', json.dumps({k: v for k, v in b3.items() if k not in ('dist_json', 'cross_source_rows')},
                                    ensure_ascii=False)[:700])
    print('== B3b by batch', json.dumps(b3['cross_source_mismatch_by_batch'], ensure_ascii=False))
    print('== B3b by field', json.dumps(b3['cross_source_mismatch_by_field'], ensure_ascii=False))
    print('== B3b expA manifest vs json dist')
    print('   manifest:', json.dumps(b3['expA_manifest_type_dist'], ensure_ascii=False))
    print('   json    :', json.dumps(b3['expA_json_type_dist'], ensure_ascii=False))
    print('== B4', json.dumps(out['B4'], ensure_ascii=False)[:400])
    print('== B5', json.dumps({k: v for k, v in b5.items() if k != 'catch2miss_nonhung_ids'}, ensure_ascii=False)[:600])
    print('== B6', json.dumps({k: v for k, v in b6.items() if k != 'worst10'}, ensure_ascii=False))
    print('== B2 FAIL:', [x['uid'] for x in fails])
    print('== B2 REVIEW:', [x['uid'] for x in reviews])
    print('== B6 worst10:', [(x['family_id'], x['size'], x['n_distinct_defect_type']) for x in rows[:10]])


if __name__ == '__main__':
    main()
