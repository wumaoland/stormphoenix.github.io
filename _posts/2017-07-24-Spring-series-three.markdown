---
layout: post
title:    "Spring系列（三）"
description: 创建Bean之间的依赖
date:    2017-07-24 00:00:41 +0800
categories:    Spring | blog
comments: true
---

前言
===

在面向对象程序设计中，程序是由一个个的对象组成的，不同的对象负责不同的工作。程序要实现某一个功能，通常是由多个对象协同工作来实现的。

对象和对象之间的协同，意味着对象和对象之间的依赖。这一点可以参考之前写的[博客](https://stormphoenix.github.io/2017/06/24/Spring系列-一-初识Spring/)。

所谓的Java Bean，我简单的理解成Java对象。创建对象之间的依赖就是创建Bean之间的依赖。

下面举一个例子讲解一下。

{% highlight ruby %}
public class Foo {
	private Boo boo;
}
{% endhighlight %}
这个例子里面，类Foo的属性boo引用了类Boo，这就是Foo依赖于Boo。

那么问题在于，Foo如何初始化这个Boo呢？

{% highlight ruby %}
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
{% endhighlight %}

实现一有如下两个问题：
* 创建Boo对象不是Foo应该负责的功能。（违反了单一职责原则，一个类只要专注于实现自己的功能就好了，不要管其他。在这里，Foo的并不负责如何创建Boo对象）
* 假设由于某种原因，导致Boo的构造函数变化了，那么Foo对象也要跟着变化。（变化的和不变化的要分开，在这里，Boo的构造函数是可能会变化的，但Foo对Boo的依赖形式是不变的，所以Foo是不能靠创建Boo来实现对Boo对象的依赖）

实现二和实现三则避免了上述问题。那么麻烦的地方在于，在哪里调用这个Foo构造器或者setter方法？当然，可以通过工厂的方法将Boo注入。不过在这里，当然是用Spring。

预备知识
==

* Component。意思是`组件`，一个简单的概念。可以认为一个Bean就是一个组件。建立对象之间的依赖关系可以理解为将 Bean 和 Bean 组装在一起。
* Autowire。自动装配。Spring的自动装配功能，可以自动将不同的Component组装在一起，构成组件和组件之间的依赖。
* 阅读过[Spring 系列（二）](https://stormphoenix.github.io/2017/06/25/Spring系列-二-Spring内部实现的简单理解)


利用Spring配置Bean之间的依赖
==

先看一个很简单的例子：
{% highlight ruby %}
/**
* 车辆
*/
public interface Car {
	void drive();
}

/**
* 车轮
*/
public interface Wheel {
	void role();
}

/**
* 橡胶轮胎，Wheel 的一个实现
*/
public class RubberWheel implements Wheel {
	void role() {
		// do something
	}
}

/**
* 奔驰车， Car 接口的一个实现
*/
public class Bench implements Car {
	private Wheel wheel;

	void drive() {
		wheel.role();
	}
}
{% endhighlight %}

这里 Bench Bean依赖于 Wheel，所以 Wheel 是要被注入到 Bench 的。在第一篇[博客](https://stormphoenix.github.io/2017/06/24/Spring系列-一-初识Spring/)中提到了 Spring 可以帮我们做`注入`这件事情，那就用这个例子来说明 Spring 是怎么做的吧。

创建Bean之间依赖的方式分为两大类：Java方式；XML配置文件方式。其中Java方式又划分成两种：Java注解方式；Java代码方式。依次讲解。

* **Java注解方式**
思路：这种方式是和`自动扫描`功能搭配起来的。首先`Spring容器`会加载`Spring 配置类`，然后发现`Spring 配置类`设置成自动扫描模式，于是`Spring 容器`会自动扫描配置类所在的整个包里面的Java类，查看是否有Java类被加上了`@Component`注解，如果加上了，就认为这个类是`Spring 容器`中的一个组件，然后把这个组件初始化。在初始化这个组件的过程中，如果发现有属性字段被`@Autowire`注解修饰，就认为这个字段是这个组件依赖的另外一个组件，就在`Spring 容器`中查找是否以及初始化了这个被依赖的组件，如果初始化了，就把这个组件赋值给`@Autowire`修饰的字段。从而实现了 Spring 的依赖注入功能。下面利用例子来解释。(`Spring容器`这个概念可以参考[Spring 系列（二）](https://stormphoenix.github.io/2017/06/25/Spring系列-二-Spring内部实现的简单理解))

{% highlight ruby %}
/**
* 车辆
*/
public interface Car {
	void drive();
}

/**
* 车轮
*/
public interface Wheel {
	void role();
}

/**
* 橡胶轮胎，Wheel 的一个实现
*
* 这里用了 @Component 注解，代表 RubberWheel 是 Spring 容器中的
* 一个 Bean 。Spring 容器在自动扫描的时候会自动初始化这个 Bean 。
*/
@Component
public class RubberWheel implements Wheel {
	void role() {
		System.out.println("RubberWheel is rolling")
	}
}

/**
* 奔驰车， Car 接口的一个实现
*
* 同 Wheel 的用法。
*/
@Component
public class Bench implements Car {
    /**
    * Spring 发现 wheel 字段被 @Autowire 修饰，就会从 Spring 容器
    * 中查找是否有实例化了 Wheel 这个 Bean。如果有，那么这个 Wheel
    * 就会被赋值到这个字段。
    *
    * 在这个例子中， Wheel 的实现只有 RubberWheel 这个类，并且这个
    * 类被 @Component 所修饰，所以 RubberWheel 的实例会被赋值给这
    * 个字段。
    */
    @Autowire
	private Wheel wheel;

	void drive() {
		wheel.role();
	}
}

/**
* 之前提到的配置类。
*
* @Configurable 。被这个类修饰表明这个类是一个配置类，Spring 会从这
* 个类中加载需要的信息。
*
* @ComponentScan 。一个 Java 配置类如果有这个注解修饰，表明 Spring
* 不需要从这个配置类中加载信息，而是自己扫描这个配置类所在的整个包来搜
* 寻信息。如果之前的 Bench 类和 RubberWheel 类与 JavaConfig 同处
* 于一个包下，那么这两个类就会被 Spring 实例化。
*/
@Configurable
@ComponentScan
public class JavaConfig {
}

public class Main {
    public static void main(String[] args) {
        // 创建 Spring 容器，并加载 JavaConfig 配置类
        // 这个 ApplicationContext 就是 Spring 容器，
        // 而 AnnotationConfigApplicationContext 是
        // 它的一种实现，用于加载 Java配置类
		ApplicationContext context = new AnnotationConfigApplicationContext(JavaConfig.class);
		// 等上面的代码执行完毕，那么 RubberWheel 和 Bench 两个类就
		// 被实例化了。下面通过 Spring 容器来获取，实例化的这两个类。

        // 获取奔驰车
        // 这里的疑问就是，传入的参数是 Car.class 对象，为什么获得
        // 的是 Bench 类型的对象。原因是 Bench 是 Car 实现，并且
        // 是唯一的一个实现。如果 Car 有多个实现，并且都被 Spring
        // 容器初始化，那么这段代码就会抛出异常，因为 Spring 不知道
        // 要返回哪一个实现。
        Bench benchCar = context.getBean(Car.class);
        // 调用方法
        benchCar.drive();
    }
}
{% endhighlight %}
所有的说明已经写入了代码注释之中。

* **Java代码方式**
Java注解方式 ... ... 不也是 Java代码么 ... ...，而且 Java代码方式也用到了注解，不过两者还是有区别的，区别在于自动扫描 : )
思路：依然是 `Spring 容器`加载 `Java 配置类`，不过此时 `Java配置类`没有被设置成自动扫描，所有的信息都要从这个配置类中获取。一个类是否属于`Spring 容器`、是否需要初始化完全由配置类决定 ... ... 所以，`@Component`注解在这种方式下是没有作用的。其他的地方和`Java注解方式`一样。

{% highlight ruby %}
/**
* 车辆
*/
public interface Car {
	void drive();
}

/**
* 车轮
*/
public interface Wheel {
	void role();
}

/**
* 橡胶轮胎，Wheel 的一个实现
*
* 这里去掉了 @Component 注解。也就意味着 RubberWheel 是否是
* Spring 容器中的组件完全由Java配置类中的信息决定。
*/
public class RubberWheel implements Wheel {
	void role() {
		System.out.println("RubberWheel is rolling")
	}
}

/**
* 奔驰车， Car 接口的一个实现
*
* 同 Wheel 的用法。
*/
public class Bench implements Car {
    /**
    * Spring 发现 wheel 字段被 @Autowire 修饰，就会从 Spring 容器
    * 中查找是否有实例化了 Wheel 这个 Bean。如果有，那么这个 Wheel
    * 就会被赋值到这个字段。
    *
    * 在这个例子中， Wheel 的实现只有 RubberWheel 这个类，并且这个
    * 类被 @Component 所修饰，所以 RubberWheel 的实例会被赋值给这
    * 个字段。
    */
    @Autowire
	private Wheel wheel;

	void drive() {
		wheel.role();
	}
}

/**
*
* @Configurable 。被这个类修饰表明这个类是一个配置类，Spring 会从这
* 个类中加载需要的信息。
*/
@Configurable
public class JavaConfig {
    /**
    * 当一个方法被 @Bean 修饰的时候，它的返回值就会作为
    * Spring 容器中的一个组件。所以说 @Bean 实现的效果
    * 和用 @Component 注解实现是一样。 不过他们还是有区别
	*
	* 用 @Component 修饰的类是由 Spring 容器初始化的，而
	* 初始化参数默认是无参数，也就意味着用 Java注解方式实例
	* 化的类的构造函数是无参数的。
    *
    * 很明显，如果用 @Bean ，那么具体的构造方式是由自己确定
    * 的... ...虽然这个地方也是使用无参数的构造方法 :)
    */
    @Bean
	public Car getCar() {
		return new Bench();
	}

	@Bean
	public Wheel getWheel() {
		return new RubberWheel();
	}
}

public class Main {
    public static void main(String[] args) {
	    // 同上
		ApplicationContext context = new AnnotationConfigApplicationContext(JavaConfig.class);
        // 同上
        Bench benchCar = context.getBean(Car.class);
        // 调用方法
        benchCar.drive();
    }
}
{% endhighlight %}
详细说明见注释

* **XML配置方式**
{% highlight ruby %}
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!-- 这里实例化一个 RubberWheel， 这里 rubberWheel 是它的id，用来被其他位置引用 -->
    <bean id="rubberWheel" class="com.stormphoenix.demo.RubberWheel"/>

    <!-- 实例化奔驰车，这里的属性wheel是bench的字段名字，引用了 rubberWheel id，效果就是把RubberWheel注入到这个类 -->
    <bean id="bench" class="com.stormphoenix.demo.Bench">
        <property name="wheel" ref="rubberWheel">
    </bean>
</bean>

// 导入的步骤和之前的 Main 一样，不同之处在于 Spring容器，XML配置采
// 用的是ClassPathXmlApplicationContext
{% endhighlight %}

混合配置
==
不同人的对配置方式的偏好不一样，所以一个项目中几种不同的配置方式共存是很正常的。同时，一个配置类或者XML配置文件如果包含的内容太多，就需要拆分成好几个配置项目，否则就显得臃肿。

也就意味着，一个项目有好几种配置方式，一种配置方式有好几个配置类或配置文件。如果存在这样的情况，就需要把不同的配置合并成一个，方便 Spring容器加载。如果不合并的化，那么 Spring 容器一个一个加载是很麻烦的。

下面简单说明。

* Java配置与XML配置合并
  在 Java 配置类里面，利用 @ImportResource 注解导入 XML 配置

{% highlight ruby %}
/**
* @ImportResource 里面的值的固定格式是
* classpath:xxx.xml，其中xxx就是XML配置
* 文件的名称。
*
* 导入后，JavaConfig中的信息就和XML配置文件
* 中的信息合并了。只要 Spring容器加载了 JavaConfig
* 配置类，就自然而然的加载了 XML配置文件的信息。
*/
@Configurable
@ImportResource("classpath:xxx.xml")
public class JavaConfig {
	// do something
}
{% endhighlight %}

* Java配置类和Java配置类合并
利用 @Import 导入另外一个配置类
{% highlight ruby %}
/**
* OtherConfig.class 是另外一个配置类，可以在任何包路径下，
* 其他的同上。
*/
@Configurable
@Import(OtherConfig.class)
public class JavaConfig {
	// do something
}
{% endhighlight %}
* XML配置文件与Java配置类合并
{% highlight ruby %}
<!-- XXX 是 Java配置类的名称 -->
<!-- 当 ClassPathXmlApplicationContext 容器加载了XML文件时，XXX配置类中的信息也一样会被加载。 -->
<bean class="XXX" />
{% endhighlight %}

* XML配置文件与XML配置文件合并

{% highlight ruby %}
<!-- 道理同上 -->
<import resource="xxx.xml" />
{% endhighlight %}
一些注意事项
==
时间有限，不可能讲把具体细节讲的面面俱到，所以这个博客只记录原理性的东西。所以要真正的使用这个框架，看博客坑定不够，必须看相关书籍。

下面记录一些额外的知识点。

* Java注解方式中的自动扫描，其默认扫描的地方是配置类所在的包。不过这个地方可以自己配置。可以看源码注释。下面列举几种：
{% highlight ruby %}
// 指定多个包路径
@ComponentScan(basePackages = {"xxx", "yyy"})

// 制定多个类，扫描类所在的包
@ComponentScan(basePackageClasses = {"XXX.class", "YYY.class"})
{% endhighlight %}

* XML配置文件功能没有讲全，其实还有很多标签用来配置bean的细节。

* @Autowire 不仅仅可以添加在属性字段上，还可以添加到SETTER方法、构造方法上。

* @Bean 注解可以给 Bean 设置ID
{% highlight ruby %}
// 返回的 bean 的 id 是 beanId
@Bean("beanId")
// an method
{% endhighlight %}

* @Bean 注解的方法返回的 Bean 默认情况下是单例。
