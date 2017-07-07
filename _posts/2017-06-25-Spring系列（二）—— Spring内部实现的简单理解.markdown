---
layout: post
title:    "Spring系列（二）—— Spring内部实现的简单理解"
date:    2017-06-25 00:43:19 +0800
categories:    Spring
comments: true
tag: Spring
---

* content
{:toc}

前言
==

看懂本文需要准备的知识：
* Java反射
* Java注解
* 依赖注入（Dependency Injection，DI)
* Spring 是如何使用注解的 （比如@Bean，@Component之类）
* 阅读过上一篇[博客](https://stormphoenix.github.io/2017/06/24/Spring系列-一-初识Spring/)

从自动扫描说起
==

在 Spring 里面有一个我觉得比较厉害的功能——自动扫描。不了解的没有关系下面我举一个例子来说明一下。

例子依旧沿用 Spring 系列的上一篇[博客](https://stormphoenix.github.io/2017/06/24/Spring系列-一-初识Spring/)的例子：

{% highlight ruby %}
/**
* 在上一篇的例子上做了修改，改成了使用 Spring 框架的形式
*/
public class Kid {
	/**
	* @Autowire 是 Spring 里面的一个注解，
	* 表示被注解的属性需要被外界注入。
	*
	* Autowire 的意思就是自动装配
	*/
	@Autowire
    private Ball ball;

	public vodi play() {
		ball.play();
	}
}

public interface Ball {
	void play();
}
{% endhighlight %}

在上一篇博客中，我留下了一个疑问，Kid 里面的 Ball 是需要被外界注入的，那么到底是谁注入的？（反正不是程序员自己）这就涉及到 Spring 的自动扫描功能了！

假设我在配置文件中配置 Spring 使用自动扫描功能（具体如何配置的目前不管，先了解原理），Spring 就会将程序员指定的包路径下面的所有的类全部扫描一遍，读取里面的信息。如果 Spring 读取 Kid 类时，发现有一个属性字段 ball 被加上了 @Autowire 注解，那么就会在 **Spring容器** 里面查找是否有类型是 Ball 的一个 **Bean** 的实现，如果有，就会把这个 Bean 赋值给 Kid 的 ball 字段。从而实现了 Spring 的 **DI** 功能。

如何实现的
==
这个神奇的自动扫描、自动注入是如何实现的？我查找了一些资料，这里仅谈谈个人理解。

首先，Spring 会读取配置，从配置中直到它要扫描的包，然后解析包里面的所有的类。那么关键就是如何解析了。解析的方法就是利用 **Java 反射**，是 **Java 反射**！

Java 反射可以解析类的各种属性，有构造器、方法、属性等等。而 Spring 就利用这个特性将包里面所有被 @Bean、@Service、@Component 注解的的类全部解析一遍，并封装成一个 Bean 信息类，这个 Bean 信息类包含了很多信息，有 Bean 的 constructor信息、method信息、property信息等等。然后，**最重要的一步**，将这个 Bean 信息类放进一个 map 里面，所谓的 map 其实就是前文提到的 **Spring容器**！理解这个很关键！

当程序需要一个 Bean 的实现的时候（比如上文的 @Autowire），Spring 就会在 ** Spring容器** 里面查询一下是否有这个 Bean 的定义 —— 翻译一下，就是在 map 里面查找是否有关于这个 Bean 定义的信息类。如果有，那就根据这个 Bean定义里面的 constructor 信息构造一个对象（构造完毕后在这个对象里面继续查找是否有需要注入的属性，所以你懂的，又是一层递归）。相反，如果没有在 Spring容器里面找到这个 Bean 的定义，那么就会抛出异常。

当 Bean 对象完全被构造出来后，就会被赋值给需要它的地方，比如上面提到的 @Autowire（也就是所谓的依赖注入，Spring 已经在底层全部替你做好了）。

最后是否需要根据 Bean定义构造一个对象也是需要商榷的，如果实现确定了这个 Bean对象是单例的（Singleton），那么就只构造一次这个对象，以后需要的话只要复用这个对象即可。

完毕～～
