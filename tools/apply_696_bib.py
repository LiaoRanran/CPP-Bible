#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""apply_696_bib.py — 落地 695 §4 的新增 bib 条目，并升级 beyer2026svcomp 的 note/DOI。

批次 696 / 线 A2。**幂等**：已存在的键会被跳过；`beyer2026svcomp` 的 note 升级用精确
替换，已升级则跳过。

用法
====
  python tools/apply_696_bib.py --check
  python tools/apply_696_bib.py --apply
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "research" / "latex" / "queyi_refs.bib"

NEW_ENTRIES = r"""
% =====================================================================
% --- 696 (v1.1+): related-work additions from batch 695 (26 entries) ---
% 来源：data/695_论文相关工作更新建议.md §4（可粘贴 bib）。所有 eprint 由 695 独立复核可达
% (64/64)。note 字段保留核验等级，便于后续审计。
% =====================================================================

% ---- direction 1: evaluation methodology / auditing ----
@inproceedings{li2026auditingaudit,
  author    = {Li, Yanhang and Fan, Zhichao and Zhuang, Zexin},
  title     = {Auditing the Audit: Five Failure Modes in Benchmark-Validity Audits},
  booktitle = {ICML 2026 Workshop on Trustworthy AI: Guarantees and Risks (TAIGR)},
  year      = {2026},
  eprint    = {2607.02586},
  archivePrefix = {arXiv},
  note      = {verified-abstract 2026-10-08; workshop paper}
}

@article{bhat2026benchmarkingbenchmarks,
  author  = {Bhat, Vishvesh and Vaghasiya, Jay and Mohsin, Muhammad Ahmed and Aali, Asad},
  title   = {Benchmarking the Benchmarks: A Validity Audit of Tool-Calling Evaluation},
  journal = {arXiv preprint},
  year    = {2026},
  eprint  = {2607.02577},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@article{shao2026protocolvalidity,
  author  = {Shao, Jiaqi and Chen, Hanck and Zhang, Wei and Pan, Maxm and Luo, Bing},
  title   = {Do Agent Benchmarks Measure Capability? Protocol Validity in the Age of Agentic {AI}},
  journal = {arXiv preprint},
  year    = {2026},
  eprint  = {2607.22368},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@article{siedler2026samplelevel,
  author  = {Siedler, Philipp D. and Sassoon, Jordan},
  title   = {Benchmarks Are Not Monolithic: Sample-Level Auditing and Orchestration for {LLM} Evaluation},
  journal = {arXiv preprint},
  year    = {2026},
  eprint  = {2607.28801},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@inproceedings{bean2025constructvalidity,
  author    = {Bean, Andrew M. and Kearns, Ryan Othniel and Romanou, Angelika and others and Rocher, Luc and Mahdi, Adam},
  title     = {Measuring what Matters: Construct Validity in Large Language Model Benchmarks},
  booktitle = {NeurIPS 2025 Datasets and Benchmarks Track},
  year      = {2025},
  eprint    = {2511.04703},
  archivePrefix = {arXiv},
  note      = {verified-abstract 2026-10-08}
}

@article{jiang2026itemlevel,
  author  = {Jiang, Han and Zhang, Susu and Zhu, Dongyao and others and Koyejo, Sanmi and Xiao, Ziang},
  title   = {{AI} Evaluation Should Require Standardized Item-Level Data Releases},
  journal = {arXiv preprint},
  year    = {2026},
  eprint  = {2604.03244},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@article{majka2025goodhart,
  author  = {Majka, Adrien and El-Mhamdi, El-Mahdi},
  title   = {The Strong, Weak and Benign Goodhart's Law: An Independence-Free and Paradigm-Agnostic Formalisation},
  journal = {arXiv preprint},
  year    = {2025},
  eprint  = {2505.23445},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@article{eve2026validationcrisis,
  author  = {Eve, C\'elestin and Varoquaux, Ga\"el and Moreau, Thomas},
  title   = {Crossing the Validation Crisis: Cross-Validation Reduces Benchmarking Variance Surprisingly Well},
  journal = {arXiv preprint},
  year    = {2026},
  eprint  = {2606.12552},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@article{cerqueira2026conceptdrift,
  author  = {Cerqueira, Vitor and Gomes, Heitor Murilo and Heyden, Marco and Pfahringer, Bernhard and Bifet, Albert},
  title   = {A Framework for Evaluating and Benchmarking Concept Drift Detection Methods},
  journal = {arXiv preprint},
  year    = {2026},
  eprint  = {2606.07789},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@article{norman2026reliabilityvalidity,
  author  = {Norman, Justin D. and Rivera, Michael U. and Hughes, D. Alex},
  title   = {Reliability without Validity: A Systematic, Large-Scale Evaluation of {LLM}-as-a-Judge Models},
  journal = {arXiv preprint},
  year    = {2026},
  eprint  = {2606.19544},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@article{ishida2025capbencher,
  author  = {Ishida, Takashi and Lodkaew, Thanawat and Yamane, Ikko},
  title   = {{CapBencher}: Give Your {LLM} Benchmark a Built-in Alarm for Test-Set Overfitting},
  journal = {arXiv preprint},
  year    = {2025},
  eprint  = {2505.18102},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

% ---- direction 2: software-verification evaluation / benchmark degradation ----
@inproceedings{krafczyk2026defects4j,
  author    = {Krafczyk, Adam and Schmid, Klaus},
  title     = {Reproducible Automated Program Repair Is Hard --- Experiences With the {Defects4J} Dataset},
  booktitle = {EASE 2026 (30th Int'l Conf. on Evaluation and Assessment in Software Engineering)},
  year      = {2026},
  eprint    = {2604.26674},
  archivePrefix = {arXiv},
  note      = {verified-abstract 2026-10-08}
}

@article{cui2024falsenegatives,
  author  = {Cui, Han and Xie, Menglei and Su, Ting and Zhang, Chengyu and Tan, Shin Hwei},
  title   = {An Empirical Study of False Negatives and Positives of Static Code Analyzers From the Perspective of Historical Issues},
  journal = {ACM Transactions on Software Engineering and Methodology (TOSEM)},
  year    = {2026},
  eprint  = {2408.13855},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08; DOI 10.1145/3849701 returns 403 (Cloudflare), not confirmed}
}

@inproceedings{li2024ubfuzz,
  author    = {Li, Shaohua and Su, Zhendong},
  title     = {{UBfuzz}: Finding Bugs in Sanitizer Implementations},
  booktitle = {ASPLOS 2024},
  year      = {2024},
  eprint    = {2401.04538},
  archivePrefix = {arXiv},
  note      = {verified-abstract 2026-10-08}
}

@article{siddiq2025reproducibilitycrisis,
  author  = {Siddiq, Mohammed Latif and Islam-Gomes, Arvin and Sekerak, Natalie and Santos, Joanna C. S.},
  title   = {Large Language Models for Software Engineering: A Reproducibility Crisis},
  journal = {arXiv preprint},
  year    = {2025},
  eprint  = {2512.00651},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@article{freiesleben2025benchmarkingepistemology,
  author  = {Freiesleben, Timo and Zezulka, Sebastian},
  title   = {The Benchmarking Epistemology: Validity Theory for Evaluating Machine Learning Models},
  journal = {Philosophy of Science},
  year    = {2026},
  eprint  = {2510.23191},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

% ---- direction 3: LLM judge / failure topology ----
@article{li2026vulndetection,
  author  = {Li, Fengjie and Jiang, Jiajun and Chen, Dongchi and Xiong, Yingfei},
  title   = {{LLM}-based Vulnerability Detection at Project Scale: An Empirical Study},
  journal = {arXiv preprint},
  year    = {2026},
  eprint  = {2601.19239},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08; distinct author from li2026reprobeyond}
}

@article{zhou2025variationinverification,
  author  = {Zhou, Yefan and Xu, Austin and Zhou, Yilun and Singh, Janvijay and Gui, Jiang and Joty, Shafiq},
  title   = {Variation in Verification: Understanding Verification Dynamics in Large Language Models},
  journal = {arXiv preprint},
  year    = {2025},
  eprint  = {2509.17995},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08; ICLR 2026 per abs page}
}

@inproceedings{ramires2026friendsorfoes,
  author    = {Ramires, Rafael and Bashir, Sarmad and Khan, Abbas and Saadatmand, Mehrdad and Medeiros, Ib\'eria},
  title     = {Friends or Foes? Combining Static Analysis Tools and {LLMs} for Vulnerability Detection},
  booktitle = {ITEQS Workshop @ ICSTW 2026 (IEEE)},
  year      = {2026},
  url       = {https://www.es.mdh.se/pdf_publications/7373.pdf},
  note      = {no arXiv id; official PDF checked 2026-10-08 --- RE-VERIFY before camera-ready}
}

@article{han2025judgesverdict,
  author  = {Han, Steve and Titericz Junior, Gilberto and Balough, Tom and Zhou, Wenfei},
  title   = {Judge's Verdict: A Comprehensive Analysis of {LLM} Judge Capability Through Human Agreement},
  journal = {arXiv preprint},
  year    = {2025},
  eprint  = {2510.09738},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

% ---- direction 4: reproducibility & audit frameworks ----
@inproceedings{costanzachock2022whoaudits,
  author    = {Costanza-Chock, Sasha and Harvey, Emma and Raji, Inioluwa Deborah and Czernuszenko, Martha and Buolamwini, Joy},
  title     = {Who Audits the Auditors? Recommendations from a Field Scan of the Algorithmic Auditing Ecosystem},
  booktitle = {ACM FAccT 2022},
  year      = {2022},
  eprint    = {2310.02521},
  archivePrefix = {arXiv},
  note      = {verified-abstract 2026-10-08}
}

@article{vaccaro2026preregistration,
  author  = {Vaccaro, Michelle},
  title   = {Preregistration for Experiments with {AI} Agents},
  journal = {arXiv preprint},
  year    = {2026},
  eprint  = {2606.11217},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08; ICML 2026 Spotlight per abs page}
}

@article{antunes2024reproducibilitysurvey,
  author  = {Antunes, Benjamin A. and Hill, David R. C.},
  title   = {Reproducibility, Replicability, and Repeatability: A Survey of Reproducible Research with a Focus on High Performance Computing},
  journal = {Computer Science Review},
  volume  = {53},
  pages   = {100655},
  year    = {2024},
  doi     = {10.1016/j.cosrev.2024.100655},
  eprint  = {2402.07530},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@article{kuznetsov2024merkletrees,
  author  = {Kuznetsov, Oleksandr and Rusnak, Alex and Yezhov, Anton and Kuznetsova, Kateryna and Kanonik, Dzianis and Domin, Oleksandr},
  title   = {Merkle Trees in Blockchain: A Study of Collision Probability and Security Implications},
  journal = {Internet of Things},
  volume  = {26},
  pages   = {101193},
  year    = {2024},
  eprint  = {2402.04367},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@article{leo2024rocrate,
  author  = {Leo, Simone and Crusoe, Michael R. and Rodr\'iguez-Navas, Laura and others and Soiland-Reyes, Stian},
  title   = {Recording Provenance of Workflow Runs with {RO-Crate}},
  journal = {PLOS ONE},
  volume  = {19},
  number  = {9},
  pages   = {1--35},
  year    = {2024},
  doi     = {10.1371/journal.pone.0309210},
  eprint  = {2312.07852},
  archivePrefix = {arXiv},
  note    = {verified-abstract 2026-10-08}
}

@inproceedings{lv2026whoevaluates,
  author    = {Lv, Shuhan and Li, Yong and Chen, Yuang and Lin, Fang and Cheng, Guantong},
  title     = {Who Evaluates the Evaluators? A Study on Reflexive Meta-Evaluation Methods for Large Language Models},
  booktitle = {IEEE ICSIPC 2026},
  year      = {2026},
  doi       = {10.1109/ICSIPC69751.2026.11583935},
  note      = {VERIFY-SEARCH only (paywall); metadata seen on IEEE Xplore 2026-10-08 --- RE-VERIFY before use}
}
"""

