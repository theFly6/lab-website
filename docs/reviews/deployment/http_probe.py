import json, urllib.request, urllib.error, datetime, re
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import install_opener, build_opener, ProxyHandler
install_opener(build_opener(ProxyHandler({})))
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(); self.links=[]; self.lang=None; self.h1=0; self.canonical=[]; self.feed(text)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='html': self.lang=a.get('lang')
  if t=='h1': self.h1+=1
  if t in ('a','link') and 'href' in a: self.links.append(a['href'])
  if t in ('img','script') and 'src' in a: self.links.append(a['src'])
  if t=='link' and a.get('rel')=='canonical': self.canonical.append(a.get('href'))
result={'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':'http://127.0.0.1:4000','pages':[],'resources':[]}
resources=set()
for path in ['/']+['/'+l+'/'+p for l in ['zh','en'] for p in ['','people/','research/','projects/','publications/','news/','join/','contact/']]+['/definitely-does-not-exist/']:
 try: r=urllib.request.urlopen(result['base']+path,timeout=5)
 except urllib.error.HTTPError as e: r=e
 text=r.read().decode('utf-8'); page=Page(text)
 result['pages'].append({'path':path,'status':r.status,'lang':page.lang,'h1':page.h1,'canonical':page.canonical,'escaped_document_tags':bool(re.search(r'&lt;(?:html|h1|body)',text))})
 resources.update(x for x in page.links if x.startswith('/_styles/') or x.startswith('/assets/'))
for path in sorted(resources):
 try:
  with urllib.request.urlopen(result['base']+path,timeout=5) as r: result['resources'].append({'path':path,'status':r.status,'bytes':len(r.read())})
 except Exception as e: result['resources'].append({'path':path,'error':str(e)})
for path in ['/docs/SOURCES.md','/scripts/check_site.py','/FINAL_REPORT.md','/Gemfile','/.git/config']:
 try:
  r=urllib.request.urlopen(result['base']+path,timeout=5); result.setdefault('excluded_paths',[]).append({'path':path,'status':r.status})
 except urllib.error.HTTPError as e: result.setdefault('excluded_paths',[]).append({'path':path,'status':e.code})
Path('docs/reviews/deployment/http-current.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'page_count':len(result['pages']),'resource_count':len(result['resources']),'resource_failures':[x for x in result['resources'] if x.get('status')!=200],'excluded_paths':result['excluded_paths']},ensure_ascii=False,indent=2))

