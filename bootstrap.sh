#!/bin/bash
#
# Configure the CSS.

STATIC_FOLDER=fat/static/
TMP_FOLDER=/tmp/
BOOTSTRAP_ZIP=/tmp/bootstrap.zip
FONT_AWESOME_ZIP=/tmp/fontawesome.zip

# Bootstrap
curl \
    -L \
    -o $BOOTSTRAP_ZIP \
    https://github.com/twbs/bootstrap/releases/download/v3.3.6/bootstrap-3.3.6-dist.zip
unzip \
    $BOOTSTRAP_ZIP \
    -d $TMP_FOLDER

# Font Awesome
curl \
    -L \
    -o $FONT_AWESOME_ZIP \
    https://github.com/FortAwesome/Font-Awesome/archive/v4.6.3.zip
unzip \
    $FONT_AWESOME_ZIP \
    -d $TMP_FOLDER

# Copy files
for folder in css fonts js
do
    cp -r $TMP_FOLDER/*/$folder $STATIC_FOLDER
done
