---
permalink: /archive
layout: page
title: Archive
---
<style>
  .center {
    margin-bottom: 20px; /* Adjust the value as needed */
  }
</style>

<div class="center">
<a href="/tag/" title="View Posts by Tag"><ins>View Posts organized by Tags</ins></a>
</div>

<ul>
  {% for post in site.posts %}
  <li class="post">{{ post.date | date_to_string | date: "%b %d, %Y" }} » <a href=".{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

