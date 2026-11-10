import sys
sys.path.insert(0, ".")
from src.demo.app import resolve_statute_passage

t1, s1 = resolve_statute_passage("Republic Act No. 7160 §143(f)")
print("=== RA 7160 §143(f) ===")
print(s1)

t2, s2 = resolve_statute_passage("Republic Act No. 8791 §3")
print("\n=== RA 8791 §3 ===")
print(s2)

