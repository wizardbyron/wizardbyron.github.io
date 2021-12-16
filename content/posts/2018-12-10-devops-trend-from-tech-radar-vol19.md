---
title: 从第19期技术雷达看 DevOps 的发展趋势
date: 2018-12-10
categories: 
  - DevOps
tags:
  - 技术雷达
  - 微服务
  - 安全
  - 容器
  - Docker
  - Kubernetes
---

2018年下半年的技术雷达发布了。看过的朋友可能和我的感觉一样，会发现大部分条目都是和微服务和 DevOps 相关，但这些条目散落在不同的象限里。本文将这些散落在不同象限的条目采用以下 5 个主题进行重组：

1. DevOps 合作新实践
2. 云计算新实践
3. 容器新技术
4. 微服务及其误区
5. 安全

特别要提出的是，这期技术雷达采纳了 [2018 年的 DevOps 报告](https://cloudplatformonline.com/2018-state-of-devops.html) 中的**四个关键指标(FOUR KEYMETRICS)**:前置时间，部署频率，平均恢复时间(MTTR)和变更失败百分比。而这四个关键指标也是业界度量 DevOps 效果的统一方式。

每个指标都创造了一个良性循环，并使团队专注于持续改进:缩短交付周期，减少浪费的活动，从而使你可以更频繁地部署，进而改进他们的实践和自动化流程。通过更好的实践，自动化和监控可以提高你从故障中恢复的速度，从而降低故障频率。

## DevOps 的合作

如何更好的在组织内合作是 DevOps 实践中永恒不变的的话题。随着 DevOps 合作理念的深入，合作的范围越来越越广，随之带来了新的问题和挑战。这期的技术雷达介绍了以下几方面的合作：

1. 和外包团队/供应商的 DevOps 合作
2. 和用户/客户/UX设计师的合作
3. 分布式团队之间的合作

### 和外包团队的 DevOps 合作

而随着 DevOps 应用的加深，会不可避免的碰到组织结构上带来的问题。特别是和外包方的合作，会影响组织的 DevOps 表现。这样的合作往往充满了漫长繁冗且火药味十足的会议和合同谈判，这是 DevOps 运动中不希望看到的但是又无法避免的问题。在 [2018 年的 DevOps 报告](https://cloudplatformonline.com/2018-state-of-devops.html)中看到**外包会带来效能下降**——“低效能团队将整部分职能进行外包的可能性几乎是高效能团队的 4 倍，这些 **外包功能包括测试或运维等等**。”

看到这里，千万不要得出“不要用外包的结论”。这里说得是不要“职能的外包”，而“端到端的外包”（End-2-End OutSourcing）则会免除这种顾虑。很多业界一流的 IT 服务企业都提供端到端的 IT 外包服务，你只需要告诉它们你要DevOps，它们会用最有效的方式交付给你。与**供应商一起增量交付(INCREMENTAL DELIVERY WITH COTS (commercial off-the-shelf))** 就是这期技术雷达中提出的和外包商一起进行 DevOps 策略之一。与供应商的做端到端的 DevOps 性质的外包另外一个优点则是这样的供应商适合做“长期合作伙伴”来补充你业务、IT 等多样性的不足，甚至能够帮你培训员工。

而随着组织开始采用**四个关键指标**，这对对供应商的要求也越来越高，但盈利空间相对越来越小。和任何行业一样，成本的降低和效率的提升永远是不变的主节奏。外包也要提升自己的能力水平以跟上技术发展的节奏，这是不可避免的成本。

但是，和外包方的合作仍然是在 DevOps 转型过程中不可避免的痛苦，可以采用一些方式减轻这种痛苦。例如这期技术雷达中介绍的**“风险相称的供应商策略(RISK-COMMENSURATE VENDOR STRATEGY) ”**，它鼓励在高度关键系统中维持其供应商的独立性。而那些相对不太重要的业务可以利用供应商提供的成熟解决方案，这可以让企业更容易承受失去该供应商所带来的影响。这不光是说 IT 产品供应商，同样也指的 IT 服务供应商。

[“**边界购买（BOUNDED BUY）**”](https://www.slideshare.net/tgriffo/agile-australia-2017-hypothesisdriven-cots-software-selection-tiago-griffo)就是这样一种实践，在采购产品中即只选择模块化、解耦的，且 只包含于单一业务能力(Business Capability)的限界上下文(Bounded Context)中的厂商产品。应该将这种对 模块化和独立交付能力的要求，加入对供应商选择的验收标准中去。也可以将一小部分业务的端到端维护外包出去，在获得灵活性的同时，又获得高效。

### 和 UI 的合作 ——DesignOps

DevOps 的目标就是尽可能的缩短最终用户想法到代码之间的距离，避免传递过程中的信息失真。特别是用户的反馈，于是有了 DesignOps 实践。这个领域的实践和工具也日渐成熟。这期的技术雷达介绍的一整套支持 UI 的开发环境(也称为UI DEV ENVIRONMENTS)专注于用户体验设计人员与开发人员之间的协作，例如 :[Storybook](https://storybook.js.org/) ，[react-styleguidist](https://react-styleguidist.js.org/)，[Compositor](https://compositor.io/) 及 [MDX](https://mdxjs.com/)。这些工具大部分围绕 React 的生态圈产生。既可以在组件库或设计系统的开发过程中单独使用，也可以嵌入到 Web应用项目中使用。

### 分布式团队的合作

随着组织的扩大，分布式的团队是一个无法回避的问题。你很可能会和不同地理位置的其它同事一起开发，例如：不同的办公楼，不同的城市，甚至是不同的国家。但这些问题不是 DevOps 的阻碍，可以通过一系列的工具来弥合地理上的界限。

Visutal Studio Code 目前是最受欢迎的编辑器和开发环境。而 [VS Live Share](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare) 给分布式的跨地域协作开发的能力，它是用于 Visual Studio Code 与 Visual Studio 的插件。提供实时合作编辑与调试代码、语音通话、共享终端和暴露本地端口等功能，能够减少远程结对编程时遇到的障碍。开发人员可以在使用Live Share 协作时沿用自己的编辑器配置，包括主题、快捷键和扩展。

## 云计算新实践

如果你仔细看技术雷达，这期的技术雷达把 AWS，Azure 和 Google Cloud Platform 这三个世界上最大的云计算供应厂商放到了 Trail（试验）象限。这说明在采用云计算的时候，需要注意防止被云供应商绑定。从这个角度来说，Kubernetes 这样平台无关的技术要更好。

设置多云账号(MULTI-ACCOUNT CLOUD SETUP)可以避免被单一的云供应商绑定，可以平衡的结合采用多个云平台的优势来动态的配置你的云计算经验。

CHAOS KATAS 是一项为基础设施和平台工程师提供技能培训和提升的技术。它将 Kata （我个人更倾向于把 Kata 翻译为 套路）的方法论与Chaos Engineering 的相关技术(具体指在受控环境中模拟故障和停机)进行结合，对工程师进行系统化教学和培训。这里的 Kata 是指触发受控故障的代码模式，它允许工程师发现问题，恢复故障，开展事后分析并找到根本原因。工程师通过重复执行Kata能帮助他们真正掌握新的技能。

### 用基础设施即代码提升基础设施的质量

管理云计算资源最有效的形式是采用基础设施即代码技术。在这一方面，早期的 Chef，Puppet 已被 Ansible、Salt 等取代。而后继之秀 Terraform 则简化了很多的云计算平台上的基础设施配置工作。现在，Terraform 已经成为公有云基础设施即代码的第一选择。这期的技术雷达介绍了[Terragrunt](https://github.com/gruntwork-io/terragrunt)，它是Terraform 的一个轻量级的封装，用来落地《 Terraform: Up and Running 》书中主张的实践。当然，在采用它之前你可以先读一下这本书。

如果你使用了 AWS，并且向通过编程的方式生成基础设施即代码。你可以使用[Troposphere](https://github.com/cloudtools/troposphere)，Troposphere 是一个Python 库，可以使用 Python 代码生成 JSON 格式的 CloudFormation 描述。这样的代码的复用性和设计都会很好，同时它也有类型检测、单元测试以及 DRY 组合 AWS 资源等功能。

在云原生的环境下，跨平台，跨实践的基础设施即代码技术将成为下一个基础设施即代码的发展方向。[Pulumi](https://www.pulumi.com/)就是这样一款“云原生即代码”工具，它提供了一个云原生开发平台，为所有的云原生应用通过一致的编程模型和统一的DevOps实践，帮助团队大幅提升生产力，并以很快的速度将代码迁移到云中。

结合往期的技术雷达，可以看出，在有效的采用基础设施即代码的技术上，除了版本化和自动化以外，基础设施即代码正在向可测试性和合规性的方向发展。对基础设施质量的度量和检测可以通过基础设施即代码来实现。而除了公有云平台，很少可以见到企业对私有的基础设施质量的关注。和软件产品一样，基础设施也会存在技术债，而这些技术债会引发应用程序的技术债的连锁效应。比如，你采用了老旧的设备和老旧的操作系统，在缺乏管理的情况下，网络、安全甚至是性能问题越来越凸显，而系统会越来越脆弱。

## Kubernetes 和容器

Kubernetes 已经是容器生态的核心，因为除了 Docker 以外，还有其它的替代容器方案可以选择。但编排方案的选择却不会太多。为了保持容器镜像的大小，大家往往会采用 Alpine 和 Busybox 这样袖珍的镜像作为基础镜像。避免安装和配置那些无用的软件包和SDK。现在有了 [DISTROLESS DOCKER IMAGES](https://github.com/GoogleContainerTools/distroless) 这样的选择，可以被翻译做 “非发行版的 Docker 镜像”，它由 Google 开发，并给每种语言运行时都建立了发行版无关的镜像，兼顾了安全性和大小两方面。

在 Kubernetes 运维方面，这期的技术雷达新增了两个工具。[Kube-Bench](https://github.com/kubeflow/kubebench) 和 [Heptio ARK](https://github.com/heptio/ark)。前者是大名鼎鼎的 K8S 机器学习社区 Kubeflow 推出的一款基础设施配置扫描工具，基于 K8S的 CIS 评分自动检查 Kubernetes 配置，涵盖用户身份验证，权限控制和数据安全等方面。后者是Kubernetes 跨云的解决方案厂商 Heptio 推出的一个集群和持久化卷的灾难恢复管理工具。使用 Ark 可以显著缩短基础架构发生故障时的恢复时间，还能轻松地将 Kubernetes 资源从一个集群迁移到另一个集群，或者复制生产环境用于测试和排错。Ark支持主流的云存储提供商(包括 AWS ，Azure 和 GoogleCloud )，并且从版本0.6.0开始，提供了插件系统用于兼容其他备份与卷存储平台。虽然 GKE 等 Kubernetes 托管环境已经提供了这类服务，但如果需要自行运维 Kubernetes ，不论是在本地还是云端，都请仔细考虑使用 Heptio Ark 进行灾难恢复。

[Rook](https://rook.io/) 是一款运行在Kubernetes集群中的开源云原生存储编排工具，现在仍然在CNCF 进行孵化。与Ceph集成之后的Rook，能将文件、块和对象存储系统引入到 Kubernetes 集群中，并能与使用这些存储的其他应用和服务一起无缝地运行。通过使用一些 Kubernetes operator，Rook可以在控制层上编排Ceph，这样就可以避免挤占应用程序和Ceph之间的数据通道。

Kubernetes 一直是 无服务器架构（Serverless Architecture）的理想平台，围绕着 Kubernetes 已经有了很多 Serverless 解决方案，如 Kuberless 和 OpenFaaS。[Knative](https://github.com/knative/)  是 Google 推出的基于 Kubernetes Serverless 方案，[你可以把它部署在任何 Kubernetes 集群上](https://github.com/knative/docs/blob/master/install/Knative-with-any-k8s.md)。

Service Mesh 提供一致的发现、安全性、跟踪、监控和故障处理，而无需共享API网关或ESB等设施。典型的实现是将每个服务进程和轻量级反向代理以Side-Car 的方式一起部署，反向代理进程可能在单独的容器中。这些代理与服务注册表，身份提供者，日志聚合器和其他服务进行通信。服务互操作性和可观测性是通过此代理的共享实现而不是共享运行时实例获得的。

随着集中式的微服务网关和服务注册/发现机制的逐渐臃肿，Service Mesh 会接起微服务规模化的接力棒。随着 Linkerd 和 Istio 等开源项目将逐步成熟，这使得 service mesh 更容易实现。目前 Istio 仍遭受了来自性能方面的担心，但我相信在某些场景下，这些性能损耗是可以被复杂性平衡的。

Kubernetes 生态圈的发展一直围绕着微服务进行的。所以，结合微服务技术的发展更可以看清Kubernetes的发展轨迹。

## 微服务及其误区

微服务的实践正在渡过深水区，判断的依据很简单：关于微服务的工具出现的越来越少，而实践和经验越来越多。这表明很多不会有很多新的通用问题需要解决。**事件风暴(EVENT STORMING)** 被放入了“采用”环中，这意味着事件风暴将作为微服务实践的核心技术之一。事件风暴是一项团队活动，旨在通过领域事件识别出聚合根，进而划分微服务的限界上下文。在活动中，团队先通过头脑风暴的形式罗列出领域中所有的领域事件，整合之后形成最终的领域事件集合，然后对于每一个事件，标注出导致该事件的命令（Command），再然后为每个事件标注出命令发起方的角色，命令可以是用户发起，也可以是第三方系统调用或者是定时器触发等。最后对事件进行分类整理出聚合根以及限界上下文。事件风暴还有一个额外的好处是可以加深参与人员对领域的认识。

在微服务的应用中，分布式追踪一直是一个困扰人们很久的问题。CNCF 的 [Jaeger](https://www.jaegertracing.io/) 的机制同样来源于谷歌的 Dapper，并遵循 OpenTracing 。它在 Kubernetes 集群中安装它也很简单，它可以和Istio 配合使用，在 Kubernetes 集群中与 Envoy集成进行应用程序追踪。而 CNCF 所提供的工具渐渐会和 Spring Cloud 这种微服务全家桶的解决方案结合，变成未来微服务架构的基准参考模型。

除了 Java 社区以外，其它语言的社区也跃跃欲试。例如这一期技术雷达介绍的 [Ocelot](https://github.com/ThreeMammals/Ocelot)，它是基于.NET Core实现的轻量级API网关项目，它可以通过轻松的配置来实现路由转发、请求聚合、服务发现、认证授权、限流熔断、负载均衡等特性，它还集成了Service Fabric、Consul、Eureka等功能。目前 Ocelot 的功能已经相当完整，它在.NET Core社区的活跃度也很高。目测能够作为未来 .NET 社区微服务实践的首选。

而在 Python 社区，出现了一个超轻量级的微服务框架 [NameKo](https://nameko.readthedocs.io/en/stable/)，它也是 Flask的 替代方案。与 Flask 不同的是 Nameko 只包含了 WebSocket、HTTP、AMQP 支持等有限功能。我非常喜欢这种简单而轻量的框架，如果你采用 Python 作为微服务的实现语言，你可以考虑考虑它。

JavaScript 社区曾经有一个从前端到后端“一统天下”的设想。也出现了 [MEAN](http://mean.io/) 这样的全栈 Javascript框架。现在 F# 社区出现了一个有力的竞争者：SAFE 。[SAFE 技术栈](https://safe-stack.github.io/)是 Suave、Azure、Fable 和 Elmish 的简称。SAFE 囊括了一系列技术，形成了前后端一致的 Web 开发技术栈。SAFE 在服务端和浏览器端都使用了 F# 语言，因此注重于异步函数式类型安全的编程机制。它不仅提供了一些提高开发效率的功能比如热加载; 还允许替换技术栈里的某些模块，例如服务器端 Web 框架或云提供商。它很有希望成为微软技术栈下 Serverless 微服务架构的候选者。

### 微服务的误区

随着微服务越来越火，很多组织开始盲目的追求微服务架构。但很多团队都把架构通过把简单的 API 进行复杂的整合使架构更加难以维护。它用运维复杂性换取了开发的复杂性。然而，这需要坚实的自动化测试，持续交付和 DevOps 能力作为支撑。

这期技术雷达提出的分层式微服务架构(LAYERED MICROSERVICES ARCHITECTURE)的组织是一种反模式，他们在某些方面存在着明显的矛盾。这些组织都陷入了以技术角色为主来划分服务的误区，比如，用户体验API、进程 API 或系统 API等。这样会导致业务变更仍然会有缓慢而昂贵的多团队合作。

另外一点是，当中台战略逐渐开始流行后，会导致前台团队和后台团队被从技术上分开，而缺乏了微服务所需要的整体业务能力。中台更多强调的是内部应用的产品化和 SaaS 化能力。而不仅仅是割裂为独立的微服务。这样，你需要额外的一个中间层来做前台和中台之间的转换。而这样一个中间层，无论是放到前台和中台都是不合理的。我仍然推荐围绕业务能力组建一个端到端的微服务团队。

由于微服务很多都支持基于事件的异步调用方式，这也影响到了前端用户体验的设计。这就是**在面向用户的工作流中使用请求 — 响应事件 (REQUEST-RESPONSE EVENTS IN USER-FACING WORKFLOWS)**的系统设计。这样一来，要么UI被阻塞，要么用户就必须等页面收到响应消息后重新加载。做出这类设计的主要依据往往是为了性能或是为了用统一的方式来处理后端之间的同步和异步通信。但这样做会在开发、测试和运维上所增加不必要的复杂度，远远超过了采用这种统一方式带来的好处。所以，在用户可接受的场景下，直接使用同步HTTP 请求来处理后端服务之间的同步通信，而不必改成事件驱动的设计。如果设计的精妙，使用HTTP通信很少会成为分布式系统的瓶颈。

微服务架构的一个显著特征是系统组件和服务是围绕业务能力进行组织的。无论系统规模大小，微服务都需要将系统功能和信息进行有意义的分组和封装，以便拆分后的微服务能彼此独立地交付业务价值。微服务是从业务角度对架构的重新审视，而以前的服务架构方式会从技术角度组织服务。

## 安全

技术雷达从来没有像这一期有这么多的安全相关的内容。今年的信息安全事件频发，并和技术的发展结合在一起，往往给人们一种“新技术一定会带来安全问题”的错觉。而安全的主要因素是人，工具只是降低工作量和节省工作时间的一种方式，它不能替代安全设计和安全活动本身。我把安全单独列为一节主要是为了能够使您对安全实践有一个端到端的认识。

### 运维相关的安全实践和工具

对敏感数据保持适当的控制是相当困难的，尤其是在出于对数据备份和恢复的目的而将数据复制到主数据系统之外的时候。**密钥粉碎(CRYPTO SHREDDING)**是通过故意覆盖或删除用于保护该数据的加密密钥来使敏感数据无法读取的做法。例如，可以使用随机密钥对数据库中客户个人详细信息表的所有记录进行一对一加密，然后使用另一张表来存储密钥。如果客户行使了“被遗忘的权利”，您可以简单地删除相应的密钥，从而有效地“粉碎”加密数据。当你有信心对小规模加密密钥集合维持适当控制，但对较大数据集的控制信心不足时，此项技术非常有效。

在云计算平台上维护基础设施首要的工作就是设立一个安全的框架，其次需要实践和工具来进行安全检查。

继混沌工程（Chaos Engineering）之后，安全混沌工程(Security Chaos Engineering) 也发展的越来越好，使用此技术的团队确信他们的安全策略足以应对常见的安全故障模式。不过，这方面的实践仅有 [ChaoSlingr](https://github.com/Optum/ChaoSlingr)一个工具，且仅支持 AWS 平台。就像之前提到的 Chaos Engineering Katas，我相信未来会有 Security Chaos Engineering Katas 作为日常安全的练习。

随着云计算平台基础设施即代码的复杂度提升，相应的安全扫描工具也应运而生。[Watchmen](https://github.com/iagcl/watchmen)是个采用 Python 编写的工具，它为由交付团队自主拥有和运营 AWS 账户配置提供基于规则驱动的扫描。技术雷达所提到的 Scout2 已经不再维护，它被迁移到了[ScoutSuite](https://github.com/nccgroup/ScoutSuite)，目前支持 AWS，但即将包括 Azure 和 Google Cloud Platform。我强烈建议你将这些工具集成到你的**基础设施流水线（Pipeline for Infrastructure）**里。

### 开发相关的安全实践和工具

我们已经经历了一些把密码存储到代码库上导致的数据泄露实践。将安全凭据或其他机密提交到源代码仓库是一个主要的攻击向量。[GIT-SECRETS](https://github.com/sobolevn/git-secret) 是防止将密码或其他敏感信息提交到 git 仓库的小工具。[AWS 实验室也提供了一个同名的工具](https://github.com/awslabs/git-secrets)，git-secrets 内建支持常见的 AWS 密钥和凭据，也可以为其他的提供商进行快速配置。

[SNYK](https://snyk.io/)是一个可以查找、修复及监控 npm 、Ruby 、Python 、Scala 、Golang 、.NET 、PHP 、Java 与 Docker 依赖树中漏洞的平台。将 Snyk 加入构建流水线后，它会基于一个托管的漏洞数据库，持续地监控和测试你的库依赖树。在发现漏洞时，还可以给出可以解决该安全问题的最小的依赖版本。目前它支持多种 Git 仓库服务和 PaaS 平台服务。

如果你想对 Web 应用进行安全扫描，你可以采用 [Archery](https://github.com/archerysec/archerysec)，它是一个开源的安全工具，并正在将其与其他工具(包括 Zap )相结合，轻松地将安全工具集成到构建与部署系统中。你也可以通过 Archery 的工作面板，跟踪漏洞及应用程序和网络的安全扫描结果。

同样，随着微服务的流行，它的安全问题也被提升到了最高的高度。[SPIFFE (Secure Production Identity Framework For Everyone， 适用于所有人的安全生产身份框架)](https://spiffe.io/)以特制X.509证书的形式为现代生产环境中的每个工作负载提供安全标识。 SPIFFE消除了对应用程序级身份验证和复杂网络级ACL配置的需求，Istio 默认就采用了 SPIFFE。

## 参考

[https://www.thoughtworks.com/cn/radar/](https://www.thoughtworks.com/cn/radar/)

[https://cloudplatformonline.com/2018-state-of-devops.html](https://cloudplatformonline.com/2018-state-of-devops.html)

[https://puppet.com/resources/whitepaper/state-of-devops-report](https://puppet.com/resources/whitepaper/state-of-devops-report)
