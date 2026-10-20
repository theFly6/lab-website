# 临时演示访问码遮罩

当前启用轻量前端遮罩，便于向受邀者演示尚在整理的网站。中英文内容页与404页打开后先要求输入访问码；根入口仍跳转中文首页。正确输入后，在当前标签页的会话中记忆，刷新、站内跳转和语言切换无需重复输入。新会话需重新验证；浏览器恢复标签页时可能同时恢复该会话。

这是展示限制，**不是保密或服务端身份认证**。正文、图片、资源和校验摘要均可公开下载；本项目源码仓库也是公开的。关闭样式、修改前端脚本或查看源码可以绕过，搜索摘要也可能展示正文。请勿据此放入未公开、敏感或未经授权的材料。

## 关闭遮罩，恢复公开浏览

编辑项目根目录的 `_config.yaml`：

```yaml
preview_gate:
  enabled: false
  # 原有 code_sha256 一行保持不变
```

只修改 `enabled`，保留实际的 `code_sha256` 字段值。重新构建后，页面不再输出遮罩HTML、锁定属性、遮罩脚本或样式引用。重新设为 `true` 可恢复。

- 本地：停止本项目原有Jekyll进程，再运行 `.\start.ps1`。Jekyll不会自动重新加载配置文件。
- 线上：提交并推送到 `main`，进入GitHub仓库 **Actions → 手动发布已审核网站到 GitHub Pages → Run workflow**，选择 `main`。仅推送源码不会触发当前手动发布工作流。
- 更新后如仍显示旧页面，强制刷新或等待浏览器/CDN缓存更新。

不需要重新验证Google Search Console或重新设置Sitemap。

## 更换访问码

页面只输出SHA-256摘要，避免将明文直接嵌入HTML；这不会使前端方案具备真正的认证安全性。在项目目录运行下面的命令，按提示输入新码，再将输出摘要填入 `preview_gate.code_sha256`：

```powershell
python -c "import getpass,hashlib; print(hashlib.sha256(getpass.getpass('New access code: ').encode('utf-8')).hexdigest())"
```

访问码区分大小写，输入前后空白会被忽略，不要给新码设置首尾空白。修改后同样需要重新构建与发布。旧摘要对应的会话会失效；页面已打开且未刷新的访客仍可能继续查看。会话只存储摘要，不保存输入的明文，不向服务器发送访问码。

## 文件与兼容性

- `_includes/preview-gate-head.html`：首屏遮挡与条件资源加载。
- `_includes/preview-gate.html`：共享双语输入界面。
- `assets/preview-gate.js`：前端校验、会话记忆、模态交互。
- `assets/preview-gate.css`：独立响应式样式。
- `_data/locales/{zh,en}.json`：独立维护中英文文案。
- `_layouts/default.html` 与 `404.html`：接入共享组件。

使用浏览器原生 `dialog`、Web Crypto与 `sessionStorage`，无新增依赖。支持现代浏览器的 **HTTPS** 与 **localhost / 127.0.0.1**；通过局域网IP访问明文HTTP时，Web Crypto可能不可用，需改用HTTPS或本机预览。禁用JavaScript时显示说明并阻止正常预览；如脚本加载失败，保留输入卡片和禁用的提交按钮。浏览器限制会话存储时，可放行当前页，但下一页可能需重新输入。

所有访问者使用同一份HTML与校验逻辑，未按搜索引擎User-Agent放行。正文与资源照常加载，title、description、canonical、hreflang、Google验证标记和17个Sitemap网址保留。遮罩文案使用 `data-nosnippet`，以减少它进入Google摘要的机会。

**保留SEO基础配置不等于排名不受影响。** 搜索引擎会渲染页面，全屏遮罩可能影响页面理解、抓取后的评估与搜索表现；无法保证现有收录、摘要和排名维持不变。若搜索流量优先，建议尽早关闭遮罩，让正式内容可直接浏览。参考Google的[全屏插页说明](https://developers.google.com/search/docs/appearance/avoid-intrusive-interstitials)与[摘要控制说明](https://developers.google.com/search/docs/appearance/snippet?hl=zh-cn)。

本轮实际构建、浏览器与发布结果见 [TESTING.md](TESTING.md) 和项目根目录的 `FINAL_REPORT.md`。此前所有来源记录、开发笔记与TODO保留。
