import re


# --------------------------------------------------------------------------------------------------
# CLASS PatternMatcher
# used to efficiently match string with patterns
# p = PatternMatcher(pattern, modifier, not_modifier)
#       pattern : string
#       modifier : 'i', 'rx', 'rxi' or None
#       not_modifier : 'not' or None
# --------------------------------------------------------------------------------------------------
class PatternMatcher:
    _ALLOWED_MODIFIERS = {'i', 'rx', 'rxi'}

    def __init__(self, pattern, modifier=None, not_modifier=None):
        if modifier is not None and modifier not in self._ALLOWED_MODIFIERS:
            raise ValueError('Pattern modifier not known : {}'.format(modifier))
        if not_modifier is not None and not_modifier != 'not':
            raise ValueError('"not" keyword expected : {}')

        self.pattern = None
        self.match = None
        base_compare_method = ''

        if not_modifier:
            base_compare_method += base_compare_method + '_not'
        if modifier == 'rx' or modifier == 'rxi':
            if modifier[-1] == 'i':
                self.pattern = re.compile(pattern, re.I)
            else:
                self.pattern = re.compile(pattern)
            base_compare_method += '_rx'
        else:
            if pattern.startswith('*'):
                if pattern.endswith('*'):
                    # pattern  = *string*
                    self.pattern = pattern[1:-1]
                    base_compare_method += '_in'
                else:
                    # pattern = *string
                    self.pattern = pattern[1:]
                    base_compare_method += '_ends'
            elif pattern.endswith('*'):
                # pattern = string*
                self.pattern = pattern[:-1]
                base_compare_method += '_starts'
            else:
                # pattern = string
                self.pattern = pattern
                base_compare_method += '_equals'
            if modifier == 'i':
                base_compare_method += '_i'
                self.pattern = self.pattern.upper()
        self.match = getattr(self, base_compare_method)

    def __repr__(self):
        return '<PatternMatcher({}'.format(self.pattern)

    def _in(self, string):
        return self.pattern in string

    def _ends(self, string):
        return string.endswith(self.pattern)

    def _starts(self, string):
        return string.startswith(self.pattern)

    def _equals(self, string):
        return string == self.pattern

    def _not_in(self, string):
        return not self._in(string)

    def _not_ends(self, string):
        return not self._ends(string)

    def _not_starts(self, string):
        return not self._starts(string)

    def _not_equals(self, string):
        return not self._equals(string)

    def _in_i(self, string):
        return self._in(string.upper())

    def _ends_i(self, string):
        return self._ends(string.upper())

    def _starts_i(self, string):
        return self._starts(string.upper())

    def _equals_i(self, string):
        return self._equals(string.upper())

    def _not_in_i(self, string):
        return not self._in(string.upper())

    def _not_ends_i(self, string):
        return not self._ends(string.upper())

    def _not_starts_i(self, string):
        return not self._starts(string.upper())

    def _not_equals_i(self, string):
        return not self._equals(string.upper())

    def _rx(self, string):
        return bool(self.pattern.match(string))
