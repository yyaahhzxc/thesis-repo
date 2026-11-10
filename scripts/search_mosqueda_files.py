import os

for root, dirs, files in os.walk("corpus"):
    for f in files:
        if "0309" in f or "mosqueda" in f.lower():
            print(os.path.join(root, f))

for root, dirs, files in os.walk("data"):
    for f in files:
        if "0309" in f or "mosqueda" in f.lower():
            print(os.path.join(root, f))

