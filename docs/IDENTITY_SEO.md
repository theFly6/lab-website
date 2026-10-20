# 首页、导师身份与研究生申请指南优化

## 本轮范围

按前两项优先工作整理首页/导师身份，以及博士、硕士申请指南。保持原模板、导航、双语路由、学生悬浮联系与既有TODO。没有新增招生年份、计划、名额、门槛、考核或资助承诺。

- 首页H1改为学校与课题组名称，原宣传标语保留为副标题；中文正文自然使用“北京科技大学（北科大）”，英文展开USTB全称。
- 导师页主标题、简介和搜索元数据明确李建江教授、计算机与通信工程学院、博士生导师及清华大学工学博士身份。事实均来自既有已核实资料，没有增加新的任职或成果。
- 申请页明确区分博士、硕士申请，补充研究主题入口、导师与论文链接、交流准备建议及3项常见问题。未知年度安排仍保留TODO，沟通建议不作为正式申请条件。
- 6个中英文页面的标题/摘要与可见正文同步调整，不将不同关键词拆成大量重复页面。

## 内容维护

- `_data/locales/zh.json`、`en.json`：`hero.heading`为首页主标题，`hero.tagline`为原宣传标语，`hero.text`为首屏介绍。
- `page_titles.people`、`page_titles.join`控制页面H1，与较短的导航名称分离；其他页面仍回退到原导航名称。
- `seo.home`、`seo.people`、`seo.join`控制相应搜索标题/摘要。
- `_data/people.json`的`bio`维护导师首段简介，其他任职、教学和历史成果保持原记录。
- locale的`join`维护申请说明，`join.faq`维护可见问答。研究主题链接由现有`_data/research.json`生成。

资料确认边界和原始来源继续见 [SOURCES.md](SOURCES.md)、[HPCDE_RESEARCH.md](HPCDE_RESEARCH.md)、[TODO.md](../TODO.md)。本轮不删除未完成事项。

## Sitemap与Google更新

网站地址、语言目录与页面路径都没有变化，Google验证码也没有更换。因此：

1. 不需要重新添加Search Console资源或验证所有权。
2. 不需要重新设置或反复提交Sitemap。Jekyll会在构建时重新生成同一地址的地图；本轮地图的17个网址集合与之前已发布版本完全一致。
3. 将修改发布到Pages后，搜索引擎下次抓取时才会看到新内容。搜索结果中的标题/摘要不会随部署立刻同步。
4. 如需主动通知Google，可对已修改的首页、导师页、申请页分别用网址检查请求重新抓取一次；这是可选步骤，不是每次内容更新的必要流程，重复申请不会加速。
5. 不承诺某关键词排名、展示样式或生效时间。Google可能自行选择搜索标题与摘要。

官方说明：[请求重新抓取](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl?hl=zh-cn)、[标题优化](https://developers.google.com/search/docs/appearance/title-link?hl=zh-cn)。

## 本地验收

- [根路径检查](identity-seo-check-root.json)和[生产子路径检查](identity-seo-check-production.json)：各18个HTML、16条双语路由、1,122处内部引用，0错误；验证标记、canonical、hreflang与元数据检查通过。
- [浏览器检查](identity-seo-ui.json)：中英文首页/导师页/申请页，1440、390、320像素共18个组合，0横向溢出、0标题越界、0损坏图片；每个页面1个H1、语言对应正确，申请页各3项问答。
- 实际点击中文申请页的英文切换，仍停留对应`/en/join/`。

首次Windows管道传递含中文的维护脚本时出现编码错误，随后改用本地UTF-8脚本执行；之后两种路径构建均成功。批量浏览器命令改用文件接收输出，避免后台进程继承管道导致等待；18组合检查最终通过。这两项仅涉及本地验收辅助脚本，没有引入运行依赖。
