# pyhocr

pyhocr is a package to help you pull date out of hocr files.
(This parser is based on [https://github.com/concordusapps/python-hocr](https://github.com/concordusapps/python-hocr).)

## Installation

To install the module, run:

`pip install pyhocr`

# Usage
pyhocr parses the following elements from hocr:
- ocr pages: represented by `<ocr_page>`,
- ocr content areas: represented by `<ocr_carea`
- ocr paragraphs: represented by `<ocr_par>`
- ocr lines: represented by `<ocr_lines>`
- ocr words: represented by `<ocr_?words`

and  returns them  as `Page`, `Blocks`, `Paragraphs`, `Lines`, and `Words` objects respectively.

You can navigate through the hocr by asking for any children elements or the parent element. You can navigate down the strucure as:
```
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

You can also navigate up the data structre:
```
word = page.words[0]
# get parent page
page = word.page
# get parent line:
line = word.line
```
