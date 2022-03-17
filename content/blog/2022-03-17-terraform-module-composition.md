---
title: "【翻译】Terraform 最佳实践：模块组合"
date: 2022-03-06
tags:
- Terraform
- 基础设施即代码
---

原文：<https://www.terraform.io/language/modules/develop/composition>

在只有一个根模块的简单 Terraform 配置中，我们创建一组资源并使用 Terraform 的表达式语法来描述这些资源之间的关系：

```terraform
resource "aws_vpc" "example" {
  cidr_block = "10.1.0.0/16"
}

resource "aws_subnet" "example" {
  vpc_id = aws_vpc.example.id

  availability_zone = "us-west-2b"
  cidr_block        = cidrsubnet(aws_vpc.example.cidr_block, 4, 1)
}
```

当我们引入模块时，我们的配置开始变得分层而不是扁平化：每个模块都包含自己的一组资源，可能还有自己的子模块，这可能会创建一个深层、复杂的资源配置树。

但是，在大多数情况下，我们强烈建议保持模块树扁平化：只有一层子模块，并使用类似于上述的技术，使用表达式来描述模块之间的关系：

```terraform
module "network" {
  source = "./modules/aws-network"

  base_cidr_block = "10.0.0.0/8"
}

module "consul_cluster" {
  source = "./modules/aws-consul-cluster"

  vpc_id     = module.network.vpc_id
  subnet_ids = module.network.subnet_ids
}

```

我们将这种扁平化的模块使用方式称为模块组合，因为它需要多个可组合的构建块模块并将它们组装在一起以产生更大的系统。

模块不是嵌入其依赖项，创建和管理自己的副本，而是从根模块接收其依赖项，因此可以以不同的方式连接相同的模块以产生不同的结果。

## 依赖倒置

在上面的示例中，我们看到了一个名为 `consul_cluster` 的模块，它可能描述了在 AWS VPC 网络中运行的 `HashiCorp Consul` 服务器集群，因此它需要 VPC 和该 VPC 内的子网标识符作为参数。

另一种设计是让 `consul_cluster` 模块描述它自己的网络资源。如果我们这样做，那么 Consul 集群将很难与同一网络中的其它基础设施共存，所以我们希望尽可能保持模块相对小，并传递它们的依赖项。

这种依赖倒置方法还提高了未来重构的灵活性，因为 `consul_cluster` 模块不知道也不关心调用模块如何获取这些标识符。 未来的重构可能会将网络创建分离到自己的配置中，因此我们可以将这些值从数据源传递到模块中：

```terraform
data "aws_vpc" "main" {
  tags = {
    Environment = "production"
  }
}

data "aws_subnet_ids" "main" {
  vpc_id = data.aws_vpc.main.id
}

module "consul_cluster" {
  source = "./modules/aws-consul-cluster"

  vpc_id     = data.aws_vpc.main.id
  subnet_ids = data.aws_subnet_ids.main.ids
}
```

### 有条件的创建对象

在跨多个环境使用同一个模块的情况下，通常会看到一些必要的对象已经存在于某些环境中，但在其他环境中还需要创建。

例如，这可能出现在开发环境场景中：出于成本原因，某些基础架构可能会在多个开发环境中共享，而在生产环境中，基础架构是唯一的，并由生产配置直接管理。

我们建议采用依赖倒置的方式：让模块通过输入变量接受它需要的对象作为参数，而不是尝试编写一个检测其存在并创建它的模块。

例如，考虑一个 Terraform 模块基于磁盘映像部署计算实例的情况，并且在某些环境中有一个专用磁盘映像可用，而其他环境共享一个公共基础磁盘映像。与其让模块本身处理这两种情况，不如为表示磁盘映像的对象声明一个输入变量。以 AWS EC2 为例，我们可以声明 aws_ami 资源类型和数据源模式的公共子类型：

```terraform
variable "ami" {
  type = object({
    # 仅使用模块所需的属性子集声明对象。 
    # Terraform 将允许任何至少具有这些属性的对象。
    id           = string
    architecture = string
  })
}

```

该模块的调用者现在可以自己直接表示这是要内联创建的 AMI 还是要从其他地方检索的 AMI：

```terraform
# 这种情形下我们将自己管理 AMI

resource "aws_ami_copy" "example" {
  name              = "local-copy-of-ami"
  source_ami_id     = "ami-abc123"
  source_ami_region = "eu-west-1"
}

module "example" {
  source = "./modules/example"

  ami = aws_ami_copy.example
}

```

```terraform
# 或者，AMI 已经在某处存在了

data "aws_ami" "example" {
  owner = "9999933333"

  tags = {
    application = "example-app"
    environment = "dev"
  }
}

module "example" {
  source = "./modules/example"

  ami = data.aws_ami.example
}
```

这与 Terraform 的声明式风格一致：我们并不构建条件分支复杂的模块，而是直接描述应该存在的内容以及希望 Terraform 管理的内容。

通过遵循这种风格，我们可以确定在哪些情况下应该 AMI 存在，哪些情况下不应该存在。维护配置的人以后可以了解这些配置的意图，而无需检查云上的状态。

