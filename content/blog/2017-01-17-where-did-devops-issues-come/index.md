---
title: DevOps 前世今生 - 2. DevOps 矛盾从何而来
date: 2017-01-27
tags:
- DevOps
- DevOps 前世今生
---

在[**#DevOps的前世今生# 1.DevOps编年史**](/blog/2016-11-27-devops-annals)一文中，通过追溯 DevOps 活动产生的历史起源，我们发现了 DevOps 是敏捷思想从软件开发端(**Dev**)到系统维护端(**Ops**)的延伸。无论是 DevOpsDays 的创始人 **Patrick Debois**，还是同时期的 The Agile Admin。都想通过敏捷来改进传统的系统维护工作以及软件开发部门和系统维护部门的合作关系。但是，DevOps 的矛盾从何而来？这还要从 Dev 和 Ops 的起源开始讲起。

## 上古时代——抱着计算机使用手册，自开发自运维

历史要追溯到刚刚出现计算机的时期。当时，软件开发还是少数人通过高学历才能够掌握的技能，那个时候只有“程序”（Program），但没有“软件”（Software），所以那个时候编写程序的人员被称为“程序员”（Programmer）。基本的学习材料还只是计算机设备厂商附送的使用手册。所以，只能先购买设备，再自己培养人才。

最先购买计算机的是科研单位，军队，政府以及少数大型企业。同时组建了新的部门，成立了信息技术部（IT Department)，或者叫信息化办公室（IT Office）。在中国的有些单位里干脆直接叫“电脑部”。他们一个科室，一个办公室主任，外加两三个科级干部和几个科员，专门管理这些电脑的使用情况，并且学习软件编程技术，用程序来解决其他各部门的。

这是最初的IT运维雏形，在这个时期是没有 Dev 和 Ops 之分的，他们统称为 Programmer。由于开发和运维都由同样的人包揽，自己维护自己开发的程序，也可以被看做是原始的 DevOps。这个时期的计算机系统和问题较简单，开发和维护并不复杂，无需进行专业区分。

## 桌面通用软件时代——软件成为了一门生意，出现了专业的软件开发工程师（**Dev**）

随着计算机的成本不断下降，尤其是以 IBM PC 为代表微型计算机（ MicroComputer ）开始普及。企业也开始大规模使用计算机进行办公。由于软件开发人员数量仍然很少，加之需求很旺盛，专业的软件开发人员成本依然高昂。

最开始的时候，软件仅仅通过磁盘拷贝进行流传，某些介绍计算机或者软件的杂志开了先河。程序员通过磁盘向杂志社投稿，杂志社通过变卖杂志和软件获利。由于软件的边际生产成本几乎是0，所以渐渐有人把销售软件变成了一门生意。随着软件的扩展，当初为个人目的（Personal
Purpose）所编写的软件渐渐的开始走通用化的路线，慢慢形成了软件产品。接着有了专门从事软件开发的公司，并逐渐成为一个产业。并且有了软件开发工程师（Developer，简称Dev）这个职业。

在这个时期，开发软件仍然是很专业的事情，企业的IT部门要想开发软件的代价十分高昂。因此，大部分单位，组织和企业通过购买的形式获得软件。IT部门逐渐成为了负责信息化采购以及软硬件基本操作培训的部门。此外，由于信息化发展加速，各行各业软件层出不穷，加之软件企业越来越多，IT部门不得不通过更广泛的学习了解技术的变化。

## 企业级定制化软件时代——企业级应用的快速发展，出现了专业的系统维护工程师（**Ops**）

随之带来的问题是：无论企业买来多少软件，企业的信息化需要仍然无法被满足。一台台电脑成为了企业的信息孤岛，解决了信息的分析和存储问题最多实现了无纸化办公。没有让部门间的信息有效的流动起来。大型企业最先发现这些问题并且给出了最初的解决方案，使得**企业级软件开发和系统集成**（System Integration）慢慢成为了一个热门的领域。

企业级软件系统最大的特点是通过计算机网络解决了企业内部的信息孤岛。但这样的系统无法在PC上运行需要专业的工作站，服务器以及网络设备。而这些设备的管理就理所当然的成为了企业IT部门的职责。

随着软硬件技术的发展，特别企业级应用开发的经验不断积累，设备的采购成本和软件的开发成本进一步降低。大型IT厂商开始瞄准企业级应用市场，尤其是IBM，Oracle和EMC推出了相应的产品。使得软件定制开发的成本不断下降。加之随着开发人员越来越多，开发成本逐渐降低，于是出现了企业定制化软件开发，出现了MIS和ERP这样的应用以及J2EE这样的企业级软件开发框架。

在这个过程中，IT运维的概念逐渐产生，维基百科上是这样定义IT运维（IT Operations）的：

> IT Operations is responsible for the smooth functioning of the infrastructure and operational environments that support application deployment to internal and external customers, including the network infrastructure; server and device management; computer operations; IT infrastructure library (ITIL) management; and help desk services for an organization.

翻译成中文就是：

> IT运维的责任是要为内部和外部客户的应用部署提供平滑的基础设施和操作环境，包括网络基础设施，服务器和设备管理，计算机操作，ITIL管理，甚至作为组织的IT帮助中心。

