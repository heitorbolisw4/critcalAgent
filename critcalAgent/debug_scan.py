import os
from critcalAgent import scan_directory

target_path = r"Coloque aqui o caminho do seu projeto"

print(f"Testing access to: {target_path}")
if os.path.exists(target_path):
    print("Path exists.")
    files = scan_directory(target_path)
    print(f"Found {len(files)} files:")
    for f in files:
        print(f" - {f}")
else:
    print("Path does NOT exist.")
