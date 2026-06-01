"""
V3: 用 Wikimedia Commons API 搜索并下载 IPA 音标音频。
通过 category 和 search 找到每个音标对应的 .ogg 文件。
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "audio", "ipa")
HEADERS = {"User-Agent": "Mozilla/5.0 (EnglishStudySite/1.0 educational)"}

# 维基百科页面标题 → 本地输出文件名（纯英文，无特殊字符）
PHONEME_PAGES = {
    # 单元音
    "Close front unrounded vowel":           "vowel_ii",
    "Near-close near-front unrounded vowel":  "vowel_i",
    "Close-mid front unrounded vowel":        "vowel_e",
    "Near-open front unrounded vowel":        "vowel_ae",
    "Open-mid back unrounded vowel":          "vowel_cup",
    "Open back unrounded vowel":             "vowel_aa",
    "Open back rounded vowel":               "vowel_o",
    "Open-mid back rounded vowel":           "vowel_oo",
    "Near-close near-back rounded vowel":     "vowel_uu",
    "Close back rounded vowel":              "vowel_u",
    "Open-mid central unrounded vowel":       "vowel_er",
    "Mid central vowel":                      "vowel_schwa",
    # 双元音 — 用近似的单元音
    # 爆破音
    "Voiceless bilabial plosive":            "cons_p",
    "Voiced bilabial plosive":               "cons_b",
    "Voiceless alveolar plosive":            "cons_t",
    "Voiced alveolar plosive":               "cons_d",
    "Voiceless velar plosive":               "cons_k",
    "Voiced velar plosive":                  "cons_g",
    # 摩擦音
    "Voiceless labiodental fricative":       "cons_f",
    "Voiced labiodental fricative":          "cons_v",
    "Voiceless dental fricative":            "cons_th",
    "Voiced dental fricative":               "cons_dh",
    "Voiceless alveolar fricative":          "cons_s",
    "Voiced alveolar fricative":             "cons_z",
    "Voiceless postalveolar fricative":       "cons_sh",
    "Voiced postalveolar fricative":          "cons_zh",
    "Voiceless glottal fricative":           "cons_h",
    # 破擦音
    "Voiceless postalveolar affricate":       "cons_tsh",
    "Voiced postalveolar affricate":          "cons_dzh",
    # 鼻音
    "Voiced bilabial nasal":                 "cons_m",
    "Voiced alveolar nasal":                 "cons_n",
    "Voiced velar nasal":                    "cons_ng",
    # 近音/边音
    "Voiced alveolar lateral approximant":    "cons_l",
    "Voiced postalveolar approximant":        "cons_r",
    "Voiced labial-velar approximant":        "cons_w",
    "Voiced palatal approximant":             "cons_j",
}

COMMONS_API = "https://commons.wikimedia.org/w/api.php"

def get_audio_url_from_page(page_title):
    """
    通过 Wikipedia API 解析页面，提取音频文件名，
    然后通过 Commons API 获取直链。
    """
    # Step 1: Wikipedia parse → 提取 File:xxx.ogg
    params = urllib.parse.urlencode({
        "action": "parse",
        "page": page_title,
        "prop": "text",
        "format": "json",
        "formatversion": "2",
    })
    url = f"https://en.wikipedia.org/w/api.php?{params}"

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        return None, f"API error: {e}"

    html = data.get("parse", {}).get("text", "")
    if not html:
        return None, "no content"

    # 找所有 File:xxx.ogg 引用
    filenames = re.findall(r'File:([^\"<>|]+\.ogg)', html)
    if not filenames:
        return None, "no ogg file found"

    # 取第一个
    fname = filenames[0].replace(" ", "_")

    # Step 2: Commons API → 获取直链
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
        req2 = urllib.request.Request(url2, headers=HEADERS)
        with urllib.request.urlopen(req2, timeout=15) as resp2:
            data2 = json.loads(resp2.read().decode())
    except Exception as e:
        return None, f"Commons API error: {e}"

    pages = data2.get("query", {}).get("pages", [])
    for p in pages:
        ii = p.get("imageinfo", [])
        if ii:
            return ii[0]["url"], fname

    return None, f"no imageinfo for {fname}"

def download(url, dest):
    """下载文件"""
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

    success, fail, skip = 0, 0, 0
    tasks = list(PHONEME_PAGES.items())

    print(f"共 {len(tasks)} 个音标页面\n")

    for i, (page_title, local_name) in enumerate(tasks, 1):
        status = f"[{i:2d}/{len(tasks)}]"
        dest = os.path.join(OUTPUT_DIR, local_name + ".ogg")

        if os.path.exists(dest) and os.path.getsize(dest) > 800:
            print(f"{status} {local_name}.ogg 已存在，跳过")
            success += 1
            continue

        print(f"{status} {local_name} ← {page_title}")
        audio_url, info = get_audio_url_from_page(page_title)

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

        time.sleep(0.3)

    # 列出已下载文件
    files = sorted(os.listdir(OUTPUT_DIR))
    ogg_files = [f for f in files if f.endswith('.ogg')]
    print(f"\n===== 成功: {success}, 失败: {fail} =====")
    print(f"已下载 {len(ogg_files)} 个 .ogg 文件:")
    for f in ogg_files:
        kb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / 1024
        print(f"  {f} ({kb:.1f} KB)")

if __name__ == "__main__":
    main()
