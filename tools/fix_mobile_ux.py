"""
批量修复全站移动端体验问题:
1. .recent-row 加 -webkit-overflow-scrolling: touch (iOS平滑滚动)
2. .audio-btn 28px → 36px (触控目标)
3. .hamburger / .theme-toggle / .srch-btn 加 min-width/min-height: 44px
4. .mobile-panel height:100vh → bottom:0 (iOS Safari兼容)
"""
import os
import sys
import io

# Windows GBK 兼容
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FIXES = [
    # 1. iOS 平滑滚动 (仅 index.html)
    {
        "old": ".recent-row{display:flex;gap:16px;overflow-x:auto;padding-bottom:8px}",
        "new": ".recent-row{display:flex;gap:16px;overflow-x:auto;padding-bottom:8px;-webkit-overflow-scrolling:touch}",
        "desc": "recent-row iOS平滑滚动",
    },
    # 2. 音频按钮扩大触控面积
    {
        "old": ".audio-btn{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;margin-left:8px;background:var(--accent);color:#fff;border:none;border-radius:50%;cursor:pointer;font-size:14px;flex-shrink:0;vertical-align:middle;transition:background .2s,transform .15s}",
        "new": ".audio-btn{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;margin-left:8px;background:var(--accent);color:#fff;border:none;border-radius:50%;cursor:pointer;font-size:16px;flex-shrink:0;vertical-align:middle;transition:background .2s,transform .15s}",
        "desc": "audio-btn 36px触控目标",
    },
    # 3a. 汉堡菜单触控目标
    {
        "old": ".hamburger{display:none;background:none;border:none;cursor:pointer;padding:8px;flex-direction:column;gap:5px}",
        "new": ".hamburger{display:none;background:none;border:none;cursor:pointer;padding:8px;flex-direction:column;gap:5px;min-width:44px;min-height:44px}",
        "desc": "hamburger 44px触控目标",
    },
    # 3b. 主题切换触控目标
    {
        "old": ".theme-toggle{background:none;border:none;cursor:pointer;padding:6px 8px;color:var(--white);display:flex;align-items:center;flex-shrink:0}",
        "new": ".theme-toggle{background:none;border:none;cursor:pointer;padding:6px 8px;color:var(--white);display:flex;align-items:center;flex-shrink:0;min-width:44px;min-height:44px}",
        "desc": "theme-toggle 44px触控目标",
    },
    # 3c. 搜索按钮触控目标
    {
        "old": ".srch-btn{background:none;border:none;cursor:pointer;padding:6px 8px;margin-left:4px;color:#fff;display:flex;align-items:center;border-radius:6px;transition:background .2s}",
        "new": ".srch-btn{background:none;border:none;cursor:pointer;padding:6px 8px;margin-left:4px;color:#fff;display:flex;align-items:center;border-radius:6px;transition:background .2s;min-width:44px;min-height:44px}",
        "desc": "srch-btn 44px触控目标",
    },
    # 4. 移动面板 iOS Safari 兼容
    {
        "old": "height:100vh;background:var(--navy);z-index:201",
        "new": "bottom:0;background:var(--navy);z-index:201",
        "desc": "mobile-panel bottom:0 替代 100vh",
    },
]

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    for fix in FIXES:
        if fix["old"] in content:
            content = content.replace(fix["old"], fix["new"])
            modified = True
            print(f"  ✓ {fix['desc']}")
        # 静默跳过不适用的修复

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    html_files = sorted(
        f for f in os.listdir(ROOT) if f.endswith(".html")
    )
    total = 0
    for fname in html_files:
        filepath = os.path.join(ROOT, fname)
        if fix_file(filepath):
            print(f"  → {fname} 已更新")
            total += 1

    print(f"\n共更新 {total} 个文件")

if __name__ == "__main__":
    main()
