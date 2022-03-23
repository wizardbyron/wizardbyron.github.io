---
title: "采用 Multipass 管理本机虚拟 K8S 集群"
date: 2022-03-22
tags:
- Kubernetes
- 开源
---

在 [通过 Vagrant 一键初始化 K8S 集群](/blog/2022-02-08-setup-k8s-cluster-with-vagrant/) 之后，发现 VirtualBox 只支持 X86 芯片，对 Apple M1 不支持。加之 CentOS 的支持也将近尾声。而我在捣鼓 [Provisioner](https://github.com/wizardbyron/provisioners) 脚本的时候总要花大量的时间测试 CentOS 的兼容性，很耗时间。

偶然发现 [Multipass](http://multipass.run) 可以支持在 Apple M1 虚拟 Ubuntu 实例，效果还不错。所以将 Provisioner 的脚本进行了移植，并基于 Multipass 进行了一层封装以管理整个 k8s 集群。所以花了两周的业余时间调整了一下。

本文就介绍一下 `k8s-multipass`，项目地址：<https://github.com/wizardbyron/k8s-multipass>，欢迎PR。

## 当前功能介绍

1. 一个 Multipass 的包装器（wrapper），管理本地 k8s 集群生命周期。
2. 创建一个控制面节点，并启用 NFS 和本地 DNS 服务（Bind9），通过 NFS 服务共享加入脚本。并采用 Calico 初始化 Pod 网络。
3. 创建两个工作节点，并通过 NFS 自动加入控制面。
4. 通过 docker 在控制面上新建 LDAP 服务。

## 使用方法

1. 下载 [Multipass](http://multipass.run)。
2. 克隆本项目：`git clone git@github.com:wizardbyron/provisioners.git`
3. 你可以在 `k8sctl` 命令中调整配置。未来我考虑增加一个读取配置的模块。
4. 进入项目目录，通过`./k8sctl create`命令一键创建具有两个工作节点的 K8S 集群。
5. 通过`./k8sctl login`登录到控制面进行管理。

## 命令介绍

`./k8sctl create`: 创建一个新的本地 k8s 集群，默认包含一个控制面和两个工作节点。
`./k8sctl start`: 启动已停止的本地 k8s 集群上的所有节点。
`./k8sctl stop`: 停止的本地 k8s 集群上的所有节点。
`./k8sctl restart`: 重启本地 k8s 集群上的所有节点。
`./k8sctl destroy [节点名]`: 销毁本地 k8s 集群上的所有节点或指定节点。
`./k8sctl check`: 检查 k8s 集群上各节点和 Pod 的状态。
`./k8sctl status`: 检查 k8s 集群上各节点虚拟机工作状态。
`./k8sctl login`: 登陆控制面进行操作。

## 项目目录介绍

```sh
├── k8sctl 主控制文件
├── scripts # 各服务脚本目录
│   ├── dns # DNS 服务端和客户端安装和配置脚本
│   │   ├── client.sh
│   │   └── server.sh
│   ├── init.sh # 虚拟机初始化脚本目录
│   ├── k8s
│   │   ├── install.sh # K8S 安装脚本
│   │   ├── setup-control-plane.sh # 控制面配置脚本。
│   │   └── setup-worker-node.sh # 工作节点配置脚本。
│   ├── nfs # NFS 服务端和客户端安装和配置脚本
│   │   ├── client.sh
│   │   └── server.sh
│   └── openldap # LDAP 服务端配置脚本
│       └── server.sh
└── share # 和虚拟机之间交换文件的共享目录
```

## 未来的计划

这个项目和 [MicroK8S](https://microk8s.io) 以及 [MiniKube](https://minikube.sigs.k8s.io/docs/start/) 不同。这个项目和 Provisioner 一样，用于产生一个最小的可验证功能的虚拟 K8S 集群环境。随着我的学习和总结，这个项目也会不断完善。
