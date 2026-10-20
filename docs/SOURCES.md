# 信息来源与采用边界

2026-10-20导师页优化：依据用户提供并与学校教师主页对应的完整简介，补充教学奖励、人才培养及课程认定。原始届次、等级、括号信息和未采用的评教统计口径见 [TEACHING_CONTENT.md](TEACHING_CONTENT.md)；不将历史论文总数展示为实时统计。

2026-10-20补充：用户提供的HPCDE新旧站与学校资料交叉核查结果见 [HPCDE_RESEARCH.md](HPCDE_RESEARCH.md)。本轮新增公开任职记录、学术服务、课程、书名及相关科研平台介绍；没有据多导师团队目录导入个人课题组学生或毕业生。HPCDE导师邮箱与学院来源存在拼写差异，已记录并保留学院来源。

核查日期：2026-10-19。网页可访问并不代表其中每个职务或历史字段均已更新到当天；本项目优先采用稳定事实，并保留时效说明。

## 身份确认

本网站的对象为北京科技大学计算机与通信工程学院的**李建江（Jianjiang Li）教授、博士生导师**。学校教师主页与学院英文教师页的单位、研究方向、2005 年清华博士经历相互吻合；代表性论文还通过 USTB 作者单位和教师主页论文记录交叉确认。没有采用清华大学其他同名学者、建设银行人员或仅凭姓名检索到的成果。

## 教师、机构与联系方式

| 来源 | URL | 采用内容与限制 |
| --- | --- | --- |
| 学校教师主页 | https://faculty.ustb.edu.cn/JianjiangLi/zh_CN/index.htm | 教授、博士生导师、2005 年清华博士、同年进入北科大、主要研究方向。未将累积论文数当成当前统计。 |
| 学院英文教师页 | https://enscce.ustb.edu.cn/Teach/TeacherList/2020-06-03/43.html | `lijianjiang@ustb.edu.cn`，办公室 MEE Building 826，历史项目编号。页面路径含 2020，办公室明确标为待复核。 |
| 工程研究中心团队简介，2021-07-20 | https://ercis.ustb.edu.cn/?p=1390 | 确认李老师列于该中心团队，曾为天普大学访问学者。中心人数、其他教师和累计成果不归到个人课题组。 |
| 学校教师平台学科目录 | https://faculty.ustb.edu.cn/xkjs.jsp?id=5673&lang=zh_CN&st=0&urltype=tsites.DisciplineTeacherList&wbtreeid=1005 | 学校地址为北京市海淀区学院路30号、邮编100083。 |
| 导师学生栏目 | https://faculty.ustb.edu.cn/JianjiangLi/zh_CN/xsxx/72144/list/index.htm | 本次核查为0条，不能证明没有学生。未从共同作者名单推断当前学生身份。 |

学校教师平台邮箱、办公地址在 HTML 抽取中呈加密字符串，本项目没有猜测或解码这些字段；邮箱采用学院官方英文页的明文记录。

## 论文与书目信息

`_data/publications.json` 是实际展示数据。作者顺序、卷期、页码、DOI 由 Crossref API 核查，并与教师主页或出版社的作者单位及内容对照。原始筛选字段保存在 [`crossref-verified.json`](crossref-verified.json)。英文题目采用 Crossref 元数据，未自造中文题名。

| 论文 | 年份 | 出版社来源与 DOI |
| --- | --- | --- |
| Memory access optimization of molecular dynamics simulation software Crystal-MD on Sunway Taihulight | 2021 | https://www.sciopen.com/article/10.26599/TST.2019.9010074?issn=1007-0214 · `10.26599/TST.2019.9010074` |
| Parallel optimization of the Crystal-KMC on Tianhe-2 | 2021 | https://www.sciopen.com/article/10.26599/TST.2019.9010075?issn=1007-0214 · `10.26599/TST.2019.9010075` |
| Crystal-KMC: Parallel Software for Lattice Dynamics Monte Carlo Simulation of Metal Materials | 2018 | https://www.sciopen.com/article/10.26599/TST.2018.9010107 · `10.26599/TST.2018.9010107` |
| Kernel optimization for short-range molecular dynamics | 2017 | https://www.sciencedirect.com/science/article/abs/pii/S0010465516301928 · `10.1016/j.cpc.2016.07.010` |
| A data-check based distributed storage model for storing hot temporary data | 2017 | https://www.sciencedirect.com/science/article/abs/pii/S0167739X1630557X · `10.1016/j.future.2017.03.019` |
| Research and implementation of a distributed transaction processing middleware | 2017 | https://www.sciencedirect.com/science/article/abs/pii/S0167739X1630005X · `10.1016/j.future.2016.01.021` |
| Frequency and Similarity-Aware Partitioning for Cloud Storage Based on Space-Time Utility Maximization Model | 2015 | https://www.sciopen.com/article/10.1109/TST.2015.7128935 · `10.1109/TST.2015.7128935` |

