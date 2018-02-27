---
layout: post
title:    "简单使用Spring——Bean的装配（三）"
date:    2017-07-01 23:21:41 +0800
categories:    Spring
comments: true
---

* content
{:toc}

简单使用Spring——Bean的装配（三）
==

在面向对象程序设计中，程序是由一个个的对象组成的，不同的对象负责的工作一般来说是不一样的。如果程序要实现某一个功能，通常是由多个对象协同工作来实现的。

对象和对象之间的协同，意味着对象和对象之间的依赖。我理解的依赖，就是一个对象对另外一个对象的引用，如下：
```
public class Foo {
	private Boo boo;
}
```
这个例子里面，类Foo的属性boo引用了类Boo，这就是Foo依赖于Boo。

那么问题在于，Foo如何初始化这个Boo呢？
```
// 实现1
public class Foo {
	...
	public Foo() {
		this.boo = new Boo();
	}
	...
}

// 实现2
public class Foo {
	...
	public Foo(Boo boo) {
		this.boo = boo;
	}
	...
}

// 实现3
public class Foo {
	...
	public void setBoo(Boo boo) {
		this.boo = boo;
	}
	...
}
```

实现一有如下两个问题：
* 创建Boo对象不是Foo应该负责的功能。（违反了单一职责原则，一个类只要专注于实现自己的功能就好了，不要管其他。在这里，Foo的并不负责如何创建Boo对象）
* 假设由于某种原因，导致Boo的构造函数变化了，那么Foo对象也要跟着变化。（变化的和不变化的要分开，在这里，Boo的构造函数是可能会变化的，但Foo对Boo的依赖形式是不变的，所以Foo是不能靠创建Boo来实现对Boo对象的依赖）

实现二和实现三则避免了上述问题。那么麻烦的地方在于，在哪里调用这个Foo构造器或者setter方法？当然，可以通过工厂的方法将Boo注入。不过在这里，当然是用Spring。

预备知识
==

* Component。组件，一个简单的概念。目前可以认为一个对象就是一个组件。建立对象之间的依赖关系可以理解为将组件和组件组装在一起。
* Autowire。自动装配，Spring里面的自动装配可以自动将Component组装在一起。（具体如何组装看自己是如何配置的）

学习如何装配Bean
==

* 纯Java方式装配Bean
```
Component
public class Boo {
	...
}

public class Foo {
	...
	@Autowire
	private Boo boo;
}

@Configuration
@ComponentScan
public class JavaConfig {
}
```
