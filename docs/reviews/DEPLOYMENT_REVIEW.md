# 测试与部署独立审查

审查日期：2026-10-19。范围：构建检查脚本、浏览器检查脚本、Jekyll 配置、启动脚本、发布 workflow、README，以及现有本地产物和运行中的 HTTP 服务。审查者只写本报告和 `docs/reviews/deployment/` 证据，没有安装依赖、构建或修改实现，没有执行 GitHub 发布。

## 结论

主要路由和资源实测可用，维护资料未泄漏到公开路径。初审发现的关键问题集中在验收脚本的假通过与新增 404 页：根 Agent 已修复实现，故障注入复验确认测试现在会保留历史页面错误，并以非零状态拒绝浏览器脚本错误。404 修复源码已检查，最终产物与生产域名构建由根 Agent 统一复验，避免多个 Agent 同时写 `_site/`。

## 本轮独立实测

- 在根 Agent 修改验收逻辑前，使用原 `check_site.py` 检查现有产物：根路径 18 个 HTML / 1,010 处内部链接与资源，通过；既有 `/lab-preview` 产物 18 个 HTML / 1,042 处内部链接与资源，通过。这些是当时产物的实测计数，不代表最终修复后的计数。
- HTTP 探测根入口及中英文各 8 页：17 个正常路由均返回 200。发现的 50 个独立 CSS、JavaScript、图片资源均返回 200；不存在页面返回 404。记录：[http-current.json](deployment/http-current.json)。该快照取于 404 修复构建前，因此保留了当时 404 的转义标签问题。
- `/docs/SOURCES.md`、`/scripts/check_site.py`、`/FINAL_REPORT.md`、`/Gemfile`、`/.git/config` 均返回 404。
- 验收修复后做了合成故障注入：在内存中提供一个横向溢出页面和一个脚本错误，拦截浏览器调用及报告写入，不访问真实浏览器、不覆盖 `docs/browser-checks.json`。结果两个失败均保留，退出码为 1。证据：[test-blindspot-probe.json](deployment/test-blindspot-probe.json)，复现程序：[test_blindspot_probe.py](deployment/test_blindspot_probe.py)。此结果只验证测试框架会拒绝失败，不能解释成真实页面发生了这些故障。

## 问题与处理情况

| 优先级 | 初审问题与证据 | 修复与复验 |
| --- | --- | --- |
| P2 | `browser_checks.py` 原先只把 `call('errors')` 写入 `browser_errors`，退出码只看 `REPORT['errors']`，真实 JavaScript 错误可能未影响验收结果。 | 根 Agent 将脚本错误合并到失败列表。合成注入已确认退出码 1。 |
| P2 | `--interactions-only` 原先仅复制旧报告的 `pages`，丢弃旧页面 `errors`；已有布局失败可能在部分复验后消失。 | 新增 `page_failures()`，重新验证继承的页面状态；合成注入确认旧页面失败仍保留。 |
| P2 | 新增 `404.md` 将整页 HTML 写在一行，Markdown 构建后把文档及 h1 标签转义为文字。旧检查只验 16 个主页面，因此仍通过。 | 根 Agent 改为独立 `404.html`，有效文档结构已静态检查；`check_site.py` 新增 404 的 lang / h1 检查。产物最终复验交由根 Agent。 |
| P3 | 论文交互断言写死 7/3/2 篇，与文档承诺的直接追加论文数据不一致。 | 改为从数据文件取得总量、从页面数据计算筛选预期；保留关键词、年份、主题及三条件组合检查。已读源码核实。 |
| P3 | 进程中断或浏览器异常可能留下旧报告，缺少明确的本轮完成状态。 | 报告新增 `complete` 状态，入口异常处理记录本轮失败。已读源码核实；完整实浏览器运行由根 Agent 执行。 |

## 部署与环境审查

- 发布工作流只支持 `workflow_dispatch`，普通 push 不会部署；采用 `ruby/setup-ruby` 的 Ruby 3.3、锁文件安装、生产环境 Jekyll 构建、内部链接验收、上传 `_site`、独立 deploy job。适用于本项目含自定义插件的情况。没有执行云端 workflow，不能将本地检查称为 GitHub Actions 实测通过。
- `actions/configure-pages` 的 `base_path` 同时传给构建和链接检查。README 明确要求正式发布前填写 `url` 和 `baseurl`，并选择 GitHub Actions 发布方式。
- 开发配置的 `url` 为空，旧子路径产物中的 sitemap 为相对路径；本地 `jekyll serve` 中的 sitemap 使用本地地址。这些不能直接作为最终线上 SEO 配置。根 Agent 已安排使用示例 HTTPS 域名及 `/lab-preview` 的生产构建，对 canonical、hreflang、sitemap 统一复验。正式域名仍需要用户填写。
- Windows 启动脚本经 `wsl --exec` 调用 `wslpath`，再执行项目 `start.sh`；后者设置项目级 Bundler 路径，开发启动显式覆盖空 baseurl，支持 PORT。依赖安装和启动记录读取自 `docs/TESTING.md`，本审查没有重新启动第二个服务。
- 本机 Python 3.9 能执行检查脚本；`Path.is_relative_to()` 要求 Python 3.9 或更新版本。GitHub `ubuntu-latest` 默认 Python 可满足，建议 README 明确 Python 下限，避免维护者使用旧环境。

## 仍有边界

- 独立 HTTP 检查验证了返回状态、资源加载和排除目录，没有代替浏览器布局与交互；完整桌面/移动端浏览器复验由根 Agent 与 UI 审查承担。
- 外部链接的访问控制、长期可用性不能由本地内部链接脚本保证；论文和官方来源核查由内容审查负责。
- 当前没有可证据支持的发布阻塞性缺陷；最终生产构建与 404 产物复验需以根 Agent 的最终记录为准。
