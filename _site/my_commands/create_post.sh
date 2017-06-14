categories=$1
name=$2

basePath='/home/Developer/Workspace/Blog/stormphoenix.github.io/_drafts/'
fileName=$(date "+%Y-%m-%d-")
time=$(date "+%Y-%m-%d %H:%M:%S +0800")

fileName=${fileName}${name}'.markdown'

touch ${basePath}${fileName}

echo "---
layout: post
title:    \"${name}\"
date:    ${time}
categories:    ${categories}
comments: true
---

* content
{:toc}

write your content" >> ${basePath}${fileName}
