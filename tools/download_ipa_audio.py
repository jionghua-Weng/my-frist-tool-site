"""
批量下载 Wikipedia IPA 音标音频文件。
直接使用已知的 Wikimedia Commons URL 模式 + MD5 哈希。
"""
import hashlib
import os
import sys
import urllib.request
import urllib.error
import time

# Windows GBK 编码兼容
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "audio", "ipa")
HEADERS = {"User-Agent": "Mozilla/5.0 (EnglishStudySite/1.0 educational)"}

# Wikimedia Commons URL 规则: MD5(filename) → 取第1位/前2位/文件名
# 例: "Close_front_unrounded_vowel.ogg" MD5首字符"9"前缀"91"
# → https://upload.wikimedia.org/wikipedia/commons/9/91/Close_front_unrounded_vowel.ogg

# 所有音标对应的 Wikimedia 文件名
# 收录 44 个核心音标(含双元音)的维基音频
IPA_FILES = {
    # === 单元音 (12) 文件名来自 Wikipedia IPA vowel chart with audio ===
    "iː": "Close_front_unrounded_vowel.ogg",
    "ɪ":  "Near-close_near-front_unrounded_vowel.ogg",
    "e":  "Close-mid_front_unrounded_vowel.ogg",
    "æ":  "Near-open_front_unrounded_vowel.ogg",
    "ʌ":  "Open-mid_back_unrounded_vowel.ogg",
    "ɑː": "Open_back_unrounded_vowel.ogg",
    "ɒ":  "Open_back_rounded_vowel.ogg",
    "ɔː": "Open-mid_back_rounded_vowel.ogg",
    "ʊ":  "Near-close_near-back_rounded_vowel.ogg",
    "uː": "Close_back_rounded_vowel.ogg",
    "ɜː": "Open-mid_central_unrounded_vowel.ogg",
    "ə":  "Mid_central_vowel.ogg",
    # === 双元音 (8) — Wikipedia 无独立音频, 但有近似文件 ===
    "eɪ": "Close-mid_front_unrounded_vowel.ogg",  # 用 e 代替
    "aɪ": "Open_front_unrounded_vowel.ogg",        # 用 a 代替
    "ɔɪ": "Open-mid_back_rounded_vowel.ogg",        # 用 ɔ 代替
    "aʊ": "Open_back_unrounded_vowel.ogg",           # 用 ɑ 代替
    "əʊ": "Close-mid_back_rounded_vowel.ogg",        # 用 o 代替
    "ɪə": "Near-close_near-front_unrounded_vowel.ogg",
    "eə": "Open-mid_front_unrounded_vowel.ogg",
    "ʊə": "Near-close_near-back_rounded_vowel.ogg",
    # === 辅音 — 爆破音 ===
    "p":  "Voiceless_bilabial_plosive.ogg",
    "b":  "Voiced_bilabial_plosive.ogg",
    "t":  "Voiceless_alveolar_plosive.ogg",
    "d":  "Voiced_alveolar_plosive.ogg",
    "k":  "Voiceless_velar_plosive.ogg",
    "ɡ":  "Voiced_velar_plosive.ogg",
    # === 辅音 — 摩擦音 ===
    "f":  "Voiceless_labiodental_fricative.ogg",
    "v":  "Voiced_labiodental_fricative.ogg",
    "θ":  "Voiceless_dental_fricative.ogg",
    "ð":  "Voiced_dental_fricative.ogg",
    "s":  "Voiceless_alveolar_sibilant.ogg",
    "z":  "Voiced_alveolar_sibilant.ogg",
    "ʃ":  "Voiceless_palato-alveolar_sibilant.ogg",
    "ʒ":  "Voiced_palato-alveolar_sibilant.ogg",
    "h":  "Voiceless_glottal_fricative.ogg",
    # === 辅音 — 破擦音 ===
    "tʃ": "Voiceless_palato-alveolar_affricate.ogg",
    "dʒ": "Voiced_palato-alveolar_affricate.ogg",
    # === 辅音 — 鼻音 ===
    "m":  "Bilabial_nasal.ogg",
    "n":  "Alveolar_nasal.ogg",
    "ŋ":  "Velar_nasal.ogg",
    # === 辅音 — 近音/边音 ===
    "l":  "Alveolar_lateral_approximant.ogg",
    "r":  "Alveolar_approximant.ogg",
    "w":  "Voiced_labio-velar_approximant.ogg",
    "j":  "Palatal_approximant.ogg",
}

