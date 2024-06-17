---
permalink: /archive
layout: page
title: Archive
---
<div class="center">
<a href="/tag/" title="View Posts by Tag">View Posts organized by Tags</a>
</div>

<ul>
  {% for post in site.posts %}
  <li class="post">{{ post.date | date_to_string | date: "%b %d, %Y" }} » <a href=".{{ post.url }}">{{ post.title }}</a></li>
  {% endfor %}
</ul>

