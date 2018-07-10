import os

from django_extensions.management.jobs import DailyJob

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter

class Job(DailyJob):
    help = "Convert Jupyter Notebook in lowfat/reports to HTML page in lowfat/reports/html."

    def execute(self):
       notebook_filenames = os.listdir("lowfat/reports")

       for notebook_filename in notebook_filenames:
            if not notebook_filename.endswith(".ipynb"):
                continue

            print("Processing lowfat/reports/{}".format(notebook_filename))

            # Based on Executing notebooks, nbconvert Documentation by Jupyter Development Team.
            # https://nbconvert.readthedocs.io/en/latest/execute_api.html
            with open("lowfat/reports/{}".format(notebook_filename)) as file_:
                nb = nbformat.read(file_, as_version=4)

                # Kernel is provided by https://github.com/django-extensions/django-extensions/
                ep = ExecutePreprocessor(timeout=600, kernel_name='django_extensions')
                ep.preprocess(nb, {'metadata': {'path': '.'}})

                html_exporter = HTMLExporter()
                html_exporter.template_file = 'basic'

                (body, resources) = html_exporter.from_notebook_node(nb)

                with open('lowfat/reports/html/{}.html'.format(notebook_filename), 'wt') as file_:
                    file_.write(body)
