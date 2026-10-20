# 本地构建与验收记录

## 2026-10-20：SEO与Google验证标记

- 从 `main` 创建 `feature/search-seo`，保留既有布局、TODO与开发记录；仅调整元数据、验证配置和维护文档。
- 为16个中英文内容页添加独立标题与摘要，Open Graph保持一致；保留canonical、hreflang和自动Sitemap。根入口补齐摘要、中文首页canonical和验证标记。
- 已接入用户提供的Google公开验证标识；检查器验证根入口与16页各有且只有一个正确标记，不将本地通过等同于Google账号验证成功。
- [生产子路径检查](seo-check-production.json)与[本地根路径检查](seo-check-root.json)：Jekyll构建均成功，各18个HTML、16条双语路由，标题/摘要唯一性、Open Graph、canonical、hreflang及Sitemap检查0错误。生产路径有1,110处内部引用。
- 负向检查：临时移除构建产物中中文首页的验证标记，检查器正确返回非零并报告缺失；随后完整恢复该产物。
- 使用agent-browser在4011端口独立预览正式子路径，实际点击中文首页的EN切换到英文首页，两个页面的浏览器标题、头部验证标记和canonical正确，当前桌面视口均无横向溢出。查看英文首页截图，导航、招生入口和联系浮层正常。专用浏览器随后关闭，不占用用户的4000端口。
- 本轮未改动布局与交互脚本，不重复此前完整响应式矩阵。Search Console账号内的验证、地图提交和索引状态仍需所有者操作，步骤见 [SEARCH_INDEXING.md](SEARCH_INDEXING.md)。

## 2026-10-20：导师教学荣誉与人才培养优化

本轮修改导师数据、双语文案、People共用组件与对应样式；下文保留之前版本的验收快照。

- 简介精简，教育/工作年份集中到经历区；新增5项教学奖励、2类人才培养成果及1项研究生课程认定。页面顺序为简介、任职/服务、教学/著作、荣誉/培养、经历、成员/平台。
- 首次构建发现含花括号的届次占位符在Liquid直接输出表达式中解析失败；改为先用 `assign` 替换，再转义输出。修复后的根路径和生产子路径构建均成功。
- [根路径检查](teaching-check-root.json)：18个HTML、1,142处站内引用、16条双语路由，0错误。
- [子路径检查](teaching-check-production.json)：18个HTML、1,110处站内引用，canonical、hreflang及sitemap通过。
- [HTTP复验](teaching-http.json)：17个页面、54项资源、5个维护路径与实际404均符合预期。
- 独立[UI报告](reviews/teaching-ui/REVIEW.md)与[结构化结果](reviews/teaching-ui/summary.json)：中英文People × 1440/768/390/320，共8组合；每页5项奖、2张培养卡、1项课程认定均完整，0横向溢出、0标题/卡片/括号记录裁切，语言对应8/8正确。
- 实际点击同页语言切换成功，320px悬浮联系面板可用，Escape关闭并归还焦点。人工查看[中文桌面荣誉区](teaching-honors-zh-desktop.png)及审查目录中的小屏截图。
- 独立[内容审查](reviews/TEACHING_CONTENT_REVIEW.md)通过：届次、等级、括号、历史统计和培养成果与给定原文一致。评教4.07%与讲台排名第5未放入页面，待补口径记录在 [TEACHING_CONTENT.md](TEACHING_CONTENT.md)。
- 当前源码差异检查通过，没有改动运行依赖或交互脚本。专用测试浏览器已关闭，用户的4000端口服务继续运行。

## 2026-10-20：HPCDE公开资料内容补充

本轮仅调整中英文内容、相应展示组件与样式，没有改动悬浮联系或论文筛选脚本。以下为本轮最新验收；之前的完整交互记录保留为对应版本快照。

