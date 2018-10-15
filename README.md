[![Build Status](https://travis-ci.com/algorythmik/python-hocr.svg?branch=master)](https://travis-ci.com/algorythmik/python-hocr)

# pyhocr

pyhocr is a Python package to help you parse and navigate hocr documents.

## Installation

To install the module, run:

`pip install pyhocr`

## Usage

pyhocr parses the following elements from hocr:
- ocr pages: represented by `<ocr_page>`,
- ocr content areas: represented by `<ocr_carea>`
- ocr paragraphs: represented by `<ocr_par>`
- ocr lines: represented by `<ocr_lines>`
- ocr words: represented by `<ocr?_words`

and  returns them  as `Page`, `Blocks`, `Paragraphs`, `Lines`, and `Words` objects respectively.

You can navigate through the hocr by asking for any children elements or any parent element. You can navigate down the structure like:

```python
import pyhocr

with open('example.hocr') as f:
    hocr_string = f.read()

hocr_document = pyhocr.parse(hocr_string)

# get the first page
page = hocr_document.pages[0]

# pulling all lines out:
lines = page.lines

# getting text of last line
last_line_text = lines[-1].text

# getting all words of page
words = page.words
```

Or navigate up the data structure by:

```python
# get parent page
page = word.page

# get parent line
line = word.line

# get parent block
line = word.block

# get parent page of the block
page = block.page
```

## Contributions

Please feel free to post pull requests or report issues.
