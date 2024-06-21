from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegExp

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.initializeFormats()

    def initializeFormats(self):
        self.highlightingRules = []

        # Keyword format
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(0, 0, 255))
        keywordFormat.setFontWeight(QFont.Bold)
        keywords = [
            "\\band\\b", "\\bas\\b", "\\bassert\\b", "\\bbreak\\b", "\\bclass\\b", "\\bcontinue\\b",
            "\\bdef\\b", "\\bdel\\b", "\\belif\\b", "\\belse\\b", "\\bexcept\\b", "\\bFalse\\b",
            "\\bfinally\\b", "\\bfor\\b", "\\bfrom\\b", "\\bglobal\\b", "\\bif\\b", "\\bimport\\b",
            "\\bin\\b", "\\bis\\b", "\\blambda\\b", "\\bNone\\b", "\\bnonlocal\\b", "\\bnot\\b",
            "\\bor\\b", "\\bpass\\b", "\\braise\\b", "\\breturn\\b", "\\bTrue\\b", "\\btry\\b",
            "\\bwhile\\b", "\\bwith\\b", "\\byield\\b"
        ]
        for keyword in keywords:
            self.highlightingRules.append((QRegExp(keyword), keywordFormat))

        # String format
        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor(255, 0, 0))
        self.highlightingRules.append((QRegExp("\".*\""), stringFormat))
        self.highlightingRules.append((QRegExp("'.*'"), stringFormat))

        # Number format
        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor(255, 165, 0))
        self.highlightingRules.append((QRegExp("\\b[0-9]+\\b"), numberFormat))

        # Comment format
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor(0, 128, 0))
        self.highlightingRules.append((QRegExp("#[^\n]*"), commentFormat))

        # Function and class format
        functionClassFormat = QTextCharFormat()
        functionClassFormat.setForeground(QColor(0, 0, 255))
        functionClassFormat.setFontWeight(QFont.Bold)
        self.highlightingRules.append((QRegExp("\\bdef\\s+\\w+"), functionClassFormat))
        self.highlightingRules.append((QRegExp("\\bclass\\s+\\w+"), functionClassFormat))

        # Operator format
        operatorFormat = QTextCharFormat()
        operatorFormat.setForeground(QColor(128, 0, 128))
        operators = ["=", "==", "!=", "<", ">", "<=", ">=", "\\+", "-", "\\*", "/", "//", "%", "\\*\\*", "\\+=",
                     "-=", "\\*=", "/=", "%=", "\\^", "\\|", "&", "~", ">>", "<<"]
        for operator in operators:
            self.highlightingRules.append((QRegExp(operator), operatorFormat))

        # Brackets and braces format
        bracketFormat = QTextCharFormat()
        bracketFormat.setForeground(QColor(255, 255, 0))
        brackets = ["\\(", "\\)", "\\{", "\\}", "\\[", "\\]"]
        for bracket in brackets:
            self.highlightingRules.append((QRegExp(bracket), bracketFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)
