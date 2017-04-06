---
layout: page
title: "Before You Start"
category: dev
date: 2016-12-22 11:32:24
order: 1
---

**First off, thanks for taking the time to contribute!**

The following is a set of guidelines for contributing to FAT.
**These are just guidelines, not rules.**
Use your best judgment,
and feel free to propose changes to this document in a pull request.

## License

FAT is licensed under the BSD 3-Clause License and by submiting any pull request to FAT you agree to make your contribution also avaiable under the BSD 3-Clause License.

## Code style

We follow [PEP8](https://www.python.org/dev/peps/pep-0008/).

## Development Environment

If you are using [Anaconda](https://docs.continuum.io/anaconda/)
you can run the follow commands:

~~~
$ conda create -n lowfat python=3.6
$ git clone git@github.com:softwaresaved/lowfat.git
$ cd lowfat
$ git config core.hooksPath $(pwd)/hooks
$ source actiave lowfat
$ python -m pip install -r requirements.txt
~~~

Similar commands can be use if you aren't using Anaconda.

`git config core.hooksPath $(pwd)/hooks` will enable
a pre-commit hook to run the unit test collecion and
[Pylint](https://www.pylint.org/) to enforce PEP8.