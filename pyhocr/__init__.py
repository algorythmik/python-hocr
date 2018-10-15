from bs4 import BeautifulSoup, UnicodeDammit

from .classes import Document, HOCRParseError


def parse(content):
    """Parse a HOCR string into a Document object.
    """
    # Parse the HOCR xml string.
    ud = UnicodeDammit(content, is_html=True)
    soup = BeautifulSoup(ud.unicode_markup, 'lxml')

    # Get all the pages and parse them into page elements.
    html = soup.find('html')

    if html is None:
        raise(HOCRParseError('No html tag was found!'))

    return Document(html)
