---
permalink: /
title: "About Blazewing"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

Blazewing is a nonbinary queer academic whose studies focus on anti-trans narratives. Their current focus right now is the anti-trans legislation in the US and the rhetorical patterns contained within it at both the state and federal levels. Overall, they aim to study how anti-queer rhetoric repeats throughout history. Their current personal hobbies include a love of travel and seeing new places, table-top roleplaying games like Dungeons and Dragons, Vampire the Masquerade, and a love for the gothic, morbid, and anything vampire-related. 

Current Project:
Blazewing's current research project is analyzing 2025's passed anti-trans legislation on both a state and federal level.

Blazewing has 3 cats:
Salem - Pure Black (totally original, I know, lol)
Bastet - Street rescue, partial Russian Blue, and 20 lbs
Rasputin - Tortoise shell and always into mischief.


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
    <a href="/research-journal/">View all journal entries →</a>
  </p>
</section>


This is where my epic bio goes when I get it done. Here, I'll talk about what I'm up to, what I'm contemplating, and all that jazz.
