"""
V4: 重试失败的辅音页面 + 用备选 URL 方案补充。
对 rate-limit 429 加更长延迟。
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
import hashlib

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "audio", "ipa")
HEADERS = {"User-Agent": "Mozilla/5.0 (EnglishStudySite/1.0 educational)"}

# 仍需下载的辅音（只包含之前失败/跳过的）
CONSONANTS = {
    "Voiceless bilabial plosive":             "cons_p",
    "Voiced bilabial plosive":                "cons_b",
    "Voiceless alveolar plosive":             "cons_t",
    "Voiced alveolar plosive":                "cons_d",
    "Voiceless velar plosive":                "cons_k",
    "Voiced velar plosive":                   "cons_g",
    "Voiceless labiodental fricative":        "cons_f",
    "Voiced dental fricative":                "cons_dh",
    "Voiceless alveolar fricative":           "cons_s",
    "Voiced alveolar fricative":              "cons_z",
    "Voiceless postalveolar fricative":        "cons_sh",
    "Voiced postalveolar fricative":           "cons_zh",
    "Voiceless glottal fricative":            "cons_h",
    "Voiceless postalveolar affricate":        "cons_tsh",
    "Voiced postalveolar affricate":           "cons_dzh",
    "Voiced bilabial nasal":                  "cons_m",
    "Voiced alveolar nasal":                  "cons_n",
    "Voiced velar nasal":                     "cons_ng",
    "Voiced alveolar lateral approximant":     "cons_l",
    "Voiced postalveolar approximant":         "cons_r",
    "Voiced labial-velar approximant":         "cons_w",
    "Voiced palatal approximant":              "cons_j",
}

COMMONS_API = "https://commons.wikimedia.org/w/api.php"

def md5_commons_url(filename):
    """MD5-based Wikimedia Commons URL"""
    h = hashlib.md5(filename.encode()).hexdigest()
    return f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{filename}"

def api_get_json(url, max_retries=4):
    """带重试的 API 调用"""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = (attempt + 1) * 5
                print(f"    限速429，等待 {wait}s…")
                time.sleep(wait)
            else:
                raise
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(3)
            else:
                raise
    return None

def get_audio_url(page_title):
    """通过 Wikipedia API 获取音频文件名 + 直链"""
    params = urllib.parse.urlencode({
        "action": "parse",
        "page": page_title,
        "prop": "text",
        "format": "json",
        "formatversion": "2",
    })
    url = f"https://en.wikipedia.org/w/api.php?{params}"

    try:
        data = api_get_json(url)
        if not data:
            return None, None
    except Exception as e:
        return None, f"Wiki API: {e}"

    html = data.get("parse", {}).get("text", "")
    if not html:
        return None, "no content"

    filenames = re.findall(r'File:([^\"<>|]+\.ogg)', html)
    if not filenames:
        return None, "no ogg"

    fname = filenames[0].replace(" ", "_")

    # Commons API → 直链
    params2 = urllib.parse.urlencode({
        "action": "query",
        "titles": f"File:{fname}",
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json",
        "formatversion": "2",
    })
    url2 = f"{COMMONS_API}?{params2}"

    try:
        data2 = api_get_json(url2)
        if not data2:
            return None, fname
    except Exception as e:
        return None, f"Commons API: {e}"

    pages = data2.get("query", {}).get("pages", [])
    for p in pages:
        ii = p.get("imageinfo", [])
        if ii and "url" in ii[0]:
            return ii[0]["url"], fname

    # 如果 Commons API 返回了页面但没有 imageinfo，
    # 尝试用 MD5 方案直接构造 URL
    direct = md5_commons_url(fname)
    return direct, fname + " (direct)"

def download(url, dest):
    """下载文件"""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                ct = resp.headers.get("Content-Type", "")
                if "html" in ct.lower() or "text" in ct.lower():
                    time.sleep(2)
                    continue
                data = resp.read()
                if len(data) < 800:
                    continue
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                with open(dest, "wb") as f:
                    f.write(data)
                return True
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep((attempt + 1) * 5)
            else:
                time.sleep(2)
        except Exception:
            time.sleep(3)
    return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    success, fail = 0, 0
    tasks = list(CONSONANTS.items())

    print(f"仍需下载 {len(tasks)} 个辅音音频\n")

    for i, (page_title, local_name) in enumerate(tasks, 1):
        status = f"[{i:2d}/{len(tasks)}]"
        dest = os.path.join(OUTPUT_DIR, local_name + ".ogg")

        if os.path.exists(dest) and os.path.getsize(dest) > 800:
            print(f"{status} {local_name}.ogg 已存在，跳过")
            success += 1
            continue

        print(f"{status} {local_name} ← {page_title}")
        audio_url, info = get_audio_url(page_title)

        if not audio_url:
            print(f"  [SKIP] {info}")
            fail += 1
            continue

        print(f"  → {info}")

        if download(audio_url, dest):
            kb = os.path.getsize(dest) / 1024
            print(f"  [OK] {kb:.1f} KB")
            success += 1
        else:
            print(f"  [FAIL]")
            fail += 1

        time.sleep(2)  # 每次间隔 2 秒，避免限速

    # 统计
    all_files = sorted([f for f in os.listdir(OUTPUT_DIR) if f.endswith('.ogg')])
    print(f"\n===== 本轮: {success} 成功, {fail} 失败 =====")
    print(f"目录共 {len(all_files)} 个 .ogg 文件")
    total_kb = sum(os.path.getsize(os.path.join(OUTPUT_DIR, f)) for f in all_files) / 1024
    print(f"总大小: {total_kb:.0f} KB")

if __name__ == "__main__":
    main()
