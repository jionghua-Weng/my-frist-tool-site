#!/usr/bin/env python3
"""移动端基础审计。"""
import os
import re

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'404.html', 'google7d301929e65a4f2c.html', 'baidu_verify_codeva-uvo9gEjPEy.html'}

issues = []
ok_count = 0
total = 0

for fname in sorted(os.listdir(SITE_DIR)):
    if not fname.endswith('.html'): continue
    if fname in SKIP: continue
    total += 1
    fpath = os.path.join(SITE_DIR, fname)
    html = open(fpath, encoding='utf-8').read()
    page_ok = True

    # 检查 viewport
    if 'viewport' not in html or 'width=device-width' not in html:
        issues.append((fname, '缺 viewport'))
        page_ok = False

    # 检查汉堡菜单
    if 'hamburger' not in html:
        issues.append((fname, '缺汉堡菜单（移动端导航）'))
        page_ok = False

    # 检查媒体查询
    if '@media' not in html or 'max-width' not in html:
        issues.append((fname, '缺响应式媒体查询'))
        page_ok = False

    # 检查 -webkit-text-size-adjust
    if 'text-size-adjust' not in html:
        issues.append((fname, '缺 text-size-adjust（iOS字体缩放）'))
        page_ok = False

    if page_ok:
        ok_count += 1

print(f"总检查: {total} 页")
print(f"四项全过: {ok_count}")
print(f"有问题的: {len(issues)}\n")

if issues:
    for fname, msg in issues:
        print(f"  {fname:<50} {msg}")
else:
    print("全站无移动端基础问题")
