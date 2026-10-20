# 搜索引擎收录与后续维护

## 网站与配置

本站已通过 GitHub Pages 发布，中文入口为 <https://thefly6.github.io/lab-website/zh/>，英文入口为 <https://thefly6.github.io/lab-website/en/>。发布、收录、搜索排名是不同状态：网址可打开不代表搜索引擎已经抓取或收录，也不保证某个词的排名。

- `_data/locales/zh.json`、`en.json` 的 `seo` 保存各页面独立标题和摘要。修改研究内容时同步检查对应摘要，避免堆砌关键词。
- 共用头部输出 title、description、Open Graph、canonical 和中英文 hreflang；根入口指向中文首页，并保留两种语言入口。
- `_config.yaml` 的 `google_site_verification` 保存用户提供的公开验证标识，根入口及16个中英文内容页均引用同一配置。验证成功后继续保留；它不是账号密码。
- `jekyll-sitemap` 已负责生成 `sitemap.xml`，无需手动列出新增网址。当前地图包含16个内容页及根入口。
- 本地预览使用空 `baseurl`；Pages 工作流根据仓库自动传入 `/lab-website`。配置中的 `url` 保留 `https://thefly6.github.io`。

## 首次验证与提交

1. 在 [Google Search Console](https://search.google.com/search-console) 用自己的账号添加**网址前缀**资源：`https://thefly6.github.io/lab-website/`，结尾保留 `/`。这样包含中英文子页面。本站不能通过项目仓库控制 `github.io` 的 DNS。
2. 选择 HTML 标记验证。用户本轮给出的验证码已接入源码。必须先将包含标记的版本发布到 Pages，再点“验证”；仅本地构建成功还不够。
3. 仓库 Actions → **手动发布已审核网站到 GitHub Pages** → **Run workflow**，选择已经包含这些更改的分支（合并后通常选 `main`）。推送源码本身不会自动部署。
4. 发布成功后打开线上中文首页的“查看网页源代码”，搜索 `google-site-verification` 确认标记存在，再回 Search Console 点“验证”。根入口也含标记，跳转后的中英文首页同样含标记。
5. 在“站点地图 / Sitemaps”提交 `sitemap.xml`；完整网址为 <https://thefly6.github.io/lab-website/sitemap.xml>。
6. 在顶部“网址检查 / URL Inspection”粘贴中文首页完整地址，检查实时网址；可索引时请求编入索引。英文首页、导师页、论文页、加入我们页也可以分别提交。提交请求不代表已经收录，不必反复点击。
7. 之后查看“网页索引”报告及各网址的检查结果。Google 没有保证收录或时限；官方说明抓取可能需要数天至数周。每次普通内容更新无需重做验证，新增页面通过 Sitemap 被发现即可。

以上账号内操作尚需站点所有者完成。本地构建、公开网页可访问和验证标记存在，均不能代替 Search Console 给出的验证或索引结果。Google 的提交只针对 Google，其他搜索引擎需各自处理。

## 可以使用的搜索词

以下是在 **Google 搜索框**中输入的查询示例；收录之前可能没有结果，不承诺这些词已经能搜到本站。

```text
北京科技大学 李建江 课题组
"李建江课题组"
李建江 高性能计算 北京科技大学
Jianjiang Li USTB research group
site:thefly6.github.io/lab-website 李建江
site:thefly6.github.io/lab-website 研究生 申请
site:thefly6.github.io/lab-website "Crystal-MD"
```

前三类自然词适合访客寻找团队；加学校名称有助于区分同名学者。`site:` 后不要加空格，它将结果限定到本站路径，适合自己检查相关页面。`site:` 结果并不完整：查不到不能单凭这一项判定未收录，应查看 Search Console 的网址检查。直接访问完整网址仍是当前可靠的分享方式。

后续可以在有权限的学院/导师主页、真实学术个人主页中添加本站链接，并持续发布可核实的论文、研究介绍及招生说明，帮助访客与搜索引擎发现内容。是否添加由相关主页的维护者决定。

## 复验命令

```powershell
wsl -d Ubuntu --exec env JEKYLL_ENV=production bundle exec jekyll build --baseurl /lab-website --destination .local/site-seo
python -X utf8 scripts/check_site.py --site .local/site-seo --baseurl /lab-website --expected-origin https://thefly6.github.io --expected-verification MHs2HiN4OVxke_pajT57NCcAlCY_WsPziCcv8quTOf4
```

检查内容包括16页独立标题/摘要、Open Graph一致性、无 `noindex`、语言对应、canonical、Sitemap 和根入口/内容页验证标记。验证码更新时同步调整上述命令参数。

## 官方参考

- [Search Console 所有权验证](https://support.google.com/webmasters/answer/9008080?hl=zh-Hans)
- [Sitemaps 报告](https://support.google.com/webmasters/answer/7451001?hl=zh-Hans)
- [请求 Google 重新抓取](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl?hl=zh-cn)
- [site: 查询的用途和限制](https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site?hl=zh-cn)
- [搜索结果标题](https://developers.google.com/search/docs/appearance/title-link?hl=zh-cn)
- [搜索摘要与 description](https://developers.google.com/search/docs/appearance/snippet?hl=zh-cn)
