# 因果推断学习笔记

[打开学习网站](https://fxt-gw-pb.github.io/CausalInferenceLearning/)

一套中文因果推断自学网站。从研究问题、潜在结果与 DAG 开始，逐步进入标准化、倾向得分、机器学习、双重稳健估计、TMLE 和拓展应用。

## 内容与功能

- 九周、39 节独立撰写的学习正文，82 道带解释的自测题。
- 原创合成例子、方法推导、可复制代码及公开学术引用。
- 交互标准化实验：改变目标人群构成，观察粗比较与标准化风险的差别。
- 搜索、章节导航、收藏、阅读进度和答案保存；记录仅保存在当前浏览器。
- 响应式页面、键盘可用的原生对话框及原生 MathML；无登录、后台、追踪器或外部 CDN。

代码块分别显示执行状态。18 个 Python 示例已独立执行检查；65 个 R 示例经过静态检查，尚未实际运行，不提供虚构的软件输出。内容校核不保证适用于具体研究，使用时仍应检查识别假设、数据质量和软件环境。

## 本地运行

需要 Python 3 和 Node.js 18+。网站不依赖 npm 包。安装 `jsonschema` 可启用完整 JSON Schema 校验；CI 会安装它。

```sh
npm test
npm run build
npm run dev
```

打开 `http://localhost:4173/`。开发命令先执行一次构建，再提供静态文件；修改内容后需重新构建。路由使用 URL fragment，资源路径均为相对路径，适用于 GitHub Pages 项目子路径。

## 项目结构

- `content/catalog.json`：学习目录
- `content/lessons/`：逐课 JSON 正文
- `content/schema/`：内容结构约束
- `src/`：静态界面、公式、状态和交互逻辑
- `scripts/` 与 `tests/`：构建和测试支持
- `docs/CONTENT_AUTHORING.md`：内容编辑约定
- `docs/QA.md`：验证范围与复查清单

## GitHub Pages

`.github/workflows/pages.yml` 在 `main` 更新后测试、构建并部署。仓库的 Pages source 应设为 GitHub Actions。工作流只上传 `dist/`，不会发布整个源码目录。`dist/` 由显式文件白名单生成，不纳入版本控制。

本站只包含独立组织的文字、代码、图形和合成例子。参考链接指向公开学术资料，不附带原始课件、录音、视频、转录、截图或个体研究数据。
