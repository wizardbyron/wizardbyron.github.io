---
title: "博客主题升级到 Congo 2.0"
date: 2022-03-18T15:50:35+08:00
---

近期，发现我的博客一直使用的博客主题 [Congo](https://jpanther.github.io/congo/docs/w) 升级到了 2.0 版本。新版本增加了一些新特性，并且和最新的 Hugo 保持一致。具体的升级参考可以参考官方升级说明 <https://jpanther.github.io/congo/docs/version-2/upgrade/#paramstoml>，这里我仅仅将自己的升级过程做一个简单的记录。

由于我之前是下载主题并直接安装到 hugo 的 themes 目录里。这样做不利于主题的同步更新，同时代码库也较大。因此，这次升级我采用 submodule 的方式。

## 删除旧 1.0 主题

首先，删除旧的 1.0 主题，创建一个提交：

```sh
git rm -rf themes/congo
git commit -m "Remove congo 1.0"
```

### 通过 Submodule 安装新主题

然后，通过 Submodule 下载新的 congo 2.0, 创建一个提交：

```sh
git submodule add --force -b stable https://github.com/jpanther/congo.git themes/congo
git commit -m "Install congo 2.0"
```

这时候，通过 `git status` 你会发现多了两个文件：`.gitmodules`和`themes/congo`

`.gitmodules`里是配置 submodule 的信息

`themes/congo`则是以 submodule 方式存在的目录文件。它提交后会在 Github 上引导你进入到 congo 代码库主页。

### 调整配置文件

安装完 Congo 2.0 后运行`hugo server` 会出现一堆错误，这时候要调整配置了。

首先，创建 `config/_default` 文件夹，并创建以下文件：

- `config.toml`: 站点主配置文件，里面的`defaultContentLanguage`要设置为`zh`，他会检索`languages.<语言>.toml`和`menu.<语言>.toml`两个配置。
- `languages.zh.toml`: 语言配置文件，这里我配置的中文（zh）。
- `menu.zh.toml`: 主页菜单文件，和语言一样，文件需要有中文（zh）的说明。
- `params.toml`: 主题功能参数配置文件。包括主题颜色的切换和一些功能的配置。

具体文件配置内容可以参照<https://jpanther.github.io/congo/docs/configuration/#configuration> 的说明。

### 调整静态资源目录

由于 Congo 2.0 遵循最新版本的 Hugo 采用了 Pipeline 优化资源。因此之前放在 `static` 目录下的 作者头像和网站 Logo 要水平迁移至 `assets` 目录下。只需要新建 `assets` 目录，将 `static` 下的图片复制过来即可。

## 启用新特性

Congo 2.0 新增了几个我喜欢的新特性，比如：

- 站内搜索功能: 需要在`params.toml`文件里新增 `enableSearch = true`选项。
- 代码复制按钮: 需要在`params.toml`文件里新增 `enableCodeCopy = true`选项。（当前还有 bug，我提了一个 [issue](https://github.com/jpanther/congo/issues/154)）。
- 回到文章开头按钮: 需要在`params.toml`文件里新增`showScrollToTop = true`选项。
- 文章目录功能: 需要在`params.toml`文件里的`[article]`选贤管辖新增 `showTableOfContents = true`选项。同时需要在 `config/_default` 文件夹下增加 `markup.toml` 配置来说明目录格式。例如:

```toml
# config/_default/markup.toml

[tableOfContents]
  startLevel = 2
  endLevel = 4
```

其中的 Level 是 Markdown 标题标记的需要。它会根据标题级别自动在文章右边新增目录。

具体文件配置内容可以参照<https://jpanther.github.io/congo/docs/configuration/#configuration> 的说明。

（完）
