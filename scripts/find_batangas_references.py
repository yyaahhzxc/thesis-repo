import os

keywords = ['11_batangas', 'SC-PHIL-11', 'batangas_catv']
target_dirs = ['ground_truth', 'src/demo', 'output', 'scripts']

for d in target_dirs:
    for root, dirs, files in os.walk(d):
        for f in files:
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                for kw in keywords:
                    if kw in content or kw in f:
                        print(path, '|', kw)
                        break
            except Exception:
                pass