在上面的示例中，要创建或读取的对象非常简单，可以作为单个资源内联提供，但是在依赖项本身足够复杂以从中受益的情况下，我们也可以将多个模块组合在一起，如本页其他地方所述的一样。

## 多云（Multi-cloud）抽象

Terraform 本身不会尝试抽象不同供应商提供的类似服务，因为我们希望在每个产品中开放全部功能，但在单个接口后面统一多个产品往往需要“最小公分母”方法。

但是，通过 Terraform 模块的组合，可以通过自己权衡哪些平台功能对您很重要来创建自己的轻量级多云抽象。

在多个供应商实现相同概念、协议或开放标准的任何情况下，都会出现这种抽象的机会。例如，域名系统的基本功能在所有供应商中都是通用的，尽管一些供应商通过地理定位和智能负载平衡等独特功能来区分自己，但您可能会得出结论，在您的用例中您愿意避开这些功能作为对创建模块的回报，这些模块将多个供应商的通用 DNS 概念抽象化：

```terraform
module "webserver" {
  source = "./modules/webserver"
}

locals {
  fixed_recordsets = [
    {
      name = "www"
      type = "CNAME"
      ttl  = 3600
      records = [
        "webserver01",
        "webserver02",
        "webserver03",
      ]
    },
  ]
  server_recordsets = [
    for i, addr in module.webserver.public_ip_addrs : {
      name    = format("webserver%02d", i)
      type    = "A"
      records = [addr]
    }
  ]
}

module "dns_records" {
  source = "./modules/route53-dns-records"

  route53_zone_id = var.route53_zone_id
  recordsets      = concat(local.fixed_recordsets, local.server_recordsets)
}

```

在上面的示例中，我们以“记录集”的形式创建了一个轻量级的抽象。这个抽象包含描述应该可映射到任何 DNS 供应商的 DNS 记录的一般概念的属性。

然后，我们将该抽象实例化为一个模块。在本例中将记录集部署到 AWS 的 Route53 服务上。

如果你想以后切换到不同的 DNS 供应商，只需将 dns_records 模块中的内容替换为新供应商的实现，从而使记录集中定义的所有记录配置保持不变。

你可以在 Terraform 通过定义代表所涉及概念的对象，然后将这些对象类型用于模块输入变量来创建像这样的轻量级抽象。 在这种情况下，所有的“DNS 记录”实现都将声明以下变量：

```terraform
variable "recordsets" {
  type = list(object({
    name    = string
    type    = string
    ttl     = number
    records = list(string)
  }))
}

```

DNS 只是一个简单的示例，但仍有更多机会利用供应商之间的通用元素。 一个更复杂的例子是部署 Kubernetes 集群，现在有许多不同的供应商提供托管的 Kubernetes 集群服务，甚至还有更多运行 Kubernetes 的方法。

如果所有这些实现中的通用功能足以满足您的需求，您可以选择实现一组不同的模块来描述特定的 Kubernetes 集群实现，并且都具有将集群的主机名导出为输出值的共同特征：

```terraform
output "hostname" {
  value = azurerm_kubernetes_cluster.main.fqdn
}
```

然后，您可以编写仅期望 Kubernetes 集群主机名作为输入的其他模块，并将它们与您的任何 Kubernetes 集群模块互换使用：

```terraform
module "k8s_cluster" {
  source = "modules/azurerm-k8s-cluster"

  # (Azure-specific configuration arguments)
}

module "monitoring_tools" {
  source = "modules/monitoring_tools"

  cluster_hostname = module.k8s_cluster.hostname
}

```

## 只读模块

大多数模块都包含 `resource` 部分，它描述了要创建和管理的基础设施。有时编写根本不描述任何新基础设施，而只用来检索有关使用`data sources`在其他地方创建的基础设施信息也是一种常见的方式。

作为模块的使用约定，我们建议仅在模块以某种方式提高抽象级别时才用这种用法。在这种情况下会通过精确封装的数据的检索方式。

这种技术的一个常见用途是当一个系统被分解为几个子系统配置，但某些基础设施在各子子系统之间共享的时候。例如一个公共 IP 网络。 在这种情况下，我们可能会编写一个名为 `join-network-aws` 的共享模块，当部署在 AWS 中时，任何需要共享网络信息的配置都可以调用该模块：

```terraform

module "network" {
  source = "./modules/join-network-aws"

  environment = "production"
}

module "k8s_cluster" {
  source = "./modules/aws-k8s-cluster"

  subnet_ids = module.network.aws_subnet_ids
}

```

网络模块本身可以通过多种不同的方式检索这些数据：它可以使用 `aws_vpc` 和 `aws_subnet_ids` 数据源直接查询 AWS API，或者它可以使用 `consul_keys` 从 Consul 集群中读取保存的信息，或者它可以直接从 使用 `terraform_remote_state` 管理网络的配置状态。

这种方法的主要好处是，此信息的来源可以随时间变化，而无需更新依赖它的每个配置。 此外，如果您将纯数据模块设计为具有与相应管理模块相似的一组输出，则在重构时可以相对轻松地在两者之间进行切换。

(完)
