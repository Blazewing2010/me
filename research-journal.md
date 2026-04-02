---
layout: default
title: Research Journal
permalink: /research-journal/
---

<section>
  <h2>Latest Research Journal Entries</h2>
  <ul>
    {% for post in site.data.substack limit:5 %}
      <li style="margin-bottom: 1.5rem;">
        <strong>
          <a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">
            {{ post.title }}
          </a>
        </strong><br>
        <span style="font-size: 0.95rem; opacity: 0.8;">
          {{ post.date | date: "%B %d, %Y" }}
        </span>
        <p>{{ post.excerpt }}</p>
      </li>
    {% endfor %}
  </ul>

  <p>
    <a href="../research-journal/">View all journal entries →</a>
  </p>
</section>

# Research Journal

Recent entries from my Substack research journal.

<ul class="research-journal-list">
  {% for post in site.data.substack %}
    <li style="margin-bottom: 2rem;">
      <h2 style="margin-bottom: 0.25rem;">
        <a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">
          {{ post.title }}
        </a>
      </h2>
      <p style="margin: 0 0 0.5rem 0; font-size: 0.95rem; opacity: 0.8;">
        {{ post.date | date: "%B %d, %Y" }}
      </p>
      <p style="margin: 0 0 0.5rem 0;">
        {{ post.excerpt }}
      </p>
      <p style="margin: 0;">
        <a href="{{ post.link }}" target="_blank" rel="noopener noreferrer">
          Read on Substack →
        </a>
      </p>
    </li>
  {% endfor %}
</ul>
