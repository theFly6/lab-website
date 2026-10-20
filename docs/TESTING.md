# 本地构建与验收记录

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