- `bundle exec jekyll build`通过；[根路径检查](hpcde-check-root.json)：18个HTML、1,142处站内引用、16条双语路由，0错误。
- `/lab-preview`生产构建通过；[子路径检查](hpcde-check-production.json)：18个HTML、1,110处站内引用，canonical、hreflang与sitemap检查通过。
- [HTTP复验](hpcde-http.json)：17个页面、54项资源、5个维护路径、实际404均符合预期。
- 独立[UI复验报告](reviews/hpcde-ui/REVIEW.md)与[结构化记录](reviews/hpcde-ui/summary.json)：中英文Home/People/Contact × 1440/768/390/320，共24组合，0横向溢出、0破图、0新增内容裁切，语言对应24/24正确。
- 在书目增加出版社、第一作者和ISBN之后，另行复验中英文People 320px；两条书目及学校原始链接完整、无元数据溢出。悬浮联系在320px正常展开，Escape关闭并归还焦点。
- 独立[内容审查](reviews/HPCDE_CONTENT_REVIEW.md)：没有P1/P2阻断问题；修复2处P3措辞，补充两本书的官方原始记录。书目年份/版次/完整作者及具体导师对应学生仍保留TODO。
- 资料采用范围、邮箱拼写差异、旧站停更与往届目录边界见 [HPCDE_RESEARCH.md](HPCDE_RESEARCH.md)。本轮未导入内网入口、未新增无日期新闻、未推断新的论文或项目。
- 当前源码差异空白检查通过；专用测试浏览器已关闭，用户的4000端口服务继续运行。本轮没有执行远程推送或网站发布。

## 2026-10-20：学生联系悬浮卡片

本节对应 `feature/floating-contact` 的首版功能，最新浏览器报告为 [floating-contact-browser.json](floating-contact-browser.json)。后续章节保留早期验收快照。

- 16个中英文内容页及404均加入原生 `details/summary` 联系入口。默认收起，点击后展开非模态卡片，首选学生邮箱为 `zhangyunfei@xs.ustb.edu.cn`。
- 32个页面与视口组合、62项交互全部通过，浏览器脚本错误0条，`complete=true`。其中新增26项检查覆盖学生邮箱、卡片内不推荐导师邮箱、键盘展开、Escape及关闭按钮、焦点恢复、外部点击、真实剪贴板写入、权限拒绝提示与选中邮箱、双语内部链接、390px/320px短屏与404。
- 复制成功路径使用真实 `navigator.clipboard.writeText`；失败路径在测试浏览器中模拟拒绝权限，验证不会显示成功提示。未点击邮件发送链接或发送实际邮件。
- [根路径检查](floating-contact-root.json)与[GitHub Pages子路径检查](floating-contact-production.json)均通过：18个HTML、1,110处站内引用、16条双语路由。生产构建额外检查canonical、hreflang及sitemap。
- [HTTP检查](floating-contact-http.json)：17个页面、54项资源、5个维护路径、实际404均符合预期。
- `node --check assets/site.js`、浏览器检查脚本Python语法检查及当前源码差异空白检查通过。
- 人工查看[桌面卡片](floating-contact-desktop.png)、[390px手机卡片](floating-contact-mobile.png)与[320×480短屏卡片](floating-contact-small.png)。窄屏留有边距，短屏可在卡片内滚动；页脚预留收起按钮空间。
- 无JavaScript时可依靠原生折叠结构访问邮箱和内部链接，复制与关闭按钮默认隐藏；此降级路径依据HTML与样式核查，未完成浏览器禁用JavaScript的独立实测。
- 配置、界面文案及维护方式见README；未新增运行依赖。`v0.1-layout-baseline`仍指向原提交 `aa7f5c5`。

## 2026-10-20：导航与站点图标增量验收

本节为最新结果，下文2026-10-19的数量与截图说明保留为初始交付记录。

