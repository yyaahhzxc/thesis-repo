from pathlib import Path

# Search for GSIS real property tax documents in corpus
print("--- Searching for GSIS / Real Property Tax in corpus ---")
for p in Path("corpus").rglob("*"):
    if p.is_file() and p.suffix in [".txt", ".json"]:
        name_lower = p.name.lower()
        if "gsis" in name_lower or "226" in name_lower or "property_tax" in name_lower:
            print(f"  {p} ({p.stat().st_size:,} bytes)")

print("\n--- Searching for Watershed in corpus ---")
for p in Path("corpus").rglob("*"):
    if p.is_file() and p.suffix in [".txt", ".json"]:
        name_lower = p.name.lower()
        if "watershed" in name_lower or "panigan" in name_lower:
            print(f"  {p} ({p.stat().st_size:,} bytes)")

