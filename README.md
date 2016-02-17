# python-hocr

HOCR parsing based on [https://github.com/concordusapps/python-hocr](https://github.com/concordusapps/python-hocr).

## convert_hocr.py

Convert hOCR files to .csv or .json format. Lightly tested on python 2.7 and 3.5. 

Assumes that each hOCR file has only one closing `</html>` tag; some hOCR outputs mangle html by giving each pages an opening and closing html tag (as opposed to just an opening and closing ocr_page tag). This script will only convert the content that appears before the first html closing tag in such files; it's recommended that you pre-process such files ahead of time. 
	
	$ python convert_hocr.py  --help
	usage: hocr2csv [-h] [--pages PAGES [PAGES ...]] [--format {csv,json}]
	                infile outfile
	
	positional arguments:
	  infile
	  outfile
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --pages PAGES [PAGES ...]
	  --format {csv,json}

examples:

	python convert_hocr.py infile.html --pages=1-4 infile.csv

page ranges are inclusive. 

	python convert_hocr.py infile.html --format=json infile.json


## License

Unless otherwise noted, all files contained within this project are liensed under the MIT opensource license. See the included file LICENSE or visit [opensource.org][] for more information.

[opensource.org]: http://opensource.org/licenses/MIT