- 一级导航改为7项：「首页、研究方向、科研项目、学术论文、更多、加入我们、联系我们」；「更多 / More」含团队、新闻两个链接，页面全集仍为8类。
- 原生 `details/summary` 实现子菜单；支持键盘展开、Escape关闭并恢复焦点、点击外部关闭。手机端先关闭子菜单，再关闭主菜单。
- 修复模板通用 `details` 样式的菜单裁切、额外箭头和间距；限定覆盖在 `.nav-dropdown`，不影响正文折叠组件。
- 使用页眉的计算节点SVG标识，补齐32×32 PNG、180×180收藏图标和16/32/48多尺寸ICO。
- 根路径构建成功；[根路径检查](navigation-check-root.json)：18个HTML、1,090处站内引用、16条双语路由，0错误。
- `/lab-preview`生产构建成功；[子路径检查](navigation-check-production.json)：18个HTML、1,058处站内引用；资源、语言对应页、canonical、hreflang与sitemap检查均通过。
- [实际浏览器复验](navigation-browser-checks.json)：32个页面与视口组合、36项交互全部通过，0脚本错误，`complete=true`。包括中英文导航顺序、下拉仅含团队/新闻、当前子页和分组、新闻对应页语言切换、图标HTTP加载、手机菜单及原有论文筛选。
- [HTTP复验](navigation-http.json)：17个页面、53项资源、5个维护资料路径检查通过，实际404响应有效。
- `node --check assets/site.js` 与浏览器检查脚本Python语法检查通过。
- 人工查看[英文桌面下拉截图](nav-desktop-open.png)、[中文手机下拉截图](nav-zh-mobile-open.png)与[320px英文下拉截图](nav-en-small-open.png)，菜单清楚、无横向溢出。
- 没有安装新运行依赖，没有发布网站，没有停止用户正在运行的4000端口服务。测试专用浏览器会话已关闭。

## 初始交付记录

日期：2026-10-19。执行环境为 Windows PowerShell + 已有 Ubuntu WSL，浏览器为 agent-browser 启动的 Chromium。仅测试本地站点，没有执行远程发布。

## 环境与构建

- Ruby 3.3.8、Bundler 2.5.6（锁文件版本）。
- Jekyll 4.4.1、jekyll-sass-converter 3.1.0、sass-embedded 1.105.2。
- 交叉审查后定向升级：Nokogiri 1.19.4、mini_portile2 2.8.9、REXML 3.4.4、WEBrick 1.9.2。
- gems 位于项目 `vendor/bundle/`；没有更改全局代理、PowerShell 执行策略或现有业务项目。
- `bundle exec jekyll build` 成功，生成 `_site/`。
- 模拟 GitHub Pages 项目路径 `/lab-preview` 的生产构建成功，最终产物在被忽略的 `.local/site-production/`。
- 两种最终构建的 HTML、站内链接、锚点、图片/样式/脚本引用、语言对应页检查均通过。精确计数见 [`check-root.json`](check-root.json) 与 [`check-production.json`](check-production.json)。`check-subpath.json`保留为上一阶段历史记录。
- `node --check assets/site.js`、Python检查脚本语法编译、`bash -n start.sh` 均通过。
- PowerShell `.\start.ps1 -Port 4001` 已实际启动，英文首页返回 HTTP 200；标准 `start.sh` 启动的中文首页也返回 HTTP 200。测试服务在交付前已停止，可按README重启。

## 浏览器检查

机器可读结果：[browser-checks.json](browser-checks.json)。

| 检查 | 范围 | 结果 |
| --- | --- | --- |
| 桌面页面 | 1440×1000，中英文各8页 | 16个页面与视口组合通过 |
| 手机页面 | 390×844，中英文各8页 | 16个页面与视口组合通过 |
| 横向溢出、图片加载、h1、8项导航 | 上述32个组合 | 无溢出，无失败图片，每页一个h1 |
| 窄屏和平板补充 | 320px、768px，中英文首页 | 4项通过 |
| 语言切换 | 论文页中文→英文→中文 | 保持对应论文页，HTML lang正确 |
| 论文关键词 | `Crystal` | 7篇中显示3篇 |
| 组合筛选 | `Crystal` + 2021 | 显示2篇 |
| 主题组合 | 关键词、年份、主题叠加 | 与页面数据计算的预期数量一致 |
| 不匹配检索词 | 输入明确不匹配的字符串 | 显示0篇及空结果提示 |
| 条件重置 | 清空关键词，年份/主题恢复首项 | 恢复7篇 |
| 手机菜单 | 展开、Escape关闭、People导航 | 通过，aria-expanded随状态变化 |
| 浏览器脚本错误 | 本地功能检查会话 | 0条 |

审查后最终交互报告包含 **16项检查，全部通过、0项失败，complete=true**，浏览器脚本错误为0。浏览器截图位于本目录，未发布到网站：

