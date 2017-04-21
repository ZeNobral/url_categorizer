import re
from collections import namedtuple


# --------------------------------------------------------------------------------------------------
# CLASS Tokenizer
# used to tokenize the rule file
# --------------------------------------------------------------------------------------------------
class Tokenizer:
    _PATTERNS = [
        ('NEWLINE', r'\n'),
        ('WS', r'\s'),
        ('AT', r'@'),
        ('C_BRACE', r'\]'),
        ('O_BRACE', r'\['),
        ('O_PARENTHESIS', r'\('),
        ('C_PARENTHESIS', r'\)'),
        ('SEMI_COLUMN', r':'),
        ('BOOLEAN', r'\b(?:or|and)(?:\b|\()'),
        ('NOT', r'\bnot\b'),
        ('SELECTOR', r'\b(?:hostname|host|pathquery|path|query|protocol|proto|scheme|domain|host|url)\b'),
        ('SEG', r'segment'),
        ('PATTERN_MODIFIER', r'\b(i|rx|rxi)(?=:)'),
        ('SEGMENT', r'(?<=\[segment:).+(?=\])'),
        ('CATEGORY', r'(?<=@)\S+'),
        ('COMMENT_LINE', r'#.+'),
        ('PATTERN', r'\S+')
    ]

    def __init__(self):
        self.master_pat = re.compile('|'.join('(?P<%s>%s)' % pair for pair in self._PATTERNS))

    def tokenize(self, text):
        Token = namedtuple('Token', 'type value line')
        line = 1
        scanner = self.master_pat.scanner(text)
        yield Token('BEGIN', '', 1)
        for m in iter(scanner.match, None):
            type, value = m.lastgroup, m.group()
            if type == 'NEWLINE':
                line += 1
            if type != 'WS' and type != 'NEWLINE' and type != 'COMMENT_LINE':
                yield Token(type, value, line)
        yield Token('EOF', '', line)
