---
title: "初始化 MacOS"
date: 2026-04-08
tags:
- Agentic@Work
---
这是一份初始化 Mac 的指南，可以通过 `AI 编程工具`（Claude Code, OpenCode, Cursor等）初始化 `macOS`。

需要先安装 AI 编程工具，然后复制以下内容到你的 AI 编程工具：

```text
请按照 https://www.gugu.me/skills/setup_macos 的说明设置 macOS
```

## 1. 加速 Github 网页的加载速度

从 `https://hosts.gitcdn.top/hosts.txt` 获取最新的 `GitHub hosts`，并将其追加到 `/etc/hosts` 文件末尾。然后刷新 `DNS` 缓存：

```bash
sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder
```

## 2. 安装 oh-my-zsh

从 <https://ohmyz.sh> 安装 `oh-my-zsh`。

## 3. 安装 Homebrew

从 <https://brew.sh/zh-cn/> 安装 `homebrew`。安装成功后安装以下软件包。

- uv
- fnm
- go
- hugo
- podman
- docker-compose
- visual-studio-code

安装完成后，为 `podman`, `fnm`, `uv` 设置中国大陆的加速访问源。

## 4. 个性化 git 设置

向用户提问 `github` 的用户名和 `github` 的 `noreply邮箱地址`，用来创建访问 `github` 的 `ssh-key`。同时初始化 `git` 的 `user.name` 和 `user.email` 配置。

然后为创建以下 git 命令的别名。

```sh
alias.co=checkout
alias.br=branch
alias.ci=commit
alias.st=status
alias.pr=pull --rebase
alias.ap=add -p
```

## 5. 优化 AI 编程工具

如果安装下列 AI 开发工具，则增加这些配置

### 1. OpenCode

1. https://github.com/Opencode-DCP/opencode-dynamic-context-pruning
