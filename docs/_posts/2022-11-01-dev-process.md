---
layout: page
title: "Development Cycle"
category: dev
date: 2022-11-01 14:41:00
order: 4
---

## Development Lifecycle

The development lifecycle for LowFAT should follow this pattern.

1. Raise issues at the [GitHub Issues](https://github.com/softwaresaved/lowfat/issues) page.
2. Collect issues into a milestone at [GitHub Milestones](https://github.com/softwaresaved/lowfat/milestones).
3. Create a milestone branch off the [dev branch](https://github.com/softwaresaved/lowfat/tree/dev).
4. Open issue branches using the development pane following the branch naming convention <issue-number>-<issue-name>.
   1. Make changes on the issue branch.
   2. Commit to the branch.
   3. Open a pull request into the milestone branch.
   4. Close the issue when pull request is accepted.
5. Once milestone is complete open a peer-reviewed pull request from the milestone branch into dev.
6. Close and delete the milestone once the pull request is accepted.

## Pull to main

The maintainers of LowFAT will periodically run full tests on the dev branch. On success open pull requests to main and 
deploy new versions. In rare occasions where critical bugs arise issue branches will be pulled directly to main.

