# 李建江课题组双语网站：最终交付报告

## 2026-10-20功能试版：学生联系悬浮卡片

功能分支：`feature/floating-contact`。所有中英文内容页及404右下角增加联系入口，默认收起，点击后展示学生联系人张云飞、邮件与复制按钮、同语言的招生信息和完整联系方式入口。使用此前用户留存的学生邮箱 `zhangyunfei@xs.ustb.edu.cn`，该配置不代表学校正式指定的招生咨询邮箱。

联系人配置集中在 `_data/floating_contact.json`，中英文文案分别位于locale文件。共享Liquid组件、独立SCSS与少量原生JavaScript支持移动端安全边距、短屏滚动、键盘展开、Escape关闭、焦点恢复、外部点击关闭和复制失败提示；不增加后端或运行依赖。

本地及 `/lab-preview`生产构建通过。实际浏览器32个页面/视口组合、62项交互全部通过，0脚本错误；HTTP检查17个页面、54项资源及404通过。完整记录及验证边界见 [docs/TESTING.md](docs/TESTING.md) 最新章节，使用及邮箱更换方式见README。原有TODO、来源及审查记录继续保留。

## 2026-10-20增量更新：导航整合与Favicon

- 中英文一级导航统一为首页、研究方向、科研项目、学术论文、更多、加入我们、联系我们；团队介绍与新闻动态移入「更多 / More」下拉，加入我们保留强调样式。
- 导航分组由 `_data/navigation.json` 的 `primary` 与 `dropdowns` 管理；`pages` 保留完整页面列表。两种语言的文字仍独立维护。
- 子菜单使用原生 `details/summary`，兼容触摸、键盘与无JavaScript访问。新增外部点击关闭、Escape关闭及焦点恢复；团队和新闻页面标记当前分组。
- 沿用与系统研究主题一致的计算节点SVG标识，新增PNG、Apple touch icon和多尺寸ICO，所有图标路径支持baseurl。
- 已修复模板通用折叠框样式对导航的裁切与重复箭头；没有添加运行依赖。
- 根路径与模拟GitHub Pages子路径构建通过；18个HTML的站内引用及双语对应检查均无错误。
- 浏览器32个页面/视口组合、36项交互全部通过，0脚本错误；HTTP复验17个页面、53项资源与404均通过。
- 验收细节及机器可读报告见 [docs/TESTING.md](docs/TESTING.md)。本轮没有发布网站，原有启动方式不变。

以下为初始交付及启动兼容性记录；其中早期测试数量为当时快照，最新结果以上述增量验收为准。

日期：2026-10-19。项目目录：`D:\ClaudeSessions\with-zetero\lab-website`。

2026-10-20启动兼容性补修：原启动脚本仅在PowerShell 7测试，Windows PowerShell 5.1会按本地编码误读无BOM的UTF-8中文字符串。已添加UTF-8 BOM；5.1和7均解析通过，5.1实际启动后中英文首页均HTTP 200。见[测试记录](docs/TESTING.md)。

当前阶段为本地开发与验收，**未部署到 GitHub Pages、未创建远程仓库、未购买服务器或域名**。正式名称、成员及招生计划尚待课题组确认；它们不妨碍本地浏览，也未被编造成既定事实。

> 最终验收完成：根路径和生产子路径构建通过；主Agent32个浏览器页面/视口组合、16项交互检查全部通过；独立UI审查48组合通过。测试服务已在交付前停止，启动命令保持可用。

## 一、启动与浏览

在 PowerShell 中运行：

```powershell
cd D:\ClaudeSessions\with-zetero\lab-website
.\start.ps1
```

若 PowerShell 执行策略阻止运行本地脚本，可直接执行，不需要修改系统策略：

```powershell
wsl -d Ubuntu -- bash /mnt/d/ClaudeSessions/with-zetero/lab-website/start.sh
```

中文：<http://localhost:4000/zh/>；英文：<http://localhost:4000/en/>。等待终端显示 `Server running` 后访问；按 `Ctrl+C` 停止。端口占用可使用 `.\start.ps1 -Port 4001`。

本机已具备 Ubuntu WSL、Ruby 3.3 与项目 gems，正常预览不需要 Node.js。另一个机器的依赖安装、内容维护及构建步骤见 [README.md](README.md)。

## 二、已完成的功能

