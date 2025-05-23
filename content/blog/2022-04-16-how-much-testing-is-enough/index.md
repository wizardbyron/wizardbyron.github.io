---
title: "【翻译】做多少测试才足够"
date: 2022-04-16
tags:
- 翻译
- 测试
---

> 原文: <https://testing.googleblog.com/2021/06/how-much-testing-is-enough.html>

每个软件开发人员和团队都要面临的一个熟悉问题是：“发布一个版本要做多少测试才足够？”

这个问题的答案很大程度上取决于软件的类型、用途和目标受众。相比测试智能手机中“手电筒”这种简单的应用程序，人们会期望用一种更严格的方法来测试商业搜索引擎。然而，无论是什么应用，做多少测试才足够的问题很难有一个明确的答案。更好的办法是为当下的情况提供一组用于定义质量验证过程和测试策略的考虑因素或规则。下面提供了一个有用的评估项列表：

- 记录你的测试过程或策略
- 拥有坚实的单元测试基础
- 不要吝啬集成测试
- 对关键用户旅程执行端到端测试
- 理解并实施其他层次的测试
- 了解你的代码和功能覆盖率
- 利用现场反馈来改进测试流程

## 记录你的测试过程或策略

如果你已经在测试产品，请记录下整个过程。这对于未来发布版本的重复测试及其质量改进分析至关重要。如果这是你第一次发布软件，有一个书面的测试计划或测试策略是一个好主意。事实上，任何产品设计都应该有书面的测试计划或策略。

## 拥有坚实的单元测试基础

一个很好的测试起点是随同代码编写单元测试。单元测试会测试功能单元级别的代码。外部服务的依赖采用 Mock 或者 Fake 的方式处理。

**Mock**有与生产环境上的依赖服务相同的接口，但这种方法仅检查对象是否根据期望和返回由测试本身控制的值，而不会完整实现依赖项的功能。

**Fake**是依赖项的轻量级实现，但理想情况下它自己应当没有依赖。

Fake 提供了比 Mock 更广泛的功能，并且应该由提供该依赖项生产环境的团队维护。这样一来，随着依赖项的更新，Fake 和单元测试的编写者对 Fake 完整反映了生产环境的功能是充满信心的。

包括 Google 在内的许多公司，都会要求代码变更必须通过相应的单元测试用例这一最佳实践。并且随着代码库的扩大，在提交代码之前执行大量单元测试是在 Bug 引入代码库之前捕获它们的重要措施。 这可以节省以后编写集成测试、调试以及验证对当前代码修复的时间。

## 不要吝啬集成测试

随着代码库的增长，一定会到达一个点，可以把一组功能单元作为一组进行测试。这时候就该拥有一个坚实的集成测试基础了。一个集成测试需要一些功能单元，通常只有两个功能单元，作为一个整体来测试它们的行为，验证它们是否可以协同工作。

开发人员通常认为可以降低集成测试的优先级甚至跳过编写集成测试，这有利于完整的端到端测试。 毕竟，后者真正测试了用户使用产品的行为。 然而，拥有一套全面的集成测试与拥有坚实的单元测试同样重要（请参阅早期的 Google 博客文章：Fixing a test hourglass）。

由于集成测试比完整的端到端测试的依赖更少。因此，集成测试需要较少的资源。这比拥有完整依赖项的端到端测试更快、更可靠（请参阅早期的 Google 博客文章，Test Flakiness - One of the main challenges of automated testing）。

## 为关键用户旅程（Critical User Journeys）执行端到端测试

目前为止的讨论涵盖了在产品组件级别的测试，首先作为单个组件（单元测试），然后作为一组组件及其依赖项（集成测试）。现在是时候像用户一样端到端地测试产品了。 这一点非常重要，因为不仅要测试独立的功能，还要测试包含其他功能的整个流程。 在谷歌，这些工作流程（关键目标和用户为实现该目标而执行的任务旅程的组合）被称为关键用户旅程 (Critical User Journeys，CUJ)。 理解 CUJ 并记录整个流程，然后使用端到端测试（理想情况下是以自动化方式）完成整个自动化测试测试金字塔。

## 理解并实施其他层次的测试

