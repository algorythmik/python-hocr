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
        return self.left, self.top, self.right, self.bottom

    def __repr__(self):
        return '<Box(%r, %r, %r, %r)>' % (
            self.left, self.top, self.right, self.bottom)


class Base(object):

    _tag_hierarchy = ['document', 'page', 'block', 'paragraph', 'line', 'word']
    _dir_methods = []

    def __init__(self, soup_element):
        """
        @param[in] element
            XML node for the OCR element.
        """
        # Store the element for later reference.
        self._element = soup_element

        # Create an element cache.
        self._cache = {}

        name = self.__class__.__name__.lower()
        self._allowed_childs = \
            [child_name + 's' for child_name in
             self._tag_hierarchy[self._tag_hierarchy.index(name) + 1:]]
        self._allowed_parents = \
            self._tag_hierarchy[:self._tag_hierarchy.index(name)]

        # Parse the properties of the HOCR element.
        properties_raw = soup_element.get('title')
        properties = properties_raw.split(';') if properties_raw else []
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
            super_dir = dir(super())
        else:
            super_dir = dir(super(Base, self))

        return super_dir + self._allowed_childs +\
            self._allowed_parents + getattr(self, '_dir_methods', [])

    def __getattr__(self, name):
        classes = {
            'document': Document,
            'word': Word,
            'line': Line,
            'paragraph': Paragraph,
            'block': Block,
            'page': Page,
        }
        norm_name = name.rstrip('s')

        # Return the cached version if present.
        if name in self._cache:
            return self._cache[name]

        # Parse the named OCR elements.
        if name in self._allowed_childs:
            class_ = classes[norm_name]
            nodes = self._element.find_all(**class_.soup_params)
            self._cache[name] = elements = list(map(class_, nodes))
            return elements

        if name in self._allowed_parents:
            class_ = classes[norm_name]
            node = self._element.find_parent(**class_.soup_params)
            self._cache[name] = element = class_(node)
            return element

        # Attribute is not present.
        raise AttributeError(name)

    def __eq__(self, other):
        return self._element == other._element


class Document(Base):
    soup_params = {'name': 'html'}

    def __init__(self, element):
        if six.PY3:
            super().__init__(element)
        else:
            super(Document, self).__init__(element)


class Word(Base):
    soup_params = {'class_': 'ocrx_word'}
    _dir_methods = ['bbox', 'bold', 'italic', 'lang', 'wconf']

    def __init__(self, element):
        # Initialize the base.
        if six.PY3:
            super().__init__(element)
        else:
            super(Word, self).__init__(element)
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
        return "<Word('{}', {})>".format(self.text, self.bbox)


class Line(Base):
    soup_params = {'class_': 'ocr_line'}
    _dir_methods = ['bbox', 'text', 'vertical', 'textangle']
    vertical = False
    textangle = 0

    def __init__(self, element):
        if six.PY3:
            super().__init__(element)
        else:
            super(Line, self).__init__(element)

    @property
    def text(self):
        return ' '.join([w.text for w in self.words])


class Paragraph(Base):
    soup_params = {'class_': 'ocr_par'}
    _dir_methods = ['bbox', ]

    def __init__(self, element):
        if six.PY3:
            super().__init__(element)
        else:
            super(Paragraph, self).__init__(element)


class Block(Base):
    soup_params = {'class_': 'ocr_carea'}
    _dir_methods = ['bbox', ]

    def __init__(self, element):
        if six.PY3:
            super().__init__(element)
        else:
            super(Block, self).__init__(element)


class Page(Base):
    soup_params = {'class_': 'ocr_page'}

    def __init__(self, element):
        if six.PY3:
            super().__init__(element)
        else:
            super(Page, self).__init__(element)

    _dir_methods = ['image', ]


class HOCRParseError(ValueError):
    pass
