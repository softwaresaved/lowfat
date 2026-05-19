---
layout: page
title: "Templates and Permissions"
category: dev
date: 2026-05-08 10:40:00
order: 5
---

lowFAT uses Django templates extensively for rendering views, forms, navigation, and user-specific actions.

Many interface decisions are handled through a combination of:

- Django views,
- template conditions,
- crispy-forms layouts,
- context processors,
- and custom template filters.

## Django Templates

Templates are primarily located inside the `templates/` directories within the Django application.

Templates are used to render:

- dashboards,
- funding requests,
- expense claims,
- blog posts,
- staff review pages,
- forms,
- navigation elements,
- and status-dependent actions.

lowFAT uses Django’s template system together with Bootstrap-based styling and crispy-forms.

## Crispy Forms

lowFAT uses [django-crispy-forms](https://django-crispy-forms.readthedocs.io/) to control form layout and presentation.

Crispy forms are used throughout the project to:

- organise form fields,
- structure layouts,
- add helper text,
- customise buttons and sections,
- and improve consistency across forms.

Most form configuration is handled inside the Django form classes.

## Context Processors

lowFAT uses Django context processors to expose common information to templates.

For example, templates can directly access the current authenticated user:

~~~ text
{% raw %}{{ user.username }}{% endraw %}
~~~
{: .language-plain-text }

Templates may also use conditions such as:

~~~ text
{% raw %}{% if user.is_staff or user.is_superuser %}
...
{% endif %}{% endraw %}
~~~
{: .language-plain-text }

## Permissions and Rendering Logic

lowFAT uses Django’s built-in authentication system. The Django admin exposes standard permissions, groups, staff status, and superuser status.

In practice, lowFAT currently relies mainly on `staff` and `superuser` status, together with view logic, template conditions, and custom template filters. The project does not currently use a fully configured group-based role model.

As the project evolved, reusable template filters and helper logic were introduced to reduce duplication and improve consistency across templates.

Examples include permission-aware filters such as:

- `can_edit_fund`
- `can_edit_expense`

These filters are used to control the visibility of actions such as edit buttons and status-dependent options.

## Template Filters and Tags

Custom template filters and tags are located in the Django `templatetags/` modules.

These are used to:

- simplify template logic,
- avoid duplicated conditions,
- and centralise reusable rendering behaviour.

<div class="box-note" >
When changing visibility or edit behaviour, check both the view logic and the related templates. Some actions may be hidden in templates while still requiring protection at the view level.
</div>

<div class="doc-pagination">
  <a class="doc-prev" href="{{ site.baseurl }}{% post_url 2026-05-08-data-model-overview %}">
    <span class="arrow">←</span>
    <span class="label">Data Model Overview</span>
  </a>

  <a class="doc-next" href="{{ site.baseurl }}{% post_url 2026-05-08-routing-and-naming-conventions %}">
    <span class="label">Routing and Naming Conventions</span>
    <span class="arrow">→</span>
  </a>
</div>