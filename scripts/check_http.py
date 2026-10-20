"""对运行中的本地网站做HTTP验收；不使用系统代理，不发起外部请求。"""
import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from check_site import Document


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--origin', default='http://127.0.0.1:4000')
    parser.add_argument('--baseurl', default='')
    parser.add_argument('--output', default='docs/http-final.json')
    args = parser.parse_args()
    origin = args.origin.rstrip('/')
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    result = {'origin': origin, 'baseurl': args.baseurl, 'pages': [], 'resources': [], 'private_paths': [], 'errors': []}

    def get(path):
        try:
            with opener.open(origin + path, timeout=15) as response:
                return response.status, response.read().decode('utf-8', errors='replace')
        except urllib.error.HTTPError as error:
            return error.code, error.read().decode('utf-8', errors='replace')

    assets = set()
    routes = ['/'] + ['/' + lang + '/' + ('' if page == 'home' else page + '/')
                     for lang in ['zh', 'en']
                     for page in ['home', 'people', 'research', 'projects', 'publications', 'news', 'join', 'contact']]
    for route in routes:
        path = args.baseurl + route
        status, text = get(path)
        result['pages'].append({'path': path, 'status': status})
        if status != 200:
            result['errors'].append('页面返回异常: ' + path)
        doc = Document(text)
        for link in doc.links:
            url = urllib.parse.urlsplit(link)
            if not url.scheme and not url.netloc and url.path.startswith('/') and Path(url.path).suffix in ['.css', '.js', '.svg', '.jpg', '.png', '.ico']:
                assets.add(url.path)
    for path in sorted(assets):
        status, _ = get(path)
        result['resources'].append({'path': path, 'status': status})
        if status != 200:
            result['errors'].append('资源返回异常: ' + path)
    status, text = get(args.baseurl + '/this-page-does-not-exist/')
    doc = Document(text)
    result['not_found'] = {'status': status, 'lang': doc.lang, 'h1': doc.h1}
    if status != 404 or doc.lang != 'zh-CN' or doc.h1 != 1:
        result['errors'].append('实际404响应不是有效错误页')
    for path in ['/docs/SOURCES.md', '/scripts/check_site.py', '/FINAL_REPORT.md', '/Gemfile', '/.git/config']:
        status, _ = get(args.baseurl + path)
        result['private_paths'].append({'path': path, 'status': status})
        if status != 404:
            result['errors'].append('维护资料可能泄漏: ' + path)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'pages': len(result['pages']), 'resources': len(result['resources']), 'private_paths': len(result['private_paths']), 'errors': result['errors']}, ensure_ascii=False))
    raise SystemExit(1 if result['errors'] else 0)


if __name__ == '__main__':
    main()
