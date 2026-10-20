"""通过已安装的 agent-browser 验证实际渲染、交互和响应式布局。"""
import base64
import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = shutil.which('agent-browser.cmd') or shutil.which('agent-browser')
SESSION = 'ustb-final'
BASE = 'http://localhost:4000'
REPORT = {'pages': [], 'interactions': [], 'errors': [], 'complete': False}


def page_failures(pages):
    failures = []
    for page in pages:
        route = page['route']
        expected_lang = 'zh-CN' if route.startswith('/zh/') else 'en'
        other = '/en/' + route[4:] if route.startswith('/zh/') else '/zh/' + route[4:]
        if (page['horizontalOverflow'] or page['imagesBroken'] or len(page['h1']) != 1
                or page['navigationLinks'] != 8 or page['lang'] != expected_lang
                or page.get('primaryNavigationItems') != 7
                or page['alternateLanguage'] != other):
            failures.append(f"{page['width']}px {route}: 页面验收失败")
    return failures


def save_report():
    (ROOT / 'docs/browser-checks.json').write_text(json.dumps(REPORT, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def call(*args):
    run = subprocess.run([CLI, '--session', SESSION, '--json', *map(str, args)],
                         capture_output=True, text=True, encoding='utf-8', timeout=50)
    if run.returncode:
        raise RuntimeError(run.stderr or run.stdout)
    result = json.loads(run.stdout)
    if not result.get('success'):
        raise RuntimeError(str(result))
    return result.get('data', {})


def evaluate(code):
    encoded = base64.b64encode(code.encode('utf-8')).decode('ascii')
    return call('eval', '-b', encoded)['result']


def check(name, value):
    REPORT['interactions'].append({'check': name, 'passed': bool(value)})
    if not value:
        REPORT['errors'].append(name)
    save_report()


def open_page(path):
    call('open', BASE + path)
    call('wait', '--load', 'networkidle')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interactions-only', action='store_true')
    args = parser.parse_args()
    if not CLI:
        raise SystemExit('请先安装 agent-browser，参见其官方说明。')
    # Windows 新会话的守护进程可能继承输出句柄；首次启动写文件，避免PIPE等不到EOF。
    bootstrap = ROOT / '.local/browser-bootstrap.log'
    bootstrap.parent.mkdir(parents=True, exist_ok=True)
    with bootstrap.open('w', encoding='utf-8') as output:
        subprocess.run([CLI, '--session', SESSION, '--json', 'open', BASE + '/zh/'],
                       stdout=output, stderr=output, timeout=50, check=True)
    if args.interactions_only:
        previous = json.loads((ROOT / 'docs/browser-checks.json').read_text(encoding='utf-8'))
        REPORT['pages'] = previous['pages']
        REPORT['errors'].extend(page_failures(previous['pages']))
    viewports = [] if args.interactions_only else [(1440, 1000), (390, 844)]
    for width, height in viewports:
        call('set', 'viewport', width, height)
        for lang in ['zh', 'en']:
            for page in ['', 'people/', 'research/', 'projects/', 'publications/', 'news/', 'join/', 'contact/']:
                route = '/' + lang + '/' + page
                open_page(route)
                state = evaluate('''(() => ({
                  lang: document.documentElement.lang,
                  width: innerWidth,
                  scrollWidth: document.documentElement.scrollWidth,
                  horizontalOverflow: document.documentElement.scrollWidth > innerWidth,
                  h1: [...document.querySelectorAll('h1')].map(x => x.textContent.trim()),
                  imagesBroken: [...document.images].filter(x => !x.complete || x.naturalWidth === 0).map(x => x.src),
                  navigationLinks: document.querySelectorAll('#main-nav a').length,
                  primaryNavigationItems: document.querySelector('#main-nav').children.length,
                  alternateLanguage: document.querySelector('.language-switch a:not([aria-current])').getAttribute('href'),
                  footerColor: getComputedStyle(document.querySelector('.site-footer a')).color
                }))()''')
                state['route'] = route
                REPORT['pages'].append(state)
                REPORT['errors'].extend(page_failures([state]))
                save_report()
                if page == '' or (width == 1440 and page in ['people/', 'projects/', 'join/', 'publications/']):
                    name = f'{lang}-{page.strip("/") or "home"}-{width}.png'
                    call('screenshot', '--full', ROOT / 'docs' / name)
                print(f'{width}px {route}', flush=True)

    call('set', 'viewport', 1440, 1000)
    open_page('/zh/publications/')
    publications = json.loads((ROOT / '_data/publications.json').read_text(encoding='utf-8'))
    papers = evaluate('[...document.querySelectorAll("[data-publication]")].map(p => ({year:p.dataset.year,topic:p.dataset.topic,text:p.textContent.toLocaleLowerCase()}))')
    total = len(publications)
    check('全部论文初始显示（数量来自数据文件）', evaluate('document.querySelectorAll("[data-publication]:not([hidden])").length') == total)
    query_matches = [p for p in papers if 'crystal' in p['text']]
    call('fill', '#publication-search', 'Crystal')
    check('关键词检索结果与数据一致', evaluate('document.querySelectorAll("[data-publication]:not([hidden])").length') == len(query_matches))
    years = sorted({p['year'] for p in query_matches or papers}, reverse=True)
    selected_year = years[0] if years else None
    if selected_year:
        call('select', '#publication-year', selected_year)
        expected = sum(p['year'] == selected_year for p in query_matches)
        check('关键词叠加年份结果正确', evaluate('document.querySelectorAll("[data-publication]:not([hidden])").length') == expected)
    topic_options = evaluate('[...document.querySelector("#publication-topic").options].map(o=>o.value).filter(Boolean)')
    if topic_options:
        selected_topic = topic_options[0]
        call('select', '#publication-topic', selected_topic)
        expected = sum((not selected_year or p['year'] == selected_year) and p['topic'] == selected_topic for p in query_matches)
        check('关键词叠加年份与主题结果正确', evaluate('document.querySelectorAll("[data-publication]:not([hidden])").length') == expected)
    call('fill', '#publication-search', '__no_publication_matches_this_query__')
    check('空结果提示', evaluate('document.querySelectorAll("[data-publication]:not([hidden])").length === 0 && !document.querySelector("#publication-empty").hidden'))
    call('fill', '#publication-search', '')
    for control in ['#publication-year', '#publication-topic']:
        call('focus', control)
        call('press', 'Home')
        call('press', 'Enter')
    check('清空条件恢复全部论文', evaluate('document.querySelectorAll("[data-publication]:not([hidden])").length') == total)
    call('click', '.language-switch a[hreflang=en]')
    call('wait', '--load', 'networkidle')
    check('论文页中文转英文停留同页', evaluate('location.pathname === "/en/publications/" && document.documentElement.lang === "en"'))
    call('click', '.language-switch a[hreflang=zh-CN]')
    call('wait', '--load', 'networkidle')
    check('论文页英文转中文停留同页', evaluate('location.pathname === "/zh/publications/"'))

    # 核对一级顺序、下拉交互与当前分组，防止仅移动文字却破坏可访问性。
    for lang, labels in [('zh', ['首页', '研究方向', '科研项目', '学术论文', '更多', '加入我们', '联系我们']),
                         ('en', ['Home', 'Research', 'Projects', 'Publications', 'More', 'Join Us', 'Contact'])]:
        open_page('/' + lang + '/')
        actual = evaluate('[...document.querySelector("#main-nav").children].map(e => e.querySelector("summary")?.textContent.trim() || e.textContent.trim())')
        check(lang + '一级导航顺序正确', actual == labels)
        check(lang + '下拉默认收起', evaluate('!document.querySelector(".nav-dropdown").open'))
        call('focus', '.nav-dropdown summary')
        call('press', 'Enter')
        check(lang + '键盘展开下拉', evaluate('document.querySelector(".nav-dropdown").open'))
        check(lang + '下拉仅含团队和新闻', evaluate('[...document.querySelectorAll(".nav-dropdown a")].map(a=>a.pathname)') == ['/' + lang + '/people/', '/' + lang + '/news/'])
        call('press', 'Escape')
        check(lang + 'Escape关闭下拉并归还焦点', evaluate('!document.querySelector(".nav-dropdown").open && document.activeElement.matches(".nav-dropdown summary")'))
        call('click', '.nav-dropdown summary')
        call('click', 'h1')
        check(lang + '点击外部关闭下拉', evaluate('!document.querySelector(".nav-dropdown").open'))
        call('click', '.nav-dropdown summary')
        call('click', '.nav-dropdown a[href="/' + lang + '/news/"]')
        call('wait', '--load', 'networkidle')
        check(lang + '新闻页标记当前分组和子页', evaluate('document.querySelector(".nav-dropdown").classList.contains("has-current-page") && document.querySelector(".nav-dropdown a[aria-current=page]").pathname === location.pathname'))
        other = 'en' if lang == 'zh' else 'zh'
        call('click', '.language-switch a:not([aria-current])')
        call('wait', '--load', 'networkidle')
        check(lang + '下拉页面语言切换保持新闻页', evaluate('location.pathname') == '/' + other + '/news/')
        check(lang + '图标资源可访问', evaluate('''(async () => {
          const icons = [...document.querySelectorAll('link[rel="icon"], link[rel="apple-touch-icon"]')];
          const responses = await Promise.all(icons.map(icon => fetch(icon.href)));
          return icons.length === 4 && responses.every(response => response.ok);
        })()'''))

    call('set', 'viewport', 390, 844)
    open_page('/en/join/')
    check('手机导航初始收起', evaluate('getComputedStyle(document.querySelector("#main-nav")).display === "none"'))
    call('click', '.menu-toggle')
    check('手机菜单可展开', evaluate('document.querySelector(".menu-toggle").getAttribute("aria-expanded") === "true" && getComputedStyle(document.querySelector("#main-nav")).display !== "none"'))
    call('screenshot', ROOT / 'docs' / 'mobile-menu.png')
    call('press', 'Escape')
    check('Escape关闭导航', evaluate('document.querySelector(".menu-toggle").getAttribute("aria-expanded") === "false"'))
    call('click', '.menu-toggle')
    call('click', '.nav-dropdown summary')
    check('手机更多菜单可展开', evaluate('document.querySelector(".nav-dropdown").open'))
    call('press', 'Escape')
    check('手机Escape先关闭子菜单', evaluate('!document.querySelector(".nav-dropdown").open && document.querySelector(".menu-toggle").getAttribute("aria-expanded") === "true"'))
    call('click', '.nav-dropdown summary')
    call('screenshot', ROOT / 'docs' / 'nav-mobile-open.png')
    call('click', '#main-nav a[href="/en/people/"]')
    call('wait', '--load', 'networkidle')
    check('手机菜单链接可访问', evaluate('location.pathname === "/en/people/"'))

    for width in [320, 768]:
        call('set', 'viewport', width, 900)
        for lang in ['zh', 'en']:
            open_page('/' + lang + '/')
            check(f'{width}px {lang}首页无横向溢出', evaluate('document.documentElement.scrollWidth <= innerWidth'))
    REPORT['browser_errors'] = call('errors')
    for error in REPORT['browser_errors'].get('errors', []):
        REPORT['errors'].append('浏览器脚本错误: ' + str(error))
    call('set', 'viewport', 1440, 1000)
    open_page('/zh/')
    REPORT['complete'] = True
    save_report()
    print(json.dumps({'pages_checked': len(REPORT['pages']), 'interactions': len(REPORT['interactions']), 'errors': REPORT['errors']}, ensure_ascii=False))
    raise SystemExit(1 if REPORT['errors'] else 0)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        REPORT['errors'].append('浏览器测试未完成: ' + str(error))
        save_report()
        raise
