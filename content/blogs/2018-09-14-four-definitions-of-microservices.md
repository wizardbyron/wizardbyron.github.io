---
title: 讨论微服务之前，你知道微服务的 4 个定义吗？
date: 2018-09-14
tags:
  - 微服务
---

关于“什么是微服务”的问题，其实并没有一个统一的认识。这些年在不同的场合里和不同背景的朋友都在探讨微服务。但聊得越多，就越发现大家聊的不是同一回事。和 DevOps 一样，“微服务”也是一个内涵十分广泛的词。本文从“Microservice“这个概念的源头出发，总结了 4 个常用的微服务定义。

## James Lewis 原始版的微服务 6 大特征

这个版本起源于2012年，这里首先要注意年份，那时候还没有 Docker，而且 Netflix 的微服务化过程也在这个概念提出之前——2008年就开始了，那时候甚至连 DevOps 还没发明出来。James Lewis 在波兰第 33 次 Degree in Kraków 会议上分享了一个案例，名称是 “Micro Services - Java, the Unix Way”。在这个分享里， James Lewis 分享了在 2011 年中参与的一个项目中所采用的一系列实践，以 UNIX 的哲学重新看待企业级 Java 应用程序，并且把其中的一部分称之为“ Micro-Services ”。

这个时候的微服务所用的单词和我们现在所用的 Microservices 这个单词有所不同。一方面，采用 Micro 作为形容词，是和 Monolithic 相对，而不是和 Macro 相对是源于操作系统这门大学课程。我们知道，现代的操作系统课程都是以 UNIX 作为案例进行讲解的。而这两个单词来自于“微内核”（Micro-Kernel）和“宏内核”（Monolithic kernel）的比较。而非常见的“微观经济学”和“宏观经济学”中的 Micro 和 Macro 两个相对应的单词。

另一方面，服务要以复数形式出现，表示的是一个以上。由于汉语里单复数是同型的，所以我们在翻译的时候会出现问题。因此，“微服务”在作为架构的形式出现的时候，我们会用“微服务架构”称呼。单个的微服务从概念上为了和 SOA 以及其它领域的“服务”有所区分，会以“单个微服务”以示区别。而”微服务“单独拿出来是被看作为一系列技术实践的总称。

在这个分享里，James Lewis将所实践的“微服务架构”总结为 5 大特征：

1. **Small with a single responsibility —— “小到只有单一原则”**

   在这个特征里，关于微服务有多小有两个标准：

   第一个标准是：如果一个类复杂的超过一个开发人员的理解范围，那么它就太大了，需要被继续拆分。

   第二个标准是：如果它小到可以随时丢弃并重写，而不是继续维护遗留代码，那么它就足够小。这个标准有个很重要的原则就是 Rewrite over Maintain，即“重写胜于维护”。

2. **Containerless and installed as well behaved Unix services —— “去容器化并且作为 Unix Service 安装”**

   在这个特征中，James Lewis 提倡采用 Jetty 这样的工具集成到 Maven 里，可以很方便的调试或者部署。然后打包成一个可执行的 JAR 包并以 UNIX 守护进程的方式在系统启动时执行。

   特别是在 AWS 这样的公有云环境下，把这样的应用程序和虚拟机实例的初始化脚本结合在一起。使得应用程序的生命周期和虚拟机的生命周期绑定成为一体，由于守护进程在所有 Unix 系统中都是通用的，因此简化整体架构的开发和运维。

3. **Located in different VCS roots ——“分布在不同的版本控制代码库里”**

   在这个特征中，James Lewis 提到了应用程序的分离，他认为一个“微服务”应该完全和另外一个服务实现彻底的隔离，这里当然是指的从开始的代码库就开始隔离了。

   他同样也要求开发人员看到相似性和抽象，并采用单一的领域来指导开发团队的开发。

   因此接下来他继续讨论了领域驱动设计领域驱动设计和康威定律的重要性。他认为界限上下文要足够的清晰，但可以有所重合。如果没有办法做到领域之间很清晰，就通过“物理上的手段”——分离不同的团队来做到这一点。

   这不可避免的带来一些公共代码，但要把这些公共代码作为“库”和“基础设施即代码”来对待，就像你代码中用到的开源软件。并搭建一个 nexus 库来存储那些二进制依赖。

4. **Provisioned automatically ——“自动初始化”**

   自动初始化的要点不在于如何自动化，因为不同的应用不同的平台有不同的初始化方式。这里的重点在于管理分布式应用的复杂性。所以对于每个服务，能够采用声明出这些初始化。例如：服务 A，需要一个 负载均衡，并且可以自动扩展。服务 B，也是同样的声明方式。而这些声明可以用基础设施即代码技术很好的管理起来。

