---
layout: post
title:    "如何在 Github Pages 中配置 LaTeX"
date:    2021-09-23 12:51:46 +0800
categories:    blog
description: 用 jekyll + markdown 的形式部署 github pages，该如何支持 latex 语法？
comments: true
---

### 配置环境

- OS：macOS Catalina
- Github pages 构建工具：jekyll

我自己试了三种方法，最后一种直接在本地用 MathJax javascript 库解析 LaTeX 效果是最好的。

### 用 jekyll-spaceship 插件处理 LaTeX 语法

之前没接触过 ruby 语言，对 jekyll 的执行流不太清楚。这次借机会把 ruby \ rvm \ gem \ bundle 之间的关系理了一下。

- ruby： 一种脚本语言
- rvm：ruby 版本管理工具
- gem：全局包管理器，管理 ruby 库的版本、依赖关系
- bundle： 项目中的包管理器。有了 bundle，每个 ruby 项目都可以管理同版本的 ruby 库

gem 可以理解为全局的包管理器，而 bundle 理解为项目级别的包管理器。一个项目可以是一个文件夹下面的所有内容。而 bundle 又是通过项目下面的 Gemfile / Gemfile.lock 文件起作用的。

转入正题，jekyll-spaceship 是 jekyll 下的插件（本质上也是一个 ruby 库），功能很多，包括了处理 LaTeX 语法。而一个 github pages 本质上是一个项目，可以用 bundle 管理 jekyll-spaceship 插件。

在 Gemfile 中的 `group` 标签添加 jekyll-spaceship 库：
```
group :jekyll_plugins do
  gem 'jekyll-spaceship'
end
```

运行 bundle，bundle 会检查 Gemfile 配置更新项目依赖的库：
```
bundle install
```

安装过程如果无误，那么配置就完成了，可直接在 markdown 里编写 LaTeX 代码。

缺点：jekyll 项目在本地运行可以完美解析 LaTeX 语法，但上传到 github pages 就不行了，猜测是 github 在构建 jekyll 项目时是没有 jekyll-spaceship 插件的。

### CDN 分发 MathJax.js

这种方法最方便简洁，在每篇 post 之前插入下面这行代码即可：

```
<script type="text/javascript" async src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
```

这段链接会指向一个 CDN 分发服务，将最新的 MathJax Js 库 发送到本地用于 LaTeX 渲染。

缺点：虽然做起来很简单，但每次打开新 post 都会重新加载这段代码，引起不必要的网络开销，网页会卡上一会。

### 本地添加 MathJax 库

用 CDN 分发服务会让网页卡顿，所以我考虑将 MathJax Js 库全部存放到本地 js 文件夹。这里参考了 [Hosting Your Own Copy of MathJax](https://docs.mathjax.org/en/latest/web/hosting.html) 这篇文章。首先将已经编译发布的 MathJax 库用 npm 工具下载下来：

```
npm install mathjax@3
```

npm 的执行目录下会出现 node_modules 文件夹，里面存放着 mathjax/es5，es5 文件夹里面有着所有编译发布好的 mathjax 库。然后，在 github pages 的 /js 目录下建立 mathjax 文件夹，把 mathjax/es5 里面的 mathjax 库复制过来。

最后一步，依然是在每片 post 之前插入 ```<script>``` 标签，引用 /js 下的 mathjax，如下：

```
<script src="/js/mathjax/tex-chtml.js" id="MathJax-script" async></script>
```

至此可以完美解析 LaTeX 语法，网页加载速度也很快。