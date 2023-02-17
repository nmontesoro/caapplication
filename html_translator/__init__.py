"""A module containing HTMLTranslator
"""

import argostranslate.translate
from translatehtml import translate_html
from bs4 import BeautifulSoup, Comment, Script, Stylesheet, PageElement
from queue import Queue, Empty
import logging
from time import time

log = logging.getLogger(__name__)

class HTMLTranslator:
  """A class to translate HTML files using argostranslate
  
  This class allows for translation of HTML files, with some caveats:
  
  * Comments are removed
  * All `script` tags are moved to the end of the `<body>` section
  * All `style` tags are moved to the end of the `<head>` section

  This is done as a workaround for some issues with the argostranslate
  API, so do not rely on this behavior as it may change if and when 
  those issues are fixed.

  Args:
      from_lang: Language to translate from.
      to_lang: Language to translate to.

      Both languages have to be provided in ISO 639-1 format.
  """

  _DOCTYPE_TAG = "<!DOCTYPE html>"
  _DOCTYPE_TAG_LEN = len(_DOCTYPE_TAG)
  _PARSER = "html.parser"

  def __init__(self, from_lang: str, to_lang: str) -> None:
    self._content = ""
    self._translated_content = ""
    self._setup_translation_environment(from_lang, to_lang)

  def _setup_translation_environment(self, str_from: str,
                                     str_to: str) -> None:
    lang_from = argostranslate.translate.get_language_from_code(str_from)
    lang_to = argostranslate.translate.get_language_from_code(str_to)

    if lang_from is not None and lang_to is not None:
      self._translation_obj = lang_from.get_translation(lang_to)
    else:
      raise ValueError(f"Language '{str_from}' or '{str_to}' "
                        "could not be found")

    if self._translation_obj is None:
      raise ValueError(f"No valid translations from '{str_from}' "
                        f"to '{str_to}' were found.")

  def translate(self, in_filename: str, out_filename: str = None) -> None:
    """Translates a file

    Check out the caveats in the docstring for this class!

    Args:
        in_filename: The name of the file to translate.
        out_filename: The name of the file to write. If unspecified,
          default behavior is to override the input file.
    
    Raises:
        OSError: An error ocurred while reading or writing from/to the 
          file.

    """
    self._in_filename = in_filename
    self._out_filename = (
      out_filename if out_filename is not None else in_filename)

    self._open_file()
    self._translate_contents()
    self._write_translated_contents()

  def _open_file(self) -> None:
    with open(self._in_filename, "rt", encoding="utf-8") as fp:
      self._content = fp.read()

  def _translate_contents(self) -> None:
    self._remove_conflicting_elements()
    soup = translate_html(self._translation_obj, self._content)
    # Why!?
    soup = BeautifulSoup(str(soup), "html.parser")
    self._add_conflicting_elements_back(soup)
    self._translated_content = HTMLTranslator._DOCTYPE_TAG + "\n" + \
      soup.prettify()

  def _remove_conflicting_elements(self) -> None:
    # This step is done to work around some issues in argostranslate.

    # First, we remove the <!DOCTYPE html> tag, as keeping this
    # caused the translated "html" text to be displayed at the top of
    # the final document.
    self._remove_doctype_tag()

    # I found that when keeping comments, their <!-- --> tags where
    # being stripped, leading to the content of the comment being
    # visible in the final document.
    # See https://github.com/argosopentech/translate-html/issues/9.
    self._remove_comments()

    # Finally, and this may be related to the previous issue: CSS and
    # Javascript were being HTML-encoded. Characters like '&' were
    # being escaped as '&amp;', which would result in invalid code.
    self._remove_scripts()
    self._remove_stylesheets()

  def _remove_doctype_tag(self) -> None:
    if self._content.startswith(HTMLTranslator._DOCTYPE_TAG):
      self._content = self._content[HTMLTranslator._DOCTYPE_TAG_LEN:]

  def _remove_comments(self) -> None:
    self._remove_tag(Comment)

  def _remove_scripts(self) -> None:
    self._scripts = self._remove_tag(Script)

  def _remove_stylesheets(self) -> None:
    self._stylesheets = self._remove_tag(Stylesheet)

  def _remove_tag(self, tag_class) -> list:
    soup = BeautifulSoup(self._content, self._PARSER)
    tags = soup.find_all(text=lambda text: isinstance(text, tag_class))
    removed_tags = []
    for tag in tags:
      removed_tags.append(tag.extract())
    self._content = str(soup)
    return removed_tags

  def _add_conflicting_elements_back(self, soup: BeautifulSoup) -> None:
    self._add_elems_to_soup(self._scripts, "script", "body", soup)
    self._add_elems_to_soup(self._stylesheets, "style", "head", soup)

  def _add_elems_to_soup(self, elems: list[PageElement], tag_name: str,
                         parent_name: str, soup: BeautifulSoup) -> None:
    parent = soup.find(parent_name)

    # For some reason, simply appending the PageElement objects that
    # we removed earlier causes issues in the final document. That's
    # why I'm re-creating each tag
    for elem in elems:
      elem_content = elem.string
      elem_tag = soup.new_tag(tag_name)
      elem_tag.string = elem_content
      parent.append(elem_tag)

  def _write_translated_contents(self) -> None:
    with open(self._out_filename, "wt", encoding="utf-8") as fp:
      fp.write(self._translated_content)
