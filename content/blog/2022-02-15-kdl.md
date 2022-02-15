---
title: "【翻译】Kubernetes 部署语言（Kubernetes Deployment Language）"
date: 2022-02-15
tags:
- kubernetes
---

在网上搜索规范化的 K8S 的部署架构图画法时，发现了 Redhat 的一篇博客。觉得非常不错，遂翻译分享之。

原文: <https://github.com/raffaelespazzoli/kdl>

## 介绍

这篇博文介绍了 Kubernetes API 对象的图形表示法：Kubernetes 部署语言（简称 KDL）。 Kubernetes API 对象可被用于描述如何在 Kubernetes 中部署一个解决方案。

笔者认为有必要描述和记录如何在 Kubernetes 中部署应用程序，特别是当应用程序用到了多个不同的 Kuberenetes 组件时。

笔者想创建一个简单的图形符号约定来描述这些应用程序的部署，以便这些图形可以轻松地在白板或文档中绘制。

为了更好地解释该符号体系的目标，我们可以将其与 [UML](https://en.wikipedia.org/wiki/Unified_Modeling_Language)比较。UML 有几种图形语言来描述应用程序架构的不同方面。 不过，与 UML 的不同之处在于，在 KDL 中，我们没有进行正向或逆向工程的目标（即我们不转换 yaml 文件中的图表，反之亦然）。 这样，我们就有机会管理要在图表中显示的信息量。 作为一般经验法则，我们只会显示与架构相关的信息。

您还可以下载[KDL 的 visio模板](/img/blogs/20220214/kdl.vssx)。

### 目标

该图形符号体系的目标如下：

- 创建一种通用的图形语言来描述如何在 Kubernetes 中部署应用程序。
- 表示 Kubernetes API 对象与架构最相关的方面。
- 简单地说，在理想情况下，一个拥有白板和一些彩色便利贴的人应该能够创建这些图表。

以下内容不是该符号体系的目标：

- 自动生成 API 对象定义

### 颜色编码

一般来说，Kubernetes API 对象涵盖以下范畴：

| 范畴  | 颜色约定  | 例子  |
|---|---|---|
| Kubernetes 集群  | 红  | Kubernetes 解决方案中包含的若干个集群 |
| 计算  | 绿  | 部署  |  
| 网络  | 黄  | 服务  |  
| 存储  | 蓝  | 持久卷申领（PersistentVolumeClaim），持久卷（PersistentVolume） |

## Kubernetes 集群

Kubernetes 集群可以简单地表示为一个红色的矩形：

![KubernetesCluster](/img/blog/20220215/kubernetes-template.png)

所有其他 API 对象都存在于集群内部或集群边缘。
永远不需要显式表现 Kubernetes 集群内的各个节点。

您可以用其它的图形表示集群外部的组件以及它们如何与集群内部的组件连接。 此图形约定不含集群外的组件的展示方式。

## 计算

计算对象是最复杂的图形。 通常，它们由一个带有组件标识的矩形表示，用于展示计算对象的附加信息。 这是一个模板：

![ComputeTemplate](/img/blog/20220215/compute-template.png)

图片的中心部分代表一个 [Pod](https://kubernetes.io/docs/concepts/workloads/pods/pod/)。 在其中我们可以看到一个或多个容器。 Pod 和容器都应该有一个名称。

在 Pod 的左侧，我们有额外的计算附加信息。 顶部标记指定此 Pod 的控制器类型。 以下是控制器的类型及其缩写：

| 控制器类型  | 缩写  |  
|---|---|
| [Replication Controller](https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/)  | RC  |
| [Replica Set](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)  | RS  |
| [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)  | D  |  
| [DeploymentConfig](https://docs.openshift.com/container-platform/latest/architecture/core_concepts/deployments.html#deployments-and-deployment-configurations) (OpenShift only)  | DC  |
| [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)  | DS  |  
| [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)  | SS  |  
| [Job](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/) | J |
| [Cron Job](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) | J |

在底部，我们有该 Pod 实例的基数。 根据控制器的类型，该字段具有不同的含义和格式，这里有一个参考表格：

| 控制器类型  | 格式 |  
|---|---|
| Replication Controller  | 一个数字或者数字范围 (例如 3 或 2:5)  |
| ReplicaSet  | 一个数字或者数字范围 (例如 3 或 2:5)  |  
| Deployment  | 一个数字或者数字范围 (例如 3 或 2:5)  |
| DeploymentConfig (只有 OpenShift 有) | 一个数字或者数字范围 (例如 3 或 2:5) |
| DaemonSet  | 节点选择器: 例如 storage-node=true  |
| StatefulSet  | 一个数字: 例如 3  |
| Job  | 一个表示并行度的数字: 例如 3  |
| Cron Job  | 一个表示并行度的数字: 例如 3  |

在 pod 的顶部，是暴露的端口。 您可以使用小矩形仅显示端口号或添加端口名称。 这是一个例子：

![PortExample](/img/blog/20220215/port-example.png)

这些小矩形是黄色的，因为代表网络配置。您可以将每个端口与实际暴露该端口相关的容器连接起来。 但在大多数情况下，这不是必需的，因为大多数 pod 只有一个容器。

在 pod 的底部，我们有 [附加卷](https://kubernetes.io/docs/concepts/storage/volumes/)。 卷的名称应显示在矩形中。 在大多数情况下，这些将是持久卷。 如果卷类型不是持久卷，则显示它可能是相关的。 此外，有时显示安装点也很重要。 以下是卷的符号示例：

![VolumeExample](/img/blog/20220215/volume-example.png)

在 Pod 的右侧，具有与 Pod 的配置相关的卷：[secrets](https://kubernetes.io/docs/concepts/configuration/secret/) 和 [configmaps](https://kubernetes .io/docs/tasks/configure-pod-container/configmap/）。 对于数据卷，应该指明卷的名称，通常区分**configmaps**和**secret**很重要，所以还应该指明卷的类型，如果需要还可以显示挂载点。 这里有些例子：

![SecretExample](/img/blog/20220215/secret-example.png)

## 网络

网络对象有两种: [services](https://kubernetes.io/docs/concepts/services-networking/service/) 和 [ingresses](https://kubernetes.io/docs/concepts/services-networking/ingress/) ([routes](https://docs.openshift.com/container-platform/latest/architecture/core_concepts/routes.html) 在 OpenShift 里有).

### 服务

服务可以用椭圆表示，如下图所示:

![ServiceTemplate](/img/blog/20220215/service-template.png)

左侧有一个代表服务类型的小矩形。 以下是缩写：

| 类型  | 缩写  |
|---|---|
| [Cluster IP](https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies)  | CIP  |
| [Cluster IP, ClusterIP: None](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services)  |  HS a.k.a. Headless Service |
| [Node Port](https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport)  | NP  |
| [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#type-loadbalancer) |  LB |
| [External Name](https://docs.openshift.com/container-platform/3.5/dev_guide/integrating_external_services.html#using-fqdn-2) (OpenShift only) | EN  |
| [External IP](https://kubernetes.io/docs/concepts/services-networking/service/#external-ips) |  EIP |  

在服务的顶部有暴露的端口。 此处适用与计算对象端口相同的约定。

该服务应连接到计算对象。 这将隐式定义服务选择器，因此无需在图片中指示它。

如果服务允许从集群外部到内部 pod 的流量（例如负载均衡器或节点端口或外部 IP），则应在集群边缘进行描述。

![EdgeService](/img/blog/20220215/edge-service.png)

相同的概念适用于调节出站流量（例如外部名称）的服务，尽管在这种情况下它们可能会出现在 Kubernetes 集群矩形的底部。

### Ingresses

Ingresses 可以用平行四边形表示，如下图：

![IngressTemplate](/img/blog/20220215/ingress-template.png)

Ingresses 显示入口名称和可选的主机暴露。 Ingresses 将连接到服务（相同的规则适用于 OpenShift 路由）。

Ingresses 始终显示在 OpenShift 集群的边缘。

![EdgeIngress](/img/blog/20220215/edge-ingress.png)

#### 路由 (OpenShift)

OpenShift 路由使用与 Ingress 相同的符号表示。

## 存储

存储用于指示持久卷。 存储的颜色是蓝色的，它的形状是一个桶，部署如下图：

![StorageTemplate](/img/blog/20220215/storage-template.png)

存储应指明持久卷名和存储提供程序（例如 NFS、gluster 等）。
存储始终位于集群的边缘，因为它是指向外部可用存储的配置。

![EdgeStorage](/img/blog/20220215/edge-storage.png)

## Putting it all together

在本节中，我们将通过一个示例来说明如何使用此表示法来描述应用程序的部署。
我们的应用程序是一个银行服务应用程序，它使用 mariadb 数据库作为其数据存储。 作为银行应用程序，一切都必须在 HA 中。
以下是部署图：

![mariadb-example](/img/blog/20220215/mariadb-example.png)

请注意，mariadb pod 使用 StatefulSet 和一个持久卷来存储其数据。 这个 pod 没有暴露给集群外部，但它的服务被 BankService 应用程序使用。
BankService 应用程序是一个由部署配置控制的无状态 pod，该部署配置具有用于访问数据库的凭据的机密。 它还有一个服务和一个路由，以便它可以接受来自集群外部的入站连接。
