---
title: "通过 Github Actions 部署 Mkdocs 文档"
date: 2021-12-17
tags:
- 其它
---

Mkdocs 是一个采用 Python 构建轻量级的静态 HTML 在线文档框架，内置部署到 Github Pages 的功能。我用来创建[实践指南](/guides/)，用来做个人的知识积累。

## 安装 Mkdocs 以及 Mkdocs 主题

Mkdocs 以及主题都通过`pip`安装，例如我采用的[mkdocs-material](https://squidfunk.github.io/mkdocs-material/)主题，如下所示：

```shell
pip install --user mkdocs mkdocs-material
```

值得一说的是，如果你安装主题，mkdocs 会作为依赖被安装。

更多的主题请参考 Wiki 页：<https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes>

## 创建并测试站点

通过`mkdocs new <目录>`就可以快速创建文档站点。目录里会生成`mkdocs.yml`文件和`docs`目录，目录内有默认的`index.md`文件，你可以修改和增加文件。

在所在目录执行`mkserve`，你就可以在<http://localhost:8000>看到初始化的文档。Mkdocs 会监测目录的改动并重新生成站点更新浏览器。

但如果你修改了配置，比如主题。就有可能出错中断进程。

这时站点还没有加载主题，你要修改`mkdocs.yml`，增加`theme`配置：

```yaml
theme: 
  name: material
  language: zh
  highlightjs: true
```

不同的主题有不同的参数配置，详情可以参考对应主题的文档。

## HTML 生成和部署

执行`mkdocs build`会新建`site`目录，并将 markdown 文件构建为 html 文件。


执行`mkdocs gh-deploy`就可以`site`中的 html 内容提交到代码仓库的`gh-pages`分支上，你要在 Github 上 代码库的配置中起用 Pages 才可以看见站点，地址是 `https://<你的用户名>.github.io/<你的代码仓库>` 。

## 通过 Github Actions 部署到 Github Pages

我们可以用 Github Actions 把上述的构建和发布工作自动化，只需要在代码库上新建`.github/workflow/gh-deploy.yml`文件，内容如下：

```yaml
name: Deploy to Github Pages
  on:
    push:
      branches:
        - master
        - main
  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v2
        - uses: actions/setup-python@v2
          with:
            python-version: 3.x
        - uses: actions/cache@v2
          with:
            key: ${{ github.ref }}
            path: .cache
        - run: pip install mkdocs-material
        - run: mkdocs gh-deploy --force
```

提交后，你就可以看到自己的站点自动部署到 Github Pages。未来的提交也会出发这个流程。
