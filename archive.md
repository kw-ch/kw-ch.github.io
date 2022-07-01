---
permalink: /archive
layout: page
title: Archive
---


<ul>
  {% for post in site.posts %}
  <li class="post">{{ post.date | date_to_string | date: "%b %d, %Y" }} » <a href=".{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

