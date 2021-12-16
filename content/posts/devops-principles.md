---
title: DevOps前世今生 - DevOps 的原则
date: 2019-08-24
category: 
  - DevOps
tags:
  - DevOps
---

> [2019-08-24] 在写完《 DevOps前世今生 - DevOps 的文化》之后，这个系列我就停止更新了。在这期间发生了两件事：1. 《DevOps Handbook》出版，我准备阅读完《DevOps Handbook》后再继续写。2. 我在不同的社区活动中分享了自己对 DevOps 的理解，和不同行业的朋友交流了很多，很受启发，于是写下了[关于 DevOps ，咱们聊的可能不是一回事](https://www.guyu.me/posts/2017-12-03-we-are-talking-different-devops/)。没想到这个系列一搁置就是两年（咨询师的工作充满了太多不确定性）。

> 

由于工作内容的不同，我开了很多坑。然后发现自己今年可以完成的有限。我决定还是把自己开的坑先填完，而不是挖新的坑。

## 从 CAMS 到 CLAMS

在 DevOps 运动的早期， John Willis 和  Damon Edwards 一起创立了一个叫做[DevOps Cafe](http://devopscafe.org) 的播客，在上面定期分享关于 DevOps 的内容。在 2010年 Montain View 的 DevOpsDays 之后，他们提出了 [CAMS 原则](https://blog.chef.io/2010/07/16/what-devops-means-to-me/)，他们分别是：

**C - 文化（Culture）**：人和流程优先，如果你没有 DevOps 的文化，所有自动化的尝试都是枉然。

**A - 自动化（Automation）**：这是您了解自己的文化后开始的地方之一。 此时，工具可以开始将DevOps的自动化结构拼接在一起。 用于管理发布，设备初始化，配置管理，系统集成，监视和控制以及编排的工具成为构建Devops结构的重要部分。

**M - 度量（Measure）**：如果你无法度量，你就无法改善。 成功的Devops 实施会尽可能多且频繁地测量它所能做的一切......性能指标，流程指标，甚至是人员指标。

**S - 分享和共担（Sharing）**：创造一种人们分享想法和问题的文化至关重要。  DevOps运动的另一个有趣动机是分享DevOps成功的故事以帮助他人。 首先，它吸引了人才，其次，有一种信念，即通过揭露想法，你可以创造一个开放的反馈机制，最终帮助他们改进。

在 2010 年 的 DevOpsDays 上， Jez Humble 发表了名为“DevOps and Agile Release Management”（DevOps 和敏捷发布管理）的演讲。在这篇演讲里他在 CLAMS 的基础上增加了 ”Lean“（精益），使之从 CAMS 变为 CLAMS 原则。精益思想，特别是“Value Stream Mapping”（价值流映射图）可以帮助企业可视化并且帮助他们度量 DevOps 的结果。

精益生产（英语：Lean Manufacturing，或lean production），又译为精实生产、精益企业、精益生产法 ，简称为精益（lean）或精实，一种系统性的生产方法，其目标在于减少生产过程中的无益浪费（日语：無駄，Muda），为终端消费者创造经济价值。在消费者消费产品或服务的过程中，"价值"应该定义为消费者愿意为其买单的行为或流程。

简单来说，精益生产的核心是用最少工作，创造价值。精益生产主要来源于丰田生产方式 (TPS)的生产哲学，因此也称为丰田主义 (Toyotism)，一直到1990年间才称为精益生产。[1][2]丰田生产系统以降低丰田的七项浪费、降低浪费、提升整体客户价值而闻名。但达到这个目标的方法有很多。丰田多年以来的持续增长，从一个默默无闻的小公司成长为世界最大的汽车制造商。[3]让人们注意到如何获得生产上的成功。

实际上，精益

在 CALMS 原则被广泛传播开来之后，CLAMS 原则也成为了 DevOps 成熟度模型的基础。很多的 DevOps 的成熟度模型都按照 CALMS 原则来设计。

首先，CALMS 原则中，人和流程优先，这和

我们可以注意到，CLAMS 原则中只有“自动化”是和工具相关的。剩下的内容基本上是和管理制度相关的。所以，尽管我们看到了很多打着“DevOps” 名号的工具，但如果没有办法落地其它原则，DevOps 其实只做了很小一部分。所以，如果想到“DevOps”就想到买软件产品和工具，就会制造一种“DevOps”的幻觉：所有的工具最后都成了玩具，但并没有很显著的改进。声称能做 DevOps 解决方案的公司，如果只是引入了自己的解决方案。没有帮助团队建立出文化、度量、价值流图和解决冲突和矛盾的制度就不算是成功的。

另一方面，我们可以

## 用三步工作法落地 CALMS 原则

2013 年，一部小说引起了广泛关注，不仅仅是 IT 领域，它影响到了未来 DevOps 的发展。它就是《凤凰项目—一个IT运维的传奇故事》，联合作者之一的 Kim Gene 
《凤凰项目》是一部里程碑式的著作，它通过小说的方式介绍了当今 IT 在企业生死存亡中所处的关键地位以及所面临的挑战。最重要的，是这部书中提到的

在第一步的中，我们需要采用价值流映射图来标记

本书中阐述了一个原理：所有开发运维模式都来自“三步工作法”，可以说它是我们平台开发运维的指导思想。

### 在第一工作法中应用 CALMS 原则

第一工作法是关于从开发到技术运营，再到客户的整个自左向右的工作流。为了使流量最大化，我们需要小的批量规模和工作间隔，绝不让缺陷流向下游工作中心，并且不断为了整体目标（相对于开发功能完成率、测试发现/修复比例或运维有效性等局部目标）进行优化。
流程自动化

在第一工作法中应用 Culture 原则：
在第一工作法中应用 Automation 原则：采用持续交付流水线自动化从开始到部署之间的工作流
在第一工作法中应用 Lean 原则：采用 Value Stream Mapping 可视化所有的工作项
在第一工作法中应用 Measurement 原则：列出所有的 让每个工作项
在第一工作法中应用 Sharing 原则：不区分 我们要把开发到运营连接起来，在一起制定流水线

实践：持续构建、持续集成、持续部署，按需创建环境、限制半成品，构建起能够顺利变更的安全系统和组织。

### 在第二工作法中应用 CALMS 原则

第二工作法是关于价值流各阶段自右向左的快速持续反馈流，放大其效益以确保防止问题再次发生，或者更快地发现和修复问题。这样，我们就能在所需之处获取或嵌入知识，从源头上保证质量。
保证上游的质量


在第二工作法中应用 Culture 原则：
在第二工作法中应用 Automation 原则：在每个阶段增加自动化的测试和验证。分散的持续部署和测试要好于集中的测试和部署。
在第二工作法中应用 Lean 原则
在第二工作法中应用 Measurement 原则
在第二工作法中应用 Sharing 原则

实践：在部署管道中的构建和测试失败时“停止生产线”、日复一日持续的改进日常工作、创建快速的自动化测试套装软件，以确保代码总是处于可部署的状态、在开发和技术运营之间建立共同的目标和共同的解决问题的机制、建立普遍的产品遥测技术，让每个人都能知道，产品和环境是否在按设定的运行，以及是否达到了客户的目标。

### 在第三工作法中应用 CALMS 原则

第三工作法是关于创造公司文化，该文化可带动两中风气的形成：不断尝试，这需要承担风险并从成功和失败中吸取经验教训、理解重复和联系是熟练掌握的前提、尝试和承担风险让我们能够不懈地改进工作系统，这经常要求我们去做一些和以往做法大不相同的事。一旦出现问题，不断重复的日常操作赋予我们的技能和经验，令我们可以撤回至安全区域并恢复正常运作。
不断试错，持续改进

在第三工作法中应用 Culture 原则：
在第三工作法中应用 Automation 原则：根据运营情况增加更多的非功能性测试，不断尝试缩短
在第三工作法中应用 Lean 原则：
在第三工作法中应用 Measurement 原则：
在第三工作法中应用 Sharing 原则：

实践：营造一种勇于创新、敢于冒险（相对于畏惧和盲目服从命令）以及高度信任（相对于低信任度和命令控制）的文化；把至少20%的开发和技术运营周期划拨给非功能性需求，并且不断鼓励进行改进。

## 时时刻刻反思自己的 CALMS 结果

DevOps 并不是一次性的技术升级

并非工具不重要，而是所有的工具都应该为提升管理的目的服务的，工具是手段，提升反馈和质量最终
在 CALMS 原则提出很多
所有的工具是为管理目的服务的






## 参考

https://blog.chef.io/2010/07/16/what-devops-means-to-me/

https://itrevolution.com/devops-culture-part-1/

https://itrevolution.com/devops-culture-part-2/


https://zhuanlan.zhihu.com/p/25675203