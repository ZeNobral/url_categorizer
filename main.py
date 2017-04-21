import argparse
import csv

from url_categorizer.node_evaluator import NodeEvaluator
from url_categorizer.parser import Parser


def _read_csv(filename, newline='', encoding='utf-8', quotechar='"', delimiter=',', ignore_lines=0):
    with open(filename, newline=newline, encoding=encoding) as f:
        while ignore_lines > 0:
            next(f)
            ignore_lines -= 1
        f_csv = csv.DictReader(f, quotechar=quotechar, delimiter=delimiter)
        for d in f_csv:
            yield d


def _get_evaluator(filename, encoding='utf-8'):
    with open(filename, encoding=encoding) as f:
        content = f.read()
    p = Parser(content)
    root = p.parse()
    return NodeEvaluator(root)


def _write_csv(filename, data, encoding='utf-8', headers=None, quotechar='"', delimiter=','):
    with open(filename, mode='wt', newline='', encoding=encoding) as f:
        f_csv = csv.DictWriter(f, headers = headers, quotechar=quotechar, delimiter=delimiter)
        f_csv.writeheader()
        f_csv.writerows(data)


def run(**args):
    ev = _get_evaluator(categorization_rules_file, encoding=encoding)
    source = _read_csv(filename, encoding=encoding, quotechar=quotechar, delimiter=delimiter, ignore_lines=ignore_lines)
    first_line = next(source)
    source_headers = first_line.keys()
    for header in headers:
        if header not in source_headers:
            raise ValueError('{} not found in source csv file'.format(header))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='categorize urls, given a categorization rules file')
    parser.add_argument('-o', '--output_file', help='output_file, default to "result.csv"', default='result.csv')
    parser.add_argument('-f', '--field_names', nargs='+',
                        help='categorize urls of the fields named by those headers')
    parser.add_argument('filename', help='the input file containing the urls to categorize')
    parser.add_argument('-e', '--encoding', default='utf-8',
                        help='encoding for the input file and the categorization file.Default to "utf-8"')
    parser.add_argument('-d', '--delimiter', default=',', help='the field delimiter, default to ","')
    parser.add_argument('-q', '--quotechar', default='"', help='Quote character to delimit the fields. Default to "')
    parser.add_argument('-c', '--categorization-rules-file', default='categorization.txt',
                        help='File containing the rules for url categorization')
    parser.add_argument('-i', '--ignore-lines', default=0, type=int, help='ignore first lines of the input file')
    args = vars(parser.parse_args())

    for d in _read_csv(filename=args['filename'], encoding=args['encoding'], quotechar=args['quotechar'],
                       delimiter=args['delimiter'], ignore_lines=args['ignore_lines']):
        print(d)