- [桌面首页预览](preview-desktop.png)
- [中文桌面完整首页](zh-home-1440.png)
- [英文桌面完整首页](en-home-1440.png)
- [中文手机完整首页](zh-home-390.png)
- [英文手机完整首页](en-home-390.png)
- [手机英文菜单](mobile-menu.png)

## 测试中修复的问题

1. 原模板旧版依赖在当前Ruby/GCC下失败：更新Sass及Jekyll，移除未使用的文件修改时间插件，保留可重复安装的Gemfile.lock。
2. Liquid页面正文先于layout渲染：统一由 `lab/page.html` 在渲染内容前建立语言上下文。
3. 模板基础footer对链接使用了important颜色：定制样式明确覆盖，修复深色页脚上的低对比度。
4. `start.ps1` 的Windows路径经WSL默认shell解析会丢失反斜杠：改用 `wsl --exec`。
5. 论文筛选最初只监听input：增加change监听，复测程序选择和组合筛选通过。
6. 首轮自动化的URL通配等待发生工具超时；真实链接可正常切换。改为等待网络空闲后直接断言实际路径，在新浏览器会话完成复测。

## 复验方式

先按README启动本地服务，再在项目目录执行：

```powershell
python -X utf8 scripts/check_site.py
python -X utf8 scripts/browser_checks.py
python -X utf8 scripts/check_http.py
```

浏览器检查依赖已安装的 `agent-browser`，使用本任务专用会话 `ustb-final`，不会连接现有私人浏览器。只有交互代码改变而布局未变时，可运行 `python -X utf8 scripts/browser_checks.py --interactions-only`，沿用32个页面的渲染记录并更新交互结果。

## 独立交叉审查后的补充验收

4个独立Subagent的审查、问题和修复对应关系见 [FINAL_REPORT.md](../FINAL_REPORT.md) 与 `reviews/`。

- UI独立审查覆盖48个组合：中英文6类页面×1440/768/390/320宽度，未发现横向溢出、破损图片或语言目标错误。
- 内容审查实时Crossref核对7篇书目，差异均为空；姓名无官方拼写的部分已移除猜测。
- 测试审查以合成故障注入确认，历史页面失败和JavaScript错误能导致非零退出。该合成错误不是网站实际错误。
- `scripts/test_template_escaping.rb` 使用实际论文组件渲染特殊字符，6项检查通过。
- 新版 `check_site.py` 除主路由外检查404、维护文件泄漏；指定 `--expected-origin` 时还检查canonical、hreflang和sitemap。
- 新版 `browser_checks.py` 从内容数据读取论文数量，保留部分复验的旧页面失败；脚本异常写入报告，只有执行完毕才设置`complete: true`。
- `scripts/check_http.py` 显式绕过系统代理，仅向本地服务探测17个正常路由、实际404、CSS/JS/图片和5项维护资料路径。
- 生产元信息验收使用保留示例域名 `https://ustb-lab.example` 与 `/lab-preview`，不代表创建或发布了真实域名。记录在 `check-production.json`。
- 升级依赖后的实际HTTP复验见 [http-final.json](http-final.json)：17个正常路由、50项资源均200，实际不存在页面返回404且具有效HTML，5项维护路径均404。

## 验证边界

2026-10-20补测：上轮启动验证使用PowerShell 7，未覆盖Windows自带的PowerShell 5.1。用户报告后，在5.1.26100.9168复现无BOM的UTF-8脚本解析错误；将`start.ps1`保存为UTF-8 with BOM后，5.1与7.6.5均解析通过，并实际从5.1启动WSL/Jekyll，中文与英文首页均返回HTTP 200。未修改系统编码、执行策略或WSL配置。

- 外部出版社及学校网页可能有访问控制，本站检查不替代对其未来可用性的承诺；内容出处已逐项记录。
- 没有测试真实报名、邮件发送、账号登录或服务器接口，因为网站不提供这些功能。
- 没有执行GitHub Actions云端发布；本地子路径构建与链接检查验证了相应静态路径处理，不能等同于已经部署。
- 未宣称已覆盖所有设备、所有浏览器或完整的无障碍认证。