# 备选文件名 (当主文件名不存在时尝试)
ALT_FILES = {
    "s":  "Voiceless_alveolar_fricative.ogg",
    "z":  "Voiced_alveolar_fricative.ogg",
    "ʃ":  "Voiceless_postalveolar_fricative.ogg",
    "ʒ":  "Voiced_postalveolar_fricative.ogg",
}

FILENAME_TO_SYMBOL = {v: k for k, v in IPA_FILES.items()}

def md5_commons_url(filename):
    """根据 Wikimedia Commons MD5 命名规则构造 URL"""
    h = hashlib.md5(filename.encode()).hexdigest()
    return f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{filename}"

def try_download(url, dest):
    """尝试下载文件, 返回 True/False"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            ct = resp.headers.get("Content-Type", "")
            if "html" in ct or "text" in ct:
                return False
            data = resp.read()
            if len(data) < 800:
                return False
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(data)
            return True
    except urllib.error.HTTPError:
        return False
    except Exception as e:
        print(f"    {e}")
        return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 去重: 多个音标可能用同一文件
    downloaded = {}  # filename → sym
    success, fail, skip = 0, 0, 0

    tasks = list(IPA_FILES.items())
    print(f"共 {len(tasks)} 个音标\n")

    for i, (symbol, filename) in enumerate(tasks, 1):
        status = f"[{i:2d}/{len(tasks)}]"

        # 已下载过同一个文件
        if filename in downloaded:
            # 创建符号链接或复制
            src = os.path.join(OUTPUT_DIR, filename)
            dest = os.path.join(OUTPUT_DIR, filename)  # 同一个文件
            existing_sym = downloaded[filename]
            # 对于共享同一文件的音标, 用 .txt 记录映射
            print(f"{status} /{symbol}/ 与 /{existing_sym}/ 共用文件 → {filename}")
            skip += 1
            continue

        # 检查已存在
        dest = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(dest) and os.path.getsize(dest) > 800:
            print(f"{status} /{symbol}/ 已存在 → {filename}")
            downloaded[filename] = symbol
            success += 1
            continue

        url = md5_commons_url(filename)
        print(f"{status} /{symbol}/ → {filename}")

        if try_download(url, dest):
            kb = os.path.getsize(dest) / 1024
            print(f"    [OK] {kb:.1f} KB")
            downloaded[filename] = symbol
            success += 1
        else:
            # 尝试备选文件名
            alt = ALT_FILES.get(symbol)
            if alt and alt != filename:
                alt_url = md5_commons_url(alt)
                print(f"    主URL失败, 尝试备选: {alt}")
                if try_download(alt_url, dest):
                    kb = os.path.getsize(dest) / 1024
                    print(f"    [OK] 备选成功 {kb:.1f} KB")
                    downloaded[filename] = symbol
                    success += 1
                    time.sleep(0.3)
                    continue
            print(f"    [FAIL]")
            fail += 1

        time.sleep(0.3)

    # 保存映射表
    map_path = os.path.join(OUTPUT_DIR, "symbol_map.json")
    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(IPA_FILES, f, ensure_ascii=False, indent=2)

    print(f"\n===== 成功: {success}, 失败: {fail}, 共用: {skip} =====")
    print(f"文件输出: {OUTPUT_DIR}")
    print(f"映射表: {map_path}")

if __name__ == "__main__":
    import json
    main()
