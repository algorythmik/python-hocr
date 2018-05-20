# pyhocr

pyhocr is a package to help you pull data out of hocr files.

## Installation

To install the module, run:

`pip install pyhocr`

## Usage
pyhocr parses the following elements from hocr:
- ocr pages: represented by `<ocr_page>`,
- ocr content areas: represented by `<ocr_carea`
- ocr paragraphs: represented by `<ocr_par>`
- ocr lines: represented by `<ocr_lines>`
- ocr words: represented by `<ocr?_words`

and  returns them  as `Page`, `Blocks`, `Paragraphs`, `Lines`, and `Words` objects respectively.

You can navigate through the hocr by asking for any children elements or any parent element. You can navigate down the strucure like:
```python
import pyhocr.parser
filepath = 'example.hocr'
page = pyhocr.parser.parse(stream)[0]
# pulling all lines out:
lines = page.lines
# getting text of last line
last_line_text = lines[-1].text
# getting all words of page
words = page.words
```

Or navigate up the data structre by:
```python
# get parent page
page = word.page
# get parent line:
line = word.line
# get parent block
line = word.block
# get parent page of the block
page = block.page
```
