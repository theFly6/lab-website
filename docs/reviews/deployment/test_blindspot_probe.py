"""Synthetic unit probe for failure reporting; does not operate browser or modify implementation."""
import importlib.util, json, sys
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('browser_checks_audit',Path('scripts/browser_checks.py'))
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.CLI='synthetic-command'; m.save_report=lambda: None; m.open_page=lambda _: None
papers=[{'year':'2021','topic':'hpc','text':'crystal'} for _ in range(3)]
values=iter([papers,7,3,3,['hpc'],3,True,7]+[True]*10)
m.evaluate=lambda _: next(values)
m.call=lambda *a: {'errors':['Synthetic TypeError: broken feature']} if a==('errors',) else {}
prior={'pages':[{'route':'/zh/','width':390,'horizontalOverflow':True,'imagesBroken':[],'h1':['Title'],'navigationLinks':8,'lang':'zh-CN','alternateLanguage':'/en/'}],'errors':['390px /zh/: horizontal overflow']}
read_text=Path.read_text
def mocked_read(path,*a,**kw):
 return json.dumps(prior) if path.name=='browser-checks.json' else read_text(path,*a,**kw)
with patch.object(sys,'argv',['browser_checks.py','--interactions-only']),patch.object(Path,'read_text',mocked_read):
 try: m.main()
 except SystemExit as e: code=e.code
result={'probe_type':'synthetic harness logic only, not real browser result','prior_page_errors':prior['errors'],'injected_browser_errors':m.REPORT['browser_errors'],'final_errors':m.REPORT['errors'],'exit_code':code,'prior_page_failure_preserved':any('页面验收失败' in x for x in m.REPORT['errors']),'browser_error_causes_nonzero_exit':code!=0 and any('浏览器脚本错误' in x for x in m.REPORT['errors'])}
Path('docs/reviews/deployment/test-blindspot-probe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))

