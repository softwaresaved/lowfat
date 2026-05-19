---
layout: page
title: "Runtime Configuration"
category: dev
date: 2026-05-08 11:10:00
order: 8
---

lowFAT uses [django-constance](https://django-constance.readthedocs.io/en/latest/index.html) for a number of runtime-configurable settings.

These settings can be changed through the Django admin interface without modifying the source code or restarting the application.

The runtime configuration panel is available through:

~~~ text
/admin/constance/config/
~~~
{: .language-plain-text }

<div class="doc-screenshot">
<div style="max-height: 550px; overflow-y: auto; border: 1px solid #ddd;">
  <img src="{{ site.baseurl }}/img/constance-2026.png" style="width:100%;">
</div>
</div>

Typical examples include:

- email notification toggles,
- finance notification configuration,
- workflow-related settings,
- public-facing configuration values,
- and application behaviour flags.

Email templates themselves are managed separately through Flat Pages, as described in the Staff Guide.

## Adding New Runtime Settings

New runtime settings must first be added to:

~~~ text
CONSTANCE_CONFIG
~~~
{: .language-plain-text }

inside:

~~~ text
lowfat/settings.py
~~~
{: .language-plain-text }

Once added, the setting becomes available through the django-constance admin interface.

For more information, see the official [django-constance documentation](https://django-constance.readthedocs.io/en/latest/index.html).

<div class="box-warning" markdown="1">
Do not include production secrets, access tokens, or sensitive configuration values in public documentation screenshots.
</div>

<div class="doc-pagination">
  <a class="doc-prev" href="{{ site.baseurl }}{% post_url 2026-05-08-testing %}">
    <span class="arrow">←</span>
    <span class="label">Testing</span>
  </a>

  <a class="doc-next" href="{{ site.baseurl }}{% post_url 2026-05-08-authentication-and-oauth%}">
    <span class="label">Routing and Naming Conventions</span>
    <span class="arrow">→</span>
  </a>
</div>