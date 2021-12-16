---
title: 测试驱动开发 Nginx 配置
date: 2018-06-12
categories: 
  - DevOps
tags:
  - 停机时间
  - Python
  - 流量测试
---

2017年中，我参与了一个亚太地区互联网公司并购的项目，客户收购了亚太地区 7 个国家的同行业互联网企业和产品。我作为其中的 DevOps 咨询师和 DevOps 工程师，和客户一起完成并购后的产品迁移和技术能力提升的设计、实施和培训。

客户希望采用新的统一产品，并根据不同地区的业务特色进行一些定制，与此同时，需要进行数据迁移以保证业务可以继续运行。其中一个很关键的步骤是把原系统的 URL 通过重定向的方式到新的产品中，因为有很多的第三方链接和搜索引擎依然保留了原系统中的链接。

初步统计了一下，将近有3000多个 URL 需要重定向，光是规则和正则表达式就写了 400 多条（没有统一模式的 URL 害死人啊），这就引发了一个问题：我该如何验证这些规则和覆盖这些 URL ？此外，大量的重定向不光对用户来讲不是很好的体验，如果我要优化这些规则，我如何保证我当前的转发规则不被破坏？

## 解决方案

最早，我们写了一个 Shell 脚本，用 `curl`命令来验证这些 URL，最初只需要验证 200 条就可以满足需求，时间也不到两分钟。后来，我们采用了一个 Excel 文件来跟踪这些 URL，产品经理只需要把新的重定向 URL 补充到上面，我们就依据这些 URL 来开发 nginx 的重定向规则。

这让我想到了 TDD：先写出一个自动化测试用例，然后修复这个自动化测试用例。更好的是，有了自动化的测试做保护，你可以放心和安全的对代码进行重构。

此外，随着更多的 URL 需要重定向，这个数字在不断的增加。原先的  Shell 脚本执行的时间也从最初的 2 分钟增长到了15分钟。

现有的工具满足不了要求，一怒之下，我决定开发一个自己的工具。它必须具备以下特点：

1. 可以通过文件读取规则，进行大批量验证。
2. 多线程并发执行，可以提升效率。
3. 很容易和 CI 集成。
4. 能帮我做一定程度的重定向优化分析。

于是，我在一个周末的时间用 Python 写下了 `vivian`：  一个多线程的批量自动化重定向验证工具。

它把原先的 15 分钟的验证时间缩短到了 17 秒，效率提升了 5294 % !!

此外，我把测试用例集成到了代码库里。并把 vivian 提交到了 pipy，这样我就可以通过 pip 在初始化 CI 上安装了。也无需增加到代码库里变成一个需要维护的代码脚本。

选择 Python 的原因主要是因为相较于 Ruby, Go, Java, NodeJS 来说。Python 的语言环境比较稳定，几乎每种 Linux 都包含 Python 的运行环境，且容易安装和集成。

## 安装使用 Vivian

安装

```bash
pip install vivian
```

使用

```bash
vivian -f example.csv
```

test.csv 非常简单，第一列是源 URL，第二列是目标 URL。例如：

```csv
http://www.github.com, https://github.com/
http://www.facebook.com, https://facebook.com/
```

采用 csv 文件的目的主要是方便使用 Excel 和文本工具编辑。

之后会得出下列结果：

```bash
vivian -f example.csv
load test case from example.csv
2 cases loaded running in 2 threads
verifying http://www.github.com to https://github.com/
verifying http://www.facebook.com to https://facebook.com/
Failed cases:
============================================================
  line: 2
origin: http://www.facebook.com
  dist: https://www.facebook.com/
expect: https://facebook.com/
status: 200
redirect_count:1
------------------------------------------------------------
1/2 PASS in 5.8494720458984375 seconds
```

第一行输出提示测试用例文件位置。

第二行输出提示测试用例数量和线程数量。你也可以通过增加 -n 来指定线程的数量，默认线程数量等于 CSV 文件记录行数。

第三行到第四行列出了需要验证的 URL。

第五行开始就是失败的测试用例信息：

