import re

import six


class BBox(object):

    def __init__(self, text=None, left=0, right=0, top=0, bottom=0):

        # Parse the text string representation if given.
        if text is not None:
            left, top, right, bottom = map(int, text.split())

        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    @property
    def width(self):
        return self.right - self.left

    @property
    def height(self):
        return self.bottom - self.top

    @property
    def coords(self):
        return (self.top, self.left, self.right, self.bottom)

    def __repr__(self):
        return '<Box(%r, %r, %r, %r)>' % (
            self.left, self.top, self.right, self.bottom)


class Base(object):

    _hierarchy = ['pages', 'blocks', 'paragraphs', 'lines', 'words']

    _dir_methods = []

    def __init__(self, element):  # noqa
        """
        @param[in] element
            XML node for the OCR element.
        """
        # Store the element for later reference.
        self._element = element

        # Create an element cache.
        self._cache = {}

        # Parse the properties of the HOCR element.
        properties = element.get('title', '').split(';')
        for prop in properties:
            prop = prop.strip()

            if six.PY3:
                name, value = prop.split(maxsplit=1)
            else:
                name, value = prop.split(' ', 1)

            if name == 'bbox':
                self.bbox = BBox(value)

            elif name == 'image':
                self.image = value.strip('" ')

            elif name == 'x_wconf':
                self.wconf = int(value)

            elif name == 'textangle':
                self.textangle = int(value)
                if value == '90':
                    self.vertical = True

            elif name == 'x_size':
                self.size = value

            elif name == 'x_ascenders':
                self.ascenders = float(value)

            elif name == 'x_descenders':
                self.descenders = float(value)

            elif name == 'ppageno':
                self.ppageno = int(value)

    def __dir__(self):

        if six.PY3:
            return super().__dir__() + list(self._allowed_ocr_childs)
        else:
            return list(
                self._allowed_ocr_childs) + getattr(self, '_dir_methods', [])
            return super(
                Base, self).__dir__() + list(self._allowed_ocr_childs)

    def __getattr__(self, name):
        # Return the cached version if present.
        if name in self._cache:
            return self._cache[name]

        # Parse the named OCR elements.
        if name in self._allowed_ocr_childs:
            ref = OCR_CLASSES[name]
            nodes = self._element.find_all(class_=re.compile(ref['name']))
            self._cache[name] = elements = list(map(ref['class'], nodes))
            return elements

        if name + 's' in self._allowed_ocr_parents:
            name = name + 's'
            ref = OCR_CLASSES[name]
            node = self._element.find_parent(class_=ref['name'])
            self._cache[name] = element = ref['class'](node)
            return element

        # Attribute is not present.
        raise AttributeError(name)


class Word(Base):

    _dir_methods = ['bbox', 'bold', 'italic', 'lang', 'wconf']

    def __init__(self, element):
        # Initialize the base.
        if six.PY3:
            super().__init__(element)
        else:
            super(Word, self).__init__(element)
        self._allowed_ocr_childs = self._hierarchy[5:]
        self._allowed_ocr_parents = self._hierarchy[:4]
        # Discover if we are "bold".
        # A word element is bold if its text node is wrapped in a <strong/>.
        self.bold = bool(element.find('strong'))

        # Discover if we are "italic".
        # A word element is italic if its text node is wrapped in a <em/>.
        self.italic = bool(element.find('em'))

        # Find the text node.
        self.text = element.text

        self.lang = element.get("lang", '')

    def __str__(self):
        return '<Word(%r, %r)>' % (self.text, self.box)


class Line(Base):

    _dir_methods = ['bbox', 'text', 'vertical', 'textangle']
    vertical = False
    textangle = 0

    def __init__(self, element):
        if six.PY3:
            super().__init__(element)
        else:
            super(Line, self).__init__(element)
        self._allowed_ocr_childs = self._hierarchy[4:]
        self._allowed_ocr_parents = self._hierarchy[:3]

    @property
    def text(self):
        return ' '.join([w.text for w in self.words])


class Paragraph(Base):
    _dir_methods = ['bbox', ]

    def __init__(self, element):
        if six.PY3:
            super().__init__(element)
        else:
            super(Word, self).__init__(element)
        self._allowed_ocr_childs = self._hierarchy[3:]
        self._allowed_ocr_parents = self._hierarchy[:2]


class Block(Base):

    _dir_methods = ['bbox', ]

    def __init__(self, element):
        if six.PY3:
            super().__init__(element)
        else:
            super(Word, self).__init__(element)
        self._allowed_ocr_childs = self._hierarchy[2:]
        self._allowed_ocr_parents = self._hierarchy[:1]


class Page(Base):

    def __init__(self, element):
        if six.PY3:
            super().__init__(element)
        else:
            super(Page, self).__init__(element)
        self._allowed_ocr_childs = self._hierarchy[1:]
        self._allowed_ocr_parents = self._hierarchy[:0]

    _dir_methods = ['image', ]


OCR_CLASSES = {
    'words': {'name': 'ocr.?_word', 'class': Word},
    'lines': {'name': 'ocr_line', 'class': Line},
    'paragraphs': {'name': 'ocr_par', 'class': Paragraph},
    'blocks': {'name': 'ocr_carea', 'class': Block},
    'pages': {'name': 'ocr_page', 'class': Page}
}
