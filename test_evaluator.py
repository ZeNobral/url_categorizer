#! python 3
import csv

from evaluator import Evaluator
from my_parser.parser import Parser

text = open('botify_rules.txt', encoding='utf-8').read()
p = Parser(text)
ast = p.parse() 
ev = Evaluator(ast)

with open('urls_croisierenet.csv', encoding='utf-8') as f:
	f_csv = csv.reader(f)
	for line in f_csv:
		ev.evaluate_url(line[0])