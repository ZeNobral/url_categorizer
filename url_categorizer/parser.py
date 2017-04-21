from url_categorizer.node import Node
from url_categorizer.tokenizer import Tokenizer
from url_categorizer.pattern_matcher import PatternMatcher


# --------------------------------------------------------------------------------------------------
# CLASS Parser
# used to produce the rule Tree from the Token list
# --------------------------------------------------------------------------------------------------
class Parser:
    def __init__(self, text):
        token_generator = Tokenizer()
        self.tokens = token_generator.tokenize(text)
        self.current_token = None
        self.next_token = None

    def parse(self):
        self._advance()
        return self.begin()

    def _advance(self):
        self.current_token, self.next_token = self.next_token, next(self.tokens, None)

    def _accept(self, token_type):
        if self.next_token and self.next_token.type == token_type:
            self._advance()
            return True
        else:
            return False

    def _expect(self, token_type):
        if not self._accept(token_type):
            raise SyntaxError(
                'Error at line {0.line} : expected type {1}, got Token({0.type},{0.value})'.format(self.next_token,
                                                                                                   token_type))

    def _check(self, token_type):
        return token_type == self.next_token.type

    def _make_node(self):
        return Node(self.current_token)

    def begin(self):
        """ begin : segments EOF """
        self._expect('BEGIN')
        n = self._make_node()
        n.append(self.segments())
        self._expect('EOF')
        return n

    def segments(self):
        """ segments : segment (segment)* """
        while self._check('O_BRACE'):
            yield self.segment()

    def segment(self):
        """ segment : O_BRACE SEG SEMI_COLUMN SEGMENT C_BRACE rules """
        self._expect('O_BRACE')
        self._expect('SEG')
        self._expect('SEMI_COLUMN')
        self._expect('SEGMENT')
        n = self._make_node()
        self._expect('C_BRACE')
        n.append(self.rules())
        return n

    def rules(self):
        """ rules : rule (rule)* """
        while self._check('AT'):
            yield self.rule()

    def rule(self):
        """ rule : AT CATEGORY matches """
        self._expect('AT')
        self._expect('CATEGORY')
        n = self._make_node()
        n.append(self.matches())
        return n

    def matches(self):
        """ matches : match (match)* """
        yield self.match()
        while self._check('SELECTOR') or self._check('BOOLEAN'):
            yield self.match()

    def match(self):
        """ match : BOOLEAN O_PARENTHESIS matches C_PARENTHESIS | single_match """
        if self._accept('BOOLEAN'):
            n = self._make_node()
            self._expect('O_PARENTHESIS')
            n.append(self.matches())
            self._expect('C_PARENTHESIS')
            return n
        else:
            return self.single_match()

    def single_match(self):
        """ full_pattern : SELECTOR NOT? (PATTERN_MODIFIER SEMI_COLUMN)? PATTERN """
        not_token = None
        pattern_modifier = None
        pattern_value = None
        pattern_node = None
        self._expect('SELECTOR')
        selector = self._make_node()
        if self._accept('BOOLEAN'):
            not_token = self.current_token.value
        if self._accept('PATTERN_MODIFIER'):
            pattern_modifier = self.current_token.value
            self._expect('SEMI_COLUMN')
        self._expect('PATTERN')
        pattern_value = self.current_token.value
        pattern_node = self._make_node()
        pattern_node.value = PatternMatcher(pattern_value, pattern_modifier, not_token)
        pattern_node.append(selector)
        return pattern_node
