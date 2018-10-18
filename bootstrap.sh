#!/bin/bash
#
# Configure the CSS.

STATIC_FOLDER=lowfat/static/
TMP_FOLDER=$(mktemp -d)
BOOTSTRAP_ZIP=${TMP_FOLDER}/bootstrap.zip
FONT_AWESOME_ZIP=${TMP_FOLDER}/fontawesome.zip
ACADEMICONS_ZIP=${TMP_FOLDER}/academicons.zip
GARLIC_ZIP=${TMP_FOLDER}/garlic.zip
DATETIME_WIDGET_ZIP=${TMP_FOLDER}/datetimewidget.zip
SELECTIZE_ZIP=${TMP_FOLDER}/selectize.zip
TAGULOUS_ZIP=${TMP_FOLDER}/tagulous.zip

# Bootstrap
curl \
    --silent \
    -L \
    -o $BOOTSTRAP_ZIP \
    https://github.com/twbs/bootstrap/releases/download/v3.3.6/bootstrap-3.3.6-dist.zip
unzip \
    -q \
    -u \
    $BOOTSTRAP_ZIP \
    -d $TMP_FOLDER

# Font Awesome
curl \
    --silent \
    -L \
    -o $FONT_AWESOME_ZIP \
    https://use.fontawesome.com/releases/v5.4.1/fontawesome-free-5.4.1-web.zip
unzip \
    -q \
    -u \
    $FONT_AWESOME_ZIP \
    -d $TMP_FOLDER

# Academicons
#
# Supplement for Font Awesome
curl \
    --silent \
    -L \
    -o $ACADEMICONS_ZIP \
    https://github.com/jpswalsh/academicons/archive/v1.8.6.zip
unzip \
    -q \
    -u \
    $ACADEMICONS_ZIP \
    -d $TMP_FOLDER

# Sorttable
mkdir -p $TMP_FOLDER/sorttable/js
curl \
    --silent \
    -L \
    -o $TMP_FOLDER/sorttable/js/sorttable.js \
    http://www.kryogenix.org/code/browser/sorttable/sorttable.js

# Garlic.js
mkdir -p $TMP_FOLDER/garlic/js
curl \
    --silent \
    -L \
    -o $GARLIC_ZIP \
    https://github.com/guillaumepotier/Garlic.js/archive/1.4.2.zip
unzip \
    -q \
    -p \
    $GARLIC_ZIP \
    Garlic.js-1.4.2/dist/garlic.min.js \
    > $TMP_FOLDER/garlic/js/garlic.min.js

# Datetime Widget
curl \
    --silent \
    -L \
    -o $DATETIME_WIDGET_ZIP \
    https://github.com/asaglimbeni/django-datetime-widget/archive/master.zip
unzip \
    -q \
    -u \
    $DATETIME_WIDGET_ZIP \
    -d $TMP_FOLDER
mv $TMP_FOLDER/django-datetime-widget-master/datetimewidget/static $TMP_FOLDER/datetimewidget/

# Selectize
mkdir -p $TMP_FOLDER/selectize/{css,js}
curl \
    --silent \
    -L \
    -o $SELECTIZE_ZIP \
    https://github.com/selectize/selectize.js/archive/v0.12.4.zip
unzip \
    -q \
    -p \
    $SELECTIZE_ZIP \
    selectize.js-0.12.4/dist/css/selectize.bootstrap3.css \
    > $TMP_FOLDER/selectize/css/selectize.bootstrap3.css
unzip \
    -q \
    -p \
    $SELECTIZE_ZIP \
    selectize.js-0.12.4/dist/js/standalone/selectize.min.js \
    > $TMP_FOLDER/selectize/js/selectize.min.js

# Tagulous
curl \
    --silent \
    -L \
    -o $TAGULOUS_ZIP \
    https://github.com/radiac/django-tagulous/archive/0.13.2.zip
unzip \
    -q \
    -u \
    $TAGULOUS_ZIP \
    "django-tagulous-0.13.2/tagulous/static/tagulous/*" \
    -d $TMP_FOLDER
cp -v -r $TMP_FOLDER/django-tagulous-0.13.2/tagulous/static/tagulous $STATIC_FOLDER

# Copy files
for folder in css fonts js
do
    cp -v -r $TMP_FOLDER/*/$folder $STATIC_FOLDER
done
