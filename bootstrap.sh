#!/bin/bash
#
# Configure the CSS.

STATIC_FOLDER=fat/static/
TMP_FOLDER=/tmp/
BOOTSTRAP_ZIP=/tmp/bootstrap.zip
FONT_AWESOME_ZIP=/tmp/fontawesome.zip
ACADEMICONS_ZIP=/tmp/academicons.zip
GARLIC_ZIP=/tmp/garlic.zip

# Bootstrap
curl \
    -L \
    -o $BOOTSTRAP_ZIP \
    https://github.com/twbs/bootstrap/releases/download/v3.3.6/bootstrap-3.3.6-dist.zip
unzip \
    -u \
    $BOOTSTRAP_ZIP \
    -d $TMP_FOLDER

# Font Awesome
curl \
    -L \
    -o $FONT_AWESOME_ZIP \
    https://github.com/FortAwesome/Font-Awesome/archive/v4.6.3.zip
unzip \
    -u \
    $FONT_AWESOME_ZIP \
    -d $TMP_FOLDER

# Academicons
#
# Supplement for Font Awesome
curl \
    -L \
    -o $ACADEMICONS_ZIP \
    https://github.com/jpswalsh/academicons/archive/v1.7.0.zip
unzip \
    -u \
    $ACADEMICONS_ZIP \
    -d $TMP_FOLDER

# Sorttable
mkdir -p $TMP_FOLDER/sorttable/js
curl \
    -L \
    -o $TMP_FOLDER/sorttable/js/sorttable.js \
    http://www.kryogenix.org/code/browser/sorttable/sorttable.js

# Garlic.js
mkdir -p $TMP_FOLDER/garlic/js
curl \
    -L \
    -o $GARLIC_ZIP \
    https://github.com/guillaumepotier/Garlic.js/archive/1.2.4.zip
unzip \
    -p \
    $GARLIC_ZIP \
    Garlic.js-1.2.4/dist/garlic.min.js \
    > $TMP_FOLDER/garlic/js/garlic.min.js

# Copy files
for folder in css fonts js
do
    cp -r $TMP_FOLDER/*/$folder $STATIC_FOLDER
done
