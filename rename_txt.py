import os

files = sorted([f for f in os.listdir(".") if f.endswith(".txt")])

for i, name in enumerate(files, start=1):
    new_name = f"笔记{i}.txt"
    if name == new_name:
        continue
    if os.path.exists(new_name):
        print(f"跳过：{new_name} 已存在")
        continue
    os.rename(name, new_name)
    print(f"{name} → {new_name}")

print("完成。")
