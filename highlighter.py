from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegularExpression

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
            self.highlightingRules.append((QRegularExpression(keyword), keywordFormat))

        # String format
        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor(255, 0, 0))
        self.highlightingRules.append((QRegularExpression("\".*\""), stringFormat))
        self.highlightingRules.append((QRegularExpression("'.*'"), stringFormat))

        # Number format
        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor(255, 165, 0))
        self.highlightingRules.append((QRegularExpression("\\b[0-9]+\\b"), numberFormat))

        # Comment format
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor(0, 128, 0))
        self.highlightingRules.append((QRegularExpression("#[^\n]*"), commentFormat))

        # Function and class format
        functionClassFormat = QTextCharFormat()
        functionClassFormat.setForeground(QColor(0, 0, 255))
        functionClassFormat.setFontWeight(QFont.Bold)
        self.highlightingRules.append((QRegularExpression("\\bdef\\s+\\w+"), functionClassFormat))
        self.highlightingRules.append((QRegularExpression("\\bclass\\s+\\w+"), functionClassFormat))

        # Operator format
        operatorFormat = QTextCharFormat()
        operatorFormat.setForeground(QColor(128, 0, 128))
        operators = ["=", "==", "!=", "<", ">", "<=", ">=", "\\+", "-", "\\*", "/", "//", "%", "\\*\\*", "\\+=",
                     "-=", "\\*=", "/=", "%=", "\\^", "\\|", "&", "~", ">>", "<<"]
        for operator in operators:
            self.highlightingRules.append((QRegularExpression(operator), operatorFormat))

        # Brackets and braces format
        bracketFormat = QTextCharFormat()
        bracketFormat.setForeground(QColor(255, 255, 0))
        brackets = ["\\(", "\\)", "\\{", "\\}", "\\[", "\\]"]
        for bracket in brackets:
            self.highlightingRules.append((QRegularExpression(bracket), bracketFormat))

    def highlightBlock(self, text: str) -> None:
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            index = expression.globalMatch(text)
            while index.hasNext():
                match = index.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
        self.setCurrentBlockState(0)