失败用例的第一行就是测试用例所在的文件行号。

失败用例的第二行是测试用例测试的源 URL。

失败用例的第三行是访问测试的 URL 的实际目标 URL。

失败用例的第四行是期望得到的 URL。

失败用例的第五行是访问测试用例源 URL 最后得到的 HTTP 状态。

失败用例的第六行是访问测试用例源 URL 到最后结果之间的 重定向次数，有了这个数字我们可以优化 URL。

最后一行表明有多少个用例通过了测试，同时统计了完成这些测试的总时间。

## 最佳实践

以下是我总结的使用 vivian 的最佳实践场景，希望能对你的 web 服务器维护工作起到帮助。

### 采用 Excel 生成测试用例

Excel，包括 Google Sheet。都是很方便的进行团队交流用的数据文件。对于很多开发和运维工程师来说，如果手动编写测试用例肯定是很费工夫的事情。所以，你只需要创建一个两列的 Excel 文件，分别存储源 URL 和目标 URL。之后你就可以采用 Excel 便捷的复制功能和计算功能生成很多的测试用例。

不过，需要注意的是，你需要将 Excel 文件保存为 CSV 格式，才可以识别哦。

### 采用 TDD 开发 nginx 规则

当有了一个自动化的测试工具，我们就可以构建测试驱动开发实践。下面我举个例子演示一下：

首先，我希望我的 nginx 配置可以帮我把所有请求通过 301 永久重定向转发到我的博客 <http://wizardbyron.github.io> 上去。

首先，我需要创建一个虚拟域名，例如：local.testhost.com

为了方便起见，我修改了我本地的 hosts 文件。加入如下一行：

```csv
local.testhost.com 127.0.0.1
```

因此，我需要写一个测试用例文件 *redirect_case.csv* ：

```csv
http://local.testhost.com, https://wizardbyron.github.io
```

当然，你也可以采用你的测试环境。

接下来，我可以采用 vivian 来进行测试：

``` bash
vivian -f redirect_case.csv
load test case from redirect_case.csv
1 cases loaded running in 1 processs
verifying http://local.testhost.com to https://wizardbyron.github.io
Failed cases:
============================================================
  line: 1
origin: http://local.testhost.com
  dist:
expect: https://wizardbyron.github.io
status:
redirect_count:0
------------------------------------------------------------
============================================================
```

我们发现，测试失败，因为我们并没有启动任何一个 http 服务器。接下来，我们可以通过 docker 来启动一个 nginx 服务器：

```bash
docker run --name nginx -d -p 80:80 nginx
```

记得要把 80 端口映射出来。接下来我们再次进行测试：

``` bash
vivian -f redirect_case.csv
load test case from redirect_case.csv
1 cases loaded running in 1 processs
verifying http://local.testhost.com to https://wizardbyron.github.io
Failed cases:
============================================================
  line: 1
origin: http://local.testhost.com
  dist: http://local.testhost.com
expect: https://wizardbyron.github.io
status: 200
redirect_count:0
------------------------------------------------------------
============================================================
```

通过这次测试，我们发现虽然有了 nginx 服务器，但是我们的结果不正确。这时候，我们可以把 nginx 的配置文件从 nginx 容器里面复制出来：

``` bash
docker cp nginx:/etc/nginx/nginx.conf .
```

然后修改配置文件为如下所示：

``` nginx
user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;

    # 增加 server 的配置
    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        location / {
            return 301 https://wizardbyron.github.io;
        }
    }
}
```

然后，我们把这个配置文件挂载到 nginx 容器中，取代默认的 配置文件。然后重新运行 nginx 容器：

``` bash
docker run --name nginx -d -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf -p 80:80 nginx
```

然后我们再执行测试：

``` bash
vivian -f redirect_case.csv
load test case from redirect_case.csv
1 cases loaded running in 1 processs
verifying http://local.testhost.com to https://wizardbyron.github.io
Failed cases:
============================================================
No failed case.
============================================================
1/1 PASS in 0.9458322525024414 seconds
```

