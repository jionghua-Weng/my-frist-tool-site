#!/usr/bin/env python3
"""P1紧急修复：sitemap补94条URL + 93页补百度统计"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026-06-23"
BAIDU_SCRIPT = """<script>
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?2efc7dcf0f75f8ae13f0a486a1cf070a";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>"""

def get_listening_pages():
    """获取所有听力课页面文件名"""
    listening_dir = os.path.join(ROOT, "listening")
    files = sorted(f for f in os.listdir(listening_dir) if f.endswith(".html"))
    return files

def fix_sitemap():
    """在sitemap.xml末尾(</urlset>前)插入新URL"""
    sitemap_path = os.path.join(ROOT, "sitemap.xml")
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 收集要新增的URL
    new_urls = []

    # hearing index page
    new_urls.append(("listening.html", 0.8))

    # 92 hearing lesson pages
    for f in get_listening_pages():
        new_urls.append((f"listening/{f}", 0.7))

    # learning-path + phonics
    new_urls.append(("learning-path.html", 0.7))
    new_urls.append(("pronunciation-phonics.html", 0.7))

    # 构建XML片段
    lines = []
    for path, priority in new_urls:
        url = f"https://easyeng.club/{path}"
        lines.append(f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{priority}</priority></url>')

    new_block = "\n".join(lines)

    # 插入到</urlset>前
    content = content.replace("</urlset>", new_block + "\n</urlset>")

    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[sitemap] 已加入 {len(new_urls)} 条新URL → {sitemap_path}")

def fix_baidu_stats():
    """给指定页面在</head>前插入百度统计脚本"""
    listening_dir = os.path.join(ROOT, "listening")
    files_to_fix = [os.path.join(listening_dir, f) for f in get_listening_pages()]
    files_to_fix.append(os.path.join(ROOT, "learning-path.html"))

    count = 0
    for filepath in files_to_fix:
        if not os.path.exists(filepath):
            print(f"  [跳过] 文件不存在: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if "hm.baidu.com" in content:
            print(f"  [跳过] 已有百度统计: {os.path.basename(filepath)}")
            continue

        # 在第一个</head>前插入
        content = content.replace("</head>", BAIDU_SCRIPT + "\n</head>", 1)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        count += 1
        print(f"  [完成] {os.path.relpath(filepath, ROOT)}")

    print(f"\n[百度统计] 已处理 {count} 个文件")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--sitemap-only":
        fix_sitemap()
    elif len(sys.argv) > 1 and sys.argv[1] == "--baidu-only":
        fix_baidu_stats()
    else:
        fix_sitemap()
        print()
        fix_baidu_stats()
