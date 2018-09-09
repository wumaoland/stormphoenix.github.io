---
layout: post
title:    "坠入爱河"
date:    2018-09-10 01:50:34 +0800
categories:    life
description:
comments: true
---

自从我爱上[你](https://weibo.com/u/2162251055)开始，已经有
<p id="content">
    <h1 style="font-size: 30px; font-weight: bold" id="time_text">时间正在计算中... ...</h1>
</p>
<p class="vcenter">岁月悠悠，我们彼此守候。</p>
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
            var $timeText = $(' <h1 id="time_text"> ' + days + " 天 " + hours + " 小时 " + minutes + " 分钟 " + seconds + " 秒了 </h1>")
            document.getElementById("time_text").innerText = days + " 天 " + hours + " 小时 " + minutes + " 分钟 " + seconds + " 秒了 "
            
        }
        window.setInterval("show()", 1000)
</script>



