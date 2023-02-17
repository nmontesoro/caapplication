# My application for Coding Allstars

## What does it do?

All the steps performed are in `run.sh`. Basically, we first scrape the website
using `httrack`, then we create a copy of the files in a different directory and
call the main Python script, `translate_all.py`.

## How does it work?

I developed the class `HTMLTranslator` to handle everything regarding
translation. All that needs to be done is instantiate an object of said class,
telling it the origin and target languages, and then call the only public
method `translate`, which takes an input filename.

I decided against using the Google Translate API as I had no direct
experience with any of Google's APIs and had some issues setting up billing
information. Instead, I went with
[LibreTranslate](https://github.com/LibreTranslate/LibreTranslate),
a free and open-source machine translation API that can be self-hosted or
used directly with the `argostranslate` library for Python, though I had to
write my own script to translate HTML files because the one provided didn't
give me the flexibility I wanted.

If in the future the Google Translate API was absolutely necessary, I am
confident that the `HTMLTranslator` class could be modified with no alterations
to its public API.

While there's probably room for improvement, I believe that the code here is
not only functional, but clean, organized and reasonably well-documented.

## Some caveats

As of February 2023, there appear to be some
[issues](https://github.com/argosopentech/translate-html/issues/9) with the
`argostranslate` package. As a temporary workaround, all comments inside the
HTML files have to be removed, and `script` and `style` tags have to be moved
around. This should not affect the performance or look of the websites, but
is something to bear in mind.

Also, because PyTorch, a dependency of `argostranslate`,
[doesn't support Python 3.11 yet](https://github.com/pytorch/pytorch/issues/86566), these scripts have to be run with Python 3.9.