2021 年两篇论文的 SciOpen 页面注明在线发布于 **2020-10-12**，但卷期引用为 **2021, 26(3)**，本网站使用卷期年；不把 DOI 中的 2019 当成发表年。2017 年论文中“副教授”的作者简介属于当时背景，当前职称取学校教师主页的教授。天普访问时间 2014.01–2015.01 来自 POST 论文的作者简介，不从当前职务倒推。

教师主页论文索引：https://faculty.ustb.edu.cn/JianjiangLi/zh_CN/lwcg/72134/list/index.htm 。Crystal-MD 另有官方条目：https://faculty.ustb.edu.cn/JianjiangLi/en/lwcg/72150/content/14431.htm 。

部分 SciOpen 无查询参数的地址在阅读工具中报错，带 `?issn=1007-0214` 的官方页面和 Crossref 返回了可核实数据。文章可读性可能随站点访问策略变化，不影响本地页面呈现。

## 项目

主来源：https://faculty.ustb.edu.cn/JianjiangLi/zh_CN/kyxm/72137/list/index.htm 。项目编号补充来源为上表学院英文教师页。

| 公开项目 | 执行期 | 李老师角色 | 编号 |
| --- | --- | --- | --- |
| 面向E级系统的大气动力学全隐式模拟局部求解器移植与优化 | 2021–2023 | 课题负责人 | 未公开，不填 |
| 面向E级系统的并行编译优化研究 | 2017–2021 | 子课题负责人 | 2017YFB0202003 |
| 粒子类问题的可扩展并行算法研究 | 2017–2020 | 子课题负责人 | 2017YFB0202104 |
| 核反应堆关键材料性能优化高性能数值模拟软件研发 | 2015–2017 | 课题负责人 | 2015AA01A303 |
| 多范例并行构件及其关键技术研究 | 2008–2010 | 项目负责人 | 108008 |
| 高生产率并行模型与编译验证 | 2006–2008 | 项目负责人 | 2006AA01Z105 |

第一项的单项记录：https://faculty.ustb.edu.cn/JianjiangLi/zh_CN/kyxm/72137/content/6028.htm 。

项目页明确为历史公开记录，不声称项目仍在研或已验收。`Kernel optimization` 的出版社页致谢明确列有 `2015AA01A303`，因此仅这一项目附相关论文链接；未为其他项目猜配论文。

## 新闻与招生

| 来源 | 日期/状态 | 使用边界 |
| --- | --- | --- |
| https://scce.ustb.edu.cn/info/1087/3644.htm | 2025-09-26 | 中海油服科技服务团获“优秀团队”，指导教师李建江、队长李亿行，涉及RAG服务、日志传输和可视化。只摘要相应团队段落，不将同文另一团队的成果归到李老师。 |
| https://news.ustb.edu.cn/info/1095/71406.htm | 2025-10-03 | 学校新闻网对同一事件的交叉验证，不重复当作另一条新闻。 |
| https://faculty.ustb.edu.cn/JianjiangLi/zh_CN/zsxx/72143/list/index.htm | 核查时0条 | 没有据此宣称当年招生名额、资格、承诺或资助。 |
| https://yzxc.ustb.edu.cn/ | 官方入口 | 用作年度政策查询入口，不把过去年份的校企专项名额沿用到当前。 |

未采用仅凭论文作者、往年招生名单或新闻中的实践身份推断出来的在读成员名单；李亿行只在对应新闻中以当时的队长身份出现。

## 图片与设计素材

- 导师照片下载自学院教师介绍的图片链接：https://enscce.ustb.edu.cn/d/file/p/2020/06-03/726f265c6f0e0e1daa80edc0f7a56013.jpg 。用于本地预览，正式上线前请导师确认照片版本与使用授权。
- `assets/compute-fabric.svg` 与 `assets/mark.svg` 为本项目代码绘制的抽象矢量图；不是实验室设备实拍、学校校徽或已经批准的课题组标识。
- 没有复制参考网站中的照片、论文或团队资料。模板原有未使用图片保留在 `images/` 中，来源与许可沿用原模板；当前公开页面不引用它们。