单元测试、集成测试和端到端测试解决了产品的功能级别的测试。 了解其他层的测试也很重要，包括：

- 性能测试 - 度量你的应用或服务的延迟和吞吐量。
- 压力或伸缩性测试 - 在越来越高的压力下测试你的应用或服务。
- 容错性测试 - 测试你的应用的行为在不同的依赖失效或者全部宕机是否正常。
- 安全测试 - 测试您的服务或应用程序中的已知漏洞。
- 可访问性测试 - 确保产品可供所有人使用和使用，包括各种残障人士。
- 本地化测试 - 确保产品可以在特定语言或地区使用。
- 国际化测试 - 确保产品可以被世界各地的人们使用。
- 隐私测试 - 评估和转移产品中的隐私风险。
- 可用性测试 - 测试产品对用户的友好性。

同样，重要的是要在你的评审周期中尽早执行这些测试过程。较小的性能测试可以更早地检测到问题回归，并节省端到端测试期间的调试时间。

## 理解你的代码和功能的测试覆盖率

到目前为止，我们已经从定性的角度研究了做多少测试足够的问题。对不同类型的测试进行了回顾，并总结出较小和较早的测试比较大或较晚的更好。接下来将采用代码覆盖率从定量的角度继续研究这个问题。

Wikipedia 有一篇关于代码覆盖率的精彩文章，讨论了不同类型的覆盖率，包括语句（Statement）、边界（Edge）、分支（Branch）和条件（Condition）等覆盖率。 有一些开源工具可用于度量大多数流行编程语言（如 Java、C++、Go 和 Python）的测试覆盖率。以下是部分工具的列表：

| 语言   | 工具                      |
| :----- | :------------------------ |
| Java   | JaCoCo                    |
| Java   | JCov                      |
| Java   | OpenClover                |
| Python | Coverage.py               |
| C++    | Bullseye                  |
| Go     | 内置覆盖率支持(go -cover) |

表1 - 不同编程语言的开源代码覆盖率工具

这些工具中的大多数都以百分比形式提供覆盖率摘要。 例如，80% 的代码覆盖率意味着 80% 的代码被测试覆盖，20% 的代码未被测试覆盖。 同时，重要的是要理解，即便测试覆盖了特定的代码段，这段代码仍然可能出现 Bug。

覆盖率里有一个概念称为变更列表覆盖率。 变更列表覆盖率度量修改或添加代码行数的覆盖率。对于那些累积了技术债务且覆盖率低的代码库来说，这个指标对拥有这样代码库的团队很有用。这些团队可以制定一项政策，通过增加他们的增量测试覆盖率来促进整体的覆盖率提升。

到目前为止，对覆盖率的讨论集中在测试对代码（函数、行）的覆盖。另一种类型的覆盖率是特性或行为的覆盖。

- 对于特性覆盖，重点是识别特定版本中包含的特性并为其实现创建测试。
- 对于行为覆盖，重点是识别 CUJ 并创建适当的测试来追踪整个流程。

同样，了解您“未被覆盖”的特性和行为是帮助你理解风险的有用指标。

## 利用现场反馈来改进测试流程

了解和改进质量验证过程的一个非常重要的部分是软件发布后的直接反馈。拥有一个跟踪中断、Bug和其他问题的流程，以及改进质量验证的行动项列表，对于最大限度地降低后续版本中的回归风险至关重要。
此外，改进行动项列表应该：

- 强调在质量验证过程中尽早填补测试缺口。
- 解决策略问题，例如缺乏特定类型的测试，例如负载或容错测试。

这就是为什么记录质量验证过程很重要，它可以让你根据现场获得的数据重新评估整个过程。

## 总结

创建全面的质量流程和测试策略来回答“做多少测试才足够？”这个问题，也许是一项复杂的任务。希望这里给出的提示可以对你有所帮助。 总之：

- 记录你的测试过程或策略
- 拥有坚实的单元测试基础
- 不要吝啬集成测试
- 对关键用户旅程执行端到端测试
- 理解并实施其他层次的测试
- 了解你的代码和功能测试覆盖率
- 利用现场反馈来改进测试流程

（完）
