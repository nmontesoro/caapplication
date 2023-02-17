"""A script to translate html files from English into Hindi.
"""

import logging
import datetime
import sys
from html_translator import HTMLTranslator

if len(sys.argv) < 2:
  print("Usage: translate_all file1.html [file2.html] ... [fileN.html]")
  sys.exit(0)

current_date_as_ISO = datetime.datetime.now().isoformat(timespec="seconds")

logging.basicConfig(level=logging.INFO, filename=f"{current_date_as_ISO}.log",
  format="%(asctime)s,%(created)f,%(levelname)s,%(name)s,%(message)s")

translator = HTMLTranslator("en", "hi")
files = sys.argv[1:]

try:
  for file in files:
    logging.info("Translating '%s'", file)
    translator.translate(file)
except Exception as e: # pylint: disable=broad-exception-caught
  logging.exception("An unexpected error ocurred")
  sys.exit(1)
