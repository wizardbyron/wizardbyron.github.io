---
title: "【翻译】微服务和分布式对象第一法则"
date: 2022-03-30
tags:
- 翻译
- 微服务
---

> 本文源自 Martin Fowler 的 Bliki 上 2014 年的文章[Microservices and the First Law of Distributed Objects](https://martinfowler.com/articles/distributed-objects-microservices.html)

当我写《企业应用架构模式》一书时，我提出了一个我称之为**分布式对象设计第一法则**：“不要分布你的对象”。最近几个月业界对微服务的热情增加，让一些朋友对在微服务场景下对这一法则产生疑问，并且如果法则仍然成立，为什么我还要赞同微服务。

非常重要的一点就是我在第一法则中用了“分布式对象”的说法。它反映了一个在 90 年代末 00 年代初相当流行但此后（正确地）失宠的想法。分布式对象的想法是你可以设计对象并在进程内或远程选择使用相同的对象，远程则指的是在同一台机器的另外一个进程里，或者不同的机器里。比较聪明的中间件，比如，DCOM 或者一个 CORBA 实现，将会处理进程内或者远程之间的差别。因此你可以把你的系统拆分成以多个独立的进程来设计。

我对分布式对象概念的反对意见是：尽管逆可以在对象边界内封装许多东西，但逆不能封装远程/进程内的区别。 进程内函数调用很快并且总是成功（因为任何异常都是由于应用程序造成的，而不仅仅是由于进行调用的事实）。 但是，远程调用速度要慢几个数量级，并且由于远程进程或连接失败，调用总是有失败的可能。

![图](module-calls.png)

这种差异的结果是 API 的设计方式不同。 进程调用可以是细粒度的，如果你想要 100 个产品价格和库存，你可以调用你的产品价格函数 100 次，另外 100 次调用库存。 但是，如果该功能是一个远程调用，你最好将所有这些批处理在到一个调用中实现，一次调用所有 100 个价格和库存。 这会导致产品对象的界面有很大差异。 因此，你不能采用相同的类（主要是和接口相关）并以进程内或远程方式透明地使用它。

与我交谈过的微服务倡导者非常清楚这种区别，而且我还没有听到他们谈论进程内/远程调用的透明性。 所以他们并没有试图做分布式对象试图做的事情，因此不违反第一定律。 相反，他们提倡通过 HTTP 或轻量级消息和文档进行粗粒度交互。

所以本质上，我对分布式对象的看法和微服务的倡导者们对微服务的看法并不矛盾。 尽管存在这种基本的非冲突，但现在还需要提出另一个问题。 微服务意味着小型分布式单元通过远程连接进行通信，这比单体应用要多得多。这不违反第一定律的精神，即使它符合它的字面意思吗？

虽然我承认有正当理由为许多系统进行分布式设计，但我确实认为分布式是复杂性的助推器。 粗粒度的 API 比细粒度的 API 更尴尬。 你需要决定如何处理远程调用失败以及一致性和可用性的后果。 即使你通过协议设计最小化远程调用，仍然需要更多地考虑它们的性能问题。 在设计单体应用时，你必须担心模块之间的职责划分，而对于分布式系统，你必须担心模块之间的职责分配和分布因素。

虽然小型的微服务确实更加简单，但我担心这会将复杂性推向服务之间的通信，由于通信的不明确，因此更难发现问题。 当你必须跨越远程边界进行重构时，会更加困难。 微服务倡导者吹捧你会从异步通信中降低耦合，但异步是另一个复杂性助推器。千篇一律的扩展允许你在不增加分布式复杂性的情况下处理海量请求。

因此，我对分布式持谨慎态度，我是倾向整体设计。 鉴于此，为什么我要花费大量精力来描述微服务并支持倡导它的同事？ 答案是因为我知道我的直觉并不总是正确。我不能否认许多团队已经采用了微服务方法并取得了成功，无论是像 Netflix 和（可能）亚马逊这样的知名公共案例，还是我在 Thoughtworks 内外都与之交谈过的各种团队。 我天生就是一个经验主义者，相信经验证据胜过理论，即使这个理论比我的直觉要好得多。

并不是说我认为这件事已经有定论了。在软件交付中，成功是一件很难定义的事情。尽管像 Netflix 和 Spotify 这样的组织已经大肆宣传他们早先在微服务上的成功，但也有像 Etsy 或 Facebook 这样的例子在单体架构上取得了成功。无论团队认为自己使用微服务多么成功，唯一真正的比较是违反事实的——如果他们使用单体的方式构建应用会更好吗？微服务方法只出现了相对较短的时间，所以我们没有太多证据来自十年前的遗留微服务架构。但可以将微服务与我们非常不喜欢的那些古老的单体应用进行比较。并且可能存在我们尚未确定的因素，这意味着在某些情况下单体应用更好，而其他情况则有利于微服务。鉴于在软件开发中收集证据的困难，即使在多年过去之后，也很可能不会做出有利于其中一个或另一个的令人信服的决定。

鉴于这种不确定性，像我这样的作家能做的最重要的事情就是尽可能清楚地传达我们认为我们已经学到的教训，即使它们是矛盾的。 读者将自己做出决定，而作为作家，我们的工作是确保这些决定是明智的，无论他们落在架构决策的哪一边。

（完）
