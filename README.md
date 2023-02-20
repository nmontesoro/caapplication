# My application for Coding Allstars

## What was the trial task?

TD;DR: Copy ClassCentral pages and translate them into Hindi.

The trial task consisted of scraping
[ClassCentral](https://www.classcentral.com/) one level deep using `httrack`, a
custom script or another app, then translating the text inside the HTML to
Hindi, which would be hardcoded into the page.

Once all files were translated, they would be uploaded to a webserver. Special
care had to be taken to ensure all the Javascript, CSS, etc. was loading
correctly.

Having completed all of that, I had to fill in a form sending them a URL to the
live website (in this case, I used
[Github Pages](https://nmontesoro.github.io/caapplication/)) and letting them
know how I scraped the pages.

## What does the code do?

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

There are some advantages to using this API: there's no restrictions to how many
characters you can translate at a time, or how many requests you can make in a
day. And since the library can utilize hardware acceleration using Nvidia's
CUDA cores, the performance isn't bad at all: translating all 288 HTML files
on my laptop took 3h40m, around 45 seconds per file. And I believe that number
could be brought down even more if my script implemented some sort of
multi-processing.

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
[doesn't support Python 3.11 yet](https://github.com/pytorch/pytorch/issues/86566),
these scripts have to be run with Python 3.9.
