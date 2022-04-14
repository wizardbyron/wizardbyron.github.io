---
title: "【翻译】蓝绿部署的起源"
date: 2022-04-14
tags:
- 翻译
- DevOps
---

> 原文: <http://timothyfitz.com/2009/02/08/continuous-deployment/>

蓝绿部署的故事，就像经常发生的那样，是关于辅导一个棘手的客户。我领导的构建团队发现测试环境和生产环境之间存在很多差异。（每个测试环境之间也存在差异，但这是另一类模式！）

我们认为检查版本的最安全方法是将应用程序一起部署到与实时系统相同的物理机上。 我们的应用正在运行具有“域”概念的 WebLogic 上，“域”只是一个存放应用程序文件的目录。 我们会将新版本部署在相邻的目录中，我们称之为“影子域”（它有一个漂亮的幻想：“准备发布影子域！”等），并将这个应用绑定到本地另一个端口，然后直接连接到端口进行冒烟测试。 如果我们对部署感到满意，我们就可以切换前端控制器（在本例中是一个 Apache 服务器）指向新部署的应用。如果出现任何问题，我们可以通过修改控制器指向当前实例立即回滚，前提是我们没有进行任何破坏性的数据库更改 .

We thought about calling these side-by-side environments A and B, until someone pointed out that if the application broke and it happened to be deployed in the B environment, the first question would be “Why weren’t you using the A environment?” Because clearly A is better than B! We needed labels for the domains that didn’t have an obvious hierarchy, and we settled on colours. If your domains are called Blue, Green, Orange, Yellow, etc. then there isn’t an obviously “best” one. We avoided having a Red domain because that just sounded dangerous. (“You were running in RED??”)

我们考虑过将这组并排的环境称之为 A 环境和 B 环境，直到有人指出如果应用程序崩溃并且它恰好部署在 B 环境中，第一个问题将是“你为什么不使用 A 环境 ？” 因为显然 A 比 B 好！ 我们需要没有明显层次结构的方法来给域打标签。因此我们选择了颜色。如果你的域被称为蓝色、绿色、橙色、黄色等，那么显然没有“最好”的。 我们避免使用红色域，因为这听起来很危险。 （“你在红域中运行？？”）

最后我们只使用了两个域——我们曾认为我们可能有几个颜色候选并轮换，但我们发现有两个就足够了——恰好是蓝色和绿色。当我们开始为《持续交付》一书命名模式时，“蓝绿部署”这个名字在团队中有点流行。 我认为 Jez Humble 和我自己都这么称呼它，而客户并没有被这个提法吓坏。

十多年后的现在这很有趣，并成为了常见用语。

（完）
