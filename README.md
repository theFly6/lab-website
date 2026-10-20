# 李建江课题组双语网站（本地初稿）

基于 [Greene Lab Website Template](https://github.com/greenelab/lab-website-template) 搭建。保留 Jekyll / Liquid / SCSS 技术栈与模板分区、组件结构；没有部署、创建远程仓库或购买服务。

完整交付与4个独立Subagent交叉审查结果见 [FINAL_REPORT.md](FINAL_REPORT.md)。

## 本机启动

当前机器已在已有 **Ubuntu WSL** 中安装 Ruby 3.3 与 Bundler，网站 gems 安装在本项目 `vendor/bundle/`，不需要 Node.js。

构建后的自动检查需要 Python **3.9 或以上版本**。浏览器复验使用可选的 [agent-browser](https://github.com/vercel-labs/agent-browser)，需要 Node.js：`npm install -g agent-browser`，随后运行 `agent-browser install`；日常浏览网站无需这些测试工具。

在 PowerShell 中运行：

```powershell
cd D:\ClaudeSessions\with-zetero\lab-website
.\start.ps1
```

`start.ps1` 使用 **UTF-8 with BOM** 保存，以兼容 Windows 自带的 PowerShell 5.1。编辑该脚本时请保留 BOM；普通无 BOM 的 UTF-8 会使 PowerShell 5.1 把中文误读为本地编码，并可能报“字符串缺少终止符”。PowerShell 7 也能运行带 BOM 的版本。

如果 PowerShell 的本机脚本执行策略阻止执行，直接使用以下命令，不需要更改系统执行策略：

```powershell
wsl -d Ubuntu -- bash /mnt/d/ClaudeSessions/with-zetero/lab-website/start.sh
```

访问：

- 中文：<http://localhost:4000/zh/>
- 英文：<http://localhost:4000/en/>
- 根路径默认进入中文。导航栏的 `中文 / EN` 保持当前页面对应关系。

关闭运行窗口或按 `Ctrl+C` 停止服务。端口占用时可运行 `.\start.ps1 -Port 4001`。WSL 使用 `--force_polling` 监听 Windows 目录中的内容修改；配置文件修改后需要重启。

## 在其他机器安装

依赖：Ruby **3.3**、Bundler、编译工具（部分 gems 含原生扩展）。推荐 Ubuntu/WSL；原生 Windows RubyInstaller + Devkit 也可使用相同 Jekyll 命令，但本次只在 WSL 实测。

Ubuntu 安装运行环境（只需一次）：

```bash
sudo apt-get update
sudo apt-get install -y ruby-full ruby-bundler build-essential libyaml-dev zlib1g-dev
```

进入项目后安装项目级依赖并启动：

```bash
bundle config set --local path vendor/bundle
bundle install
bash start.sh
```

保留并提交 `Gemfile.lock`。第一次安装需要联网，后续本地构建与页面浏览无需加载外部字体或脚本。若 WSL 中 `127.0.0.1:7892` 无法访问 Windows 代理，不要修改系统代理配置；本机测试时 RubyGems 可直连，GitHub 与 Crossref 资料请求使用 Windows 本地代理。`scripts/collect_metadata.py` 是可选的书目核查工具，不是构建步骤。

## 页面与内容

8 个页面各有中英文版本：Home、People、Research、Projects、Publications、News、Join Us、Contact。

顶部一级导航为：首页、研究方向、科研项目、学术论文、更多、加入我们、联系我们；团队介绍和新闻动态放在「更多 / More」下拉菜单。点击或用键盘展开，移动端在主菜单内展开；`Escape` 先关闭下拉，再关闭手机菜单。访问团队或新闻页时，「更多」同步显示当前分组状态。

已填入：1位已核实导师、4个依据官方资料归纳的研究主题、6项历史项目、7篇核实后的论文、1条学院公开新闻、公开邮箱与官方招生入口。补充了3项公开任职记录、2项学术服务、2门课程、2本公开书名及HPCDE和工程研究中心两个相关科研平台。博士/硕士/毕业生分类已预留，未填造姓名。论文按题目/作者关键词、年份、主题筛选，关闭 JavaScript 也可读全部论文。

导师页还展示5项教学奖励、2类人才培养成果及研究生课程认定，来源为用户提供并与学校公开简介对应的资料。奖项保留原始届次、等级与括号信息；“70余篇”仅为公开简介中的历史记录。采用边界与未展示的评教排名说明见 [TEACHING_CONTENT.md](docs/TEACHING_CONTENT.md)。

基础论文与项目核查日期为 **2026-10-19**，HPCDE及导师扩展资料核查于 **2026-10-20**；访问日期不代表原文更新日期，这7篇也不构成最新或完整成果清单。来源与边界见 [docs/SOURCES.md](docs/SOURCES.md) 和 [HPCDE补充记录](docs/HPCDE_RESEARCH.md)，尚缺信息见 [TODO.md](TODO.md)，构建和浏览器检查见 [docs/TESTING.md](docs/TESTING.md)。

## 双语与目录

```text
_data/
  locales/zh.json             # 中文导航、文案、招生与联系说明
  locales/en.json             # 对应英文，独立编辑
  people.json                 # 人员及分类
  platforms.json              # 相关科研平台、公开入口与范围说明
  publications.json           # 论文、作者、DOI、年份、主题
  projects.json               # 项目、执行期、角色、编号与来源
  research.json               # 研究主题、关键词与来源
  news.json                   # 新闻日期、正文与出处
  sources.json                # 公共来源注册表
  navigation.json             # 页面全集 pages、一级顺序 primary、下拉分组 dropdowns 与语言
zh/、en/                     # 每页约数行的薄路由文件
_includes/lab/                # 每种页面共用一份布局
_layouts/default.html         # 共用外壳，按page.lang载入文案
_styles/zz-lab.scss            # 站点视觉与响应式覆盖
assets/                       # 本地照片、SVG、JavaScript
scripts/check_site.py         # 构建后内部链接与双语检查
docs/                         # 来源、模板改造与测试记录，不发布
```

实体数据使用 `{"zh": "中文", "en": "English"}` 独立字段；作者姓名、DOI、日期等共用。英文内容不会在运行时由翻译服务生成。修改某语言时不需改另一语言布局。

所有路由具有同一 `page_key`；顶部语言切换查找同键的另一语言页面。移动端菜单支持键盘、`Escape`关闭与明确的展开状态，关闭JavaScript后导航仍可访问。

## 日常内容修改

JSON 采用 UTF-8，字符串中的双引号需要写为 `\"`；建议编辑前备份，并运行检查防止缺少逗号或误删字段。

**添加论文**：在 `_data/publications.json` 追加一项，填 `id`、`title`、`year`、`venue`、`volume`、`issue`（可为null）、`pages`、`authors`数组、`doi`、`source`、`topic`、`featured` 和中英文 `summary`。主题键目前为 `hpc`、`storage`、`systems`，在两份locale的 `topics` 中修改主题显示名。`featured: true` 自动进入首页。追加前核对作者顺序与卷期年，不必改页面。

**添加人员**：在 `_data/people.json` 追加一项。分类 `category` 为 `faculty`、`doctoral`、`masters`、`alumni`。学生与毕业生只需 `id`、`category`、双语 `name` / `bio`，`image`、`url`可选；相应分类有数据时自动隐藏TODO。导师另有双语 `role`、`email`、`timeline` 字段。必须确认身份与展示授权，不凭共同作者关系添加。

**添加项目**：在 `_data/projects.json` 追加，提供双语 `title`、`program`、`role`、`description`，以及 `period`、`source`（指向sources中的键）、`number`（未知为null）。`related`只在有证据的论文资助对应关系时设置为论文id。

**导师与科研平台**：导师的 `appointments`、`academic_service`、`teaching` 和 `books` 分别维护任职、学术服务、课程与著作；`teaching_awards`、`mentoring` 分别维护教学奖励与人才培养记录，课程可用 `recognition` 增加双语教学认定。奖项的 `edition` 是届次，`record` 为原文括号信息。`books` 的 `first_author` 仅表示来源列出的第一作者，不能替代完整作者列表。相关平台维护在 `_data/platforms.json`，保留 `scope` 范围说明，避免把多导师平台的成员和整体成果归入个人课题组。

**添加新闻**：在 `_data/news.json` 顶部追加，提供唯一 `id`、ISO格式 `date`、双语 `title` / `summary` / `body`、`source`。页面与首页自动显示，无需修改布局；日期采用事件公告的实际发布日期。

**招生信息**：分别修改两份locale的 `join` 字段。当前“了解研究—准备交流—核对政策”是沟通建议，不是导师制定的报名条件；正式计划请先向导师确认。

**图片**：放入 `assets/` 并在数据中使用 `/assets/文件名`，模板会补上baseurl。不要写Windows绝对路径，不要把未授权实验室照片当成装饰图。

**站点图标**：采用与页眉一致的计算节点标识 `assets/mark.svg`，并提供 `assets/favicon-32.png`、`assets/apple-touch-icon.png` 和根目录 `favicon.ico`，兼容常见浏览器及主屏幕收藏。它是本站的通用科研标识，不是学校官方校徽。更换标识时请同步更新这些导出文件；图标引用统一在 `_includes/head.html` 中，支持 GitHub Pages 子路径。

**右下角悬浮联系**：在 `_data/floating_contact.json` 修改 `email` 与双语 `name`；`enabled: false` 可关闭入口。本地试版按用户要求采用学生联系人张云飞与此前记录的 `zhangyunfei@xs.ustb.edu.cn`，不表示学校正式指定的招生咨询邮箱。卡片文案位于两份locale的 `floating_contact` 字段。所有中英文内容页及404共用 `_includes/floating-contact.html`，配套样式为 `_styles/floating-contact.scss`；无需逐页修改。支持发送邮件、复制邮箱、同语言招生/联系页入口、Escape关闭和焦点恢复。复制权限受限时会选中邮箱并提示手动复制；不自动发送邮件。关闭JavaScript后仍能展开卡片与访问邮件链接，复制和关闭按钮隐藏，可再次点击「联系」收起。

## 构建与检查

在 WSL / Linux 项目目录：

```bash
bundle exec jekyll build
python3 scripts/check_site.py
```

在本机 PowerShell：

```powershell
wsl -d Ubuntu -- bash -lc 'cd /mnt/d/ClaudeSessions/with-zetero/lab-website && bundle exec jekyll build'
python -X utf8 scripts/check_site.py
```

旧模板的 `.docker/entrypoint.sh` 与 `_cite/cite.py` 自动同步流程已弃用：本站的 `sources.json` 是人工核查的来源注册表，不是旧引文输入。入口已禁用以避免误覆盖数据；本轮没有验收 Docker，不要沿用旧模板 Docker 命令。

产物在 `_site/`。检查包含内部页面、资源与锚点、16条双语路由、语言对应关系、单一h1、双语键一致性、重复DOI及示例残留。外部网站可能限流，脚本不会因出版社拦截本地浏览器而判定本地构建失败。

模拟 GitHub Pages 仓库子路径：

```bash
bundle exec jekyll build --baseurl /lab-preview --destination .local/site-subpath
python3 scripts/check_site.py --site .local/site-subpath --baseurl /lab-preview
```

## 以后发布到 GitHub Pages

本次没有执行以下发布操作。资料审核完成后：

1. 根据TODO确认名称、成员、招生、照片与联系方式；调整或移除双语页脚的草稿标记。
2. 创建自己的GitHub仓库。当前git remote仍指向上游模板，不要推送到上游；可以把它重命名为`upstream`后，将自己的仓库设置为`origin`。
3. 在 `_config.yaml` 设置 `url: "https://你的账号.github.io"`。项目仓库设置 `baseurl: "/仓库名"`；`账号.github.io` 主页仓库的 `baseurl` 留空。
4. 将源码（含Gemfile.lock和LICENSE）提交到自己的仓库，忽略vendor、_site、.bundle、.local。本站含自定义Jekyll插件，选择仓库 Settings → Pages → **GitHub Actions**，不要直接让内置Pages Jekyll编译源码。
5. Actions 中手动运行 `手动发布已审核网站到 GitHub Pages`。提供的 `.github/workflows/pages.yml` 构建并检查内部链接，然后发布静态产物；配置为手动触发，单纯push不会自动上线。
6. 上线后复查 `/zh/`、`/en/`、所有语言切换及子路径资源。

自定义域名、统计服务、表单或账号系统尚未设置，也不是本阶段所需。

## 模板与许可

原始模板与改造说明见 [docs/TEMPLATE.md](docs/TEMPLATE.md)。`LICENSE.md`保留上游BSD 3-Clause许可，页脚保留模板署名。照片与学校标识不因模板BSD许可而自动取得使用授权。
