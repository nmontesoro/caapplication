#!/bin/bash

WEBSITE=https://www.classcentral.com/ # Website to scrape
HTT_OUTPUT_DIR=original               # Directory for original files
FINAL_DIR=translated                  # Directory for translated files
LEVEL=2                               # How many levels (1 = homepage)

# Scrapes the website into a specified directory.
httrack $WEBSITE +* -r$LEVEL -O $HTT_OUTPUT_DIR -v -F "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

# Create a copy of the downloaded files
rsync -avhP $HTT_OUTPUT_DIR/ $FINAL_DIR/

# Finds every html file inside the output directory and passes it to the
# translation script. This script overwrites all these files.
echo "Now translating files. This might take a while..."
find $FINAL_DIR/ -type f -name "*.html" \
    -exec python3.9 translate_all.py '{}' \+
