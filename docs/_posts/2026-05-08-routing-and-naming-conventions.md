---
layout: page
title: "Routing and Naming Conventions"
category: dev
date: 2026-05-08 10:50:00
order: 6
---

lowFAT routes are defined in `lowfat/urls.py`.

This page summarises the main routing conventions used in the project. It does not list every route, because route availability depends on the user, the submission type, the current status, and the relevant view-level permissions.

## Main Route Areas

lowFAT groups related routes by workflow area.

| Route area                  | Purpose                           |
|-----------------------------|-----------------------------------|
| `/`                         | Public home page                  |
| `/dashboard/`               | Authenticated user dashboard      |
| `/my-profile/`              | Current user's profile            |
| `/claimant/` and `/fellow/` | Claimant/Fellow profile views     |
| `/request/`                 | Funding request workflow          |
| `/fund/`                    | Namespaced funding request routes |
| `/expense/`                 | Standalone expense claim workflow |
| `/blog/`                    | Blog post workflow                |
| `/staff/`                   | Staff dashboard and staff views   |
| `/public/`                  | Token-based public access routes  |
| `/admin/`                   | Django admin site                 |
| `/pages/`                   | Django FlatPages                  |

## Workflow Routes

Funding requests, expense claims, and blog posts use related route patterns for actions such as viewing, editing, reviewing, or removing records.

However, the existence of a route in `lowfat/urls.py` does not mean that the action is available to every user in the interface.

For example:

- Fellows can create submissions and may edit them only in specific allowed states.
- Staff users review submissions and update review/status information, but do not normally edit submitted content directly.
- Superusers and Django Admin users have broader administrative access.
- Some legacy or administrative routes may still exist even when the corresponding action is hidden from normal dashboard views.

When changing user-facing behaviour, check both:

- the route definition in `lowfat/urls.py`
- the relevant view, template, form, and template filters

## Public Routes

Routes under `/public/` use access tokens and are intended for public or unauthenticated workflows where appropriate.

Examples include public funding request, expense claim, and blog post routes.

These should be handled carefully, because access is controlled by the token and the relevant view logic.

## Source of Truth

Use `lowfat/urls.py` as the source of truth for route definitions.

Use the templates and views to understand whether a route is exposed in the interface and under what conditions.

<div class="box-note" markdown="1">
Do not assume that a route is available to a user just because it exists in `lowfat/urls.py`. lowFAT behaviour depends on role, status, view logic, templates, and custom permission filters.
</div>

<div class="doc-pagination">
  <a class="doc-prev" href="{{ site.baseurl }}{% post_url 2026-05-08-templates-and-permissions %}">
    <span class="arrow">←</span>
    <span class="label">Templates and Permissions</span>
  </a>

 <a class="doc-next" href="{{ site.baseurl }}{% post_url 2026-05-08-testing %}">
    <span class="label">Testing</span>
    <span class="arrow">→</span>
  </a>
</div>