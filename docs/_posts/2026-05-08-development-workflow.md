---
layout: page
title: "Development Workflow"
category: dev
date: 2026-05-08 10:10:00
order: 2
---

lowFAT development is organised around GitHub issues, milestones, feature branches, and pull requests.

The workflow below describes the preferred process for planned development work. Maintainers may adapt this process for smaller maintenance changes or urgent fixes.

## Issues and Milestones

Development work should normally start from a GitHub issue.

1. Raise an issue on the [GitHub Issues](https://github.com/softwaresaved/lowfat/issues) page.
2. Add the issue to a relevant milestone.
3. Use the milestone to group related issues into a planned set of work.


## Branching Workflow

For planned development work, LowFAT uses milestone branches and issue branches.

The typical workflow is:

1. Create a milestone branch from `dev`.
2. Create issue branches from the milestone branch.
3. Make changes on the issue branch.
4. Commit the changes to the issue branch.
5. Open a pull request from the issue branch into the milestone branch.
6. Repeat this process for all issues included in the milestone.
7. Once the milestone work is complete and reviewed, open a pull request from the milestone branch into `dev`.
8. Close and delete the milestone once the pull request into `dev` has been accepted.

Issue branches should follow the naming convention:

~~~ text
<issue-number>-<short-issue-name>
~~~
{: .language-plain-text }

For example:

~~~ text
813-update-expense-statuses
~~~
{: .language-plain-text }

## Pull Requests

Pull requests should clearly describe:

- the issue being addressed,
- the changes made,
- any migrations or data changes,
- any manual testing carried out, and
- any documentation updates required.

Where possible, include the issue number in the pull request description.

## Testing

Before a milestone branch is merged into `dev`, the changes should be tested locally and through the automated checks configured for the repository.

See the [Testing]({{ site.baseurl }}{% post_url 2016-12-09-testing %}) page for details.

## From `dev` to `master`

The maintainers periodically review and test the `dev` branch. Once the branch is ready, changes are merged into `master`.

The `master` branch represents the stable branch used for production releases.

## Urgent Fixes

In rare cases, such as critical production bugs, maintainers may use a shorter workflow and merge a fix directly into `master`.

This should only be done when the risk of waiting for the normal milestone workflow is greater than the risk of making the urgent change.

<div class="box-note" markdown="1">
For routine development, prefer issue branches, milestone branches, pull requests, and testing through `dev` before changes reach `master`.
</div>

<div class="doc-pagination">
  <a class="doc-prev" href="{{ site.baseurl }}{% post_url 2026-05-08-getting-started-developers %}">
    <span class="arrow">←</span>
    <span class="label">Getting Started</span>
  </a>

  <a class="doc-next" href="{{ site.baseurl }}{% post_url 2026-05-08-project-structure %}">
    <span class="label">Project Structure</span>
    <span class="arrow">→</span>
  </a>
</div>