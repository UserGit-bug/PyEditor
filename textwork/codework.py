from PyQt5 import QtCore, QtGui
import os
import sys
real_path = os.getcwd()
if real_path.split(os.sep)[-1] == 'design':
    real_path = os.sep.join(real_path.split(os.sep)[:-1])

sys.path.append(real_path)
from styles import all_together


class PythonHighlighter(QtGui.QSyntaxHighlighter):
    """Class defines work of QSyntaxHighlighter, built-in PyQt5 class
    which can check QPlainTextEdit with special rules.
    Checking is realised by using regular expressions"""
    STYLES = all_together('linter_csv_table.csv')
    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    # Python operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]
    def __init__(self, document):
        QtGui.QSyntaxHighlighter.__init__(self, document)

        self.tri_single = (QtCore.QRegExp("'''"), 1, self.STYLES['string2'])
        self.tri_double = (QtCore.QRegExp('"""'), 2, self.STYLES['string2'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, self.STYLES['keyword'])
            for w in PythonHighlighter.keywords]
        rules += [(r'%s' % o, 0, self.STYLES['operator'])
            for o in PythonHighlighter.operators]
        rules += [(r'%s' % b, 0, self.STYLES['brace'])
            for b in PythonHighlighter.braces]

        # All other rules
        rules += [
            (r'\bself\b', 0, self.STYLES['self']),
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.STYLES['string']),
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.STYLES['string']),
            (r'\bdef\b\s*(\w+)', 1, self.STYLES['defclass']),
            (r'\bclass\b\s*(\w+)', 1, self.STYLES['defclass']),
            (r'#[^\n]*', 0, self.STYLES['comment']),
            (r'\b[+-]?[0-9]+[lL]?\b', 0, self.STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, self.STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, self.STYLES['numbers']),
        ]

        self.rules = [(QtCore.QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        for expression, nth, fmt in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, fmt)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        # Многострочные строки
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            start = delimiter.indexIn(text)
            add = delimiter.matchedLength()

        while start >= 0:
            end = delimiter.indexIn(text, start + add)
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add

            self.setFormat(start, length, style)
            start = delimiter.indexIn(text, start + length)

        if self.currentBlockState() == in_state:
            return True
        else:
            return False
