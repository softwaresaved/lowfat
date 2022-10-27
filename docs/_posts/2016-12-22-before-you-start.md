---
layout: page
title: "Before You Start"
category: dev
date: 2016-12-22 11:32:24
order: 1
---

**First off, thanks for taking the time to contribute!**

The following is a set of guidelines for contributing to lowFAT.
**These are just guidelines, not rules.**
Use your best judgment, and feel free to propose changes to this document in a pull request.

## License

LowFAT is licensed under the BSD 3-Clause License and by submiting any pull request to lowFAT you agree to make your contribution also avaiable under the BSD 3-Clause License.

## Code Style

We follow [PEP8](https://www.python.org/dev/peps/pep-0008/).

## Development Environment

If you are using [Anaconda](https://docs.continuum.io/anaconda/) you can run the follow commands:

To create a development server
~~~
python3 -m venv .venv
source .venv/bin/activate
pip3 install wheel
pip3 install -r requirements.txt
cp .env_template .env
# Add the Secret key to .env
# add 'DEBUG=True' to .env
bash bootstrap.sh
bash entrypoint.sh
python3 manage.py loaddata lowfat/fixtures/*.json
python3 manage.py createsuperuser
python3 manage.py runserver
~~~
{: .language-plain-text }

You can also start a production-like environment using Docker.
~~~
$ docker-compose up --build
~~~

## Testing

Testing and linting are handled by Tox.
Using Tox, we can check code style and run the unit and integration tests with a single command.

~~~
$ tox
~~~

We use [GitHub Actions](https://github.com/softwaresaved/lowfat/actions) to run these checks against new changes pushed to the GitHub repository.
These checks are triggered with any commit pushed to or any Pull Request submitted to the `master` or `dev` branches.