5. **Status aware and auto-scaling ——“关注状态和自动扩展”**

   在这里，他认为这些应用应该是能够感知吞吐量的监控指标来自我进行扩展的。对于一个现代的应用而言，这是一个基本的架构性要求，但这需要团队有一定的 DevOps 能力。因为这不光要求开发人员能够让应用无状态化，而且要求基础设施可以及时捕获环境的变化。

6. **They interact via the uniform interface —— “它们通过统一格式的接口进行交互”**

   在这里，James 建议大家采用已经成熟的 HTTP 协议以及标准的媒体类型进行接口交互，而不是采用其它的方式。并且采用  HEATOS 的方式构建 Restful API，使其成为一个超媒体的应用状态引擎。这样就可以将状态和执行过程隔离区分开来，更加容易进行水平扩展。此外，它也构建了一个避免架构孵化的层，可以独立于客户端持续演进。

在总结的时候，它特意提到了 UNIX 哲学。这引用自Doug McIlroy 的一篇[采访](https://www.princeton.edu/~hos/frs122/precis/mcilroy.htm)：

> Everybody started putting forth the UNIX philosophy. Write programs that do one thing and do it well. Write programs to work together. Write programs that handle text streams, because that is a universal interface."   Those ideas which add up to the tool approach, were there in some unformed way before pipes, but they really came together afterwards. Pipes became the catalyst for this UNIX philosophy. "The tool thing has turned out to be actually successful. With pipes, many programs could work together, and they could work together at a distance."

从这段话里，我们看到了“微服务架构”和 UNIX 哲学之间的关联：

1. 职责独立：让多个程序（注意是 Programs 不是 Program）做好一件事。
2. 统一接口：文本流是统一的接口，每个程序都可以通过统一的接口进行消费。
3. 公共通信：采用管道（pipe）的方式

可以说，微服务架构本身是对 UNIX 哲学在企业级 Java 应用系统中的另一个案例。可以说，虽然应用场景变了，但 UNIX 分解复杂度的方式和保持简单的理念并未改变。

最后，James Lewis 把上述六点特征变成了一个六边形的业务能力：

> Hexagonal Business capabilities composed of:
> Micro Services that you can
> Rewrite rather than maintain and which form
> A Distributed Bounded Context.
> Deployed as containerless OS services
> With standardised application protocols and message semantics
> Which are auto-scaling and designed for failure

翻译过来就是：

> 微服务你可以通过重写而非维护一个分布式的界限上下文，且作为一个无应用容器的操作系统服务部署。并以标准化的应用协议和消息语义，为失败设计且可自动扩展。

## Martin Fowler & James Lewis 合作版的微服务 9 大特征

由于在 James Lewis 之后，有很多不同的项目也采用“微服务”作为它们的实践的名称。然而，不同的项目之间还是存在一些差异的，且每个人都按照自己的方式在实践“微服务”。因此，基于“求同存异”的原则，Jame Lewis 的同事 —— 大名鼎鼎的 Martin Fowler 采用一种归纳的方式来解决这个问题：[他认为“定义”是一些“共有的特征”(Common characteristics)](https://www.youtube.com/watch?v=wgdBVIX9ifA)。Martin Fowler 继续采用了 James Lewis 对这一系列实践的命名，并且做了修改，使之成为一个单独的名词 —— Microservices。

所以，他将微服务总结为以下[9大特征](https://martinfowler.com/articles/microservices.html)：

1. 通过服务组件化

2. 围绕业务能力组织

3. 是产品不是项目

4. 智能端点和哑管道

5. 去中心化治理

6. 去中心化数据管理

7. 基础设施自动化

8. 为失效设计

9. 演进式设计

这 9 大特征的中文版具体内容请参考[这里](http://blog.cuicc.com/blog/2015/07/22/microservices/)，限于篇幅原因，本文不展开讨论。

我们可以从中看出，Martin Fowler 试图将 James Lewis 的微服务定义进行一般化推广，使其不光之可以在不同的语言架构和技术栈上使用。又可以兼顾敏捷、DevOps 等其它技术，成为一个架构的“最佳实践”集合。但这样一组实践本质上并没有太多的创新，只是把我们本身知道的很多架构和设计的原则结合在当前的技术栈上进行了一次整体的组合和应用。

恰逢一系列互联网公司的成功事迹带来的新实践（持续交付、DevOps）和新技术（Docker）在经历了早期实践者（Early Adopter）实践积累后的结果井喷后。这样的最佳实践的集中反应固然得到了技术人员的掌声。然而，这样的一种定义对于妄图采用“微服务架构“的人来说是一个很高的门槛。如果这样的 9 个特征的总结是对”微服务架构“的定义。那么，为了要满足以上的 9 个定义，则需要花费很大的精力来进行改造，而且已经超出了技术升级和企业 IT 部门的职责范围。此外，即便我们知道其中每个特征所带来的收益，但却很难拿出案例和数据去佐证满足这 9 个特征的改造收益。

避开这 9 个特征的概念正交性不谈，即便这 9 个特征可以从既有的结果来回答”什么（What）是微服务“，但却没有给出“为什么（Why）要满足这些特征”和”如何（How）同时满足这些特征”。

如果自己挖的坑填不了，就教给别人来填吧：

## Sam Newman 版微服务的两大特征和 7 个原则

同样作为 Martin Fowler 的同事，Sam Newman 在其著作 ”Building Microservice“（中文译名为”微服务设计“）的第一章就重新回答了”什么是微服务架构“并回答了”为什么要采用微服务架构“的问题。

Sam Newman 在书中是这么定义微服务的（《微服务设计》的翻译）：

>微服务就是一些协同工作的小而自治的服务。

Sam Newman 自述的微服务的定义更加简单，包含了两个特征：“小” 和 “自治”。

除了继承 James Lewis 关于微服务应该有多小的描述以外（当然，大小都是基于个人的主观判断），还创造性的用康威定律来约束微服务的大小，即“能否和团队结构相匹配”：如果你的团队维护单个服务很吃力，需要保持团队大小不变的情况下还对维护工作游刃有余，那么这个服务就需要继续被拆分。

而“自治” 则很谨慎的把 Martin Fowler 微服务定义的 9 大特征中的“去中心化”、“独立” 、”松散耦合“等字眼进行了统一。并进一步解释到“一个微服务就是一个独立的实体”。并且从外部，也就是黑盒的角度来看每个符合"自治"的单个微服务所具有的特征，即：

1. 可以独立部署。
2. 通过网络通信。
3. 对消费方的透明。
4. 尽可能降低耦合，使其自治。

此外，他还采用了更简单的“黄金法则”来判断期"自治性"。即能否修改一个服务并对其部署，且不影响其他任何服务。如果答案是否定的，说明你的微服务还不够”自治“。

从 Sam Newman 的定义中，我们可以推导出“微服务”的几个基本事实：

1. 微服务架构是一个分布式系统架构。
2. 微服务是微服务架构的基本单元。
3. 网络隔离是”必要的“解耦手段。
4. 微服务的业务功能从概念上是完整的，并符合用户角度的“独立”认知。

简而言之，以上的两个特征的表述主要是将微服务从逻辑架构上和部署架构上都看作是一个正交的原子功能单元。而要做到这一点，则需要而要把整个应用系统正确的建模到这个层次，则需要参考很多的内部外部因素。

此外，为了达到“小”和“自治”的目的，Sam Newman 还总结了 7 条原则用来在实施的时候和具体实践结合，分别是：

1. 围绕业务概念建模
2. 接受自动化文化
3. 隐藏内部实现细节
4. 让一切都去中心化
5. 可独立部署
6. 隔离失败
7. 高度可观察

可以看出，Sam Newman 把 Martin Fowler 的 9 大特征用更加具体的术语来重新描述，并且从逻辑上处理了 Martin Fowler 微服务 9 大特征中概念重复和不明确的部分，使其更简单和明确并且更加可操作。例如把“去中心化的数据管理” 和 "去中心化治理"合并为“让一切都去中心化”等。

更重要的是，Sam Newman 提出了采用微服务技术的主要好处，告诉了我们“为什么要用微服务”：

1. 技术异构性：采用更合适的技术栈灵活的处理局部问题。
2. 弹性：这里的“弹性”是弹性工程学的概念，指的是局部失败会被隔离，使得整体不会失败。
3. 扩展：可以根据系统的部分组件按需扩展。
4. 简化部署：这里简化部署不是指的是部署的拓扑结构，而是通过持续的小批量、小范围的部署来降低整体失败的风险。
5. 与组织结构相匹配：微服务架构可以让组织的团队转化为合适的大小，并采用透明的制度来进行规范和复制。避免团队的人数增长而带来更多的管理层，使组织熵的上涨。
6. 可组合性：由于各个微服务间不存在依赖关系，所以可以根据用户界面的情况进行灵活的调整和复用，避免对单体应用进行整体的大规模调整。
7. 对可替代性的优化：由于风险和领域更加独立和隔离。因此，抛弃一个微服务并重写的成本并就变的十分低廉。

## Chris Richardson 的“微服务架构模式”

2017 年，Chris Richardson 使用 Microservices.io 域名开始推广自己的微服务理念。他是这样定义微服务的：

>Microservices - also known as the microservice architecture - is an architectural style that structures an application as a collection of loosely coupled services, which implement business capabilities. The microservice architecture enables the continuous delivery/deployment of large, complex applications. It also enables an organization to evolve its technology stack.

中文翻译过来，大意如下：

> 微服务，也就是微服务架构。是一种用于把一个应用程序结构化为一个实现业务功能的松散耦合的服务集合的架构风格。

微服务架构使得在大型、复杂的应用程序中实现持续交付和持续部署成为可能。它使得组织可以演进自己的技术栈。

在 Chris Richardson 采用了较为简单的架构定义和准确的目标定义相结合的方式来定义”微服务架构“：它一方面简单的把微服务架构定义成一个实现业务功能的松散耦合的服务集合，另一方面又以十分具体的目标和结果（持续交付/持续集成）来约束这样一个松散耦合系统的效果：组织可以演进自己的技术栈。

Chris Richardson 将“单体架构”和“微服务架构”看做两种架构模式。并且在同样的上下文中对二者各自的优劣进行了比较。更加重要的是，Chris  Richardson 采用 [AFK 扩展立方](https://microservices.io/articles/scalecube.html)来拆分微服务从而回答了“如何做微服务”的问题。

值得注意的是，Chris Richardson 所采用的例子虽然在同样的上下文中，但由于特征不同并不具备可比较性。因此，他采用了在[”单体架构模式“（Pattern: Monolithic Architecture）](https://microservices.io/patterns/monolithic.html)的基础上描述其局限性的方法引出了[”微服务架构模式“（Pattern: Microservice Architecture）](https://microservices.io/patterns/microservices.html)。严格的说，Chris Richardson 的“单体架构模式“是一种对现状的和举例，并没有给出其特征和方法的描述，因此不能称之为模式。而”微服务架构模式“则[又是一系列模式的总和](https://microservices.io/patterns/cn/index.html)，如下图所示：

![PatternsRelatedToMicroservices](/img/post/20180914/MicroservicePatternLanguage.jpg)

从这个角度看，Chris Richardson 的这些模式并没有突破 Sam Newman 在《微服务设计》中总结出的实践。但相较于我们所知道的微服务的优点。Chris Richardson 也列出了微服务的缺点：

1. 开发者必须应对创建分布式系统所产生的额外的复杂因素。
   - 现有开发者工具/IDE主要面向单体应用程序，因此无法显式支持分布式应用的开发。
   - 测试工作更加困难。
   - 开发者必须采取服务间通信机制。
   - 很难在不使用分布式事务机制的情况下跨服务实现功能。
   - 跨服务实现功能要求各团队进行密切协作。
2. 部署复杂。在生产环境下，对这类多种服务类型构建而成的系统进行部署与管理十分困难。
3. 内存占用量更高。微服务架构使用N*M个服务实例替代N个单体应用实例，如果每项服务运行自己的JVM（或者其它类似机制），且各实例之间需要进行隔离，那将导致M倍JVM运行时的额外开销。另外，如果每项服务都在自己的虚拟机（例如  EC2 实例）上运行，如同Netflix一样，那么额外开销会更高。

相较于之前的微服务定义而言， Chris Richardson 的微服务体系比较完整，而不仅仅是总结和列举实践。Chris Richardson 的"微服务架构模式"不光回答了“什么是（What）微服务”，也回答了“为什么（Why）要用微服务”，“什么时候（When）用微服务”，“什么场景（Where）下”以及“如何（How）实现微服务”的问题。

Chris Richardson 还编写了一套微服务的指南，可以在[这里](https://www.nginx.com/blog/introduction-to-microservices/) 查看。

## 比”什么是微服务“更重要的事

本文总结了微服务常见的 4 个定义。但比这些定义更重要的是你为什么要用微服务？你想从微服务中获得什么益处？你是否了解为了追求这些益处所带来的代价？如果不先明确这些问题，在不理解微服务架构或者技术所带来的的风险和成本。盲目的采用所谓的微服务，可能带来的结果并不理想。

不过，在讨论这些问题之前，坐下来统一一下对微服务的理解，会提升我们讨论和实践微服务的效率。
