---
layout: default
title: "FAT Documentation"
---

# LowFAT User and Developer Guide

Welcome to the documentation of the Software Sustainability Institute's Fellowship Administration Tool (FAT).

## Users
### Fellows

### Staff

## Developers

LowFAT is open source anyone can make a copy and add remove features. For those looking to add (or remove) functionality
from LowFAT they should follow this guide. For SSI staff , or external contributors, working directly on the LowFAT 
repository careful consideration should be paid to the workflow section to ensure adherence to our development practice.

#### License

LowFAT is licensed under the BSD 3-Clause License and by submiting any pull request to lowFAT you agree to make your contribution also avaiable under the BSD 3-Clause License.

#### Code Style

We follow [PEP8](https://www.python.org/dev/peps/pep-0008/).


#### Guides
To install LowFAT and start a local working server.

[Setup]({% post_url 2016-12-09-setup %})

For testing on the local server including logging in as an admin or a user.

[Testing]({% post_url 2016-12-09-testing %})

Before making changes please now familiarise yourself with the following information:
- [Files]({% post_url 2016-12-09-file-system %})
- [Style Guide and URL patterns]({% post_url 2017-07-25-url %})
- [Models]({% post_url 2017-02-15-models %})
- [Model View Controller]({% post_url 2017-04-20-mvc %})
- [GitHub OAuth]({% post_url 2016-12-09-github %})

Now you should be ready to plan your update be it adding a feature, fixing a bug, or updating the styling. To ease the 
development cycle we impose the following process. 

[Development Cycle]({% post_url 2022-11-01-dev-process %})

For backing up the database in preparation for a site update.

[Backup]({% post_url 2016-12-09-backup %})




### Reuse and Redistribution

We wrote FAT to be one of our internal tools, but it is released under the BSD 3-Clause License and you are welcome to re-use it.

**If you have any questions, please open an issue on [GitHub](https://github.com/softwaresaved/lowfat/issues).**