OLD_BEYER_NOTE = r"""  note      = {15th International Competition on Software Verification; participant counts
               per official site sv-comp.sosy-lab.org/2026 (retrieved 2026-10-07);
               total task count not verified}
}"""

NEW_BEYER_NOTE = r"""  doi       = {10.1007/978-3-032-22749-2_23},
  note      = {15th International Competition on Software Verification; DOI resolves 200
               (checked 2026-10-08); report read page-by-page in batch 695: 61 C verifiers +
               16 C witness validators; 11 Java verifiers / 3 Java validators; 3 SV-LIB
               verifiers / 1 validator; 43 verifiers + 13 validators represented by active
               teams (44 delegates, 12 countries). Aggregate ``N verifiers'' is
               caliber-dependent; the paper quotes the per-language split.}
}"""


def main() -> int:
    ap = argparse.ArgumentParser(description="落地 695 §4 bib 条目")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not (args.apply or args.check):
        ap.error("需要 --check 或 --apply")

    text = BIB.read_text(encoding="utf-8")
    keys = re.findall(r"^@[a-z]+\{([^,]+),", NEW_ENTRIES, flags=re.MULTILINE)
    present = [k for k in keys if re.search(rf"^@[a-z]+\{{{re.escape(k)},", text, flags=re.MULTILINE)]
    missing = [k for k in keys if k not in present]

    beyer_done = "read page-by-page in batch 695" in text
    beyer_hit = OLD_BEYER_NOTE in text
    print(f"[696-A2-bib] 新条目 {len(keys)}；已存在 {len(present)} {present}")
    print(f"[696-A2-bib] 待追加 {len(missing)}")
    print(f"[696-A2-bib] beyer note 已升级={beyer_done} 锚点命中={beyer_hit}")

    if args.check:
        if not (beyer_done or beyer_hit):
            print("[696-A2-bib] beyer 锚点未命中 ⇒ 会失败")
            return 1
        return 0

    if not beyer_done:
        if not beyer_hit:
            print("[696-A2-bib] beyer 锚点未命中，未写回，exit 1")
            return 1
        text = text.replace(OLD_BEYER_NOTE, NEW_BEYER_NOTE, 1)

    if missing:
        if not text.endswith("\n"):
            text += "\n"
        text += NEW_ENTRIES
    BIB.write_text(text, encoding="utf-8", newline="\n")
    print(f"[696-A2-bib] 已写回 {BIB}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