| 范围 | 已实现内容 |
| --- | --- |
| 模板基础 | 保留 Greene Lab Website Template 的 Jekyll/Liquid/SCSS 技术栈、分区机制、基础组件与 BSD 3-Clause 许可署名；未另起前端框架重写 |
| 双语 | `/zh/`、`/en/` 各8页，共用布局；locale和实体文本分别维护中文/英文，语言切换留在同一页面对应版本 |
| 首页 | 研究定位、4个研究方向、精选论文、公开动态、明显的加入我们入口 |
| 团队 | 已核实导师简介、教育/工作与访问经历、公开联系方式；博士、硕士、毕业生分类支持数据添加 |
| 研究 | 4个主题，说明研究问题、关键词并保留来源 |
| 项目 | 6项有官方来源的历史项目，区分执行期、承担角色、编号；不推定当前在研或结题 |
| 论文 | 7篇已核实代表作，作者、卷期、页码、DOI、出版社与双语简述；支持关键词、年份、主题组合筛选 |
| 新闻 | 1条2025年学院公开报道的摘要，不把同一事件的两份报道当作两条新闻 |
| 招生 | 博士/硕士研究介绍、咨询邮箱、官方政策入口；未知年度名额、条件和资助明确TODO |
| 联系 | 公开邮箱、学校地址与官方入口；旧页办公室信息明确注明待复核 |
| 响应式与交互 | 桌面/平板/手机布局；菜单展开状态、Escape关闭、键盘跳至正文；不依赖外部字体或脚本CDN |
| 错误页 | 有效的双语404 HTML，返回中英文首页，兼容项目子路径 |
| 工程交接 | 一键启动、结构化内容、构建检查、浏览器检查、来源记录、TODO、审查报告、手动发布工作流 |

实体数据在 `_data/*.json`，界面和正文文案在 `_data/locales/zh.json`、`en.json`；追加人员、新闻或论文无需改页面布局。论文显示数量及测试预期已改为由数据生成。

## 三、资料真实性与主要来源

已确认对象为**北京科技大学计算机与通信工程学院李建江教授、博士生导师**。姓名、单位、2005年清华博士经历与研究方向交叉吻合；没有采用建设银行人员或其他学校同名学者的信息。

- 教师主页：<https://faculty.ustb.edu.cn/JianjiangLi/zh_CN/index.htm>
- 学院英文介绍及公开邮箱：<https://enscce.ustb.edu.cn/Teach/TeacherList/2020-06-03/43.html>
- 官方项目列表：<https://faculty.ustb.edu.cn/JianjiangLi/zh_CN/kyxm/72137/list/index.htm>
- 官方论文列表：<https://faculty.ustb.edu.cn/JianjiangLi/zh_CN/lwcg/72134/list/index.htm>
- 相关工程研究中心：<https://ercis.ustb.edu.cn/?p=1390>
- 科技服务团新闻：<https://scce.ustb.edu.cn/info/1087/3644.htm>
- 学校招生入口：<https://yzxc.ustb.edu.cn/>

7篇论文分别为 Crystal-MD访存优化、Crystal-KMC天河二号优化、Crystal-KMC软件、短程分子动力学内核优化、热临时数据分布式存储、POST事务处理中间件、FSAP云存储划分。独立内容审查重新请求Crossref逐篇比较题名、作者顺序、卷期页码，差异均为空；年份按卷期，不误用在线日期或DOI中的年份。

完整出处、采用边界、图片来源与访问限制见 [docs/SOURCES.md](docs/SOURCES.md) 和 [内容独立审查](docs/reviews/CONTENT_REVIEW.md)。部分出版社直接抓取受限，已记录；没有把抓取失败当成论文不存在，也没有声称已重新读取全部论文全文。

## 四、Subagent交叉审查

4个独立Subagent只写各自报告及证据，网站实现由主Agent统一修改，避免交叉覆盖。

| Subagent | 范围 | 结论与记录 |
| --- | --- | --- |
| `architecture_review` | 代码、架构、依赖及安全 | 找出依赖公告、HTML转义与旧Docker引文入口问题；另确认Nokogiri升级受mini_portile2锁定影响。见 [ARCHITECTURE_REVIEW.md](docs/reviews/ARCHITECTURE_REVIEW.md) |
| `ui_review` | 视觉、响应式、导航、键盘与语言切换 | 48个页面/视口组合通过，未发现P0/P1/P2 UI缺陷。见 [UI_REVIEW.md](docs/reviews/UI_REVIEW.md) 与 [证据](docs/reviews/ui/summary.json) |
| `content_review` | 身份、来源、论文、项目、招生、双语 | 未发现P0/P1事实错误；指出学生姓名英文拼写无官方依据。见 [CONTENT_REVIEW.md](docs/reviews/CONTENT_REVIEW.md) |
| `deployment_review` | 测试有效性、HTTP、资源、路径、发布兼容 | 发现404转义与验收假通过风险；独立故障注入确认修复有效。见 [DEPLOYMENT_REVIEW.md](docs/reviews/DEPLOYMENT_REVIEW.md) |

UI独立审查覆盖中英文 Home、People、Projects、Publications、Join、Contact 与1440/768/390/320宽度，共48组合；主要8项导航、图片及同页语言目标均通过，另实际操作筛选与键盘导航。

## 五、审查后已修复的问题

