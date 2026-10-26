import os
import glob

print("🔍 Searching for admin frontend files...")
html_files = glob.glob("**/*.html", recursive=True)
print(f"Found HTML files: {html_files}")

# Find where admin login logic resides
for file in html_files:
    if "admin" in file.lower():
        print(f"\n--- Examining {file} ---")
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if "fetch" in content or "login" in content.lower():
                print(f"Found login/fetch references in {file}!")
                # Print snippet containing fetch
                for line in content.splitlines():
                    if "fetch" in line or "password" in line.lower() or "endpoint" in line.lower():
                        print(f"  > {line.strip()}")

