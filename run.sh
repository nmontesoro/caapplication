#!/bin/bash

WEBSITE=https://www.classcentral.com/* # Website to scrape
HTT_OUTPUT_DIR=./original              # Directory for original files
FINAL_DIR=./translated                 # Directory for translated files
LEVEL=2                                # How many levels (1 = homepage)

# Scrapes the website into a specified directory.
httrack $WEBSITE +* -r$LEVEL -O $HTT_OUTPUT_DIR -v --update

# Create a copy of the downloaded files
rsync -avhP $HTT_OUTPUT_DIR/ $FINAL_DIR/

# Finds every html file inside the output directory and passes it to the
# translation script. This script overwrites all these files.
echo "Now translating files. This might take a while..."
find $OUTPUT_DIR/ -type f -name "*.html" \
    -exec python3.9 translate_all.py '{}' \+