| 优先级 | 问题 | 实际处理 |
| --- | --- | --- |
| P2 | Nokogiri、REXML、WEBrick旧锁定版本有官方安全公告 | 定向升级至Nokogiri 1.19.4、REXML 3.4.4、WEBrick 1.9.2，并解锁mini_portile2至2.8.9；保留最终锁文件。没有做无范围的全量更新 |
| P2 | 标题/作者等纯文本中的尖括号、引号和`&`会变成HTML | 对15个定制模板中的普通文本及属性输出加转义，作者强调标记在转义后添加；新增6项实际Liquid渲染回归 |
| P2 | 英文新闻把“李亿行”的多音字姓名拼写当成确定事实 | 移除未经确认的拼音，暂保留中文姓名，官方拼写列入TODO |
| P2 | 404整页HTML被Markdown转义，旧验收未发现 | 改为真正的404.html；检查器增加lang和h1验收 |
| P2 | 浏览器脚本错误只被记录，不影响退出码 | 并入失败列表，存在错误即非零退出 |
| P2 | 部分复验可能丢弃历史页面失败 | 重新验证继承的页面状态；独立故障注入确认布局失败仍保留 |
| P3 | 论文计数及测试写死7/3/2 | 页面与断言改成读取当前数据，新增组合主题筛选检查 |
| P3 | 中断可能留下难以区分的新旧报告 | 报告增加complete状态，异常写入失败及未完成状态；Windows新会话首次启动写文件，避免守护进程继承PIPE导致等待不结束 |
| P3 | 遗留Docker入口自动调用不兼容的旧引文同步器 | 明确禁用旧入口并给出中文说明；README说明Docker未验收，不会误覆盖当前数据 |
| P3 | 根目录交付报告可能混入发布产物 | FINAL_REPORT.md加入exclude，构建验收检查维护文件与目录是否泄漏 |
| 维护 | 生产SEO元信息只做过空域名本地检查 | 增加可指定origin的canonical、hreflang、sitemap验证，安排示例HTTPS域名+子路径构建 |

依赖修复针对已发现公告，并不表示完成所有第三方依赖的安全认证。旧Docker运行方式不在本次交付承诺中，正式支持的是README中的WSL/Ruby启动方式。

## 六、最终验收

| 检查 | 最终状态 | 证据 |
| --- | --- | --- |
| 6项特殊字符转义回归 | 已通过 | [escaping-check.txt](docs/reviews/escaping-check.txt) |
| 升级依赖后的根路径构建及站内链接 | 通过：18个HTML、1,042处站内引用，0失败 | [check-root.json](docs/check-root.json) |
| 示例HTTPS域名+/lab-preview生产构建 | 通过：18个HTML、1,010处站内引用；canonical/hreflang/sitemap正确 | [check-production.json](docs/check-production.json) |
| 主Agent完整浏览器与交互复验 | 通过：32组合、16项检查、0浏览器错误，complete=true | [browser-checks.json](docs/browser-checks.json) |
| 最终实际HTTP与404 | 通过：17路由、50资源、5个维护路径；404响应有效 | [http-final.json](docs/http-final.json) |
| 独立UI审查48组合 | 已通过，0溢出/破图 | [summary.json](docs/reviews/ui/summary.json) |
| 独立HTTP审查17路由/50资源 | 已通过；这是修复404前快照 | [http-current.json](docs/reviews/deployment/http-current.json) |
| 独立测试失败注入 | 已通过，注入错误导致退出码1 | [test-blindspot-probe.json](docs/reviews/deployment/test-blindspot-probe.json) |

浏览器和构建复验不是GitHub云端部署实测；没有执行邮件发送、报名、登录或服务器API，因为网站不提供这些后台功能。

## 七、仍需课题组提供的资料

见 [TODO.md](TODO.md)。主要包括：正式中英文名称及简介、在读/毕业成员和展示授权、当年博士/硕士招生细则与名额、最新办公室、照片确认、2022年后完整成果、当前项目与可公开细节、李亿行同学官方英文姓名。

这些均保留TODO或明确边界。没有从共同作者推断在读学生，没有沿用历史专项名额，没有提供录取、资助或招生人数承诺。

## 八、后续发布到GitHub Pages

1. 审核TODO中的正式对外资料，按需移除页脚“本地预览稿”。
2. 创建自己的仓库；当前origin仍是上游模板，先改名为upstream，再把自己的仓库设为origin，不要误推上游。
3. `_config.yaml` 设置真实`url`与`baseurl`，项目仓库使用`/仓库名`；账号主页仓库使用空baseurl。
4. 提交源码、锁文件和许可，排除vendor、_site、.bundle和.local。
5. 仓库Settings → Pages选择GitHub Actions，手动运行“手动发布已审核网站到 GitHub Pages”。普通push不会自动发布。
6. 上线后复查真实域名下的双语页面、语言切换、资源、404及sitemap。

详细可复制命令、内容添加字段与构建步骤见 [README.md](README.md)。
