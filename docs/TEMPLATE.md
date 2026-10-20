# 模板研究与改造记录

## 上游与本地关系

- 模板：https://github.com/greenelab/lab-website-template
- 演示：https://greenelab.github.io/lab-website-template/
- 本次基线提交：`cca827da53417f039cb485bc8930a6d163aaa48a`
- 上游许可：保留根目录 `LICENSE.md`；页脚保留模板署名。
- 当前目录是上游的独立克隆，`.git` 保留原始历史与来源，未推送；开始自己的仓库前按 README 调整 remote。

## 原有技术与组织

原模板使用 Jekyll 4、Liquid、Markdown/YAML、SCSS、Ruby 自定义过滤器。`_layouts/default.html` 连接 head/header/content/footer；`_includes/content.html` 解析 `section.html` 标记，生成可设置宽度、深浅色和背景的分区。`_data` 管理论文与项目，`_members` 和 `_posts` 是原成员与博客集合；`_cite` 是可选的自动书目更新工具。原始本地构建命令为 `bundle install`、`bundle exec jekyll serve`，另有 `.docker` 容器配置。

本项目保留 Jekyll 技术栈、分区实现、自定义过滤器、SCSS 基础与现成组件源文件，定制站点标题、导航、页脚和页面内容。未改成另一个前端框架，未引入客户端数据库或服务器接口。

## 双语方案

- `/zh/` 和 `/en/` 下各8个薄路由文件，只有 `lang`、`page_key`、`permalink` 和一个 include。
- `_includes/lab/` 下维护一份页面结构；`_data/locales/zh.json`、`en.json` 分别维护界面与正文文案。
- 实体数据使用明确的 `zh`/`en` 字段，作者、DOI、日期等客观字段共用。
- 语言导航按 `page_key` 查找同页另一语言版本；不依赖 JS、不自动回首页。
- 页面设置准确的 HTML `lang`、对应语言的元信息与 alternate/hreflang；中文主页为根入口默认选择。
- 所有本地链接使用 `relative_url`，保持 GitHub Pages 项目子路径兼容。

## 视觉参考的采用

| 参考 | 观察与本项目采用 |
| --- | --- |
| Greene Lab 主模板 | 保留清晰导航、分区留白、宽正文与轻量组件方式；深色主视觉改为计算系统主题。 |
| https://www.sjkimlab.org/projects | 参考按研究问题逐项解释的方式；研究页采用独立主题、简介和来源，不复制其生物学内容。 |
| https://kenji-fukushima-lab.github.io/ | 参考首页先说明研究定位、再引导到具体内容；没有证据的团队人数和论文总数不做统计展示。 |
| https://martinbulla.github.io/bullab/ | 参考团队、论文与Join Us的清晰入口，保持学术网站的轻量排版。 |

`docs/*-reference.png` 保存了浏览器实际访问时的参考截屏，仅为设计研究记录，不进入网站构建。

## 必要调整

1. 清除原模板示例成员、博客与论文数据，排除旧演示路由，避免示例成果混入。
2. 保留组件与底层 SCSS；新增 `_styles/zz-lab.scss` 集中覆盖站点视觉、手机布局及可访问性。
3. 不加载原有 Google Fonts、Font Awesome 或 CDN 脚本；正文、图形与交互本地可用。字体使用系统字体，JavaScript只有手机菜单和论文筛选。
4. 模板锁定的 `sass-embedded 1.58.3` 在 Ruby 3.3 环境安装失败；更新为二进制可用版本及 `jekyll-sass-converter 3.1.0`，保留最终 `Gemfile.lock`。
5. Jekyll 4.3.2 与 Ruby 3.3 的 logger 接口不兼容，更新为 Jekyll 4.4.1；仍使用同一 Jekyll 4 技术栈。
6. 删除未用到的 `jekyll-last-modified-at` gem与插件配置：其 `posix-spawn` 旧扩展在当前GCC下失败；网站的内容核查日期来自显式数据，不依赖该插件。
7. 原自动定时引文/部署工作流换成单个手动 `pages.yml`，防止样例自动同步改写已核查数据；本阶段没有执行部署。

以后维护优先修改 `_data`，尽量不改底层布局。上游更新应逐项合并，不直接覆盖已定制的 header、head、footer 和 default layout。
