---
title: 从技术雷达看 DevOps 的十年——容器技术与微服务
date: 2019-07-11
tags: 
 - DevOps
 - 技术雷达
 - 微服务
 - Docker
 - Kubernetes
---

> 本文原文发表于 2019 年 7 月 11 日的 [ThoughtWorks 洞见](https://insights.thoughtworks.cn/container-technology-and-micro-services/)，后经过修改发表到博客上。

在上一篇文章中，我们讲到了基础设施即代码和云计算给运维领域带来的深远影响。而 DevOps 运动不仅仅改变了运维端，同时也改变了开发端，特别是 Docker 的兴起和微服务架构的流行。在这一篇，我们将通过技术雷达上相关条目的变化来考察 Docker 和微服务的发展。

## 容器技术

在 Docker 技术出现之前，可以说是 DevOps 技术的 1.0 的时代，人们关注如何做好 CI/CD 和基础设施即代码。而 Docker 的出现迎来了 DevOps 2.0 时代，DevOps 所有的实践都围绕着 Docker 展开，以 Docker 为中心的技术架构影响了软件开发交付的方方面面。无论是开发还是运维都在讨论和使用 Docker。它们采用统一的交付格式和技术语言在讨论交付的过程，而不像之前开发只关注“打包前”，运维只关注“打包后”。

技术雷达关注 Linux 容器技术是在 Docker 出现之前，在 2012 年 4 月 的技术雷达上。“Linux 容器” 就出现在了技术雷达上的 “试验” 区域：

> 虚拟容器是一种对 SaaS 和 PaaS 实现特别有吸引力的虚拟化风格。OpenVZ 等 Linux 容器提供了虚拟机的隔离和管理优势, 而不需要通常与通用虚拟化相关的开销。在容器模型中, Guest 操作系统仅限于与 Host 主机操作系统相同, 但这对许多云应用程序来说并不是一个严重的限制。

一年之后，Docker 问世。两年之后，Docker 进入技术雷达。

### 容器技术 1.0："轻量级的 Vagrant？"

在 Docker 出现之前，DevOps 社区就广泛采用 Vagrant 测试 Chef 或者 Puppet 做基础设施即代码。所以，当我第一次看到 Docker 时，就感觉就是一个”轻量级的 Vagrant”。它们的思路几乎一致：

- Vagrant 通过 Ruby 语法的 Vagrantfile 构建一个虚拟机。而 Docker 通过 Dockerfile 构建一个容器。
- Vagrant 通过 package 命令构建一个可复制虚拟机的镜像。而 Docker 通过 build 构建一个镜像。
- Vagrant 通过 upload 将虚拟机镜像上传至 box 分享站点。而 Docker 通过 push 将镜像上传至 image 分享站点。

此外，每一个 Vagrant 命令，你都可以找到一个对应的Docker 命令。

唯一区别在于， Vagrant 是跨平台的，而Docker 只针对 Linux 平台。这样就避免了 HAL（硬件抽象层）带来的麻烦，使得 Docker 在 Linux 服务器上运行更加轻量，启动更加快速和便捷。此外，Docker 的开发语言也使用 GO 而非 Ruby，相对而言前者更加稳定。那时，社区已经构建出来了基于 Vagrant 虚拟机的编排方案，并采用构建虚拟机镜像的方式（Packer）构建生产环境的设施并部署应用，使得开发到生产环境上的差异最小化。

不过，Docker 对 Vagrant 社区的精确定位塑造了它的成功。从 [Vagrant 的镜像站点](https://app.vagrantup.com/boxes/search) 上可以看出，排名靠前的镜像几乎都是 Linux。所以，Docker 从 Vagrant 的市场中找到了 Linux 服务器这一个头部市场，并且采用新的技术解决了这个核心头部用户群的痛点：重和慢。

此外，Docker 又借鉴了 Github 的版本化分享机制和面向对象“继承”的思想，提升了 Docker 镜像的复用性。将基础设施即代码作为“源代码”，镜像作为编译后的类，容器作为运行时的实例，完整的定义了一个应用和运行时的完整生命周期。这样，应用程序就可以基于“自部署应用程序”的思想，将基础设施和应用程序同时发布，大大降低了基础设施的配置和管理复杂度。

这样的交付流程将 DevOps 1.0 时代的的“打包前”和“打包后”的开发-运维生命周期合作转化成了“容器内”和“容器外”的双生命周期合作。

如果将应用程序开发和运维看做是一个应用程序完整的生命周期，那么容器内和容器外的划分就是做了”关注点分离：容器提供了基础设施无关的界面，使得基础设施对开发人员透明，同时使得基础设施独立于应用。而容器外则是标准化、自动化且稳定的操作系统。

这种关注点分离的方式慢慢影响了应用程序的架构思路，促进了微服务技术向容器的发展。

### 容器技术 2.0：编排工具大混战

一个运动繁荣的标志就是有很多人参与并不断涌现很多创新。在 Docker 出现之后，DevOps 在媒体上出现的频率大大上升。从技术雷达就可以看出，在 Docker 出现在技术雷达后， DevOps 迎来了第二个繁荣期。

自从 Docker 在2016年进入技术雷达之后，技术雷达每一期都会有至少一个关于 Doker的新条目。

Docker 的开放确实为 DevOps 的实施制造了很大的想象空间。如果我们把之前的虚拟机编排改成容器编排会怎么样？是不是能够基于容器构建自动水平伸缩？这样是不是就可以节约更多的资源？可以更快的发布应用。

多方都在这个领域中角逐，Docker 在开源圈不断收购工具，将 fig 收购变为 docker-compose，将 Swarm 和 Docker machine 纳入了 docker 全家桶中。Google 将自己的内部的编排方案 Borg 开源成为了 Kubernetes。此外还有基于 Apache Mesos 构建的 Mesosphare 和 Rancher 这样的轻量级竞争对手。

从它们在技术雷达所处的位置，就可以看出其发展趋势，它们都于 2015 年 11 月进入 “评估” 区域。

- Kubernetes 于 2016年 4月 从 “评估” 升入 “试验” 区域，并于 2017 年 11 月正式进入 “采纳” 区域。4 个月后从 CNCF 毕业。
- Rancher 于 2016 年 11 月进入 “试验” 区域后止步于此。
- Mesosphere DCOS 则一直处于 “评估” 区域。

然而，作为 Docker 原生方案的 Docker Swarm 则从未出现在技术雷达上。

### 容器技术 3.0：围绕微服务构建生态

当 Kubernetes 赢得了容器战争之后，所有的容器厂商俯首称臣。各大厂商在保留了自己的容器编排方案后，纷纷宣布对 Kubernetes 的支持，包括 Docker 自己。

观望容器战争的云计算厂商最后来摘取获得经过市场淘汰后的果实。就像我们上篇讲的，云计算厂商也纷纷加入到了 Kubernetes 即服务(Kubernetes As A Service)的角逐中来。

这让 Linux 基金会看到了商机。借着 Kubernetes 的东风，Linux 基金会开始琢磨围绕着 Kubernetes 构建出一个生态。为了避免被单一厂商劫持（Docker 曾经为了挤兑无法收购的竞争对手 ，强推自己的 Swarm 和 Docker EE 也发布了很多其它平台不兼容的版本），Linux 基金会在其旗下组建了 CNCF (云原生计算基金会)。

相较于 Apache 基金会，CNCF 更加专注于开源的容器应用。不过，从商业角度上，它抓住了下游用户和上游云计算供应商的痛点，依仗着对 Kubernetes 的控制，筛选了符合其”下游垄断”策略的开源项目。这样做一方面避免了上游云计算服务厂商在同一领域的竞争，另一方面给于了下游用户更少的选择。这个看似空手套白狼的生意一年能够让 CNCF 基金会进账至少 871 万美元(约合5850 万 人民币)。

如果说容器 1.0 是容器技术的竞争，容器技术 2.0 是编排技术的竞争，3.0 就是容器生态的竞争。CNCF 抓住了微服务这一大卖点。围绕着 Kubernetes 组建了基于 Kubernetes 的微服务生态。

然而这些项目也不负众望，继 Kubernetes 第一个从 CNCF 孵化毕业后，相关其余的开源项目逐个毕业。而这些开源项目在毕业前就出现在了技术雷达上：[Prometheus](https://www.thoughtworks.com/radar/tools/prometheus)、[Istio](https://www.thoughtworks.com/radar/platforms/istio)、[Helm](https://www.thoughtworks.com/radar/tools/helm)、[Jaeger](https://www.thoughtworks.com/radar/tools/jaeger)、[OpenTracing](https://www.thoughtworks.com/radar/platforms/opentracing)，[Rook](https://www.thoughtworks.com/radar/platforms/rook)

开源使得产业从厂商垄断（类似于 微软，IBM，Oracle 这样的大型IT厂商）慢慢过渡到行会垄断（类似 CNCF 这种基金会），说明了这个产业的供给在不断加大。而随着免费的内容越来越多，重复性低质量的内容反而会占据很多时间。这样虽然让开源社区集中了注意力“把一件事情做好”，另一方面，利用对社区的劫持消灭了同期的其它竞争对手。

### Windows 容器

在容器技术的大战中，微软一直是一个独立的存在。眼瞅着 Linux 和虚拟化厂商们干掉了商业 UNIX 厂商。眼看Linux 作为服务器操作系统在不断蚕食 Windows Server的份额。微软也坐不住了，开始加入容器领域。

Windows Server 最为诟病的就是太大太重，对于运行很多单一服务端应用程序和分布式系统而言过于臃肿。于是微软把图形用户界面和 32 位应用的支持以及远程桌面都移除了。

Windows Server 因为没有 Window 了，那还叫 Windows 吗？所以，没有 Window 的 Windows Server 就是就成为了 Microsoft Nano Server 。Microsoft Nano Server 就是微软在服务器操作系统领域上的第一个容器化尝试。 2015 年11月Microsoft Nano Server 和 Kubernetes 等编排工具一起出现在了进入技术雷达的 “评估” 区域。

> 与基于 Linux 的现代云和容器解决方案不同, 即使是 Windows Server Core 也很重。Microsoft 正在做出反应, 并提供了 Nano server 的第一个预览, 这是一个进一步剥离的 Windows Server 版本, 它丢弃了 GUI 堆栈、32位 win32 支持、本地登录和远程桌面支持, 从而产生了大约 400 MB 的磁盘上大小。早期的预览很难使用, 最终的解决方案将仅限于使用 CoreCLR, 但对于有兴趣运行的公司来说。基于网络的解决方案, 纳米服务器绝对值得看看这个阶段。

但作为 Windows Server 的小表弟，出道之初并没有那么顺利。相较于 Linux，Microsoft Nano Server 还是太大了。于是，微软基于 Docker 推出了自己的容器技术，Windows Containers。Windows Containers 出现在了 2017 年11月的技术雷达上：

> 微软正在用 Windows 容器在容器空间中迎头赶上。在编写本报告时, Microsoft 提供了两个 Windows 操作系统映像作为 Docker 容器, 即 Windows Server 2016 Server Core 和 Windows Server 2016 Nano Server。尽管 Windows 容器还有改进的余地, 例如, 减少了较大的镜像大小, 并丰富了生态系统的支持和文档, 但我们的团队已经开始在其他容器一直在工作的情况下使用它们成功, 例如：构建代理（Build Agent）。

容器技术作为一种轻量级的操作系统隔离和应用程序发布手段，带来了很大的便利性。它让我们能够将复杂的内容通过简单的方式封装起来，从而进一步降低复杂性，特别是对大型应用程序的解耦，这就推动了微服务技术的进一步发展。

下面是 Docker 相关条目的发展历程一览图。实线为同一条目变动，虚线为相关不同条目变动：

![容器技术相关条目](/img/post/20190721/techradar-docker.png)

相关条目：[容器安全扫描](https://www.thoughtworks.com/radar/techniques/container-security-scanning)，[Docker](https://www.thoughtworks.com/radar/platforms/docker)，[用 TDD 开发容器](https://www.thoughtworks.com/radar/techniques/tdd-ing-containers)，[Rancher](https://www.thoughtworks.com/radar/platforms/rancher)，[Kubernetes](https://www.thoughtworks.com/radar/platforms/kubernetes)，[Mesosphere DC/OS](https://www.thoughtworks.com/radar/platforms/mesosphere-dcos)，[Apache Mesos](https://www.thoughtworks.com/radar/platforms/apache-mesos)，[Prometheus](https://www.thoughtworks.com/radar/tools/prometheus)、[Istio](https://www.thoughtworks.com/radar/platforms/istio)、[Helm](https://www.thoughtworks.com/radar/tools/helm)、[Jaeger](https://www.thoughtworks.com/radar/tools/jaeger)、[OpenTracing](https://www.thoughtworks.com/radar/platforms/opentracing)，[Rook](https://www.thoughtworks.com/radar/platforms/rook)

### 从演进式架构到微服务

可以说，微服务是 DevOps 所有实践发展的一个必然结果。它不光是一种应用架构，而是包含了多年来敏捷、DevOps、云计算、容器等技术实践的综合应用。

在以 ESB 为基础的大规模企业级应用出现之前，企业级应用软件的开发规模相对较小，大部分都是基于现有软件包产品的二次定制。采用敏捷的方式来交付这些应用是可控的。然而随着 ESB 将企业级应用的信息孤岛集成起来。敏捷软件开发似乎就显得力不从心了。

[演进式架构](https://www.thoughtworks.com/radar/techniques/evolutionary-architecture)在 2010 年第一期技术雷达就被提出来。在敏捷软件开发实践开始应用于大规模应用程序的案例中。”架构”和“变化”出现了矛盾。如何让包含了“不轻易改变的决定”的架构和“拥抱变化”的敏捷共处，于是有了演进式架构：

> 我们帮助我们的许多客户调整企业软件体系结构实践, 以适应敏捷软件交付方法。在过去的一年里, 我们看到人们对进化企业架构以及面向服务的架构如何塑造企业单位之间的界限越来越感兴趣。企业架构的进化方法的价值在于创建重量更轻的系统, 从而简化不同部件之间的集成。通过采用这种方法和将 web 作为企业应用程序平台（Web as Enterprise Platform）的概念, 我们降低了应用程序体系结构的总体复杂性, 提高了质量和可扩展性, 并降低了开发成本。

2010 年 8 月演进式架构进入了”试验”区域，但在2011年1月的技术雷达上更新了对它的评价：

> 敏捷软件开发的一个原则是”最后责任时刻”的概念。这一概念适用于架构设计, 它在传统架构师中引起了争议。我们相信, 只要有适当阐述的原则和适当的测试套件, 架构就可以不断发展, 以满足系统不断变化的需求, 从而在不影响完整性的情况下, 在最后一个负责任的时刻做出体系结构决策系统的。我们将这种方法称为进化体系结构, 因为我们允许体系结构随着时间的推移而演变, 始终尊重体系结构的指导原则。

半年后，2011年6月，演进式架构进入了”采用”区域，技术雷达再次更新了评价：

> 与传统的前期、重量级企业架构设计不同, 我们建议采用演进式架构。它提供了企业架构的好处, 而没有尝试准确预测未来所造成的问题。演进式架构不应该猜测组件将如何重用, 而是支持适应性, 使用适当的抽象、数据库迁移、测试套件、持续集成和重构来获取系统中发生的重用。应尽早确定系统的驱动技术要求, 以确保在后续设计和实现中正确处理这些要求。我们主张将决定推迟到”最后责任时刻”, 这实际上可能是一些决定的先行。

在这些概念不断变化的过程中，不断有方法论、实践和工具被提出。在演进式架构的思想影响下，诞生了新的实践 —— 微服务。微服务的出现，让演进式架构有了第一个实例化的例子。

### 微服务 1.0：轻量级 SOA

在技术雷达里，微服务是以”Micro-services”而非”Microservices”出现的。在技术雷达的角度中，微服务仍然是 SOA 的一种轻量化的实现方式。在 2012 年 3月的技术雷达中，微服务首先出现在了技术雷达的“评估”区域：

> 微服务通常是脱离应用容器部署或使用嵌入式 HTTP 服务器部署, 它是对传统的大型技术服务的一种迁移。这种方法通过增加运维复杂性而提升系统的可维护性。这些缺点通常使用基础设施自动化和持续部署技术来解决。总的来说, 微服务是管理技术债务和处理不同伸缩特征的有效方法, 尤其是在围绕业务能力构建的面向服务的体系结构中部署时。

**这里需要划几个重点：**

1. 微服务脱离应用容器部署或者使用嵌入式 HTTP 服务器。这一年，Docker 还没有出现。这里的容器指的是 WebSphere，WebLogic 这样的容器。嵌入式 HTTP 服务器指的是 Jetty、Tomcat 或者 DropWizard 这样的轻量级选择。这样代码库可以自部署，而不是通过应用容器部署。
2. 微服务是一种内部复杂度向外部的转化：通过把应用隔离到不同的进程中，可以缩小变更的影响范围。通过将内部复杂性转化成外部复杂性从而使应用更易维护。而外部复杂性就交给自动化的基础设施管理。
3. 微服务提升了维护的复杂性和难度。如果没有 DevOps 组织，服务之间的 应用的风险就由开发转嫁给了维护。不过，作为Ops 可以通过自动化和持续部署/蓝绿发布来解决。
4. 微服务便于管理技术债务，可以做到部分的按需伸缩。
5. 微服务是围绕业务能力的 SOA 架构。

总的来说，微服务在那个时期就是采用轻量级技术来围绕业务实施 SOA。然而，这样的实践慢慢的形成了一种成熟的模式，并慢慢推广开来。在2012年10月的技术雷达，微服务就进入了”试验”区域，而到了 2014 年 1 月。技术雷达更新了对微服务的描述：

> 我们看到, 无论是在 ThoughtWorks 还是在更广泛的社区, 微服务作为分布式系统设计技术的采用都在上升。DropWizard 程序等框架和声明性初始化等实践表明技术和工具的成熟。避免采用通常的单体应用办法，微服务更倾向于在必要的情况下替换而非修改局部应用系统。这对应用系统的总体成本具有重要的积极影响。我们认为, 这会在中长期有着巨大的影响, 特别是大部分应用的重写周期都在 2 – 5 年。

随着 DropWizard 开始在 Java 用户群展露头角，各个其它语言社区也出现了自己的轻量级 API 框架。Ruby 社区率先出现 了 Sinatra 框架，它的轻量级语法深刻的影响了未来各语言的微服务框架。例如而 .Net 社区中出现了Nancy。Python 社区出现了 Flask 。

### 微服务 2.0：结合基础设施的全面架构设计

单一的轻量级服务端框架并不能端到端的解决服务消费者和服务提供者的所有问题。随着应用慢慢的开始被拆分成了微服务，基础设施的管理变成了一个新的问题。在分布式系统环境下，基础设施的范围要比虚拟机时代广泛的多。复杂的基础设施和即代码的集中式管理成为了另一个“单体”应用。于是有了前文介绍的去中心化的 Chef 和 Puppet 实践。让基础设施代码作为应用代码库的一个部分，这样，就可以构建出一个“自部署”的应用。

这样的想法推动了 Ansible 和 Vagrant 的流行，并伴随着持续交付的实践。我们可以通过构建可执行的虚拟机镜像将应用切分成不同的虚拟机来运行。在那个时期，一个大型应用能够被拆分到多个虚拟机中自动化管理已经很先进了。

然而，Docker 的出现，将这一系列最佳实践固化成了一个完成的应用程序生命周期：开发人员通过构建 Docker 镜像在本地开发，然后通过持续交付流水线构建成版本化镜像。容器平台按需拉取镜像并直接运行，从开发环境到生产环境几乎没有差别。运维平台只要能够通过虚拟化资源使容器能够轻易的运行，就打通了端到端的最短距离。

正如上文所述“容器内”和“容器外”被清晰的隔离开，无论从组织上还是架构上，都适应了这套模型。此外，基础设施的关注点分离变成了两个部分：应用程序的运行时管理和应用间的通信。

刚开始的时候，Docker 看起来更像是一个“轻量级的虚拟机”——我们通过镜像构建出一个运行实体。但随着应用程序的责任分离，Docker 就更像是一个“重量级的进程”。我们如果把容器按责任分离，就可以把容器看做是一个个通过 API 暴露的资源。这样，我们就可以采用云计算的资源编排的方式来处理应用之间的问题。恰逢 Docker 的容器间网络和编排工具的成熟，使我们有了更多的容器编排方案可以选择。

刚开始的时候，微服务之间还是简单的 HTTP 调用。我们可以通过 Nginx 作为 API 网关。随着服务变得复杂，对于 API 网关的要求就越来越多，于是就有了单一的 API 网关方案，简化了 API 管理。

如何让网关知道每个服务的情况呢？一方面，API 网关需要知道服务的存活情况。另一方面，服务自身要能够主动汇报自身的状态，于是 [Consul](https://www.thoughtworks.com/radar/tools/consul) 这样的服务注册发现解决方案就逐渐流行起来。

同时，日志收集和监控要集成到每个服务中去，从管理的角度也要能聚合所有的日志和监控，于是有了[OpenTracing](https://www.thoughtworks.com/radar/platforms/opentracing) 这样的解决方案。

随着微服务架构体系越来越复杂，这些零散的工具和应用开发框架的集成变成了新的问题。这样的问题最早出现在 Java 社区 —— 因为大部分大型应用仍然是基于 Java EE 的。于是 Spring 推出了[Spring Cloud](https://www.thoughtworks.com/radar/languages-and-frameworks/spring-cloud) —— 坊间称之为 Spring 微服务全家桶，它包含了所有微服务端到端的组件。虽然Spring Boot 出现的比较晚，但凭借着 Spring 在 Java 社区的号召力使其迅速超过 DropWizard，Jersey 等方案脱颖而出。成为了目前 Java 社区的 微服务构建首选。

然而，部署实例里仍然存在着安全、监控、日志收集这样的基础设施功能，就出现了”[野心过大的 API 网关](https://www.thoughtworks.com/radar/platforms/overambitious-api-gateways)“。这个问题出现在了 2015 年11 月份的技术雷达上：

> 我们常见的抱怨之一是将业务智能推入中间件, 从而产生了具有运行关键应用程序逻辑雄心的应用程序服务器和企业服务总线。这些都需要在不适合这一目的的环境中进行复杂的编程。我们看到这种疾病的重新出现令人担忧, 因为 API 网关产品常常野心过大。API 网关可以在处理一些一般问题 (例如, 身份验证和速率限制) 时提供实用程序, 但任何域智能 (如数据转换或规则处理) 都应驻留在应用程序或服务中, 这些应用程序或服务可以由与他们支持的领域密切合作的产品团队。

不光 API 会出现这样的问题。替代传统消息队列的 Kafka 也会面临同样的问题，虽然用了新技术，但貌似又回到了集中化的老路上去。这些都违背了微服务的”自治性原则”。

于是，就有人想，能不能通过容器技术，将代码无关的一类安全、反向代理、日志等拆散到各个服务实体上去。在单个服务的内部实现关注点分离——业务代码和非业务组件隔离。比如，采用[边车模式处理端点的安全](https://www.thoughtworks.com/radar/techniques/sidecars-for-endpoint-security)。这样的方式十分有效的化解了集中服务组件的负载和依赖。于是这个模式就复制扩大，变成了[服务网格(Service Mesh)](https://www.thoughtworks.com/radar/techniques/service-mesh)。服务网格出现在 2017 年底的技术雷达上：

> 随着大型组织过渡到拥有和运营自己微服务的自主团队, 它们如何在不依赖集中式托管基础结构的情况下确保这些服务之间必要的一致性和兼容性？为了高效地协同工作, 即使是自主的微服务也需要与某些组织标准保持一致。服务网格提供一致的发现、安全性、跟踪、监视和故障处理, 而不需要共享资产 (如 API 网关或 ESB)。典型的实现涉及在每个服务进程旁边部署的轻量级反向代理进程, 可能是在一个单独的容器中。这些代理与服务注册表、标识提供程序、日志聚合器等进行通信。服务互操作性和可观测性是通过此代理的共享实现获得的, 而不是通过共享运行时实例获得的。一段时间以来, 我们一直主张采用分散的微服务管理方法, 并很高兴看到这种一致的模式出现。诸如 linkerd 和 Istio 这样的开源项目将继续成熟, 使服务网格更易于实现。

时下服务网格成为了微服务架构的热门，但这种模式很明显增大了网络上的开销，但分摊了服务治理的压力。相对于微服务复杂性而言，这些开销在某种程度上是可以接受的。

### 微服务 3.0：无服务器的微服务架构

从微服务技术的发展历程来看，微服务技术的发展是不断的把业务代码和微服务运行时逐渐剥离的一个过程：让尽可能多的不经常变更的部分沉淀到基础设施里，并通过基础设施即代码管理起来。

从 DevOps 的角度来看，应用程序在分离业务代码和基础设施的过程中清晰界定了开发和运维之间的职责。开发团队要负责应用程序的业务代码能够跟随业务的变化而演进。而运维团队就要为开发团队提供尽可能透明和可靠的基础设施支持。

一言以蔽之：开发工程师除了写业务代码，什么都不需要管。

早在 服务网格之前，[后端应用即服务(Backend as service)](https://www.thoughtworks.com/radar/platforms/backend-as-a-service)就已经进入2014年的技术雷达。彼时还是移动端应用爆发的时候。开发人员可以通过这种方式专注于客户端的开发。而到 AWS 推出了 [AWS Lambda](https://www.thoughtworks.com/radar/platforms/aws-lambda) 和 [Amazon APIGateway](https://www.thoughtworks.com/radar/platforms/amazon-api-gateway) 后，函数即服务(Function as a service)的理念则标志了[无服务器应用架构（Serverless Architecture)](https://www.thoughtworks.com/radar/techniques/serverless-architecture)的到来。

Serverless 的架构把应用程序的理念推向了一个新的极致。以前的应用程序是需要考虑基础设施状态的：CPU/内存/磁盘是否足够，带宽是否足够，网络是否可靠。而在 Serverless 应用程序的世界里，基础设施层已经解决上述所有的问题，给开发者一个真正无限制的基础设施空间。

开发者只要考虑的就是设计好各资源之间的事件处理关系，而所有的资源都是通过高可用的基础设施承载。

在 UNIX 的世界里，一切皆文件。而在 Serverless 应用的世界里，一切皆 API。在 UNIX 的世界里，我们消费流(Stream)，应用程序是对流的处理。而在 Serverless 应用的世界里，我们消费事件(Event)，应用程序是对事件的处理。

这种思想特别适合基础设施逐渐复杂的微服务，使得微服务的实施更加的轻便。但这也带来了编程模型的转变：函数式编程和面向资源计算渐渐流行了起来。

从基础设施的角度来看，微服务经历了三代技术：

**第一代微服务**是基于虚拟机和物理机的基础设施，将一个难以敏捷交付的大型应用程序通过轻量级分布式系统敏捷化。为了提升可用性，我们要拆分应用的状态以支持水平扩展。

**第二代微服务**是基于容器的基础设施，我们通过容器镜像分离了应用程序运行时状态。

**第三代微服务**是基于云的”运行时即服务(Runtime as a Service)”的能力，将基础设施和应用程序的所有状态都存储在了云计算平台的高可用资源中。而应用程序本身则作为云计算资源的配置被版本化管理起来。

这样的思想影响也影响了容器社区，于是基于 Kubernetes 的 [KNative](https://www.thoughtworks.com/radar/platforms/knative) 被开发了出来。企业级应用的理念和互联网级应用的理念越来越接近。

### 应用微服务的组织问题

从上述的历史可以看到，微服务是一系列技术和理念不断革新的结果。而微服务这个词掩盖了太多的细节。

相较于技术和工具的不断发展，采用微服务的组织演进则缓慢的多。一方面是因为在大多数企业中，IT部门仍然不是核心部门，只是所有部门中的“二等公民”。另一方面是康威定律的生效时间会比较长。

特别是一些成功企业的“微服务”分享，使得那些拥有”落后”应用架构的组织开始嫉妒那些有微服务应用架构的组织。于是，就出现了”[微服务嫉妒](https://www.thoughtworks.com/radar/techniques/microservice-envy)“的问题，它出现于 2015 年 11月的技术雷达：

> 我们仍然相信, 微服务可以为组织提供显著优势, 提高团队自主权和加快变革频率。分布式系统带来的额外复杂性需要额外的成熟度和投资水平。我们感到关切的是, 一些团队在不了解开发、测试和操作的变化的情况下, 纷纷采用微服务。我们的一般建议仍然很简单。避免“微服务嫉妒”, 在匆忙开发更多服务之前, 先从一两个服务开始, 让你的团队有时间调整和理解合适的粒度水平。

强烈的攀比心态造成了微服务”大跃进”的风潮，这股风潮一直持续到现在。虽然采用的开发技术提升了，然而组织却欠缺基础的能力，使微服务的改造带来了新的问题：

> 在现代基于云的系统中, 微服务已经成为一种领先的架构技术, 但我们仍然认为团队在做出这一选择时应该谨慎行事。微服务嫉妒诱惑团队通过拥有大量的服务来使他们的体系结构复杂化, 仅仅因为它是一种时尚的架构选择。Kubernetes 等平台使部署复杂的微服务集变得容易得多, 供应商正在推动他们的解决方案来管理微服务, 这可能会使团队进一步走上这条道路。重要的是要记住, 微服务贸易发展的复杂性是运维的复杂性, 需要一个坚实的基础，例如 自动化测试, 持续交付和 DevOps 文化。

这就是我经常说的：”眼光到位了，实力没跟上”。

微服务是一系列基础能力成熟后的必然结果。如果你要在短期内跨越这个阶段，希望采用微服务架构来牵引组织能力的成长，就一定要有心理准备。你可以通过采购技术解决方案的方式一次性解决 3-5 年微服务实施中的技术问题。但组织中碰到的问题则没有容易通过采购技术方案来消化。所以，在微服务的实施过程中，要警惕康威定律的作用，并且尽快让组织里形成 DevOps 的文化。

除此之外，很多架构师还一直停留在早期的分层架构思考，造成了”[分层的微服务架构](https://www.thoughtworks.com/radar/techniques/layered-microservices-architecture)“：

> 微服务体系结构的一个决定性特征是系统组件和服务是围绕业务功能组织的。无论规模大小, 微服务都封装了有意义的功能和信息分组, 以独立交付业务价值。这与早期服务体系结构中根据技术特征组织服务的方法形成鲜明对比。我们观察到一些组织采用了分层微服务体系结构, 这在某些方面是矛盾的。这些组织已回到主要根据技术角色安排服务, 例如, 体验 Api、进程 Api 或系统 Api。技术团队很容易按层分配, 因此交付任何有价值的业务变化都需要多个团队之间缓慢而代价高昂的协调。我们注意这种分层的影响, 并建议主要根据业务能力安排服务和团队。

因此，架构师需要掌握新的技能，特别是领域驱动设计(Domain-Driven-Design，DDD)以及端口-适配器模式，采用六边形架构来描述微服务架构，就会使你对整个架构的理解更加清晰。

除了开发、基础设施、架构问题以外。微服务的测试是一个更大的问题。微服务虽然从架构上解耦了应用程序的复杂度，让更少的功能隔离进了更小的发布单元中。这样可以缩小单个部署单元的测试范围，但这无法保证整体的正确性。应用程序并不是一个线性系统，能够通过部分的正确性加总得到整体的正确性。应用程序是一个复杂适应性系统，我们通过简单的组件之间的组合只会使之更加复杂。

当我我们将复杂性通过技术设施移到了部署单元之外后，就会有更多的集成，因此集成测试的数量会立刻膨胀。如果你是一个前后端分离的团队而不是一个围绕业务的全功能团队，你就需要”[消费者驱动的契约测试](https://www.thoughtworks.com/radar/techniques/consumer-driven-contract-testing)“来做组织间的协作。

下面是微服务相关条目的发展历程一览图。实线为同一条目变动，虚线为相关不同条目变动：

![微服务技术相关条目](/img/post/20190721/techradar-microservices.png)

相关条目：[演进式架构](https://www.thoughtworks.com/radar/techniques/evolutionary-architecture)，[Nancy](https://www.thoughtworks.com/radar/languages-and-frameworks/nancy)，[Consul](https://www.thoughtworks.com/radar/tools/consul)，[OpenTracing](https://www.thoughtworks.com/radar/platforms/opentracing) ，[Spring Cloud](https://www.thoughtworks.com/radar/languages-and-frameworks/spring-cloud) ，[野心过大的 API 网关](https://www.thoughtworks.com/radar/platforms/overambitious-api-gateways)，[边车模式处理端点的安全](https://www.thoughtworks.com/radar/techniques/sidecars-for-endpoint-security)，[服务网格(Service Mesh)](https://www.thoughtworks.com/radar/techniques/service-mesh)，[后端应用即服务(Backend as service)](https://www.thoughtworks.com/radar/platforms/backend-as-a-service)，[AWS Lambda](https://www.thoughtworks.com/radar/platforms/aws-lambda)， [Amazon APIGateway](https://www.thoughtworks.com/radar/platforms/amazon-api-gateway) ，[无服务器应用架构（Serverless Architecture)](https://www.thoughtworks.com/radar/techniques/serverless-architecture)，[KNative](https://www.thoughtworks.com/radar/platforms/knative)，[分层的微服务架构](https://www.thoughtworks.com/radar/techniques/layered-microservices-architecture)，[消费者驱动的契约测试](https://www.thoughtworks.com/radar/techniques/consumer-driven-contract-testing)，[微服务嫉妒](https://www.thoughtworks.com/radar/techniques/microservice-envy)