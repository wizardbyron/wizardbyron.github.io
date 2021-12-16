---
title: 公有云(AWS)上的生产环境架构优化案例和迁移套路总结
date: 2018-08-08
categories: 
  - DevOps
tags:
  - 停机时间
  - 性能
  - AWS
  - wade
  - 流量测试
---

本文是我在 gitchat 上的文章[云计算生产环境架构性能调优和迁移套路总结（以 AWS 为例）](https://gitbook.cn/books/5b5d6f054f88ac0f2df54fdd/index.html)的后半部分，本文对原文有所修改和总结。交流实录请[点击这里](https://gitbook.cn/books/5b5d6f054f88ac0f2df54fdd/index.html)。

在[AWS 上的生产环境性能分析案例](/posts/2018-08-07-performance-analysis-case-study)一文中，记录了我对客户应用生产环境的一次性能分析。接下来，我们要根据所发现的性能问题进行架构优化，以提升可用性和性能。同时，这篇文章也总结了应用迁移到云上的套路。

## 设计云计算平台迁移计划和方案

将应用程序迁移到云计算平台上主要的目的是把自行构建的高风险高成本应用以及组件替换为云计算平台上的高可靠性低成本组件/服务。

应用架构的迁移有两种方案：

一种是**整体一次性迁移**，即重新实现一个架构并完成部署，然后通过金丝雀发布或者蓝绿发布切换。这种方式的好处是简单，直接，有效，一开始就能按照最佳实践构建应用架构。而且对于现有系统来说影响不大。但如果方案没设计好，容易造成高级别的风险，所以应当进行大量的测试以确保可靠性。

另一种是**持续部分迁移**，每次引入一点风险，保证风险可控，但缺点就是优化步骤较多。虽然持续部分迁移步骤多，但是总体时间并不一定会比整体迁移更高。

**注意：**由于自动化基础设施和架构设计会带来一些副作用，特别是配置间的耦合。因此，对于生产环境的直接优化要慎用自动化。如果一定要用，请务必在测试环境上做好测试。但如果你能做到自动化并且有完好的测试，不如直接做整体一次性迁移方案得了。

一般说来，一个完整的云平台迁移方案会分为以下三大阶段：

**第一阶段：构建高可用架构以实施水平扩展，从而保证了应用的稳定运行**。

**第二阶段：引入 APM 并根据 APM 数据进行定向优化，采用云计算的服务来优化应用的资源使用**。

**第三阶段：构建应用端的持续部署，构建 DevOps 的工作模式**。

这三个阶段是大的顺序，而每个大的阶段里又会相互掺杂一些其它阶段的内容。**但无论什么样的迁移方案，一定要通过度量进行风险/收益比排序，最先完成代价最小，收益最大的内容。**

## 第一阶段：构建高可用架构

我们之前说过，一个应用架构的第一追求就是业务的连续性和抗风险能力。一个高可用的架构能够在你的应用面对压力的时候从容不迫。因为如果资源满负荷运转，新的请求会因为没有可用资源而导致排队。这是常见的停机或者性能降低的原因。这就是 AFK 扩展矩阵常说的 X 轴扩展：通过复制自己扩展资源从而达到降低排队等待的时间。此外，水平扩展出来的机器同样也是一个预留资源，能够提高应用的可用性。应用架构不仅仅是应用程序的事情，也包含着资源的分配，二者是相辅相成的。

一般会经历如下几步：

* 第一步，有状态和无状态分离
* 第二步，牲畜化（Cattlize）应用实例
* 第三步，自动化水平扩展（AutoScaling）

### 第一步：有状态和无状态分离

先回顾一下当前应用的架构 ：
![当前应用架构](/img/post/20180808/cloud-0.svg)

状态分离的目标是把有状态的组件和无状态的组件分开，以便在做复制的时候降低不一致性。最简单的判定办法是：如果复制当前的虚拟资源，并通过负载均衡随机分配请求访问，哪些部分会造成不一致。

常见的有状态内容比如数据库，上传的文件。所以，我们要把它们独立出来。在“萨瓦迪卡”的例子中，我们首先把数据库独立了出来。如下图所示：

![数据库分离](/img/post/20180808/cloud-1.svg)

在这个过程中，我们采用 RDS 而不是另外一个 EC2 上构建一套 MySQL 来完成数据库的分离。最主要的原因就是 RDS 提供了更好的可用性和数据库维护支持，例如自动备份，更多的监控指标，更自动的数据库迁移和维护窗口等。我们采用 Aurora 引擎的 MySQL 模式，这可以将数据库做成一个集群并让另外一个只读分片，降低数据库的负担。

在分离数据库的时候，要注意以下几点：

1. 数据库分离的性能基线就是在同样的负载测试下，不能够比没分离之前更差。
2. 数据库的网络建立在一个私有的子网中，除了应用子网内的 IP 不能访问数据库，从而提高安全性。
3. 构建一个私有域名来访问数据库，这样可以固定应用的内部配置，减少对配置的修改。同时也给外部切换数据库主备等留下了更灵活的空间。
4. 注意对原有数据库 MySQL 配置信息的复制，这会导致很大程度上的性能差异。
5. 对于数据较大的数据库启动而言，会有一个几分钟的热身（Warm up）时间，这会导致性能下降。所以，做切换的时候提前启动数据库以做好准备。
6. 不要用默认的 root 账户作为应用的访问账户。
7. 由于 RDS 可以在不影响数据完整性和一致性的情况下降低使用配置，在最开始的时候采用较高的配置。随着优化的不断进行，可以采用维护时间窗口（Maintenance Time Window）在低流量时段对 RDS 实例的配置进行降级，以节约成本。

完成了数据库的隔离，我们就可以依法炮制文件的隔离了。最简单有效的方案是把文件存储在对象存储服务中。AWS S3 就是这样一种服务。避免自己构建共享文件系统或者共享存储设备。

文件相较于数据库来说，占用的内存资源和 CPU 资源较少，大部分的处理为 IO 处理，只要网络和设备的 IOPS 足够。一般不会出现大的问题。

为了降低文件隔离带来的问题，在迁移文件的时候尽量保证文件目录结构不变，只改变文件访问根（root）的位置。对于文件来说，可以通过多种方式：

1. 如果有对应的文件存储位置修改功能，可以通过修改全局文件存储位置实现。
2. 如果有反向代理，可以通过修改反向代理的配置来通过重定向实现。
3. 对时间敏感的文件读写，可以根据日期和时间建立文件夹。
4. 如果有七层的负载均衡或者 CDN 可以通过路径匹配来实现、

在“萨瓦迪卡”的例子里，我们通过 CDN 来实现了文件的隔离。将文件存储在 AWS S3 上，并且用 CloudFront 作为 CDN。用路径匹配的形式让请求通过访问 S3 而不是虚拟机实例来降低虚拟机的 IO 请求，再加上 CDN 的缓存，这就可以大大减少虚拟机实例的负担，也提升了用户的体验。最终的架构如下图所示：

![有状态部分的整体分离](/img/post/20180808/cloud-2.svg)

在采用 CDN 的时候请注意以下几点：

1. 最开始的时候取消默认缓存设置。因为对于未知的应用来说，各个访问点的内容更新频率并不清楚。这个阶段主要是为了收集应用的访问数据。
2. 灵活利用缓存的**过期时间(Expire time)**和**强制过期(Invalidate)**功能，来控制新旧内容的读写。
3. 注意 DNS 的 TTL 时间，并可以通过设置多级域名和 Failover 功能进行 0 停机切换或者蓝绿部署。例如当前总入口域名直接访问 ELB，可以增加一个 Failover 备份访问点访问 CDN，然后通过 CDN 访问 ELB。如果没有特别的 WAF 配置。
4. 出问题了多检查 HTTP 请求头和响应头的信息，一般都内藏玄机。

完成了应用的状态隔离，我们就可以开始进行水平扩展了。

### 第二步：牲畜化（Cattlize）应用实例

在“萨瓦迪卡”的例子里，它的整个架构就是一个宠物式（Pets）的架构：独一无二不可复制。但是带来的问题就是当宠物式架构出了问题之后，没有相对应的替代方案。而牲畜式（Cattles）的架构，就是可以进行复制的容错架构，其中任何一个出问题了，都有相应的备胎（alternatives），正所谓“有备无患”。

所以，可以认为，高可用架构的本质就是把宠物变成牲畜的问题。

如果你的应用是以函数式的方式进行编写的，那么它本身就自带水平扩展功能。函数本身是没有状态的，它只是对数据的加工。这样的应用仅仅是把用户手上的数据，经过一系列的转化，存储在了服务端。

如果你的应用不是以函数式的方式进行编写的，你也不想修改应用，除了做状态隔离以外，你需要将应用程序实例转变为可复制的模式：

首先，你最好有一个备份的网络可用域。可以理解为两个机房，当一个机房出问题了，你还有另外一个机房。

其次，你要通过虚拟机镜像来对应用实例进行复制。

最后，你要采取蓝绿部署或者金丝雀发布的形式来控制用户的访问以达到0停机的目的。

所以，我们在“萨瓦迪卡”上做了如下的规划：

1. 构建另外一个可用区的网络。
2. 通过虚拟机镜像复制虚拟机实例。
3. 通过负载均衡来分配应用的访问。
4. 通过 RDS 集群节点做统一的访问入口，负载均衡和高可用由 RDS 自己管理。

于是，我们就形成了如下图所示的最终方案：

![最终架构](/img/post/20180808/cloud-final.svg)

特别需要注意的是，在构建虚拟机镜像的时候，你需要对虚拟机的操作系统进行升级并安装 APM 代理程序（APM agent），在升级的时候，为了避免不必要的停机时间，我们采用了如下流程：

1. 构建一个当前虚拟机的镜像。
2. 采用新镜像启动一个虚拟机实例，这个实例的配置需要和现有虚拟机实例一致。
3. 新的虚拟机实例启动后并不加入到负载均衡里。
4. 在新启动的虚拟机实例一台上进行更新和升级。
5. 把升级后的虚拟机加到负载均衡里。
6. 检查新加入负载均衡的虚拟机正常工作后，在线升级老的虚拟机。
7. 完成之后，构建新的虚拟机镜像，并作为可复制镜像。

完成了以上的步骤之后，我们就不需要晚上在低访问量的时候进行操作了，白天可以通过创建新的虚拟机实例来完成相应的测试，并通过移入移出负载均衡的方式进行发布。

接下来，就要让这个架构可自动化伸缩了。

### 第三步，自动化水平扩展（AutoScaling）

当我们完成了前面两步，可以基本认为满足了高可用的条件。但是，由于是静态的人为操作，仍然需要人工值守来解决突发状况，这显然不是一个长久之计，我们要使架构可以处理突发状况，这也是云计算平台的优势所在。

**首先，我们需要规划冗余资源**。

**冗余值**是为了应对超过过去峰值的资源使用率，而设计的容量，它是最大值减去**保留使用率**（Reserve Utilization）所剩下的值。以我的经验，在没有特别事件出现的情况下。**保留使用率**一般取**均值的 3 倍**，或者**峰值的 2 倍** 中较高的那个值。举个例子：如果我的内存使用平均值在 2 GiB，峰值在 4 GiB。那么我的**保留使用率**是 8 GiB。

冗余值的目的不是为了应对突发状况，而是给突发状况保留一些相应时间。当应用有趋于不正常的趋势的时候，我们可以由足够的时间来为下一个特殊阶段进行处理。

**然后，构造监控告警**。

我们也可以用以上几个值来设置资源监控告警来通知我们，告警方案一般为“两线三区”：两线分别为告警线和人工干预线，三区分别为：绿区（正常），黄线（警告），红线（严重）。而每个线的设计方法也不同，一般有以下几种：

1. 按照最大资源的 60% 和 80% 设计告警线和人工干预线。60%以下为绿区，60%-80% 为黄区，80% 以上为红区。剩下的为冗余。
2. 按照边际值的增幅的平方和立方设计告警线和人工干预线。边际值平方以下增速为绿区，边际值立方以下，平方以上为黄区，边际值立方以上为红区。
3. 按照资源使用**均值的 3 倍**，或者**峰值的 2 倍**的较低值和较高值设计告警线和人工干预线。

在“萨瓦迪卡”里，我们采用了第一种方式进行了设置。因为这个应用并不会有突发的访问状况，所以我们采用了均值。

**最后，制定和测试自动伸缩策略**。

有了以上的数据之后，我们就可以制定自动伸缩策略了。一般是在监控处于“黄区”的时候开始出发自动伸缩策略。而由于自动伸缩会有一定的“热身时间”（Warm-up Time），这个时间如果资源被用完，就会导致宕机。所以，我们需要更快的响应。因此，制定自动伸缩策略的时候要采用“**快增慢减**”原则：即以两倍到三倍的速度增加以满足资源消耗，并以但倍速的方式进行减少，不怕浪费，就怕影响用户感知。

**此外，请一定要通过前面所讲的性能测试方案来测试自动伸缩策略，以确保策略是可用的**。我以前碰到过一个例子：客户想当然的制定了自动伸缩策略，但从未测试过。导致了一次自动伸缩失效而引起的停机。

这个时候，应用迁移到云上的第一步工作就完成了。我们通过使用云计算平台的可靠性特性，首先先保证了应用的稳定运行。接下来，我们要用云计算平台的优势来逐步优化云平台上的应用。

## 第二阶段：引入 APM 并根据 APM 数据进行定向优化

对于一个黑盒应用，我们需要了解应用的内部性能状况，除了自己编写相应的代码以外，就是用 APM 平台了。APM 平台往往会提供一个低侵入的方案来获取应用和操作系统的性能数据。一般会采用代理（Agent）的形式运行，并且通过网络对外传输数据，某种意义上说这是一种不安全的方式，但现代大多数  APM 工具都提供了加密的方式来传输和压缩数据。NewRelic 就是这个行业的佼佼者，它不光提供了低入侵的方案，还提供了更多的分析界面来帮助我们找到应用的性能问题。效果如下所示：

![NewRelic APM](/img/post/20180808/newrelic.png)

在“萨瓦迪卡”里，我们就用了 NewRelic 来作为 APM 方案，它帮我们发现并度量了很多问题，例如缓慢的查询，低性能的插件，不稳定的资源使用等。无论是应用本身还是架构上的问题，以指导我们更好的进行性能调优，并通过数据的对比来判断效果。此外，我们可以结合 CDN 的统计数据来看哪些 URL 和资源最常被访问，从而制定出更有效的性能优化手段。

而一般的性能优化，会采用以下四种基本的方式。**但无论是哪一作用方式，一定要根据业务数据来设计缓存，要了解对应访问点的数据更新频率和性能要求。**

### 增加缓存

缓存往往是提升性能的第一选择，主要原理是采用少量速度更高且较贵的资源替代部分速度较慢的资源，形成“短路访问”：本来需要经过四个环节才能获取的数据通过两个环节就可以获取到了。而缓存一般是根据 LRU 算法（Least Recently Used，即最近最久未使用）来实现的。

CDN 可以被看做是一种缓存，它通过网络延迟和路由帮用户找到访问更加快速的边缘服务器来加速。边缘服务器上往往根据 LRU 算法存储了 源服务器（Origin Server）的一部分拷贝。

另外一种就是内存数据库或者 Key-Value 存储，例如 Redis 或者 Memory Cache 这种方案是把数据通过一定的格式索引（最简单的方式就是 HashMap）并存储到内存里来替代访问。然而，这些服务的能力有限，并不能提供太多的复杂的操作。

### 动静分离

由于 Web 应用大多是读写，而不同的设备和内容的访问速度是不同的。对于低写入，高读取的资源。我们可以把它静态化。例如 Hexo 和 Jekyll 这样的工具，就可以把 Markdown 生成静态的 HTML 文件。然后通过 S3 或者反向代理为用户提供内容。相较于 Wordpress 或者很多动态应用，这样的内容不会占用 CPU 和内存，仅仅占用文件系统 IO。占用资源低，也较少会出错。此外，静态的内容也更容易被缓存。

唯一的问题就是区分应用架构中的静态部分和动态部分，并通过版本控制来对内容进行管理。必要的时候要采用 缓存的失效时间或者 HTTP 头的缓存控制来进行更新。

### 读写分离

如果把应用程序看成一个大的 I/O 系统或者 读/写系统。我们要明白数据是如何写入并如何读出的，特别是针对于数据库而言， 某些的操作都会带来一定的锁或者事务来解决临界资源的互斥访问问题，这种操作一定程度上也会影响性能。所以，我们如果能把数据库的读写分开，会提升应用的部分访问性能。

例如在 AWS 中，Aurora 数据引擎可以为数据库创建集群和只读分片来做读写分离。

另外一种情况下就是用搜索引擎（例如 ElasticSearch）来替代数据库查询，性能会高很多。只是要注意数据的更新频率和索引时间。

### 异步访问

在大型企业级应用中，通常会应用事务（Transaction）保证业务的完整性和一致性，代价则是系统资源的事务内占用。如果有很多的事务占用着资源，则会造成时间上的资源使用浪费。更加现代的做法是把一个较长的事务拆分成多个较短的事务，通过异步的方式进行“两步提交”来保证最终一致性。优点是释放了很多资源，缺点则是需要更多的确认操作来保证最终一致性。

通过以上的四种方式，我们还可以为不同业务组合成不同的分离方案。并通过 AFK 扩展三角的 Y 轴按能力将应用的关注点进行拆分，采用不同的技术栈和服务来实现并优化性能。例如变成微服务的架构的应用。或者当数据库达到瓶颈之后通过 Z 轴进行拆表拆库在分摊数据库的负载的情况下保证一致性。

## 第三阶段：构建应用端的持续部署

以上只是进行了基础设施方面的改造，应用的性能和稳定性得到了一定程度提升。然而，我们仍然采用部分人工的操作来进行应用和基础设施的变更。以“萨瓦迪卡”为例，如果我们需要更新应用，为了减少停机时间，则需要执行下面的步骤：

1. 为当前生产环境虚拟机创建镜像。
2. 采用新创建的新镜像创建虚拟机。
3. 在新创建的虚拟机上进行更新。
4. 更新后进行测试，测试完毕后创建新的更新镜像。
5. 采用更新后的镜像进行自动水平扩展。
6. 替换负载均衡里的新老虚拟机。
7. 终止已经下线的虚拟机实例。

然而，这些操作会带来人为因素的风险，可能会带来一些数据丢失的情况。而且，浪费了人工去做云计算环境的部署，前后时间可长达 4 个小时。

通过之前的两个阶段，我们已经把一个非分布式的应用变成了简单的分布式应用。而面对分布式应用的架构复杂性，人力处理肯定是低效的。我们需要采用自动化的方式完成应用生命周期和基础设施生命周期的完整管理。持续部署流水线就是这样一种实践，通过把流程固化成自动化的脚本和操作避免了人工干预的风险，从而构建出了一个发布软件的可靠流程。

在实践中，我们往往采用持续集成服务器（例如 Jenkins），搭配云计算平台的资源描述和编排服务（例如 CloudFormation）和一些脚本和模板管理工具来完成这一系列操作。在这之前，我们需要对应用程序的不同部分进行封装。

## 通过“三段封装”来规划应用结构

### 第一段：基础设施封装

通过基础设施即代码技术构建出一个应用程序的平台，这个平台可以做到隔离应用且对开发者透明。例如：Kubernetes 或者 AWS CloudFormation。前者可以为开发者提供一个简单的应用部署平台，并很好的支持了很多高可用的特性。后者可以用来配置包括网络在内的所有 AWS 资源。

这里需要注意的是要根据基础设施的变更频率对基础设施实施分层管理，将经常变动的部分独立成一个风险最小的变更单元，避免和其它部分相互影响。

### 第二段：应用封装

通过构建持续交付流水线构建出应用镜像或者虚拟机镜像，要做到快速复制以实现水平扩展。例如 Docker 镜像或者用 Packer 构建出 AMI。

这里需要注意的是构建镜像的时候一定要考虑无状态特性，每个镜像被创建后所展现出来的最终效果和操作都是幂等的。

### 第三段：数据封装

通过数据全量+增量的备份把数据库或者文件存储在更稳妥的地方，并修改访问方式。例如：采用  S3 或者 RDS 来存储。

这里需要注意的是如果你没有用  RDS 等高可靠的数据存储服务，就要要定时对数据进行备份恢复测试，避免需要恢复数据的时候备份不起作用。备份策略可以按照全量 + 增量的方式进行，具体的方式可以参考不同数据库的方案。

完成了三段封装后，我们需要为其构造一个可靠的生命周期管理流程：构建持续部署流水线。

## 构建持续部署流水线

首先，要把上述的内容纳入版本控制。二进制的内容就进行版本编号存储，且不可修改和删除，只能新增。

持续集成服务器本质上是一个自动化的任务调度和执行管理程序，它包含两个部分：**任务调度**和**任务执行**。

而任务调度包含主动和被动两个模式：

**主动模式**：通过定时机制进行扫描，当发现有变动之后触发任务的执行。

**被动模式**：通过类似于 web-hook 被动任务触发，或者由上一个任务进行触发。

任务执行则需要做到幂等性和线程隔离，确保每次的执行环境和结果都一致。我们可以用一个任务的执行结果成为下一个执行的输出。这样，我们通过主动扫描代码改动或者提交任务触发的方式，把测试，构建和打包的工作串联起来，就构成了一条持续交付流水线。大概会经历以下几个步骤：

1. 代码提交
2. 运行自动化功能测试和静态检查
3. 构建
4. 部署至测试环境
5. 运行自动化验收测试
6. 发布

在以上的步骤里，除了第一步和最后一步，所有的中间步骤都是要自动化的。

这里需要注意的是：我们需要把部署和发布解耦。发布（Release）和 部署（Deploy）是两个不同但又相关的动作，发布是一个业务操作，表示用户可以接触到最新版的应用系统。 而部署是一个技术操作，表示应用运行在某一环境上。

Jenkins 里，我们可以采用 Job（任务）的方式来执行任务，由代码库触发测试，测试完成后触发构建、部署和发布。

为了减少系统的停机时间，我们也需要使用一些零停机部署策略，例如”蓝绿部署“和”金丝雀发布“。

### 蓝绿部署

蓝绿部署的做法是同时生成两个相同的生产环境版本，一个叫做”蓝环境“，一个叫做”绿环境“。用户当前只能访问其中一个环境，让另外一个环境进行部署。待到部署完成并通过检查之后，再切换至部署好的环境。如果部署失败，则把用户流量切换到原先的环境就算是做到了快速回滚。某些云计算平台内置 了这样的部署策略，可以帮助快速做到这一点。我们也可以通过更新内部 DNS 记录或者 Nginx 配置做到这一点。如果你的变更中包含数据库变更，则需要额外的数据库迁移策略和切换策略，也会花费额外的时间。

### 金丝雀发布

金丝雀发布可以看做是 蓝绿发布的一种演变形式，相比蓝绿发布来说更加灵活。我们可以通过路由权重让一小部分用户尝试新的版本。就像是在煤矿坑道里的金丝雀那样，很快就能发现生产中的问题，并限制问题的影响范围。

我们还可以基于此做 A/B 测试来度量更新的使用率。但这需要你的基础设施支持“带权流量分配”和“ Session 持久化”。前者是为了更灵活的切分流量，后者则是避免同一个用户访问不同版本应用带来的不一致性。

### 基础设施变更流水线

上述描述的是应用程序的生命周期，我们还需要构造基础设施的生命周期。我们也可以如法炮制同样的流水线来进行基础设施变更。这样我们就可以避免人工调整基础设施带来的各种隐患。我们需要把不同的备份方案和测试方案增加进去以确保我们的基础设施的稳定性和反脆弱性，很多工具可能需要我们自己来编写。

这里需要注意的是一定要尽可能避免人工干预生产环境带来的风险，尽可能通过流水线来对基础设施进行变更。

## 最后

完成了以上三个阶段，我们才可以说基本上完成了一个应用程序迁移到云计算平台上的基础步骤。如果你的应用迁移到了云平台上并做到了以上的三个阶段，才算是及格。

云计算所带来的改变并不仅仅是可靠的廉价租赁式资源，还会改变组织的工作方式。特别是 DevOps 运动的兴起又为 CloudNative 的产品研发运营增加了新的助燃剂。关于构建  DevOps 团队更多的内容和套路，请参见我的 GitChat 达人课：“[DevOps 转型实战](https://gitbook.cn/gitchat/column/5a79594e74fabe0f179f3e8b)”。