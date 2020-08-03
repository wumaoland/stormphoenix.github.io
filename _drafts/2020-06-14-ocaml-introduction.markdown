---
layout: post
title:    "ocaml-introduction"
date:    2020-06-14 17:55:53 +0800
categories:    blog
description:
comments: true
---

语句结束符 ;;
注释 (* *)
函数定义 let func_name param_a param_b = some_expr ;;

局部表达式 let name = experssion in 在作用域内用 name 代替 experssion

嵌套函数 let func_a = 
		let nest_func_name arg = function-definition in
		;;

绑定：let 用来定义一个绑定。绑定的意思是 a -> b 的映射关系

引用：
	let my_ref = ref 0;;
重新绑定引用：
	let my_ref = ref ... ;;
引用赋值：
	my_ref := 100;;
引用取值：
	!my_ref;;

导入模块 
	open Graphics;;
	module Gr = Graphics;;

let () = expr / let _ = expression
	运行 expression ，并丢弃返回结构

Factors
	有点像 泛型号
