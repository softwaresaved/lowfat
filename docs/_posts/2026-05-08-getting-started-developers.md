---
layout: page
title: "Getting Started"
category: dev
order: 1
---

lowFAT is a Django application used to support the administration of the Software Sustainability Institute Fellowship Programme.

This guide explains how to set up a local development environment for contributing to the project.

<div class="box-note" markdown="1">
The public Developer Guide focuses on contributor workflows, project structure, development setup, and general maintenance concepts.

Additional operational and deployment documentation is maintained separately for authorised maintainers. This includes production infrastructure, deployment procedures, backup and recovery operations, server configuration, and related operational guidance.
</div>

## Dependencies

lowFAT currently uses:

- Python 3.10+
- Django 4.2
- SQLite3

We use `venv` for Python environments. Other environment managers, such as Conda, may also work but are not documented here.

The repository also includes Docker-related files and configuration for deployment and infrastructure workflows, but the standard contributor workflow currently uses a local Python virtual environment.

## Initialisation

Only run the following commands after cloning the repository or when pulling new commits that require dependency or database updates.

Clone the repository:

~~~ bash
git clone https://github.com/softwaresaved/lowfat.git
cd lowfat
~~~
{: .language-plain-text }

Create and activate a Python virtual environment:

~~~ bash
python3 -m venv .venv
source .venv/bin/activate
~~~
{: .language-plain-text }

Install dependencies:

~~~ bash
pip3 install wheel
pip3 install -r requirements.txt
~~~
{: .language-plain-text }

Create a local environment file:

~~~ bash
cp .env_template .env
~~~
{: .language-plain-text }

Then edit `.env`:

- add a Django secret key
- ensure `DEBUG=True` is enabled for local development

Download and configure frontend assets:

~~~ bash
bash bootstrap.sh
~~~
{: .language-plain-text }

Apply database migrations and collect static files:

~~~ bash
bash entrypoint.sh
~~~
{: .language-plain-text }

Load the example development data:

~~~ bash
python3 manage.py loaddata lowfat/fixtures/*.json
~~~
{: .language-plain-text }

Create a superuser account:

~~~ bash
python3 manage.py createsuperuser
~~~
{: .language-plain-text }

Start the development server:

~~~ bash
python3 manage.py runserver
~~~
{: .language-plain-text }

## Run

Once the server starts you should see output similar to:

~~~ text
Performing system checks...

System check identified no issues (0 silenced).
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
~~~
{: .language-plain-text }

You should now be able to access the local development server at:

~~~
http://127.0.0.1:8000/
~~~
{: .language-plain-text }

<div class="box-note" markdown="1">
`bootstrap.sh` downloads and configures frontend assets such as Bootstrap, Font Awesome, Selectize, and related static files.

`entrypoint.sh` applies database migrations and collects static files before starting the application.
</div>

<div class="doc-pagination single">
  <a class="doc-next" href="{{ site.baseurl }}{% post_url 2026-05-08-development-workflow %}">
    <span class="label">Development Workflow</span>
    <span class="arrow">→</span>
  </a>
</div>