"""
批量下载 IPA 音标音频 - v2。
从 Wikipedia "IPA vowel chart with audio" 和 "IPA consonant chart with audio"
页面直接提取所有 .ogg/.mp3 音频 URL 并下载。
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "audio", "ipa")
HEADERS = {"User-Agent": "Mozilla/5.0 (EnglishStudySite/1.0)"}

WIKI_API = "https://en.wikipedia.org/w/api.php"

# IPA 图表页面 —— 每个页面包含大量嵌入的音频文件
CHART_PAGES = [
    "IPA vowel chart with audio",
    "IPA consonant chart with audio",
    "IPA pulmonic consonant chart with audio",
]

def api_get(params):
    """调用 Wikipedia API"""
    qs = urllib.parse.urlencode(params)
    url = f"{WIKI_API}?{qs}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())

def extract_ogg_urls(html_text):
    """从 HTML 中提取所有 .ogg 音频直链"""
    # 模式1: https://upload.wikimedia.org/wikipedia/commons/.../xxx.ogg
    urls = re.findall(r'(https?://upload\.wikimedia\.org/wikipedia/commons/[^"\s<>]+\.ogg)', html_text)
    # 模式2: protocol-relative
    urls += ['https:' + u for u in re.findall(r'(?<!")(//upload\.wikimedia\.org/wikipedia/commons/[^"\s<>]+\.ogg)', html_text)]
    return list(set(urls))

def download(url, dest):
    """下载文件，返回 True/False"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            ct = resp.headers.get("Content-Type", "")
            if "html" in ct.lower() or "text" in ct.lower():
                return False
            data = resp.read()
            if len(data) < 800:
                return False
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(data)
            return True
    except Exception as e:
        return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_urls = []

    for page in CHART_PAGES:
        print(f"从页面提取音频: {page}")
        try:
            data = api_get({
                "action": "parse",
                "page": page,
                "prop": "text",
                "format": "json",
            })
            html = data.get("parse", {}).get("text", {}).get("*", "")
            urls = extract_ogg_urls(html)
            print(f"  找到 {len(urls)} 个音频文件")
            all_urls.extend(urls)
        except Exception as e:
            print(f"  [ERROR] {e}")

    all_urls = list(set(all_urls))
    print(f"\n共 {len(all_urls)} 个不重复的音频 URL\n")

    success, fail = 0, 0
    for i, url in enumerate(sorted(all_urls), 1):
        # 从 URL 提取文件名
        fname = url.split("/")[-1]
        dest = os.path.join(OUTPUT_DIR, fname)
        status = f"[{i:2d}/{len(all_urls)}]"

        if os.path.exists(dest) and os.path.getsize(dest) > 800:
            print(f"{status} {fname} 已存在")
            success += 1
            continue

        print(f"{status} {fname}")
        if download(url, dest):
            kb = os.path.getsize(dest) / 1024
            print(f"    [OK] {kb:.1f} KB")
            success += 1
        else:
            print(f"    [FAIL]")
            fail += 1
        time.sleep(0.2)

    print(f"\n===== 成功: {success}, 失败: {fail} =====")
    print(f"输出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
