import os, glob, json
d = "data/expansion_676cC"
for i in (99, 100, 107, 114):
    files = sorted(os.path.basename(x) for x in glob.glob(os.path.join(d, "sample_%03d*" % i)))
    j = json.load(open(os.path.join(d, "sample_%03d.json" % i), encoding="utf-8"))
    src = j["source_files"]
    miss = [f for f in src if not os.path.exists(os.path.join(d, f))]
    print("sample_%03d files=%s" % (i, files))
    print("  source_files=%s defect_line=%s missing=%s" % (src, j["defect_location"]["line"], miss))
