#!/usr/bin/env python3
"""为文章页批量添加结构化数据 (Article + BreadcrumbList)。"""
import re
import os
import json
import html.parser

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 前缀 → (分类名, 分类页)
CATEGORY_MAP = {
    'grammar':    ('语法精讲', 'grammar.html'),
    'vocabulary': ('词汇辨析', 'vocabulary.html'),
    'patterns':   ('实用句型', 'patterns.html'),
    'daily':      ('场景口语', 'daily.html'),
    'pronunciation': ('发音诊所', 'pronunciation.html'),
    'handbook':   ('语法魔典', 'handbook.html'),
}

# 跳过这些文件
SKIP_FILES = {
    'index.html', '404.html', 'about.html', 'contact.html', 'privacy.html',
    'family-preview.html', 'learning-path-preview.html',
    'quiz-preview.html', 'pronunciation-demo.html', 'pronunciation-test.html',
    'og-image-generator.html',
    'google7d301929e65a4f2c.html',
    'baidu_verify_bdunion.txt',  # not html
    'baidu_verify_codeva-uvo9gEjPEy.html',
}

# 分类页（已有基础 schema）
CATEGORY_PAGES = {'grammar.html', 'vocabulary.html', 'patterns.html', 'daily.html', 'pronunciation.html', 'handbook.html'}


def parse_sitemap():
    """从 sitemap 提取 URL → lastmod 映射。"""
    sm = os.path.join(SITE_DIR, 'sitemap.xml')
    if not os.path.exists(sm):
        return {}
    text = open(sm, encoding='utf-8').read()
    mapping = {}
    for m in re.finditer(r'<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>', text):
        loc = m.group(1).rstrip('/')
        filename = loc.split('/')[-1]
        mapping[filename] = m.group(2)
    return mapping


def extract_meta(filepath):
    """提取 title, description, canonical 等。"""
    html_text = open(filepath, encoding='utf-8').read()

    title_match = re.search(r'<title>([^<]*)</title>', html_text)
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html_text)
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', html_text)

    title_full = title_match.group(1) if title_match else ''
    # 去掉 " — 分类名 | 英语研习社" 后缀
    headline = re.sub(r'\s*[—|–—\-]\s*[^|]+\s*\|.*$', '', title_full).strip()

    description = desc_match.group(1) if desc_match else ''
    canonical = canonical_match.group(1) if canonical_match else ''

    return headline, description, canonical


def get_category(filename):
    """根据文件名判断分类。"""
    for prefix, info in CATEGORY_MAP.items():
        if filename.replace('.html', '').startswith(prefix + '-'):
            return info
    return None


def gen_article_jsonld(headline, description, canonical, date_str, cat_name, cat_url):
    """生成 Article + BreadcrumbList JSON-LD。"""
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": headline,
                "description": description,
                "url": canonical,
                "datePublished": date_str,
                "dateModified": date_str,
                "author": {"@type": "Organization", "name": "英语研习社"},
                "publisher": {"@type": "Organization", "name": "英语研习社"},
                "image": "https://easyeng.club/og-image.png?v=2",
                "mainEntityOfPage": {"@id": canonical},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://easyeng.club/"},
                    {"@type": "ListItem", "position": 2, "name": cat_name, "item": f"https://easyeng.club/{cat_url}"},
                    {"@type": "ListItem", "position": 3, "name": headline},
                ],
            },
        ]
    }
    return json.dumps(ld, ensure_ascii=False)


def gen_collectionpage_jsonld(cat_name, canonical_url, description):
    """升级分类页 schema。"""
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "name": "英语研习社", "url": "https://easyeng.club"},
            {
                "@type": "CollectionPage",
                "name": cat_name,
                "description": description,
                "url": canonical_url,
                "mainEntityOfPage": {"@id": canonical_url},
            },
        ]
    }
    return json.dumps(ld, ensure_ascii=False)


def has_article_schema(html_text):
    """判断是否已有 Article 或 BreadcrumbList 结构化数据。"""
    return 'Article' in html_text or 'BreadcrumbList' in html_text


def process_articles(dry_run=True):
    """处理所有文章页。"""
    dates = parse_sitemap()
    files = sorted(
        f for f in os.listdir(SITE_DIR)
        if f.endswith('.html') and f not in SKIP_FILES and f not in CATEGORY_PAGES
        and get_category(f) is not None
    )

    results = []
    for fname in files:
        fpath = os.path.join(SITE_DIR, fname)
        html_text = open(fpath, encoding='utf-8').read()

        if has_article_schema(html_text):
            results.append(('SKIP', fname, '已有结构化数据'))
            continue

        cat_info = get_category(fname)
        if not cat_info:
            results.append(('SKIP', fname, '无匹配分类'))
            continue
        cat_name, cat_url = cat_info

        headline, description, canonical = extract_meta(fpath)
        if not headline or not description:
            results.append(('SKIP', fname, f'缺元数据 headline={bool(headline)} desc={bool(description)}'))
            continue

        date_str = dates.get(fname, '2026-05-16')
        jsonld = gen_article_jsonld(headline, description, canonical, date_str, cat_name, cat_url)
        script_tag = f'<script type="application/ld+json">{jsonld}</script>'

        if dry_run:
            results.append(('ADD', fname, f'{headline[:30]}... | {date_str}'))
        else:
            # 在 </head> 前插入
            new_html = html_text.replace('</head>', f'{script_tag}\n</head>', 1)
            if new_html == html_text:
                results.append(('ERR', fname, '找不到 </head>'))
                continue
            open(fpath, 'w', encoding='utf-8').write(new_html)
            results.append(('DONE', fname, f'{headline[:30]}... | {date_str}'))

    return results


