from os import path

from pytest import raises

import pyhocr.page
import pyhocr.parser

BASE_DIR = path.dirname(__file__)


def parse(filename='example.html'):
    return pyhocr.parser.parse(path.join(BASE_DIR, filename))


class TestParse:

    def test_parse_from_stream(self):
        with open(path.join(BASE_DIR, 'example.html'), 'rb') as stream:
            pages = pyhocr.parser.parse(stream)

            assert len(pages) == len(parse('example.html'))

    def test_get_number_of_pages(self):
        assert len(parse()) == 1

    def test_parse_return_datastructure_is_pages(self):
        for item in parse():
            assert isinstance(item, pyhocr.page.Page)

    def test_page_elements_in_dir(self):
        page = parse()[0]

        assert 'words' in dir(page)
        assert 'blocks' in dir(page)


class TestPage:

    def test_page_has_proper_attribute_error(self):
        page = parse()[0]

        with raises(AttributeError):
            page.shjgioda

    def test_page_has_bounding_box(self):
        for page in parse():
            assert page.bbox.left >= 0

    def test_page_bounding_box_has_correct_value(self):
        page = parse()[0]

        assert page.bbox.left == 0
        assert page.bbox.top == 0
        assert page.bbox.right == 5100
        assert page.bbox.bottom == 6600

    def test_page_has_image_name(self):
        page = parse()[0]

        assert page.image == '/tmp/tmpepham8.tiff'

    def test_page_has_blocks(self):
        page = parse()[0]

        assert len(page.blocks) == 3

    def test_page_has_words(self):
        page = parse()[0]

        assert len(page.words) == 2665

    def test_page_blocks_have_paragraphs(self):
        page = parse()[0]

        assert len(page.blocks[0].paragraphs) == 1
        assert len(page.blocks[1].paragraphs) == 50
        assert len(page.blocks[2].paragraphs) == 1

    def test_page_block_paragraphs_have_lines(self):
        page = parse()[0]

        assert len(page.blocks[1].paragraphs[0].lines) == 2
        assert len(page.blocks[1].paragraphs[10].lines) == 1
        assert len(page.blocks[1].paragraphs[20].lines) == 1
        assert len(page.blocks[2].paragraphs[0].lines) == 1

    def test_page_block_paragraph_lines_have_words(self):
        page = parse()[0]

        assert len(page.blocks[0].paragraphs[0].lines[0].words) == 3
        assert len(page.blocks[1].paragraphs[0].lines[0].words) == 3
        assert len(page.blocks[1].paragraphs[10].lines[0].words) == 54


class TestBlock:

    def test_block_has_page(self):
        page = parse()[0]
        for block in page.blocks:
            assert isinstance(block.page, pyhocr.page.Page)


class TestWord:

    def test_word_reper(self):
        word = parse()[0].words[0]
        assert str(word) == "<Word('TABLE', <Box(2216, 1049, 2449, 1098)>)>"

    def test_word_parents_in_dir(self):
        word = parse()[0].words[0]
        parents = ['page', 'block', 'paragraph', 'line']
        dir_ = dir(word)
        assert all([attr in dir_ for attr in parents])

    def test_words_have_text(self):
        page = parse()[0]

        assert page.words[0].text == 'TABLE'
        assert page.words[2].text == 'CONTENTS'
        assert page.words[102].text == '.'

    def test_words_have_boldness(self):
        page = parse()[0]

        assert page.words[0].bold
        assert not page.words[73].bold

    def test_words_have_italicness(self):
        page = parse()[0]

        assert not page.words[0].italic
        assert page.words[2].italic
        assert not page.words[73].italic

    def test_words_have_bounding_box(self):
        page = parse()[0]

        assert page.words[0].bbox.left == 2216
        assert page.words[0].bbox.top == 1049
        assert page.words[0].bbox.right == 2449
        assert page.words[0].bbox.bottom == 1098

    def test_word_has_line(self):
        page = parse()[0]
        for word in page.words:
            assert isinstance(word.line, pyhocr.page.Line)

    def test_word_has_block(self):
        page = parse()[0]
        for word in page.words:
            assert isinstance(word.block, pyhocr.page.Block)

    def test_word_has_page(self):
        page = parse()[0]
        for word in page.words:
            assert isinstance(word.page, pyhocr.page.Page)


class TestLines:
    def test_line_has_block(self):
        page = parse()[0]
        for line in page.lines:
            assert isinstance(line.block, pyhocr.page.Block)
