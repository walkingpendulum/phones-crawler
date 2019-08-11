import argparse

import crawler
import phones_parser

parser = argparse.ArgumentParser()
parser.add_argument('--tasks', help='path to file with tasks list (one url per line)', required=True)
parser.add_argument('-n', help='number of simultaneously performed requests', default=100)
args = parser.parse_args()

with open(args.tasks) as f:
    urls = [url.strip() for url in f.readlines() if url.strip()]


pages = crawler.run(urls, limit=args.n)
phones = {phone for phone in phones_parser.parse(page for page in pages)}

for phone in phones:
    print(phone)
