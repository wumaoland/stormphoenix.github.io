---
layout: post
title:    "fall_in_love"
date:    2018-09-10 01:50:34 +0800
categories:    life
description:
comments: true
---

<div class="vcenter">李文姝和王成</div>
<p id="content"></p>
<script type="text/javascript">
        function show() {
            var date1 = '2018/06/18 02:11:00';  //开始时间
            var date2 = new Date();    //结束时间
            var date3 = date2.getTime() - new Date(date1).getTime();   //时间差的毫秒数
            //计算出相差天数
            var days = Math.floor(date3 / (24 * 3600 * 1000))
            //计算出小时数
            var leave1 = date3 % (24 * 3600 * 1000)    //计算天数后剩余的毫秒数
            var hours = Math.floor(leave1 / (3600 * 1000))
            //计算相差分钟数
            var leave2 = leave1 % (3600 * 1000)        //计算小时数后剩余的毫秒数
            var minutes = Math.floor(leave2 / (60 * 1000))
            //计算相差秒数
            var leave3 = leave2 % (60 * 1000)      //计算分钟数后剩余的毫秒数
            var seconds = Math.round(leave3 / 1000)
            document.getElementById("content").innerText = " 已经相爱 " + days + "天 " + hours + "小时 " + minutes + " 分钟" + seconds + " 秒"
        }
        window.setInterval("show()", 1000)
</script>
