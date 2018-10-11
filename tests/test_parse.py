from os import path

import pytest

import pyhocr

BASE_DIR = path.dirname(__file__)


@pytest.fixture(scope='session')
def example():
    filename = 'example.html'
    return pyhocr.parse(path.join(BASE_DIR, filename))


class TestParse:

    def test_empty_files_does_not_parse(self):
        with pytest.raises(pyhocr.classes.HOCRParseError):
            pyhocr.parse(path.join(BASE_DIR, 'empty_example.html'))

    def test_parse_from_stream(self, example):
        with open(path.join(BASE_DIR, 'example.html'), 'rb') as stream:
            hocr = pyhocr.parse(stream)

            assert hocr == example

    def test_get_number_of_pages(self, example):
        assert len(example.pages) == 1

    def test_parse_return_datastructure_is_document(self, example):
        assert isinstance(example, pyhocr.classes.Document)

    def test_page_elements_in_dir(self, example):
        page = example.pages[0]

        assert 'words' in dir(page)
        assert 'blocks' in dir(page)


class TestPage:

    def test_page_has_proper_attribute_error(self, example):
        page = example.pages[0]

        with pytest.raises(AttributeError):
            page.shjgioda

    def test_page_has_bounding_box(self, example):
        for page in example.pages:
            assert page.bbox.left >= 0

    def test_page_has_image_name(self, example):
        page = example.pages[0]

        assert page.image == '/tmp/tmpepham8.tiff'

    def test_page_has_blocks(self, example):
        page = example.pages[0]

        assert len(page.blocks) == 3

    def test_page_has_words(self, example):
        page = example.pages[0]

        assert len(page.words) == 2665

    def test_page_blocks_have_paragraphs(self, example):
        page = example.pages[0]

        assert len(page.blocks[0].paragraphs) == 1
        assert len(page.blocks[1].paragraphs) == 50
        assert len(page.blocks[2].paragraphs) == 1

    def test_page_block_paragraphs_have_lines(self, example):
        page = example.pages[0]

        assert len(page.blocks[1].paragraphs[0].lines) == 2
        assert len(page.blocks[1].paragraphs[10].lines) == 1
        assert len(page.blocks[1].paragraphs[20].lines) == 1
        assert len(page.blocks[2].paragraphs[0].lines) == 1

    def test_page_block_paragraph_lines_have_words(self, example):
        page = example.pages[0]

        assert len(page.blocks[0].paragraphs[0].lines[0].words) == 3
        assert len(page.blocks[1].paragraphs[0].lines[0].words) == 3
        assert len(page.blocks[1].paragraphs[10].lines[0].words) == 54


class TestBlock:

    def test_block_has_page(self, example):
        page = example.pages[0]
        for block in page.blocks:
            assert isinstance(block.page, pyhocr.classes.Page)


class TestLines:
    def test_line_has_block(self, example):
        page = example.pages[0]
        for line in page.lines:
            assert isinstance(line.block, pyhocr.classes.Block)


class TestWord:

    def test_word_reper(self, example):
        word = example.pages[0].words[0]
        assert str(word) == "<Word('TABLE', <Box(2216, 1049, 2449, 1098)>)>"

    def test_word_parents_in_dir(self, example):
        word = example.pages[0].words[0]
        parents = ['page', 'block', 'paragraph', 'line']
        dir_ = dir(word)
        assert all([attr in dir_ for attr in parents])

    def test_words_have_text(self, example):
        page = example.pages[0]

        assert page.words[0].text == 'TABLE'
        assert page.words[2].text == 'CONTENTS'
        assert page.words[102].text == '.'

    def test_words_have_boldness(self, example):
        page = example.pages[0]

        assert page.words[0].bold
        assert not page.words[73].bold

    def test_words_have_italicness(self, example):
        page = example.pages[0]

        assert not page.words[0].italic
        assert page.words[2].italic
        assert not page.words[73].italic

    def test_words_have_bounding_box(self, example):
        page = example.pages[0]

        assert page.words[0].bbox.left == 2216
        assert page.words[0].bbox.top == 1049
        assert page.words[0].bbox.right == 2449
        assert page.words[0].bbox.bottom == 1098

    def test_word_has_line(self, example):
        page = example.pages[0]
        for word in page.words:
            assert isinstance(word.line, pyhocr.classes.Line)

    def test_word_has_block(self, example):
        page = example.pages[0]
        for word in page.words:
            assert isinstance(word.block, pyhocr.classes.Block)

    def test_word_has_page(self, example):
        page = example.pages[0]
        for word in page.words:
            assert isinstance(word.page, pyhocr.classes.Page)


class TestBbox:
    def test_bbox_has_correct_values(self, example):
        word = example.pages[0].words[0]
        assert word.bbox.left == 2216
        assert word.bbox.top == 1049
        assert word.bbox.right == 2449
        assert word.bbox.bottom == 1098
        assert word.bbox.coords == (2216, 1049, 2449, 1098)
        assert word.bbox.height == 49
        assert word.bbox.width == 233

    def test_repr(self, example):
        word = example.pages[0].words[0]
        assert str(word.bbox) == "<Box(2216, 1049, 2449, 1098)>"
