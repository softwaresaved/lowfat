---
layout: page
title: "Data Model Overview"
category: dev
order: 4
---

To help contributors understand the structure of lowFAT, we provide a visualisation of the database model.

<div class="doc-screenshot">
<div style="max-height: 650px; overflow-y: auto; border: 1px solid #ddd;">
  <a href="{{site.baseurl}}/img/models.png" target="_blank">
    <img src="{{site.baseurl}}/img/models.png"
         style="width:100%; cursor: zoom-in;"
         alt="Model visualisation">
  </a>
</div>
</div>

## Updating the Model Diagram

The model visualisation is generated using Django Extensions and Graphviz.

### Dependencies

You will need [Graphviz](https://graphviz.org/) installed on your machine.

On Debian or Ubuntu:

~~~ bash
sudo apt-get install graphviz
~~~
{: .language-plain-text }

You will also need Django Extensions installed in your development environment.

### Regenerating the Diagram

To regenerate the model diagram, run:

~~~ bash
python3 manage.py graph_models -a -g -o docs/img/models.png
~~~
{: .language-plain-text }

<div class="box-note" markdown="1">
The model diagram provides a high-level overview of the Django models and their relationships. Depending on the number of installed applications and historical models, the generated output may become large.
</div>

<div class="doc-pagination">
  <a class="doc-prev" href="{{ site.baseurl }}{% post_url 2026-05-08-project-structure %}">
    <span class="arrow">←</span>
    <span class="label">Project Structure</span>
  </a>

  <a class="doc-next" href="{{ site.baseurl }}{% post_url 2026-05-08-templates-and-permissions %}">
    <span class="label">Templates and Permissions</span>
    <span class="arrow">→</span>
  </a>
</div>