def process_categories(dry_run=True):
    """升级分类页 schema。"""
    results = []
    for fname, (cat_name, _) in CATEGORY_MAP.items():
        fpath = os.path.join(SITE_DIR, f'{fname}.html')
        if not os.path.exists(fpath):
            results.append(('SKIP', f'{fname}.html', '文件不存在'))
            continue

        html_text = open(fpath, encoding='utf-8').read()
        if 'CollectionPage' in html_text:
            results.append(('SKIP', f'{fname}.html', '已有 CollectionPage'))
            continue

        _, description, canonical = extract_meta(fpath)
        jsonld = gen_collectionpage_jsonld(cat_name, canonical, description)
        script_tag = f'<script type="application/ld+json">{jsonld}</script>'

        if dry_run:
            results.append(('UPGRADE', f'{fname}.html', f'{cat_name}'))
        else:
            # 替换旧的 WebSite-only schema
            old_script = re.search(
                r'<script type="application/ld\+json">.*?</script>',
                html_text, re.DOTALL
            )
            if old_script:
                new_html = html_text.replace(old_script.group(0), script_tag, 1)
            else:
                new_html = html_text.replace('</head>', f'{script_tag}\n</head>', 1)
            open(fpath, 'w', encoding='utf-8').write(new_html)
            results.append(('DONE', f'{fname}.html', f'{cat_name}'))

    return results


def audit():
    """审计：统计全站结构化数据覆盖情况。"""
    results = []
    for fname in sorted(os.listdir(SITE_DIR)):
        if not fname.endswith('.html'):
            continue
        if fname in SKIP_FILES:
            continue
        fpath = os.path.join(SITE_DIR, fname)
        html_text = open(fpath, encoding='utf-8').read()
        has_ld = 'application/ld+json' in html_text
        has_article = 'Article' in html_text
        has_breadcrumb = 'BreadcrumbList' in html_text
        has_collection = 'CollectionPage' in html_text
        has_website = 'WebSite' in html_text
        results.append((fname, has_ld, has_article, has_breadcrumb, has_collection, has_website))
    return results


def print_audit_table(results):
    print(f"\n{'文件名':<45} {'LD':>4} {'Article':>8} {'Bread':>7} {'Collection':>11} {'WebSite':>8}")
    print('-' * 90)
    total = 0
    with_ld = 0
    with_article = 0
    with_breadcrumb = 0
    for r in results:
        fname, has_ld, has_article, has_breadcrumb, has_collection, has_website = r
        total += 1
        if has_ld: with_ld += 1
        if has_article: with_article += 1
        if has_breadcrumb: with_breadcrumb += 1
        print(f"{fname:<45} {'OK' if has_ld else '--':>4} {'OK' if has_article else '--':>8} {'OK' if has_breadcrumb else '--':>7} {'OK' if has_collection else '--':>11} {'OK' if has_website else '--':>8}")
    print(f"\n总计: {total} 页, 有结构化数据: {with_ld}, Article: {with_article}, Breadcrumb: {with_breadcrumb}")


if __name__ == '__main__':
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else 'dry'

    if mode == 'dry':
        print("=== 干跑模式 ===")
        print("\n【文章页】")
        for action, fname, detail in process_articles(dry_run=True):
            print(f"  {action:>6}  {fname:<45}  {detail}")
        print(f"\n【分类页】")
        for action, fname, detail in process_categories(dry_run=True):
            print(f"  {action:>6}  {fname:<45}  {detail}")

    elif mode == 'run':
        print("=== 执行模式 ===")
        arts = process_articles(dry_run=False)
        cats = process_categories(dry_run=False)
        all_results = arts + cats
        done = sum(1 for a, _, _ in all_results if a == 'DONE')
        skip = sum(1 for a, _, _ in all_results if a == 'SKIP')
        errors = sum(1 for a, _, _ in all_results if a == 'ERR')
        print(f"\n完成: {done}  跳过: {skip}  错误: {errors}")

    elif mode == 'audit':
        print_audit_table(audit())

    else:
        print(f"用法: python {sys.argv[0]} [dry|run|audit]")
