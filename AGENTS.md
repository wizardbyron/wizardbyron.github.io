# wizardbyron.github.io 项目指南

## 项目概述

这是一个基于 **Hugo** 构建的静态博客网站，使用 **Congo 主题**。内容主要为简体中文 (zh-Hans)。

## 常用命令

```bash
# 启动开发服务器
hugo server -D

# 构建（生产环境）
hugo --minify

# 创建新内容
hugo new content blog/YYYY-MM-DD-post-title/index.md
```

## 博客文章规范

新的博客文章**必须**遵循以下目录结构：

```
content/blog/YYYY-MM-DD-slug-name/index.md
```

示例：
- `content/blog/2026-04-07-meet-again/index.md`
- `content/blog/2026-02-20-trade-review-sz002163/index.md`

每篇文章是一个目录，包含 `index.md` 文件和相关资源（图片等）放在同一目录下。

### 前置元数据模板

新创建的文章默认为草稿状态（draft: true），需要发布时手动将 draft 改为 false 或删除该行。

```yaml
---
title: "文章标题"
date: YYYY-MM-DD
draft: true
tags:
- 标签1
- 标签2
---
```

## 关键目录

- `content/blog/` - 博客文章（主要内容）
- `content/skills/` - 技能/知识库文章
- `content/about.md` - 关于页面
- `config/_default/` - Hugo 配置
- `layouts/` - 自定义 HTML 模板（如有）
- `assets/` - CSS、JS、图片等主题自定义资源
- `static/` - 静态文件（favicon 等）

## Hugo 配置

- **基础 URL**: https://www.guyu.me/
- **语言**: zh-Hans（简体中文）
- **主题**: Congo v2.13.0（通过 Go 模块）
- **分页**: 每页 10 篇文章

## 部署

- 推送到 `main` 分支时自动部署到 GitHub Pages
- 工作流文件：`.github/workflows/gh-pages.yml`
- 生产构建使用 `hugo --minify`
- 输出目录：`public/`（已被 gitignore）

## 文章图片添加

将图片放在文章目录下，使用相对路径引用：

```markdown
![替代文字](image-name.png)
```

## 常用标签

基于现有内容：
- `其他`
- `交易复盘`
- `Agentic@Life`
- `Agentic@Work`

## 重要注意事项

1. **始终**将博客文章创建为带日期的目录内的 `index.md`
2. 除非主题需要英文，否则内容使用中文
3. Congo 主题支持深色模式和移动端响应式设计
4. 创建新内容时参考 `archetypes/default.md` 中的默认模板
5. 这是个人博客 - 保持专业但有个性的语调
6. **禁止自动推送到远程** - 所有 git 操作仅限本地，push 需用户明确授权