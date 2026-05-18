---
layout: page
title: "Data Management and Backups"
category: dev
date: 2026-05-08 11:40:00
order: 11
---

lowFAT stores application data, uploaded files, workflow information, and user-submitted content related to Fellowship administration.

Backups and data management are therefore an important part of maintaining a deployment safely and responsibly.

## Backup Support

lowFAT includes support for database and media backups using [django-dbbackup](https://django-dbbackup.readthedocs.io/).

Typical backup operations include:

- database backups,
- uploaded media backups,
- encrypted backup archives,
- and scheduled backup jobs.

## Encryption

The project supports encrypted backups using GPG.

Runtime backup behaviour and encryption settings are configured through the Django settings and deployment environment.

## Media and Uploaded Files

Uploaded files and media content are typically stored separately from the application source code.

This may include:

- uploaded receipts,
- supporting documents,
- profile images,
- and related workflow files.

## Operational Responsibility

Production backup, restore, retention, and disaster-recovery procedures are operational responsibilities and should be maintained separately from the public contributor documentation.

Deployment maintainers should ensure that:

- backups are performed regularly,
- backup data is stored securely,
- encrypted backups are handled safely,
- restore procedures are periodically tested,
- and sensitive information is protected appropriately.

## Related Configuration

Backup-related configuration may involve:

- `django-dbbackup`
- Django settings
- storage locations
- scheduled tasks
- and deployment-specific infrastructure configuration

<div class="box-warning" markdown="1">
Do not publish production backup paths, secrets, encryption keys, credentials, or operational recovery procedures in the public documentation.
</div>

<div class="doc-pagination single">
  <a class="doc-prev" href="{{ site.baseurl }}{% post_url 2026-05-08-privacy %}">
    <span class="arrow">←</span>
    <span class="label">Privacy and Data Visibility</span>
  </a>
</div>