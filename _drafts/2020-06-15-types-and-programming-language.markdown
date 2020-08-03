---
layout: post
title:    "Types and Programming Language"
date:    2020-06-15 16:13:34 +0800
categories:    blog
description:
comments: true
---

#### Type Systems
lightweight formal method 用来确保系统的行为是正确的.

> A type system is a tractable syntactic method for proving the absence of certain program behaviors by classifying phrases according to the kinds of values they compute.

##### What Type Systems Are Good For

- 检查类型错误
- 方便对模块做抽象，例如接口的类型就是“模块类型”

#### 区分 Language Safety 和 Static Type Safety

- Static type safety 保证程序的类型是正确的，但是不能保证语言是安全的。
- Language safety 程序运行过程中可能出错，这时候需要 run-time check，来保证 Language safety。

类型检查可以判断程序可能发生什么错误，但是不能判断不会发生什么错误。

```
public void foo() throws XXException {
    bool judge = true;
    if (judge) {
        // do something
    } else {
        throw new XXException();
    }
}
```

比如这个例子，类型检查可以判断 `foo()` 可能会抛出 `XXException`。在这个例子中 `judge` 永远都是 `true` 不可能抛出异常。但 static type check 是无法判断异常不会发生的。

所以有的语言是安全语言，比如 Java，这类语言提供 statically checked 和 dynamically checked，而 C++ 是不安全语言，没有提供 dynamically checked。

#### Syntax - How to define syntax ?

## **Semantic Styles**

三种基本方法用来形式化语义：

- *Operational semantics* 描述了一个抽象状态机，语言中的每一项是机器的 state，state 之间的转移通过一个 transition function 来定义。因此语义描述的是抽象机器的状态序列。

> - *Operational semantics* specifies the behavior of a programming language by defining a simple abstract machine for it.
> - An example
>   - terms as states
>   - transition from one state to another as simplification
>   - meaning of t is the final state starting from the state corresponding to t

- *Denotational semantics* 描述的不是一个序列化的状态，而是语义域（*semantic domains*）和将语言中每一个项映射到语义域（*semantic domain*）的解释函数（*interpretation function*）。
- *Axiomatic semantics* TODO 没看懂