---
permalink: /archive
layout: page
title: Archive
---


<ul>
  {% for post in site.posts %}
  <li class="post">{{ post.date }} » {{ post.title }}</li>
  {% endfor %}
</ul>

