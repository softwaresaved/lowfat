#!/bin/bash
#
# Configure the CSS.

STATIC_FOLDER=fellowms/static/
TMP_FOLDER=/tmp/
ZIP_FILE=/tmp/bootstrap.zip

curl \
    -L \
    -o $ZIP_FILE \
    https://github.com/twbs/bootstrap/releases/download/v3.3.6/bootstrap-3.3.6-dist.zip
unzip \
    $ZIP_FILE \
    -d $TMP_FOLDER
mkdir $STATIC_FOLDER
for folder in css fonts js
do
    cp -r $TMP_FOLDER/*/$folder $STATIC_FOLDER
done
