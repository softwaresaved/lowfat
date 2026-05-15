---
layout: page
title: "Project Structure"
category: dev
date: 2026-05-08 10:20:00
order: 3
---

This page provides a high-level overview of the lowFAT repository structure and the purpose of the main files and directories.

The goal is to help contributors and maintainers understand where different parts of the project are located.

## Repository Root

The lowFAT repository contains the Django application itself, the public documentation site, development tooling, testing configuration, and deployment-related files.

## Core Application

### `lowfat/`

The main Django application.

This directory contains:

- models,
- views,
- forms,
- templates,
- template tags,
- admin configuration,
- URL routing,
- email logic,
- and related application code.

### `manage.py`

Django management entry point used for:

- running the development server,
- migrations,
- loading fixtures,
- creating superusers,
- running tests,
- and other management commands.

### `db.sqlite3`

Default local development database.

Local development uses SQLite by default.

## Documentation

### `docs/`

Documentation source for the public GitHub Pages site.

The documentation pages are written in Markdown and generated using Jekyll.

### `README.md`

Repository overview and entry point for contributors.

### `CONTRIBUTING.md`

Contribution workflow and GitHub contribution guidance.

### `CITATION`

Citation information for the project.

## Static and Uploaded Files

### `static/`

Collected static files used by the application.

### `upload/`


Directory used for uploaded files and media content.

### `tmp/`

Temporary files generated during local development and testing.

## Development and Testing

### `requirements.txt`

Main Python dependencies for the project.

### `requirements-devel.txt`

Additional dependencies used during development.

### `tox.ini`

Configuration for automated testing and linting.

### `bootstrap.sh`

Downloads and configures frontend dependencies and static assets.

### `entrypoint.sh`

Applies migrations and collects static files before starting the application.

### `workflow/`

Project workflow and issue-management related documentation used during development and maintenance.

## Deployment and Infrastructure

### `Dockerfile`

Container build configuration for Docker-based environments.

### `docker-compose.yml`

Multi-container deployment configuration.

### `Caddyfile`

Configuration for the Caddy web server.

### `Makefile`

Common development and deployment helper commands.

<div class="box-note" markdown="1">
The public developer documentation focuses on repository structure, development workflows, and contributor guidance.

Operational deployment details, infrastructure credentials, production procedures, and security-sensitive configuration are maintained separately from the public documentation.
</div>

<div class="doc-pagination">
  <a class="doc-prev" href="{{ site.baseurl }}{% post_url 2026-05-08-development-workflow %}">
    <span class="arrow">←</span>
    <span class="label">Development Workflow</span>
  </a>

  <a class="doc-next" href="{{ site.baseurl }}{% post_url 2026-05-08-data-model-overview %}">
    <span class="label">Data Model Overview</span>
    <span class="arrow">→</span>
  </a>
</div>