---
layout: page
title: "Authentication and OAuth"
category: dev
date: 2026-05-08 11:20:00
order: 9
---

lowFAT primarily uses Django’s built-in authentication system for user accounts, password resets, and administrative access.

The project also contains optional GitHub OAuth support using `social-auth-app-django`.

## GitHub OAuth

GitHub OAuth support remains in the codebase, but maintainers should review the current authentication behaviour carefully before enabling it for a deployment.

Previous issues included duplicate-account creation when existing users authenticated through GitHub (see [issue #778](https://github.com/softwaresaved/lowfat/issues/778)).
The OAuth pipeline currently includes custom account-linking logic through:

~~~ text
lowfat.auth.wire_profile
~~~
{: .language-plain-text }

The related configuration and routes are still present in the application.

## OAuth Application Setup

GitHub OAuth applications can be created through:

~~~ text
https://github.com/settings/applications/new
~~~
{: .language-plain-text }

<div class="doc-screenshot">
<div style="max-height: 550px; overflow-y: auto; border: 1px solid #ddd;">
  <img src="{{ site.baseurl }}/img/github-oauth.jpg" style="width:100%;">
</div>
</div>

Typical configuration values include:

- Application name: `FAT`
- Homepage URL: `http://lowfat.your.domain`
- Application description: `Fellows Administration Tool`
- Authorization callback URL:

~~~ text
http://lowfat.your.domain/complete/github/
~~~
{: .language-plain-text }

## Authentication Routes

Authentication-related routes are defined in:

~~~ text
lowfat/urls.py
~~~
{: .language-plain-text }

This includes:

- login and logout views,
- password reset routes,
- and optional OAuth integration routes.

## Related Packages and Settings

The OAuth integration currently uses:

- `social-auth-app-django`
- `social_django`

Additional configuration may also exist in:

- `lowfat/settings.py`
- environment configuration files
- Django admin runtime settings

GitHub OAuth settings currently include:

- `SOCIAL_AUTH_GITHUB_KEY`
- `SOCIAL_AUTH_GITHUB_SECRET`
- `SOCIAL_AUTH_REDIRECT_IS_HTTPS`

<div class="box-warning" markdown="1">
Before enabling GitHub OAuth for a deployment, review the current account-linking and authentication behaviour carefully.
</div>

<div class="doc-pagination">
  <a class="doc-prev" href="{{ site.baseurl }}{% post_url 2026-05-08-runtime-configuration %}">
    <span class="arrow">←</span>
    <span class="label">Runtime Configuration</span>
  </a>

  <a class="doc-next" href="{{ site.baseurl }}{% post_url 2026-05-08-privacy %}">
    <span class="label">Privacy and Data Visibility</span>
    <span class="arrow">→</span>
  </a>
</div>





