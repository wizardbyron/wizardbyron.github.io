---
title:  DevOps发展的九个趋势
date: 2017-05-02
tags:
- 技术雷达
- Kubernetes
- Service Mesh
- Docker
- Python
---

DevOps 包含了太多方面的技术和实践，很难通过一个统一的工具链来描述其发展。即便如此，我们仍然可以从 ThoughtWorks 技术雷达的条目变动中看出一些趋势。今年，我有幸作为主编参与了最新一期技术雷达的翻译，作为 DevOps 的爱好者，十分高兴能在这一过程中看到 DevOps 未来发展的几个趋势，总结成了这篇文章。

## 趋势1：微服务目前仍然是 DevOps 技术应用和发展的主要领域

微服务将单块应用系统切割为多个简单独立的应用。从技术上说，这是通过工具把应用程序的内部复杂度转化为外部复杂度，需要一系列工具支撑微服务本身以及服务之间的通信。从组织上说，微服务团队要满足“快速发布，独立部署”的能力，则必须具备 DevOps 的工作方式。

如何拆解微服务一直是微服务技术应用的最大难点之一，领域驱动设计是比较理想的微服务拆解方法论。社会化代码分析帮助团队通过更精确的数据找到更加合适的拆分点。[CodeScene](https://codescene.io/)是一个在线服务，它能帮助识别出热点和复杂且难以维护的子系统，通过分析分布式子系统在时间上的耦合发现子系统之间的耦合。此外，它还能帮你认识组织中的康威定律，这会大大降低微服务解耦的难度。

此外，微服务系统本质上是一个分布式系统，分布式系统之间的通信一直是很重要的问题。本期介绍的[Kafka
Streams](http://docs.confluent.io/3.0.0/streams/)和[OpenTracing](http://opentracing.io/)就是这类技术的条目。Kafka 作为一个成熟的分布式消息系统已经被广泛采用，而 Kafka Streams 则将最佳实践以“库”的方式呈现给开发人员，使得操作 Kafka 更加自然和简单。而 OpenTracing 则弥补了跨越多个微服务之间请求追踪的空白。

另一方面，**无服务器风格的架构（Serverless architecture ）**把 DevOps 技术在微服务领域的应用推向极致。当应用程序执行环境的管理被新的编程模型和平台取代后，团队的交付生产率得到了进一步的提升。一方面它免去了很多环境管理的工作，包括设备、网络、主机以及对应的软件和配置工作，使得软件运行时环境更加稳定。另一方面，它大大降低了团队采用 DevOps 的技术门槛。然而，端到端的交付以及微服务中的函数管理问题日渐突出，尽管[AWS API gateway](https://aws.amazon.com/api-gateway/)和[AWS Lambda](https://aws.amazon.com/lambda/)几乎成了 Serverless 架构的代名词，但这二者结合的开发者体验并不佳。于是出现了[Serverless framework](https://serverless.com/)和[CLAUDIA](https://claudiajs.com/)这样的管理工具。

AWS Lambda 带来的优势也深深影响了企业级应用领域，[Apache OpenWhisk](http://openwhisk.org/)就是企业级无服务器领域的选择之一，它使得企业级应用也可以采用无服务器风格的架构构建应用程序。

在微服务端到端交付流程上，Netflix 开源了自家的[Spinnaker](http://www.spinnaker.io/)，Netflix 作为微服务实践的先锋，不断推出新的开源工具来弥补社区中微服务技术和最佳实践的缺失。 而[Spring Cloud](http://cloud.spring.io/)则为开发者提供了一系列工具，以便他们在所熟悉的 Spring 技术栈下使用这些服务协调技术(coordination techniques)，如服务发现、负载均衡、熔断和健康检查。

而在微服务的安全上，最常见的需求之一是通过身份验证和授权功能来保护服务或 API。 这部分功能往往是最重要且不断重复构造的。而[Keycloak](http://www.keycloak.org/)就是一个开源的身份和访问管理解决方案，用于确保应用程序或微服务的安全。且几乎不需要编写代码，开箱即用。它支持单点登录，社交网络登录和标准协议登录(如 OpenID Connect ， OAuth2 和 SAML 等)。

## 趋势2：以 Docker 为核心的数据中心方案逐渐走向成熟

在过去的两年，Docker 社区有了突飞猛进的发展，似乎每期技术雷达都会出现 Docker 相关的条目。而 Docker 往往和 DevOps 联系起来，被认为是推动 DevOps 发展的杀手级工具，以至于有些人会以团队是否采用 Docker 作为团队是否具备 DevOps 能力的标志。

而这一社区的创新数量则日渐平缓。一方面，开源社区激烈的竞争淘汰了一部分技术。另一方面，以 Docker 为中心的完整数据中心解决方案在不断的整合开源社区的零散工具并形成最佳实践。为端到端的开发和运维提供更完整的交付体验，各大厂商也相继开始推广自己的企业级整体收费解决方案，这表明 Docker 的使用已经走向成熟。

在本期的技术雷达里的条目中出现了[Mesosphere DC/OS](https://mesosphere.com/product/)，这是构建统一技术栈数据中心的一个征兆。在这方面[Docker EE](https://docs.docker.com/enterprise/)和[Rancher](http://rancher.com/)都是非常有力的竞争者。根据我的判断，在未来的 Docker 社区里，统一容器化数据中心的竞争者将会进一步减少。而之前的私有云方案则慢慢会被“以 Docker 为核心数据中心级全栈交付”取代。

## 趋势3：不完整的 DevOps 实践阻碍着 DevOps 的发展

很遗憾看到[单一持续集成实例](https://www.thoughtworks.com/radar/techniques/a-single-ci-instance-for-all-teams)和[不完整的持续集成](https://www.thoughtworks.com/radar/techniques/ci-theatre)（[CI Theatre](https://www.thoughtworks.com/radar/techniques/ci-theatre)）这样的条目出现在技术雷达里。可以感到企业应用 DevOps 技术的紧迫性。这同时也暴露了 DevOps 领域里“缺乏门槛较低且成熟的 DevOps 实践”的问题。

大部分企业在 DevOps 转型中仅仅关注到了工具的升级。却忽视了价值流、生产流程中各个活动中的最佳实践以及 DevOps 团队文化的构建，这会使团队陷入 “已经完成 DevOps 转型的假象 ”，而停止了团队的自我改进。

DevOps 的实践包含组织改进和技术升级两个部分，技术往往是最容易的部分。而缺乏组织改进的技术提升往往很难给组织带来质的飞跃。具备 DevOps 文化的团队则会不断反思和学习，通过共担责任和相互合作不断完善组织的 DevOps 实践。

## 趋势4：领域特定的 DevOps 实践开始出现

DevOps 的最早实践来自于互联网企业的 Web 应用，相应的思想被引入企业级应用并促进了一系列工具的发展。虽然并不是每一种应用软件交付形式都适合 DevOps，但随着 DevOps 的工具不断成熟。其它领域的 DevOps
实践也开始尝试借鉴 Web 应用领域的自动化工具，并逐渐形成领域级的 DevOps 实践。

在人工智能领域，[TensorFlow](https://www.tensorflow.org/)就是这样一个例子，它可以有多种 DevOps 友好的安装和部署方式 ，例如采用 Docker 进行部署。

在区块链领域，超级账本([HYPERLEDGER](https://www.hyperledger.org/)) 就是这样一个例子，它提供了一套工具和服务，结合 DevOps 相关技术和实践形成了一个完整的解决方案。

随着 DevOps 相关概念和技术不断向各个产业领域的深入发展，可以看到 DevOps 技术和实践带来的巨大影响力。然而，每个技术领域都有自己所关注的特性，并不是以往的 DevOps 实践可以全覆盖到的，这恰恰成为了 DevOps 技术和实践发展的契机。我很期待领域特定的 DevOps 技术实践给 DevOps 带来的发展。

## 趋势5：采用 DevOps 进行技术债务重组和技术资产管理

技术债务类似于金融债务，它也会产生利息，这里的利息其实就是指由于鲁莽的设计决策导致需要在未来的开发中付出更多的努力。投资银行业往往采用多种金融工具组合的方式来处理企业的不良债务。而清理技术债务的实践和工具却乏善可陈。

技术债务不光阻碍了企业通过新技术带来便利，还使企业偿还技术债务所承担的成本越来越高，例如技术人才的流失，技术利息等综合性风险。

虽然极少会出现企业因技术债务而走向衰败的案例，但新晋企业凭借新技术和商业模式颠覆传统行业并夺取市场份额的报道却不断发生。这从另一方面说明技术债务综合提升了采用新技术的机会成本，使企业不断失去创新和领先的巨大潜力。

DevOps 技术栈的多元化为分散遗留系统技术债务风险提供了一套灵活而又低风险的工具和方法论。不断帮助企业从遗留系统的负担中解脱出来。

而微服务则是首先通过领域拆分技术债，并用相应工具重组技术债。分离优质技术资产和不良资产，通过分散风险来降低抛弃成本。而将API 当做产品([APIs as a product](https://www.thoughtworks.com/radar/techniques/apis-as-a-product))可以从一个全新的演进视角去看待技术债，通过可用性测试和用户体验研究帮企业剥离出技术债务中的优质资产和不良资产。

另一方面，本期技术雷达中出现了[封装遗留系统](https://www.thoughtworks.com/radar/techniques/legacy-in-a-box)这样的实践，它往往配合着 Vagrant ， Packer 和 Docker
这样的工具一起使用。一方面它将技术债务的风险进行了隔离，另一方面它防止了遗留系统上产生的技术债利息的增长。

## 趋势6：安全成为推动 DevOps 全面发展的重要力量

安全是 DevOps 永远绕不开的话题，也往往是新技术在传统行业（例如金融和电信）应用中的最大阻碍。一方面，组织结构的转型迫使企业要打破原先的部门墙，这意味着很多原先的控制流程不再适用。另一方面，由于大量的 DevOps 技术来源于开源社区，缺乏强大技术实力的企业在应用相关技术时不免会有所担忧。

从代码中解耦秘密信息的管理则让我们避开了一些开发过程中可能会产生的安全隐患。采用[git-crypt](https://github.com/AGWA/git-crypt)这样的工具可以帮我们保证在开发的过程中源代码内部的信息安全。而采用[HashiCorp Vault](https://www.vaultproject.io/)则提供了脱离应用程序代码的秘密信息存储机制，使得应用在运行过程中的秘密得到了有效保护。

Linux Security Module 则一直在技术雷达的“采用”区域，通过 SELinux 和 AppArmor 这样的 LSM
兼容帮助团队评估谁可以访问共享主机上的哪些资源(包括其中的服务)。这种保守的访问管理方法将帮助团队在其SDLC流程中建立更好的安全性。以往这是 Ops 团队需要考虑的问题，而对 DevOps 的团队来说，这是每一个人的事情。

**“合规性即代码”（Compliance as Code）** 是继“基础设施即代码”，“流水线即代码”之后的又一种自动化尝试。[InSpec](https://github.com/chef/inspec)作为合规性即代码的提出者和实现者，通过自动化手段确保服务器在部署后的运维生命周期中依然保持安全与合规。它所带来的意义在于将规范制度代码化，得到了确定性的结果和解释。

在不远的将来，不难想象人们所面对的法律和法规规定不再是一堆会导致歧义的语言文字条目，而是一组由自动化测试构成的测试环境。

安全性和易用性往往被认为是鱼与熊掌不可兼得的两个方面。在 DevOps 之前，团队吞吐量和系统稳定性指标曾经也面临这样的境遇，然而 DevOps 使得二者可以兼得。同样我也有信心看到在未来 DevOps 的领域里，更多易用且安全的工具将会不断出现。在降低 DevOps 所带来的安全风险的同时，也提升团队开发过程的顺畅性和用户便利性。

## 趋势7：Windows Server 和 .NET平台下的 DevOps 技术潜力巨大

长期以来，Windows 和 .NET平台下的 DevOps 一直都是一个被低估的领域。一方面，社区缺乏对 Windows  Server 平台的兴趣。另一方面，[Windows Server 却有接近 90% 的市场占用率](https://community.spiceworks.com/networking/articles/2462-server-virtualization-and-os-trends)，在 Web 服务器领域则有[33.5% 的市场占有率](https://w3techs.com/technologies/overview/operating_system/all)。

有充足理由证明这是一个潜力巨大的市场。 我们看到了[CAKE 和 FAKE](https://www.thoughtworks.com/radar/tools/cake-and-fake)这样的条目，作为 .NET 平台下替代 MSBuild 的构建解决方案， 它增强了 .NET 平台自动化方面的能力。而[HANGFIRE](https://github.com/HangfireIO/Hangfire)则提供了更易用和灵活的自动化进程调度框架。我很期待未来有更多 Windows Server 和 .NET 平台 领域的创新。不久前，Docker 已经可以在
Windows 下运行。可以预见到，Windows Server 和 .NET 平台将会是下一阶段 DevOps 技术实践中值得深入发掘的领域。

## 趋势8：非功能性自动化测试工具的逐渐完备

技术能力高低的重要指标，尤其是针对生产环境应用程序的非功能性自动化测试工具。一直以来，技术雷达都在尝试从不同的角度宣扬自动化测试的重要性，从软件的开发阶段延展到了整个应用生命周期甚至整体 IT 资产的管理上。

这期的技术雷达仍然关注了非功能性自动化测试，[TestInfra](https://github.com/philpep/testinfra) 是 ServerSpec 的 Python 实现，它使得用Pytest测试基础设施成为可能。而[MOLECULE](https://github.com/metacloud/molecule)旨在帮助开发和测试 Ansible 的 Role 。通过 在虚拟机或容器上为正在运行的 Ansible Role 测试构建脚手架，无需再手工创建这些测试环境。 正如技术雷达所说的：“虽然这是一个相当年轻的项目，但我们看到了其蕴含的巨大潜力。”

## 趋势9：Python 成为 DevOps 工作中采用的首要编程语言

早在 DevOps 刚刚开始盛行的时候，Python 就是一个被寄予厚望的语言，因为大部分 DevOps 工具和实践都需要用到 Python。虽然也有人尝试用 Ruby 或者 NodeJS 构建 DevOps 工具，然而都没有 Python 所构建的工具流行。与此同时，仍然不断有人把其它语言下编写的工具转化为 Python 的版本，TestInfra 就是这样一个例子。

随着 Python 在大数据、人工智能、区块链、微服务以及 Docker 中的发展，可以预见 Python 在日后的领域仍然会发挥重要的作用。

以上对 DevOps 趋势的解读仅为个人观点，如有不当之处还望指出，关于更多技术在技术

雷达中的使用建议请参考[https://www.thoughtworks.com/radar/a-z](https://www.thoughtworks.com/radar/a-z)。
