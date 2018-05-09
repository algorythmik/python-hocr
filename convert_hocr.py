import argparse
import csv
import json
import six

from pyhocr.parser import parse

debug = True

fieldnames = ['pageid', 'page_dim', 'text', 'object_type', 'height', 'width',
              'x0', 'x1', 'y0', 'y1', 'lang']


# shared with coalesce words, prob
def parse_page_spec(p_str):
    if "-" in p_str:
        [start, end] = [int(x) for x in p_str.split("-")]
        return list(range(start, end + 1))
    else:
        return [int(p_str)]


def parse_args():
    parser = argparse.ArgumentParser("hocr2csv")

    parser.add_argument("infile", nargs=1)
    parser.add_argument("outfile", nargs=1)

    parser.add_argument("--pages", nargs="+", type=parse_page_spec)

    parser.add_argument(
        "--format",
        action="store",
        dest="format",
        choices=["csv", "json"],
        default="csv")

    args = parser.parse_args()
    return args


def get_page_words(parsed_hocr_page, pageid):
    """  hOCR uses distance from the *top* of the page
        but we want to use the lower left as the page origin.
        Also want pageid included.
    """
    page_words = []
    page_height = parsed_hocr_page.box.height
    page_width = parsed_hocr_page.box.width
    page_dim_string = "%sx%s" % (page_width, page_height)

    for word in parsed_hocr_page.words:
        this_word = {
            'x0': word.box.left, 'x1': word.box.right,
            'y0': page_height - word.box.bottom,
            'y1': page_height - word.box.top,
            'text': word.text, 'width': word.box.width,
            'height': word.box.height, 'pageid': pageid,
            'page_dim': page_dim_string,
            'object_type': 'word',
            'lang': word.lang,
        }
        page_words.append(this_word)

    return page_words


def write_data(data_array, outfile, format):
    if format.lower() == 'csv':

        outputfh = open(outfile, 'w')
        outputfh.write(",".join(fieldnames) + "\n")
        dictwriter = csv.DictWriter(
            outputfh, fieldnames=fieldnames, restval='', extrasaction='ignore')

        for word in data_array:
            if six.PY2:
                # csv writer can't handle unicode, so use utf-8. Hmm.
                word['text'] = word['text'].encode('utf-8')
            dictwriter.writerow(word)

    elif format.lower() == 'json':
        json.dump(data_array, open(outfile, 'w'))


def process_file(infile, outfile, format='csv', pages=None):

    page_list = parse(infile)
    page_words = []

    for i, page in enumerate(page_list):
        if (debug):
            print("processing page:%s" % i)
        # use 1-based page numbering so as to not go crazy
        this_pagenumber = i + 1
        if pages:
            if (this_pagenumber) not in pages:
                continue

        page_words += get_page_words(page, this_pagenumber)

    write_data(page_words, outfile, format)


def main():
    args = parse_args()

    if (debug):
        print("args are: ", args)

    page_list = args.pages[0] if args.pages else None
    process_file(
        args.infile[0], args.outfile[0], format=args.format, pages=page_list)


if __name__ == "__main__":
    main()
