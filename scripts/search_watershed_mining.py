import os

target = "corpus/cleaned/local/cleaned_transcriptions"
found = []

for root, dirs, files in os.walk(target):
    for f in files:
        if f.endswith(".txt"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                t = fp.read()
            if "watershed" in t.lower() or "panigan" in t.lower() or "mining" in t.lower():
                found.append((f, len(t), "watershed" in t.lower(), "mining" in t.lower()))

print(f"Total matching files found: {len(found)}")
for fname, size, has_w, has_m in found[:20]:
    print(f"{fname:<50} | size: {size:<8} | watershed: {has_w} | mining: {has_m}")

