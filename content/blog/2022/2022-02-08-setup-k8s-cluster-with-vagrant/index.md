---
title: "通过 Vagrant 一键初始化 K8S 集群"
date: 2022-02-08
tags:
- Kubernetes
- 云原生
- 开源
---
## 起因

去年初我开始系统学习 K8S，就想能生成一个集群环境。查看了一下官方文档，步骤很多。网上的一些资源已经过期或者不可用，再加上各种资源的变更和国内不可访问。

不得不说，在家按照官方文档搭建一个标准的 K8S 集群真是太难了！

所以我就自己构建了一个最小的 K8S 集群环境，放在了我的 provisioner 代码库里。现在这个开源代码库可以自动一键建立一个拥有一个控制节点和两个工作节点的最小K8S集群，可以反复销毁和启动。

过年在家的时间就对相关的脚本进行了完善，项目地址可参考：<https://github.com/wizardbyron/provisioners>，本文是对相关脚本的说明。

## 关于 Provisioner 项目

[Provisioners](https://github.com/wizardbyron/provisioners) 是我个人用于构建“最小可用集群”的一站式自动化脚本库。是我练习构建各种系统工具的一站式脚本收集仓库。它默认会通过 `vagrant`启动三个虚拟机，分别是管理节点（admin）和两个工作节点（node-1和node-2，最大支持到node-9）。管理节点的 IP 是`192.168.56.10`。工作节点是`192.68.56.11`~`192.168.56.19`。你可以通过修改`Vagrantfile`调整数量。

Provisioners 分为solution（解决方案）和facility（设施）两个脚本目录。

`facility` 里面则是单个工具的初始化脚本，包含各个工具的一键式初始化脚本。

`solution` 则是利用facility里的工具脚本组合成的解决方案，包括管理节点和工作节点。

此外，`essential`里包含了`init.sh`脚本，这是用于统一初始化 Linux 节点的统一基础脚本。而对于管理节点和工作节点的自动化初始配置则在`solution`目录里每个解决方案下的`admin/setup.sh`和`worker/setup.sh`里。

## Vagrantfile 配置说明

这个 Vagrantfile 的核心配置都写在了文件的前面。修改其中的参数可以改变集群相关配置。

```Ruby
SOLUTION = "k8s" # default/devops/k8s
BOXES ={
  "ubuntu" => "ubuntu/focal64",
  "centos" => "centos/7"
}

# 支持BOXES里面列出的 vbox 虚拟机镜像
DISTRO = "centos" 

# Linux 发行版软件镜像源：空(官方)/tencent(腾讯软件源)/aliyun(阿里云软件源)
MIRROR = "aliyun" 

# 最新的 Vagrant 版本强制了 CIDR，我保留了 1-9 的IP，并且将这个初始IP作为管理节点IP
ADMIN_IP = "192.168.56.10" 

# 调整工作节点数，根据你的资源增加，一般学习的话两个够了。
NODES = 2 

# 用于登录 Docker 镜像仓库，默认为docker.io
DOCKER_REGISTRY = "<>"
DOCKER_USERNAME = "<username for docker registry>"
DOCKER_PASSWORD = "<password for docker registry>"

```

默认控制面的主机名是`admin`，IP 是`192.168.56.10`。工作节点是`node-<数字>`，根据你的内存资源，你可以增加节点的数量。

最后只要运行`vagrant up`就可以启动你的集群，如果因为下载某些东西超时（比如镜像或者安装包），可以切换镜像重新试一下。

如果虚拟机全部初始化完成，你可以通过`kubectl get nodes`看到多个集群。

我一般会在搭建完控制面之后用`watch kubectl get ndoes`持续跟踪集群的搭建情况。

还是再说一句，在家按照官方文档搭建一个标准的 K8S 集群真是太难了！

## K8S 解决方案配置脚本说明

K8S 解决方案脚本主要分控制面配置和工作节点配置两个脚本，每个脚本都需要安装 `kubeadm`,`kubelet`和`kubectl`。

控制面配置完成以后才可以配置工作节点，因为需要加入控制面的token等一些信息。

### 控制面节点配置脚本 solution/k8s/admin.sh 说明

控制面安装要在管理节点上先通过`/facility/k8s/install.sh`安装安装 `kubeadm` 再进行通过 `kubeadm`配置。

```sh
#!/usr/bin/env bash
PATH=$PATH:/home/$(whoami)/.local/bin
export CONTROL_PANEL_IP=$1
echo "CONTROL PANEL IP: $CONTROL_PANEL_IP"

MIRROR="aliyun" # <empty>/aliyun
KUBE_VERSION="1.23.0-0"
sh -c "/vagrant/facility/k8s/install.sh $KUBE_VERSION $MIRROR"
sh -c "/vagrant/facility/k8s/setup-control-panel.sh $CONTROL_PANEL_IP $MIRROR"
```

参数说明：

- `CONTROL_PANEL_IP`: K8S控制面的IP地址，由外部传入。
- `MIRROR`: K8S所用的A镜像，除了apt源和yum源，还有k8s集群所需要的docker镜像，目前仅支持阿里云（唯一提供免费k8s镜像源）。如果为空，则会去查找官方镜像。
- `KUBE_VERSION`: K8S 的版本，可以指定版本版本。

### 工作节点脚本配置脚本  /solution/k8s/node.sh 说明

工作节点配置脚本和控制面配置脚本类似，都是先通过`/facility/k8s/install.sh`安装`kubeadm`，然后才进行配置。只是工作节点要在控制面配置完之后启动。

```sh
#!/usr/bin/env bash
PATH=$PATH:/home/$(whoami)/.local/bin
export CONTROL_PANEL_IP=$1
echo "CONTROL PANEL IP: $CONTROL_PANEL_IP"

MIRROR="aliyun" # <empty>/aliyun
KUBE_VERSION="1.23.0-0"

sh -c "/vagrant/facility/k8s/install.sh $KUBE_VERSION $MIRROR"
sh -c "/vagrant/facility/k8s/setup-worker-node.sh $CONTROL_PANEL_IP"
```

参数说明：

- `CONTROL_PANEL_IP`: K8S控制面的IP地址，由外部传入。
- `MIRROR`: K8S所用的A镜像，除了apt源和yum源，还有k8s集群所需要的docker镜像，目前仅支持阿里云（唯一提供免费k8s镜像源）。如果为空，则会去查找官方镜像。
- `KUBE_VERSION`: K8S 的版本，可以指定版本，但要和控制面的版本一致，否则会出问题。

## K8S facility 脚本说明

K8S facility 脚本包括三个脚本：

### 初始安装脚本 /facility/k8s/install.sh 说明

`install.sh`是初始化 linux 配置并安装 `kubeadm`,`kubelet`和`kubectl` 的脚本。完全按照[官方kubeadm 安装文档](https://kubernetes.io/zh/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)执行。

`install.sh`有两个参数：K8S 版本和安装包镜像。安装包镜像可以为空，采用默认的`packages.k8s.io`或阿里云镜像源。

`install.sh`的执行步骤如下：

1. 修改 docker 的配置，使用 systemd 来管理容器的 cgroup。
2. 配置网络, 允许 iptables 检查桥接流量。
3. 关闭系统交换区(swap area)。
4. 自动识别`apt`和`yum`并安装`kubeadm`相关软件包。

### 控制面配置脚本 /facility/k8s/setup-control-panel.sh 说明

`setup-control-panel.sh`是用来配置控制面的脚本。必须在`/facility/k8s/install.sh`安装之后执行。

`setup-control-panel.sh`主要做以下几件事：

1. 通过`firewall-cmd`配置k8s 集群所用端口。
2. 安装配置 K8S 等控制面组件:`kube-apiserver`。
3. 安装配置 Pod 网络插件。支持`calico`和`fannel`，默认选择`calico`。
4. 生成自动加入集群的脚本`join-cluster.sh`并通过`8000`端口暴露出来，让工作节点可以启动后自动加入集群。
5. 安装 helm。

### 工作节点配置脚本 /facility/k8s/setup-work-node.sh 说明

`setup-work-node.sh`的脚本比较简单，除了通过`firewall-cmd`打开所需端口以外，就是下载并执行控制面上的加入集群脚本。

## 从 MVP 开始

由于目前这是最小可用集群，如果你想增加自定义脚本可以在`facility`里自动化安装增加并且在`solution`自动化配置。

下一步可能会减少参数配置，尽量用内部的 DNS 服务取代 IP 的配置。

欢迎来<https://github.com/wizardbyron/provisioners>提 Issue 和 PR！
