---
title: DevOps 模式 - 定义你的DevOps
date: 2019-05-26
tags:
  - DevOps 模式
---

遗憾的是，很少有人真的关心 “DevOps 是什么”，当然其实也不重要。比 DevOps 是什么来说，更重要的是 “DevOps 能做什么”。据 John Willis 的说法，DevOps 运动的发起人 Patrick Debois 一直拒绝给 DevOps 下定义是一件了不起的事情。 Patrick Debois  他不希望把 DevOps 据为己有。DevOps 应该属于社区，属于每一个愿意投身于 DevOps 目标的个人和组织。

由于第一届 DevOpsDays 奠定 DevOps 的基础。组织者 Patrick Debois 作为第一个"官方" DevOps 发言人。第一届 DevOps 的产出内容给未来的 DevOps 发展方向上起到决定性作用。因此，DevOps 模式中的 DevOps 的相关定义均参考Patrick Debios 的博客。

然而，在我过去经历的不同的 DevOps 转型/改进项目中的经历来看。不同的组织，不同的部门，甚至是同一个部门的人，大家对 DevOps 的理解并不一致。这对 DevOps 长时间在组织内发挥改进作用是不利的。

## 模式：定义你的 DevOps (Define Your DevOps)

**模式名称**：定义你的 DevOps (Define Your DevOps)

**模式别名**：定制化 DevOps 定义 (Customize DevOps Definition)

**模式类别**： 策略模式

**风险**： 中 - 采用的时候要注意场景和条件，否则会出现反模式。

**价值**：中 - 采用该模式产生中期固定的收益，但要持续做才可以获得收益。

**见效时间**：快 - 2 周内可看到显著改进。

**说明**：

根据组织的需要，在基于对 DevOps 历史和实践的理解上建立对组织发展有益的 DevOps 的定义。DevOps 的定义包括 DevOps 的组织改进范围，DevOps 的度量，DevOps 的实践。在采用 DevOps 实践的过程中，要先取得 DevOps 共识并基于共识采取 DevOps 度量。否则无法确定 DevOps 带来的改进。

此外，DevOps 的定义会随着组织在的不同阶段而变化。要定期重新定义当前阶段的DevOps 目标，否则会导致"DevOps教条主义" 反模式和" DevOps 复制者"反模式。

DevOps 的定义要在实施 DevOps 的组织内达成共识。否则会陷入"片面的 DevOps" 反模式。

**相关模式**：DevOps 共识，DevOps 范围，建立 DevOps 度量，短期 DevOps 提升

**相关反模式**： DevOps 教条主义，DevOps 复制者，片面的 DevOps

**相关引用**：

[https://en.wikipedia.org/wiki/DevOps](https://en.wikipedia.org/wiki/DevOps)

[https://youtu.be/o7-IuYS0iSE](https://youtu.be/o7-IuYS0iSE)

[http://www.jedi.be/blog/2009/12/22/charting-out-devops-ideas/](http://www.jedi.be/blog/2009/12/22/charting-out-devops-ideas/)

[http://www.jedi.be/blog/2012/05/12/codifying-devops-area-practices/](http://www.jedi.be/blog/2012/05/12/codifying-devops-area-practices/)

如果不定义适合自己的 DevOps，或者对 DevOps 理解单一。会导致"DevOps 教条主义"和"DevOps模仿者"反模式。

## 反模式：DevOps 教条主义 ( DevOps dogmatism )

**反模式名称**：DevOps 教条主义（DevOps dogmatism）

**反模式类别**： 策略反模式

**不良后果**： 无法达到 DevOps 改进预期的效果

**常见原因**：

1. 认为 DevOps 是静态，完整的理论体系。
2. 认为体系化的 DevOps 资料，例如：文献、书籍可以覆盖所有 DevOps 内容。

**说明**：

> DevOps 的目标是"通过一系列行之有效的管理实践和技术实践，以消除软件全生命周期的中的浪费，提升软件及其过程的质量、效率和反馈频率。从而使组织能够更好的适应外部的变化。"

在此基础上，DevOps 相关的实践和模式是不断随着组织上下文和技术上下文的发展而发展的。

注意，**“DevOps 教条主义”**反模式可能会导致**“DevOps 复制者”**反模式。但**“DevOps 复制者”**反模式并不一定会导致**"DevOps 教条主义"**反模式。**“DevOps 教条主义”**反模式的关键在于 DevOps 定义和实践是不继续发展的。而 **“DevOps 复制者”**反模式的关键在于 DevOps 不需要根据组织进行定制。

**修正模式**：定义你的 DevOps，DevOps 度量

**相关反模式**：DevOps 复制者

**相关引用**：

[http://www.jedi.be/blog/2012/05/12/codifying-devops-area-practices](http://www.jedi.be/blog/2012/05/12/codifying-devops-area-practices)

## 反模式：DevOps 复制者 (DevOps Copycats)

**反模式名称**：DevOps 复制者 (DevOps Copycats)

**反模式别名**：无

**反模式类别**： 策略反模式

**不良后果**： 完全复制别人的 DevOps 实践做法，而不进行分析和定制化。导致无法达到 DevOps 转型或者改进的效果。

**常见原因**：

1. 简单的复制成功企业的经验，而没有分析成功的上下文。
2. 成功的案例很少会展示失败的部分。
3. 没有度量机制进行改进。

**说明**：

在同一行业内发现成功案例会很容易错误的以为案例可以复制。缺乏对案例成功的上下文分析会导致同样的实践产生了不同的效果。因此，有必要分析自身的上下文和成功案例上下文的区别，或者进行试点以总结经验。以便更好的定制化 DevOps 实践。任何外部的实践都只具备参考意义。

对外部案例的尝试不算是 DevOps 复制者。DevOps 复制者的关键在于尝试后没有进行回顾复盘并不进行改变。

注意，**“DevOps 教条主义”**反模式可能会导致 **“DevOps 复制者”**反模式。但 **“DevOps 复制者”**反模式并不一定会导致 **"DevOps 教条主义"**反模式。**“DevOps 教条主义”**反模式的关键在于 DevOps 定义和实践是不继续发展的。而 **“DevOps 复制者”**反模式的关键在于 DevOps 不需要根据组织进行定制。

**修正模式**：定义你的 DevOps，DevOps 度量

**相关模式**：和该模式相关的其它模式，其它模式也会导致同样的反模式。

**相关反模式**：DevOps 教条主义

**相关引用**：相关资料的引用。

## 关于 DevOps 模式

DevOps 模式的索引在 Github 上开源，地址是 [https://github.com/wizardbyron/devops_patterns](https://github.com/wizardbyron/devops_patterns)

欢迎通过 issue 和pull request 提交你的建议。

你可以通过关注我的公众号了解 DevOps 模式和反模式，也可以加入我的付费知识星球“DevOps 模式” 和所有 DevOps 的实践者共同交流，我将在知识星球中定期回答那些最受关注的问题。