对于企业的IT部门来说，工作就不仅仅是维护计算机和网络这些设备了。还要包括运行在上面的软件系统，尤其是定制化的企业级软件产品。因此在定制化企业级软件交付从乙方交付给甲方的时候就需要一系列的技术审查以确保质量，这就使得原本不需要关心软件是如何开发的企业IT部门提出了更高的要求。他们必须提升专业水准以应对这样的变化。同时需要重新思考整个IT部门的服务管理和设计。随着IT部门知识和服务专业度的提升，促生出了了**ITIL**（Information
Technology Infrastructure
Library，信息技术基础设施库）这样的最佳实践库，也使“系统维护工程师”（Ops）更加专业化。

**在这个时期，Dev和Ops的矛盾，主要是由Dev所代表的乙方和Ops所代表的甲方在定制化软件产品交付质量上的矛盾**。

## 敏捷软件开发时代——应对频繁变更的挑战

随着企业级软件开发日趋完善和成熟，形成了以**RUP**（Rational Unified Process，Rational 统一软件开发过程）为代表的方法论。**RUP**描述了如何有效地利用商业的可靠的方法开发和部署软件，是一种重量级过程（也被称作厚方法学），因此特别适用于大型软件团队开发大型项目。

后来，互联网企业的繁荣着实闪瞎了世界的眼睛。没有人想到原本用来进行国防和科研的广域网居然可以带来这么大的商业价值。互联网创业公司的成功不断的颠覆了很多人习以为常的事情，特别是IT产业。

首先，相较于最多万人的用户访问规模，来自互联网的千万级甚至是亿级的访问规模是企业级应用不曾遇到过的。这对软件开发，主机管理，网络架构都带来了很大的挑战。

其次，企业级应用和互联网应用面对的问题是不一样的。根据“**康威定理**”：设计系统的组织，其产生的设计和架构等价于组织间的沟通结构。相较于有着清晰的等级和部门分工的组织来说，互联网产品的沟通结构更加复杂。

此外，互联网应用由互联网企业自开发自维护。虽然从表面上看没有了甲方和乙方的对立。但开发和运维相互分离的工作流程和考核方式却沿用了下来，职责上的对立依然存在：

**Dev**的工作是给应用系统增加新的功能/修复软件的Bug，这一系列价值的产生是通过应用系统变更实现的。一般的组织会用代码/功能的贡献数量作为KPI作为考核的依据，以激励Dev的工作产出。

**Ops**的工作则是让应用系统保持稳定和高性能，即最大化缩短宕机时间并能够提升应用系统的性能，并以这两者作为Ops的KPI的考核指标。以激励Ops通过维护工作使应用系统能够按照预期稳定的产出价值。

而市场环境的瞬息万变和资本的集中化使得互联网软件产品的生存状态十分脆弱：

一方面，快速变化的市场难以预测。因此，基于经验的重量级软件开发方法不再适用。取而代之的是强调适应性，拥抱变化的敏捷方法。互联网软件必须通过频繁增加/修改功能来提升自身对市场的适应程度。

另一方面，互联网软件的变更给带来的风险和损失都是难以度量的。因此，互联网软件有更加严格的交付标准，需要做更多的质量保证。而基于经验的系统运维实践并没有给出足够的方法以应对这种挑战。

**因此，在这个时期，Dev 和 Ops 的矛盾主要是面向适应性的敏捷软件交付和面向经验性的传统运维之间的矛盾**。

那么，如果将敏捷的文化和原则引入运维，会如何？

请期待下一篇：[#DevOps的前世今生# 3.DevOps的文化和原则](/blog/2017-02-14-core-devops-concepts)

**感谢ThoughtWorks总监咨询师史凯对本文的改进意见和建议**。

## 参考资源

[https://en.wikipedia.org/wiki/Information\_technology\_operations](https://en.wikipedia.org/wiki/Information_technology_operations)

[https://en.wikipedia.org/wiki/Software\_developer](https://en.wikipedia.org/wiki/Software_developer)

[https://en.wikipedia.org/wiki/Management\_information\_system](https://en.wikipedia.org/wiki/Management_information_system)

[https://en.wikipedia.org/wiki/Enterprise\_resource\_planning](https://en.wikipedia.org/wiki/Enterprise_resource_planning)

[https://en.wikipedia.org/wiki/Rational\_Unified\_Process](https://en.wikipedia.org/wiki/Rational_Unified_Process)

[http://agilemanifesto.org/iso/zhchs/manifesto.html](http://agilemanifesto.org/iso/zhchs/manifesto.html)

[https://theagileadmin.com/what-is-devops/](https://theagileadmin.com/what-is-devops/)

[http://www.jedi.be/blog/2009/12/22/charting-out-devops-ideas/](http://www.jedi.be/blog/2009/12/22/charting-out-devops-ideas/)

[http://itrevolution.com/the-convergence-of-devops/](http://itrevolution.com/the-convergence-of-devops/)

[http://joehertvik.com/operations-management/](http://joehertvik.com/operations-management/)

[https://zh.wikipedia.org/wiki/IBM-Rational%E7%BB%9F%E4%B8%80%E8%BF%87%E7%A8%8B](https://zh.wikipedia.org/wiki/IBM-Rational%E7%BB%9F%E4%B8%80%E8%BF%87%E7%A8%8B)

[https://zh.wikipedia.org/wiki/%E6%95%8F%E6%8D%B7%E8%BD%AF%E4%BB%B6%E5%BC%80%E5%8F%91](https://zh.wikipedia.org/wiki/%E6%95%8F%E6%8D%B7%E8%BD%AF%E4%BB%B6%E5%BC%80%E5%8F%91)

[http://www.infoq.com/cn/news/2015/08/itil-vs-devops/](http://www.infoq.com/cn/news/2015/08/itil-vs-devops/)
