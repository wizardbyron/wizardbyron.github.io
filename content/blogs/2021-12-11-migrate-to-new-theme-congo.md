---
title: 博客迁移到了新的 Hugo 主题
date: 2021-12-11
categories: 
  - 其它
tags:
  - Hugo
  - Github Pages
  - Github Actions
---

你现在看到的主题就是我的博客最新的主题 [Congo](https://jpanther.github.io/congo/)，这些天一直没更新博客的主要原因是一直在寻找一个简洁明快的博客主题，最后就它了！（不过说不定未来还会换）

于是我就花了半天时间把原来 Github Pages 上的博客迁移到了这个主题上，并采用了 Github Action 发布我的博客，以下是迁移步骤：

1. 备份内容，并做一个全量删除提交
2. 采用 Hugo 新建一个新的博客
3. 安装 Congo 主题
4. 采用 Github Actions 部署博客
5. 覆盖配置，而不要修改
6. 迁移旧的文章和图片

## 1. 备份内容，并做一个全量删除提交

一个博客的核心内容是图片和文章。这些内容在`static`目录和`content`目录下，把这些内容保存出来就好。

然后，通过 `git rm -rf  --ignore-unmatch *`删除所有内容，并删除空的目录。

这时候创建一个删除提交，你就有之前删除内容的全量备份了。如果想恢复，只需要 `git revert`即可。

## 2. 采用 Hugo 新建一个新的博客

这时候你的目录是空的，你就可以执行`hugo new site .`重新建立一个站点了，这条命令默认会生成一个没有主题的空结构。

这个时候，你要提交一次，用于跟踪后续的主题和配置的修改。

## 3. 安装 Congo 主题

参考 <https://jpanther.github.io/congo/docs/installation/> 的安装文档，里面有三种安装方式，分别是：

1. 采用 Hugo （推荐）
2. 采用 Git Submodule
3. 下载静态文件

我采用了第三种方式下载了静态文件解压的方式来安装主题，简单粗暴，避免我想要更新时忘记一些配置，这样可以减少很多 git 或 hugo 的配置工作。

别忘了删除`theme`下面的`exampleSite`，节省一些空间。

这时候通过`hugo server`预览一下站点，看看主题是否正确加载，然后做一个提交。

## 4. 采用 Github Actions 部署博客

站点恢复的第一步是进行一次 push，并且发布站点。这时候我建议采用 Github Action 来自动化部署。

* 首先，参考[Hugos 官方的 Github Pages 部署方式](https://gohugo.io/hosting-and-deployment/hosting-on-github/)在代码库根目录创建`.github/workflows/gh-pages.yml`文件，内容如下：

``` yaml
name: github pages

on:
  push:
    branches:
      - main  # Set a branch to deploy
  pull_request:

jobs:
  deploy:
    runs-on: ubuntu-20.04
    steps:
      - uses: actions/checkout@v2
        with:
          submodules: true  # Fetch Hugo themes (true OR recursive)
          fetch-depth: 0    # Fetch all history for .GitInfo and .Lastmod

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
          # extended: true

      - name: Build
        run: hugo --minify

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        if: github.ref == 'refs/heads/main'
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

提交后你就可以看到 Github Actions 里多了一个 Workflow，如下图所示：

![Github Actions 执行部署任务](/img/post/20211211/gh-actions.png)

## 5. 修改 Github Pages 配置

* github pages 默认推荐采用`gh-pages`分支来存放静态站点的内容。`gh-pages.yml`里的配置已经会帮你把生成的文件提交到`gh-pages`分支上。所以，要在代码库的 `Settings` 里的 `Pages` 里设置采用 `gh-pages` 分支发布你的站点。如下图所示：

![Github Pages 配置界面](/img/post/20211211/gh-pages-settings.png)

* 这时候，如果你需要用自己的域名增加 CNAME 记录，你就要额外在 `static`目录下创建`CNAME`文件，里面只需要写入你的域名。并且在上图的配置中填入你的 CNAME。

## 6. 覆盖配置，而不要修改

congo 的配置都放在主题目录下的`config/_default`目录下，包含几个 toml 文件。每个 toml 文件都是根目录下的 `config.toml` 文件里的一个配置项及其子项。

根据最新版本 Hugo 的[配置合并规则](https://gohugo.io/getting-started/configuration/#merge-configuration-from-themes)，你可以选择把主题内的配置合并到最终的配置中。Hugo 会先加载根目录的`config.toml`文件，然后会进入主题加载主题内的配置文件，最后合并成一个配置。

接下来我们要覆盖一些配置，我们把需要覆盖的配置全部复制到根目录的`config.toml`文件内。你可以参考[我的配置文件](https://github.com/wizardbyron/wizardbyron.github.io/blob/main/config.toml)。

这里分享有几个配置中的坑：

### 采用 Profile 的布局需要新建 _index.md 文件

Congo 有三个布局：page、profile和custom（自定义）三种

我的主页就是 profile 模式，会显示作者的基本信息和头像。

如果要开启首页，需要在`content`文件夹下增加 `_index.md`文件。

### 开启 i18n 的中文名称

Hugo 没有简体中文（zh-cn）和繁体中文（zh-tw）的配置，统一只有 zh 配置。在主题的`i18`里有各种配置的中文配置。同时别忘了打开 Hugo 自身的`hasCJKLanguage = true`。否则，阅读时间和字数统计会不准确。

```toml
languageCode = 'zh'
defaultContentLanguage = 'zh'
hasCJKLanguage = true
```

### 在线编辑

这个是我很喜欢的一个功能，这样就可以点击博客标题下方的图标进入编辑模式，如下图所示：

![编辑图标](/img/post/20211211/edit-icon.png)

点击这个图标默认会跳转到这篇文档的原始 markdown，这样当你在 Web 上提交之后，Github Actions 会自动帮你部署。不需要一定要有笔记本电脑在手边。

配置项如下：

``` toml
[params.article]
  showEdit = true
  editURL = "https://github.com/wizardbyron/wizardbyron.github.io/tree/main/content"
```

注意，编辑的 URL 是 Github 上的content 目录，不要仅仅写 github 仓库地址，这个主题不会帮你补全。

## 7. 迁移旧的文章和图片

最后，将之前的博客文章和照片迁移到最新的目录下，在本地验证后再批量提交。Github Actions 会帮你部署新的站点。

这样，我的博客就迁移完了。

## 最后

静态站点工具很多，不同的语言都有自己的静态站点生成工具。所谓"写博客半天，找主题两天"，最近找到了更轻量级的静态内容工具 mkdocs，未来我会分享这个更轻量级的工具。
