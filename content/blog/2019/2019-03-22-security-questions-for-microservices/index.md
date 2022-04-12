---
title: 【翻译】微服务安全：所有应该被问到的问题
date: 2019-03-22
tags:
- 安全
- 微服务
---

> 本文节选自 [Graham Lea](http://www.grahamlea.com) 的博客：[Microservices Security: All The Questions You Should Be Asking](http://www.grahamlea.com/2015/07/microservices-security-questions/)

GitHub（含中文翻译）地址：[https://github.com/wombat-bros-sisters/answers-to-microservices-security-questions](https://github.com/wombat-bros-sisters/answers-to-microservices-security-questions)

以下是我的问题列表, 您和您的团队应该向自己询问有关微服务安全性的问题。它旨在用作评估您自己的系统和流程的清单。希望你会发现你已经涵盖了这些问题中的大多数, 但总是有更多的东西需要学习。每个问题之后都有一个相关内容的链接。

## 核心服务（Core Services）

(我指的是组成您的系统的服务, 不与互联网或其他外部系统接口)

1. 您是否只是在互联网边界保护您的系统？([纵深防御](https://www.us-cert.gov/bsi/articles/knowledge/principles/defense-in-depth))
2. 如果入侵者进入您的核心网络, 您有哪些保护措施？([纵深防御](https://www.us-cert.gov/bsi/articles/knowledge/principles/defense-in-depth))
3. 网络中的某个人在多大程度上可以轻松地访问您的服务之间的流量？([安全通信](https://en.wikipedia.org/wiki/Secure_communication))
4. 您的服务之间是不是过于相互信任？或者，你的服务是不是无条件相信高频调用者(您确定只有您自己的服务可以调用您自己的服务吗？)([勉强信任](https://www.us-cert.gov/bsi/articles/knowledge/principles/reluctance-to-trust))
5. 当您的服务被调用时, 它是否要求调用方对进行身份验证, 或者它是否允许任何连接请求？(服务认证)
6. 您的服务是让调用者访问服务提供的所有 API, 还是只允许他们访问履行其功能所需的 API？(服务授权)
7. 在客户端发起每个调用请求的人的身份是否会传递到您的内部服务中, 还是在网关中丢失？(当事人传播)
8. 您的服务是否可以相互请求任何数据, 或仅请求授予其权限的用户的数据？(当事人授权)
9. 如果攻击者拥有某个服务, 他们是否可以很容易地从其下游服务中请求任何内容？(当事人授权)
10. 您有什么保证措施从经过身份验证的用户收到的请求没有被篡改？(防篡改)
11. 您如何确保第二次发送的授权请求被检测和拒绝？([重播保护](https://en.wikipedia.org/wiki/Replay_attack))
12. 是不是每个人都理解 [SQL 注入](https://www.owasp.org/index.php/SQL_Injection)？您有哪些措施来确保没有人编写容易受到 [SQL 注入](https://www.owasp.org/index.php/SQL_Injection)的代码？([SQL 注入](https://www.owasp.org/index.php/SQL_Injection))
13. 您是否熟悉所有其他类型的注入, 以及如何预防？([SQL 之外的注入](https://www.owasp.org/index.php/Top_10_2013-A1-Injection))
14. 您是否掌握了[密码存储](http://www.troyhunt.com/2012/06/our-password-hashing-has-no-clothes.html)的最新状态？([密码存储](http://www.troyhunt.com/2012/06/our-password-hashing-has-no-clothes.html))
15. 您是否意识到, 如果您的密码数据库被盗, 如今简单的撒盐加密是完全无用的？([密码存储](http://www.troyhunt.com/2012/06/our-password-hashing-has-no-clothes.html))
16. 如果您需要升级[密码存储](http://www.troyhunt.com/2012/06/our-password-hashing-has-no-clothes.html)算法, 如何在不对用户造成大规模干扰的情况下进行升级？([密码存储](http://www.troyhunt.com/2012/06/our-password-hashing-has-no-clothes.html))
17. 如何积极识别数据库中的私有和敏感数据？([私隐提升](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/promoting-privacy))
18. 如果您的数据被盗, 您有哪些保护措施来防止最敏感的部分被读取？(私人和敏感数据)
19. 如果您的服务使用的是私钥, 如何保护这些密钥不被入侵者使用？([密钥管理](https://en.wikipedia.org/wiki/Key_management), [千万不要以为您的秘密是安全的](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/never-assuming-that-your-secrets-are-safe))
20. 您知道什么是硬件安全模块 ([Hardware Security Module，HSM](https://en.wikipedia.org/wiki/Hardware_security_module)), 以及何时以及如何使用硬件安全模块吗？([密钥管理](https://en.wikipedia.org/wiki/Key_management))
21. 您有哪些日志记录可用于检测和分析安全漏洞？(安全日志记录/[安全信息和事件管理 (Security Information and Event Management ，SIEM)](https://en.wikipedia.org/wiki/Security_information_and_event_management))

## 中间件（Middleware）

(我指的是您在系统和界面中运行的任何第三方软件。在我的公司里, 目前这主要是我们的数据库和邮件系统, 但它可能包括其他系统, 例如 bpm 和 中间件。这些问题大多也适用于集成的外部软件。

1. 您是否在所有服务中共享一个数据库登录权限？([最少特权](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/least-privilege))
2. 您的服务可以访问多少数据？是所有的？还是只有他们必须的？([最少特权](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/least-privilege))
3. 如果攻击者获得了一个服务的数据库凭据, 他们将获得多少数据？([最少特权](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/least-privilege))
4. 您的数据库授权策略是否允许更新和删除应用程序仅插入到的表？([最少特权](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/least-privilege))
5. 您是否在所有服务中共享单个消息传递中间件登录？([最少特权](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/least-privilege))
6. 您的消息传递中间件是否也有登录凭据？(有些还没有!)([最少特权](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/least-privilege))
7. 您的服务是否有权访问系统中的所有消息, 还是只能访问他们需要查看的邮件？([最少特权](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/least-privilege))
8. 您的服务是否可以将消息发送到任何队列, 或仅将消息发送到所需的队列？([最少特权](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/least-privilege))
9. 如果攻击者掌握了一个消息服务的凭据, 他们可以访问多少数据？([最少特权](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/least-privilege))
10. 如果攻击者掌握了一个消息服务的凭据, 他们可以启动哪些操作？([最少特权](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/least-privilege))
11. 如果您使用登录凭据保护数据库和消息, 如何保护凭据？([千万不要以为你的秘密是安全的](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/never-assuming-that-your-secrets-are-safe))
12. 架构中的遗留系统如何使其他服务处于危险之中？([保护最薄弱的环节](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/securing-the-weakest-link))

## 边缘服务（Edge Services）

(我指的是与互联网或其他外部管理的第三方系统接口的服务)

1. 您是否已将 TLS 实现升级到最新版本？([安全通信](https://en.wikipedia.org/wiki/Secure_communication))
2. 您是否配置了 TLS 以消除降级和弱密码攻击？([安全通信](https://en.wikipedia.org/wiki/Secure_communication))
3. 您的员工中谁知道有关 TLS 的所有信息, 以及如何安全地配置 TLS？([安全通信](https://en.wikipedia.org/wiki/Secure_communication))
4. 如何确保您的内部网站和管理员网址不会意外地打开到互联网上？
5. 我可以从网关服务的未经身份验证的 api 中获取哪些信息？([枚举](https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Authentication_and_Error_Messages))
6. 我有一个破解密码和用户电子邮件的列表。我可以使用您的密码提醒 url 来测试您的系统中的哪些用户吗？([认证](https://www.owasp.org/index.php/Top_10_2013-A2-Broken_Authentication_and_Session_Management))
7. 您的系统其他部分是否过于信任您的网关服务？([勉强信任](https://www.us-cert.gov/bsi/articles/knowledge/principles/reluctance-to-trust))
8. 如果您假设您的网关服务已被完全破坏, 您在其他地方会有什么不同的做法？([纵深防御](https://www.us-cert.gov/bsi/articles/knowledge/principles/defense-in-depth))
9. 如果网关服务被完全破坏, 可以从内存中收集哪些数据？([纵深防御](https://www.us-cert.gov/bsi/articles/knowledge/principles/defense-in-depth))
10. 如果网关服务被完全破坏, 可以从网络流量中捕获哪些数据？([纵深防御](https://www.us-cert.gov/bsi/articles/knowledge/principles/defense-in-depth))

## Web 和其他客户端（Web & Other Clients）

(我指的是您可能会也可能不创作与服务器端系统接口的软件, 很可能是通过 internet)

1. 您如何帮助您的用户选择更安全的密码？([密码复杂性](http://www.troyhunt.com/2011/04/bad-passwords-are-not-fun-and-good.html))
2. 当输入密码错误时, 您会给出什么反馈？它是否可以用来[枚举](https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Authentication_and_Error_Messages)用户帐户？([枚举](https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Authentication_and_Error_Messages))
3. 在多次登录尝试失败后, 是否锁定帐户？([认证](https://www.owasp.org/index.php/Top_10_2013-A2-Broken_Authentication_and_Session_Management))
4. 您给攻击者多少机会猜测每个帐户的密码？(账户安全)
5. 当您锁定帐户时, 您会给出哪些反馈？它是否可以用来[枚举](https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Authentication_and_Error_Messages)用户帐户？([枚举](https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Authentication_and_Error_Messages))
6. 您是否有密码提醒功能？是否可以使用它来[枚举](https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Authentication_and_Error_Messages)用户帐户？([枚举](https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Authentication_and_Error_Messages))
7. 您是否有密码重置功能？是否可以使用它来[枚举](https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Authentication_and_Error_Messages)用户帐户？([枚举](https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Authentication_and_Error_Messages))
8. 您是否考虑过您的系统或系统的某些部分是否需要多重身份验证？([枚举](https://www.owasp.org/index.php/Authentication_Cheat_Sheet#Authentication_and_Error_Messages))
9. 是否还有人注意到安全和良好的用户体验之间似乎有一场史诗般的战斗？(UX vs 安全)
10. 您熟悉 owasp 十大网络漏洞吗？([网络安全缺陷](https://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project#tab=OWASP_Top_10_for_2013))
11. 您能说出所有 owasp 十大网络漏洞的名称吗？([网络安全缺陷](https://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project#tab=OWASP_Top_10_for_2013))
12. 你的团队中的每个人都能说出所有 owasp 前十名的名字吗？([网络安全缺陷](https://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project#tab=OWASP_Top_10_for_2013))
13. 你团队中的每个人都能解释如何防范所有的 owasp 前十名吗？([网络安全缺陷](https://www.owasp.org/index.php/Category:OWASP_Top_Ten_Project#tab=OWASP_Top_10_for_2013))
14. 如何确保在用作输出时正确转义每一块用户数据？(xss/输出编码)
15. 如何正确地在输出用户数据的各种不同上下文中获取用户数据？(xss/输出编码)
16. 您如何帮助防止用户因使用 web 应用而受到攻击？
17. 您的 web 应用设计是否将浏览器视为不安全的环境？([勉强信任](https://www.us-cert.gov/bsi/articles/knowledge/principles/reluctance-to-trust))
18. 您的原生移动应用设计是否将设备视为不安全的环境？([勉强信任](https://www.us-cert.gov/bsi/articles/knowledge/principles/reluctance-to-trust))
19. 您如何帮助防止用户因使用本机应用而受到攻击？
20. 您在客户端上存储或缓存哪些数据？您如何保护它？如果有人窃取了这些数据, 会发生什么情况？它需要放在客户端吗？

## 人员和过程

(我指的是开发和操作您的系统的人员, 以及他们用来执行此操作的过程)

1. 你在做什么来确保安全被嵌入到你的工程团队所做的一切中去？([安全内建](https://www.bsimm.com/online/))
2. 你如何把共同的安全原则嵌入到每个人的大脑里？([安全原则](https://buildsecurityin.us-cert.gov/articles/knowledge/principles/design-principles))
3. 开发过程中明确内置了哪些安全活动？([安全软件开发过程](https://www.owasp.org/index.php/Secure_SDLC_Cheat_Sheet))
4. 您为开发人员、测试人员和操作人员提供哪些安全培训？(安全培训)
5. 技术人员是否只知道漏洞的名称, 还是真的知道如何利用和测试这些漏洞？(安全培训)
6. 您放置了哪些控制, 谁可以访问系统的哪些部分？([访问控制](https://en.wikipedia.org/wiki/Access_control))
7. 您有什么计划定期审查这些控制措施和人们的访问权限的适当性？(访问控制审核)
8. 您发现和修复第三方软件中的漏洞的过程是什么？([漏洞管理](https://en.wikipedia.org/wiki/Vulnerability_management))
9. 如何鼓励工程师将时间用于头脑风暴系统中的风险？(风险头脑风暴/"风险风暴")
10. 您是否有确保每项新服务都以极大的安全性启动的服务模板？(安全应用程序模板)
11. 让内部员工定期测试系统的安全性的计划是什么？([安全测试](https://en.wikipedia.org/wiki/Security_testing))
12. 你有什么计划, 你会多久引进一次外部安全专家, 你将如何选择他们关注的内容？([安全测试](https://en.wikipedia.org/wiki/Security_testing))
13. 你在哪些活动中得到了专家的帮助？只是渗透测试？设计和架构评论如何？([安全测试](https://en.wikipedia.org/wiki/Security_testing))
14. 您必须进行哪些自动测试来捕获编写漏洞的漏洞？([自动化安全测试](http://devops.com/2015/04/06/automated-security-testing-continuous-delivery-pipeline/))
15. 为了确保安全控制始终到位, 您必须进行哪些自动测试？([自动化安全测试](http://devops.com/2015/04/06/automated-security-testing-continuous-delivery-pipeline/))
16. 你们是否一直在问自己: "如果这个控制点失效了怎么办？下一个控制点是什么？ "([纵深防御](https://www.us-cert.gov/bsi/articles/knowledge/principles/defense-in-depth))

最后..

“ 假设您的网络受到威胁，你的系统的哪些部分会让你深夜加班？”
