"""检查构建产物的内部链接、资源、双语页面和语言切换，失败时返回非零。"""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.lang = None
        self.h1 = 0
        self.lang_links = []
        self.canonical = []
        self.alternates = []
        self.titles = []
        self.in_title = False
        self.meta = {}
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.in_title = True
            self.titles.append('')
        if tag == 'meta':
            key = attrs.get('name') or attrs.get('property')
            self.meta.setdefault(key, []).append(attrs.get('content', ''))
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'h1':
            self.h1 += 1
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag in ['a', 'link'] and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag in ['img', 'script'] and 'src' in attrs:
            self.links.append(attrs['src'])
        if tag == 'a' and 'hreflang' in attrs:
            self.lang_links.append(attrs['href'])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs.get('href'))
        if tag == 'link' and attrs.get('rel') == 'alternate' and attrs.get('hreflang'):
            self.alternates.append(attrs.get('href'))

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.titles[-1] += data


def keys(value, prefix=''):
    result = set()
    if isinstance(value, dict):
        for key, item in value.items():
            result |= keys(item, prefix + '.' + key)
    elif isinstance(value, list):
        for i, item in enumerate(value):
            result |= keys(item, prefix + '.' + str(i))
    else:
        result.add(prefix)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', default='_site')
    parser.add_argument('--baseurl', default='')
    parser.add_argument('--expected-origin', default='')
    parser.add_argument('--expected-verification', default='')
    args = parser.parse_args()
    root = Path(args.site).resolve()
    source = Path(__file__).resolve().parents[1]
    errors = []
    documents = {}
    checked_links = 0
    expected_sitemap_urls = set()
    page_titles = set()
    page_descriptions = set()
    files = sorted(root.rglob('*.html'))
    if not files:
        raise SystemExit('未找到构建后的 HTML，请先运行 jekyll build。')
    for path in files:
        text = path.read_text(encoding='utf-8')
        documents[path] = Document(text)
        if re.search(r'Lorem ipsum|your-lab|Dave Bunten|CytoTable|\{%|\{\{', text):
            errors.append(f'残留示例或未解析模板: {path.relative_to(root)}')
    missing_page = documents.get(root / '404.html')
    if not missing_page or missing_page.lang != 'zh-CN' or missing_page.h1 != 1:
        errors.append('404 页面必须是有效的双语 HTML，具有 lang 和一个 h1')
    for private_path in ['README.html', 'TODO.html', 'FINAL_REPORT.html', 'FINAL_REPORT.md', 'docs', 'scripts', 'vendor']:
        if (root / private_path).exists():
            errors.append('维护资料不应进入发布产物: ' + private_path)
    for path, doc in documents.items():
        for href in doc.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            checked_links += 1
            url_path = unquote(url.path)
            if url_path.startswith('/'):
                if args.baseurl and not url_path.startswith(args.baseurl + '/'):
                    errors.append(f'缺少 baseurl: {href}')
                    continue
                url_path = url_path[len(args.baseurl):] if args.baseurl else url_path
                target = root / url_path.lstrip('/')
            else:
                target = path.parent / url_path if url_path else path
            if target.is_dir():
                target = target / 'index.html'
            target = target.resolve()
            if not target.is_relative_to(root) or not target.exists():
                errors.append(f'失效链接: {path.relative_to(root)} -> {href}')
            elif url.fragment and target.suffix == '.html':
                target_doc = documents.get(target)
                if target_doc and unquote(url.fragment) not in target_doc.ids:
                    errors.append(f'失效锚点: {path.relative_to(root)} -> {href}')
    for lang, html_lang in [('zh', 'zh-CN'), ('en', 'en')]:
        for key in ['home', 'people', 'research', 'projects', 'publications', 'news', 'join', 'contact']:
            suffix = '' if key == 'home' else key + '/'
            path = root / lang / suffix / 'index.html'
            doc = documents.get(path)
            if not doc:
                errors.append(f'缺少页面: {lang}/{suffix}')
                continue
            if doc.lang != html_lang or doc.h1 != 1:
                errors.append(f'语言或 h1 异常: {lang}/{suffix}: {doc.lang}, {doc.h1}')
            title = doc.titles[0].strip() if len(doc.titles) == 1 else ''
            descriptions = doc.meta.get('description', [])
            description = descriptions[0].strip() if len(descriptions) == 1 else ''
            if not title or title in page_titles or not description or description in page_descriptions:
                errors.append(f'标题或描述缺失、重复: {lang}/{suffix}')
            page_titles.add(title)
            page_descriptions.add(description)
            if doc.meta.get('og:title') != [title] or doc.meta.get('og:description') != [description]:
                errors.append(f'Open Graph 与页面元数据不一致: {lang}/{suffix}')
            if any('noindex' in value.lower() for value in doc.meta.get('robots', []) + doc.meta.get('googlebot', [])):
                errors.append(f'正式页面不应禁止收录: {lang}/{suffix}')
            other = 'en' if lang == 'zh' else 'zh'
            expected = args.baseurl + '/' + other + '/' + suffix
            if expected not in doc.lang_links:
                errors.append(f'语言切换未对应当前页: {lang}/{suffix}')
            if args.expected_origin:
                origin = args.expected_origin.rstrip('/')
                canonical = origin + args.baseurl + '/' + lang + '/' + suffix
                alternate = origin + expected
                expected_sitemap_urls.add(canonical)
                if doc.canonical != [canonical] or alternate not in doc.alternates:
                    errors.append(f'生产 canonical/hreflang 错误: {lang}/{suffix}')
                if doc.meta.get('og:url') != [canonical]:
                    errors.append(f'Open Graph 地址错误: {lang}/{suffix}')
    if args.expected_verification:
        verification_pages = [root / 'index.html'] + [root / lang / ('' if key == 'home' else key) / 'index.html'
            for lang in ['zh', 'en']
            for key in ['home', 'people', 'research', 'projects', 'publications', 'news', 'join', 'contact']]
        for path in verification_pages:
            doc = documents.get(path)
            if not doc or doc.meta.get('google-site-verification') != [args.expected_verification]:
                errors.append(f'Google 验证标记缺失或重复: {path.relative_to(root)}')
    if args.expected_origin:
        root_doc = documents.get(root / 'index.html')
        if not root_doc or root_doc.canonical != [args.expected_origin.rstrip('/') + args.baseurl + '/zh/']:
            errors.append('根入口 canonical 应指向中文首页')
    if args.expected_origin:
        try:
            sitemap = ElementTree.parse(root / 'sitemap.xml')
            locations = {node.text for node in sitemap.iter() if node.tag.endswith('}loc')}
            if not expected_sitemap_urls <= locations:
                errors.append('sitemap 缺少正式中英文页面')
            prefix = args.expected_origin.rstrip('/') + args.baseurl + '/'
            if any(not (url or '').startswith(prefix) for url in locations):
                errors.append('sitemap 含有错误域名或子路径')
        except (OSError, ElementTree.ParseError) as error:
            errors.append('sitemap 无法解析: ' + str(error))
    zh = json.loads((source / '_data/locales/zh.json').read_text(encoding='utf-8'))
    en = json.loads((source / '_data/locales/en.json').read_text(encoding='utf-8'))
    if keys(zh) != keys(en):
        errors.append('中英文 locale 键不一致: ' + str(keys(zh) ^ keys(en)))
    publications = json.loads((source / '_data/publications.json').read_text(encoding='utf-8'))
    if len({item['doi'] for item in publications}) != len(publications):
        errors.append('存在重复 DOI')
    for item in publications:
        if not all(item.get(key) for key in ['title', 'doi', 'year', 'authors', 'venue', 'source']):
            errors.append('论文字段缺失: ' + item.get('id', '?'))
    result = {'html_pages': len(documents), 'internal_links_and_assets': checked_links,
              'bilingual_routes': 16, 'baseurl': args.baseurl,
              'expected_origin': args.expected_origin, 'errors': errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == '__main__':
    main()
