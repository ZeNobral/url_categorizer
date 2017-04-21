

# --------------------------------------------------------------------------------------------------
# CLASS Node
# used by the parser to build the rule Tree
# --------------------------------------------------------------------------------------------------
class Node:
    def __init__(self, token):
        self.value = token.value
        self.type = token.type.lower()
        self.childs = []

    def __repr__(self):
        return '<Node ({},{})>'.format(self.type, self.value)

    def __iter__(self):
        return iter(self.childs)

    def __len__(self):
        return len(self.childs)

    def _append(self, child):
        if child is not None:
            self.childs.append(child)

    def append(self, childs):
        if isinstance(childs, Iterable) and not isinstance(childs, (str, Node)):
            for child in childs:
                self.append(child)
        else:
            self._append(childs)

    def display(self, level=0):
        repr = ' ' * level * 3 + str(self)
        print(repr)
        for child in self.childs:
            child.display(level + 1)
