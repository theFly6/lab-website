# 代码与架构独立审查

审查日期：2026-10-19。审查对象：当前本地 `lab-website` 工作树。此报告记录审查时的发现，修复结果由主 Agent 在最终报告中统一记录。审查只读实现文件，未安装依赖、运行部署或更改网站数据。

## 发现

### ARCH-01 · P2：锁文件保留已公告安全问题的构建／预览依赖

- 位置：`Gemfile.lock:114`（Nokogiri 1.13.10）、`:132`（REXML 3.2.5）、`:160`（WEBrick 1.8.1）；`start.sh:11` 的预览服务监听 `0.0.0.0`。
- 证据：当前锁文件确实选择这些版本。REXML 官方公告列出 `<3.2.7` 受影响，异常 XML 属性可能导致耗时过长；Nokogiri 官方公告列出使用捆绑 libxml2 时 `<1.14.3` 的解析崩溃问题；WEBrick 项目已记录 1.8.1 对冲突 HTTP 长度头的处理问题。
- 影响边界：这些是 Ruby 构建工具及本地预览服务器的依赖问题。未证明当前受信任资料触发漏洞，静态 GitHub Pages 产物也不运行 Ruby。本站无登录／反向代理场景，不能把 WEBrick 的公告直接解释成本站已存在鉴权绕过。
- 建议：在项目级依赖范围定向更新 `nokogiri`、`rexml`、`webrick`，保留锁文件，重新构建并检查；默认只监听本机地址，确需局域网预览时再显式选择开放监听。无需改换技术栈。
- 一手来源：[REXML 官方公告](https://github.com/ruby/rexml/security/advisories/GHSA-vg3r-rm7w-2xgh)、[Nokogiri 官方公告](https://github.com/sparklemotion/nokogiri/security/advisories/GHSA-pxvg-2qj5-37jq)、[WEBrick 项目问题与修复关联](https://github.com/ruby/webrick/issues/145)。这些公告用于确认问题存在，不代表这里只需升级到当年最低修复版本即可覆盖后续所有公告。

### ARCH-02 · P2：结构化数据中的普通文本没有统一 HTML 转义

- 位置：`_includes/lab/publication.html:5-9`、`_includes/lab/people.html:3-4`、`_includes/lab/news.html:1`、`_includes/lab/research.html:2`，以及 `header.html`、`head.html` 的部分属性值。
- 可复现：使用本项目当前 Bundler/Liquid，在内存中以论文模板相同的表达式渲染标题 `Performance of <GPU> kernels & storage`，实际输出为 `<h3><a href="https://doi.org/10.1234/example">Performance of <GPU> kernels & storage</a></h3>`。`<GPU>` 被当作标签，浏览器无法按原文字显示；含引号的数据用于 `alt` 等属性时也会破坏属性边界。
- 影响：README 指导维护者直接向 JSON 添加论文、姓名等普通文本，合理的特殊字符会被当成标记。当前数据由本地维护、没有浏览器提交入口，本次未发现正在使用的恶意值，不应称为已遭利用的远程漏洞。
- 建议：普通文本和 HTML 属性值使用 `escape`；作者先转义，再只对目标姓名加固定 `<strong>` 标记。若某字段确实允许 HTML，应单独明确约定，不能让所有纯文本字段默认获得 HTML 语义。链接值除属性转义外，可在数据检查时限定预期 `https`／`mailto` 等协议。

### ARCH-03 · P3：遗留 Docker 入口仍调用与当前来源结构不兼容的旧引文流程

- 位置：`.docker/entrypoint.sh:8` 调用 `_cite/cite.py`；`_cite/cite.py:42-56` 扫描 `_data/sources*` 并要求 `list[dict]`；`:180-181` 在汇总错误退出前保存生成结果。
- 证据：当前 `_data/sources.json` 是以 `faculty`、`college` 等为键的对象。使用 Python 标准库读取，类型为 `dict`，与旧引文流程要求的 `list` 不相容。代码路径会报告 `sources.json data file not a list of dicts`；没有其他引文输入时，还会生成空的 `_data/citations.yaml`，随后以错误状态退出。Docker 入口未设置 `set -e`，仍继续启动后续进程。
- 影响：README 推荐的 `start.sh` 路径不使用该入口，主要功能不受影响。但保留的 Docker 启动实现容易被误当作本项目有效运行方式，产生无意义报错及额外文件。
- 建议：明确标记 Docker／旧自动引文流程当前不受支持，或者从 Docker 入口移除自动引文调用。不要在当前来源注册表上运行旧的自动引文工具；无需恢复自动采集或重新生成已核查论文。

## 已检查且未见阻塞问题的范围

- `/zh/` 与 `/en/` 为薄路由，共享 `_includes/lab/` 结构；实体双语字段与两份 locale 独立维护，架构符合维护要求。
- 语言切换按 `page_key` 和 `lang` 查找对应路由，无需运行时翻译服务。
- 论文与其他实体从 JSON 读取，增加记录无需复制整页布局；首页论文选取、年份与主题筛选均由数据生成。
- `assets/site.js` 没有 `eval`／`innerHTML` 注入路径；搜索输入只用于字符串匹配与 `textContent` 更新。手机菜单有展开状态和 Escape 处理。
- 当前 `default.html` 不调用上游 `_includes/scripts.html`，故其中遗留 CDN 脚本不会被现有页面加载；也未发现当前 SCSS 的外部字体导入。
- 上游示例成员、示例博客已删除；旧演示目录在配置中排除。生成根目录仅见预期网站路由及静态资源。
- GitHub Pages 工作流只接受手动 `workflow_dispatch`；未发现自动定时发布、`pull_request_target`、在不可信 PR 上运行高权限 shell 等模式。保留自定义插件时使用 Actions 生成静态产物的选择合理。
- `vendor`、`.bundle`、`.local`、构建缓存在忽略配置中，常规构建不会发布这些目录。未发现本站存在表单后台、用户账号或需要保管的网站运行密钥。
- 上游 `_plugins/misc.rb` 的 `data_filter` 确实使用 Ruby `eval`，`file_read` 可读文件，但当前页面没有使用这些功能，且可改写模板的作者本身拥有源码执行权限。本次不将其误判为访客可以触发的远程执行漏洞，也不建议为此大规模重构。

## 合并验收提示与限制

- 本报告写入 `docs/`，该目录已排除发布；后续新增根目录 `FINAL_REPORT.md` 应同步列入 `_config.yaml` 的 `exclude`，避免把内部交接报告发布到网站。
- 本次没有启动 Docker、攻击预览服务器或进行全量漏洞扫描；依赖结论来自锁文件与官方公告，并已说明适用条件。
- 本审查不替代资料真实性与浏览器 UI 审查，也未把历史构建记录当作本次重新构建结果。
- 仅在内存执行了 Liquid 特殊字符渲染及 Python JSON 类型检查；没有改动实现或实体数据。

## 追加：定向更新停在 Nokogiri 1.14.5 的原因

主 Agent 反馈 `bundle update nokogiri rexml webrick --conservative` 暂时解析到 Nokogiri 1.14.5。本次追加仅进行只读分析，没有启动第二个安装任务或改动锁文件。

- 当前锁文件的 `mini_portile2` 是 **2.8.1**。Nokogiri [v1.15.0 官方 gemspec](https://raw.githubusercontent.com/sparklemotion/nokogiri/v1.15.0/nokogiri.gemspec) 和 [v1.19.4 官方 gemspec](https://raw.githubusercontent.com/sparklemotion/nokogiri/v1.19.4/nokogiri.gemspec) 都要求 `mini_portile2 ~> 2.8.2`，所以冻结 2.8.1 会阻止这些版本；这是保守更新停在旧分支的具体约束。
- `html-proofer` 的 `nokogiri ~> 1.13` 与 `jekyll-spaceship` 的 `nokogiri ~> 1.6` 都允许 1.19.4。本次以 Ruby `Gem::Requirement#satisfied_by?` 对两项约束实际求值，均得到 `true`；它们不是 `<1.15` 版本上限。
- `racc` 当前锁定 1.6.2，仍满足 v1.19.4 的 `~> 1.4`。它不是硬性升级阻塞，最小范围修复只需额外解锁 `mini_portile2`；也可把 `racc` 一起点名，作为同一解析工具链的小范围更新。
- v1.19.4 要求 Ruby `>=3.2`，本项目实测环境和 Actions 选择的 Ruby 3.3 满足条件。其 [RubyGems 官方版本页](https://rubygems.org/gems/nokogiri/versions/1.19.4) 给出了 2026-06-18 的版本与平台列表。

建议主 Agent 等现有唯一安装任务结束后，在同一项目中执行：

```bash
bundle update nokogiri mini_portile2 rexml webrick --conservative
```

若希望一并更新解析器工具链，可将 `racc` 加入点名列表。不要为解除此约束运行不带 gem 名称的全量更新，也不必升级 Jekyll、html-proofer 或替换模板。解析后确认 Nokogiri 实际版本、锁文件变化范围，再运行构建及现有检查；如果仍未达到预期，保留解析日志逐项检查 Ruby／平台约束，不要仅以“bundle update 成功”作为安全问题已经解决的证据。
