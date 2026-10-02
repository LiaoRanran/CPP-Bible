#!/usr/bin/env python3
"""673i ref/label consistency analysis for the NeurIPS paper (queyi_neurips2027_v1.1.tex).

Finds:
  (1) float labels (fig:/tab:) never referenced by ANY \\ref anywhere
  (2) \\ref to a fig:/tab: label that is never \\label'ed (undefined)
  (3) which of the above float labels are referenced from the MAIN BODY
      (before \\label{page:endmain})

Usage:
  python data/673i_analyze_refs.py
"""
import re
import sys

path = "research/latex/queyi_neurips2027_v1.1.tex"
with open(path, encoding="utf-8") as fh:
    lines = fh.readlines()

endmain = None
for i, ln in enumerate(lines):
    if r"\label{page:endmain}" in ln:
        endmain = i
        break
print(f"page:endmain at line {endmain + 1}")

label_re = re.compile(r"\\label\{([^}]+)\}")
labels = {}
for i, ln in enumerate(lines):
    for m in label_re.finditer(ln):
        labels[m.group(1)] = i + 1

ref_re = re.compile(r"\\(?:ref|cref|Cref)\{([^}]+)\}")
refs = {}
for i, ln in enumerate(lines):
    for m in ref_re.finditer(ln):
        refs.setdefault(m.group(1), []).append(i + 1)

float_labels = {k: v for k, v in labels.items() if k.startswith("fig:") or k.startswith("tab:")}
print(f"\nTotal labels: {len(labels)}; float labels (fig:/tab:): {len(float_labels)}")

print("\n=== FLOAT LABEL REFERENCE MAP ===")
undef = []
never_ref = []
body_not_ref = []
for name in sorted(float_labels):
    defline = float_labels[name]
    rlines = refs.get(name, [])
    body_rlines = [r for r in rlines if r <= endmain + 1]
    if not rlines:
        never_ref.append(name)
    if not body_rlines:
        body_not_ref.append(name)
    print(f"  {name:16s} defined@{defline:4d}  refs={rlines if rlines else 'NONE'}  body_refs={body_rlines if body_rlines else 'NONE'}")

print("\n=== UNDEFINED FIG/TAB REFERENCES (ref but no label) ===")
for name in sorted(refs):
    if (name.startswith("fig:") or name.startswith("tab:")) and name not in labels:
        undef.append(name)
        print(f"  \\ref{{{name}}} at {refs[name]}  -> NO \\label found")
if not undef:
    print("  (none)")

print("\n=== SUMMARY ===")
print(f"floats never referenced anywhere ({len(never_ref)}): {never_ref}")
print(f"floats not referenced from BODY ({len(body_not_ref)}): {body_not_ref}")
print(f"undefined fig/tab refs ({len(undef)}): {undef}")
