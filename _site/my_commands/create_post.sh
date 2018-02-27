# this shell script is used to create a post template in "_drafts" 
# directory which belongs to this project

categories=$1
name=$2

basePath=$(cd `dirname $0`;cd ../_drafts;pwd)
basePath=${basePath}"/"

fileName=$(date "+%Y-%m-%d-")
time=$(date "+%Y-%m-%d %H:%M:%S +0800")

fileName=${fileName}${name}'.markdown'

touch ${basePath}${fileName}

echo "---
layout: post
title:    \"${name}\"
date:    ${time}
categories:    ${categories}
description:
comments: true
---

write your content" >> ${basePath}${fileName}
