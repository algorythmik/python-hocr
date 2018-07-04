import six
from bs4 import BeautifulSoup, UnicodeDammit

from .classes import Document


def parse(source):
    """Parse a HOCR stream into a Document object.
            @param[in] source
        Either a file-like object or a filename of the HOCR text.
    """
    # Coerce the source into content.
    if isinstance(source, six.string_types):
        if six.PY3:
            with open(source, 'r', encoding='utf-8') as stream:
                content = stream.read()
        if six.PY2:
            with open(source, 'r') as stream:
                    content = stream.read()
    else:
        content = source.read()

    # Parse the HOCR xml stream.
    ud = UnicodeDammit(content, is_html=True)

    # will take a while for a 500 page document
    soup = BeautifulSoup(ud.unicode_markup, 'lxml')

    # Get all the pages and parse them into page elements.
    html = soup.find('html')
    return Document(html) if html else None