测试通过！

## 用 TDD 的方式重构 nginx 转发规则

如果可以做 TDD ，那么我们还可以对 Nginx 规则重构，采用正则表达式来精简配置文件。例如，我们有两个 nginx 规则：

``` nginx
location = /path_to_site_a {
    return 301 https://wizardbyron.github.io;
}

location = /path_to_site_b {
    return 301 https://wizardbyron.github.io;
}
```

然后我们用 docker 启动 nginx，加载我们最新的配置文件。

接下来，我们可以编写两个测试用例：

```csv
http://local.testhost.com/path_to_site_a, https://wizardbyron.github.io
http://local.testhost.com/path_to_site_b, https://wizardbyron.github.io
```

它默认应该是通过的：

```shell
vivian -f redirect_case.csv
load test case from redirect_case.csv
2 cases loaded running in 2 processs
verifying http://local.testhost.com/path_to_site_a to https://wizardbyron.github.io
verifying http://local.testhost.com/path_to_site_b to https://wizardbyron.github.io
Failed cases:
============================================================
No failed case.
============================================================
2/2 PASS in 1.1543898582458496 seconds
```

然后，我们可以修改 nginx 配置文件为:

``` nginx
location ~ /path_to_site_(a|b) {
    return 301 https://wizardbyron.github.io;
}
```

它仍然应该是通过的：

```shell
vivian -f redirect_case.csv
load test case from redirect_case.csv
2 cases loaded running in 2 processs
verifying http://local.testhost.com/path_to_site_a to https://wizardbyron.github.io
verifying http://local.testhost.com/path_to_site_b to https://wizardbyron.github.io
Failed cases:
============================================================
No failed case.
============================================================
2/2 PASS in 1.1543898582458496 seconds
```

如果失败了，就要重新修改你的 nginx 转发规则。比如，我们在测试用例中增加一行：

```csv
http://local.testhost.com/path_to_site_c, https://stackoverflow.com
```

以上的配置文件就会失败：

``` shell
vivian -f redirect_case.csv
load test case from redirect_case.csv
3 cases loaded running in 3 processs
verifying http://local.testhost.com/path_to_site_a to https://wizardbyron.github.io
verifying http://local.testhost.com/path_to_site_b to https://wizardbyron.github.io
verifying http://local.testhost.com/path_to_site_c to https://stackoverflow.com
Failed cases:
============================================================
  line: 3
origin: http://local.testhost.com/path_to_site_c
  dist: http://local.testhost.com/path_to_site_c
expect: https://stackoverflow.com
status: 404
redirect_count:0
------------------------------------------------------------
============================================================
2/3 PASS in 0.8479752540588379 seconds
```

在这种模式下，你需要先把需要重定向的测试案例写到文件里，这时候运行 vivian 肯定会成功。之后你就可以优化合并一些正则表达式。由于有了 vivian 结合 docker 这种自动化测试的快速反馈机制。你可以很方便的优化你的 nginx 配置文件，无需部署之后再登录到主机上修改。

### 作为冒烟/回归测试集成在持续部署流水线里

我们有了自动化的测试工具，我们就可以把 nginx 配置和 测试用例文件保存到代码库里。在自己的 CI 服务器上安装 vivian，Vivian 需要你安装了 python3 和 pip，这对很多 Linux 发行版都不是一件困难的事情。

安装完成后，你可以在部署完成后用 vivian 检测测试用例当做冒烟测试来检测 nginx 是否配置得当。如果存在失败的 URL，则会以错误退出，你的流水线就会告诉你这个版本还不适合发布。如果你需要不断的修改和优化 nginx 配置文件，这些测试用例就可以作为回归测试，来避免你的修改影响到现有生产环境的配置。

## 一起来改进 Vivian

用 Dev 的方式处理 Ops 的工作，也算一种 DevOps 吧！？

如果你对该工具感兴趣或者发现问题，请不要犹豫直接 Issue 或者 PR：[https://github.com/wizardbyron/vivian](https://github.com/wizardbyron/vivian)
