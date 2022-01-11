---
title: "云计算厂商是如何定义微服务的？"
date: 2021-12-14T11:18:14+08:00
draft: true
categories: 
  - 微服务
tags:
  - 微服务
---

在2018年写下了[《讨论微服务之前，你知道微服务的 4 个定义吗？》](/posts/2018-09-14-four-definitions-of-microservices)。三年来，关于什么是微服务，分歧越来越多。其中，CNCF 的“云原生”概念虽然描述了什么是“云原生”，但是对于“微服务”的概念却避而不答。那么，我们就从主流云服务厂商（AWS，Azure，GCP）的对微服务定义中的词汇逻辑进行分析，也许能得到一些关于微服务的共识。

本文包括以下四个章节

1. AWS 的微服务定义
2. Azure 的微服务定义
3. GCP 的微服务定义
4. 不同云服务厂商微服务定义的共同之处

## AWS 的微服务定义

来源：<https://aws.amazon.com/cn/microservices/>

> 微服务是一种开发软件的架构和组织方法，其中软件由通过明确定义的 API 进行通信的小型独立服务组成。这些服务由各个小型独立团队负责。
> 微服务架构使应用程序更易于扩展和更快地开发，从而加速创新并缩短新功能的上市时间。

在 AWS 的微服务定义中，微服务不光是软件架构的方法，而且是组织的方法。 AWS 利用“康威定律”将应用架构和组织架构对应。通过组织架构来简化应用架构的复杂性。这里面显而易见的逻辑是“服务的独立”和“团队的独立”，这很像 UNIX 的哲学：

> 程序应该只关注一个目标，并尽可能把它做好。让程序能够互相协同工作。应该让程序处理文本数据流，因为这是一个通用的接口。

这是 Unix 系统上管道机制的发明者，也是Unix文化的缔造者之一 道格拉斯·麦克罗伊归纳的哲学。这和服务架构概念的最早提出者[James Lewis 的微服务定义](/posts/2018-09-14-four-definitions-of-microservices/#james-lewis-原始版的微服务-6-大特征)是一致的。微服务的本身就是来自于 UNIX 哲学。而 AWS 则更进一步将这种哲学应用到组织架构中。避免“康威定律”带来的问题。

在 AWS 的微服务定义中，第二句则是表明了作为架构方法的微服务的优势：应用“易于扩展”和“快速开发”。

以及对应的商业价值：加速创新并缩短新功能的上市时间。

而加速创新并缩短功能的上市时间则是敏捷软件开发和 DevOps 的的目标。

因此，如果你单一采用敏捷软件开发或者 DevOps，碰到的问题就是应用架构的不敏捷。

此外，在 AWS 的官网中，还补充了微服务的两个特性：

> 自主性：可以对微服务架构中的每个组件服务进行开发、部署、运营和扩展，而不影响其他服务的功能。这些服务不需要与其他服务共享任何代码或实施。各个组件之间的任何通信都是通过明确定义的 API 进行的。
> 专用性：每项服务都是针对一组功能而设计的，并专注于解决特定的问题。如果开发人员逐渐将更多代码增加到一项服务中并且这项服务变得复杂，那么可以将其拆分成多项更小的服务。

这两个特性是对“独立”这一概念进一步的补充。

第一条表明了

## Azure 的微服务定义

来源：[Azure 上的微服务 - 什么是微服务 | Microsoft Azure](https://azure.microsoft.com/zh-cn/solutions/microservice-applications/#overview)

> 微服务是一种用于构建应用程序的体系结构方法，应用程序中的每个核心功能（或服务）都单独进行构建和部署。微服务体系结构是松散耦合的分布式体系结构，因此一个组件的故障不会中断整个应用。各个独立组件协同工作，并通过定义明确的 API 协定进行通信。构建微服务应用程序，以满足快速变化的业务需求，并更快地向市场推出新功能。

Azure 的定义比较复杂，

此外，便于客户理解微服务的价值并推销自己的产品，，但包含了四个价值，这四个价值

> 灵活的构建和部署：无需重新部署整个应用程序即可轻松管理单个组件中的新功能版、更新和 bug 修补程序。使用持续集成/持续部署 (CI/CD) 管道（如 GitHub Actions）自动执行软件交付工作流。
> 微服务随需求而缩放：根据资源需求缩放各个服务和子系统，而无需缩放整个应用程序。使用 Azure Kubernetes 服务 (AKS) 或 Azure Red Hat OpenShift 等容器业务流程协调程序，将更高密度的服务打包到单个主机中。
> 使应用程序的复原能力更佳：在不影响整个应用程序的情况下，替换或停用单个服务。与传统的单一式应用程序模型不同，微服务平台使用断路等模式来容许单个服务故障，从而提高安全性和可靠性。为简化此过程，使用适用于 Azure Kubernetes 服务 (AKS) 的 服务网格接口 (SMI) 或适用于 Azure Red Hat OpenShift 的 Red Hat OpenShift 服务网格来安装一个服务网格。
> 为团队查找最佳方法：针对每个服务，选择团队的首选部署方法、语言、微服务平台和编程模型。发布微服务 API 供内部和外部使用，同时使用 Azure API 管理来管理身份验证、授权、限制、缓存、转换和监视等横切关注点。

这四个价值里

Azure 同样空滤“团队”，在

Azure 的微服务定义并不包含组织的关系，

## Google Cloud Platform 的 的微服务定义

GCP 关于微服务定义的地方有两处：

来源1：[什么是微服务架构？ &nbsp;|&nbsp; Google Cloud](https://cloud.google.com/learn/what-is-microservices-architecture?hl=zh_cn)

> 微服务架构是一种应用架构类型，其中应用会开发为一系列服务。它提供了独立开发、部署和维护微服务架构图和服务的框架。

来源2：[BeyondProd：云原生安全性的新方法 &nbsp;|&nbsp; 文档 &nbsp;|&nbsp; Google Cloud](https://cloud.google.com/security/beyondprod)

> 微服务将应用需要执行的各个任务分离成单独的服务，每项服务都可独立进行开发和管理，并且具有自己的 API、发布、扩缩和配额管理。在更现代化的架构中，诸如网站之类的应用可作为一组微服务运行，而不是作为单一的服务运行。微服务是独立的、模块化的、动态的、短暂的。它们可以分布在许多主机、集群甚至云端上。

Google 对微服务的定义很简单，也并没有

## 微服务的定义共识

从以上三点

1. 应用由微服务组成。
2. 每个微服务都可以独立开发和管理。
3. 每个微服务有明确定义的 API 进行通讯。
4. 更易于扩展和开发。

微服务的收益：

1. 在我看来，AWS 对微服务的定义事

可惜，在本文发布日之前，国内的云厂商（仅包括：阿里云、腾讯云、华为云、青云、七牛云）并没有专门的定义，但很奇怪的是，他们却有很多微服务相关的产品。