import re
from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    token_type: str
    value: str
    line: int
    column: int


class LexerError(Exception):
    pass


class Lexer:
    """Simple lexer for a tiny expression language."""

    TOKEN_SPEC = [
        ("WHITESPACE", r"[ \t]+"),
        ("NEWLINE", r"\n"),
        ("COMMENT", r"\#.*"),
        ("STRING", r'"[^"\\]*(?:\\.[^"\\]*)*"'),
        ("FLOAT", r"\d+\.\d+"),
        ("INT", r"\d+"),
        ("EQ", r"=="),
        ("NOT_EQ", r"!="),
        ("ASSIGN", r"="),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        ("MULTIPLY", r"\*"),
        ("DIVIDE", r"/"),
        ("BANG", r"!"),
        ("LT", r"<"),
        ("GT", r">"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("LBRACE", r"\{"),
        ("RBRACE", r"\}"),
        ("LBRACKET", r"\["),
        ("RBRACKET", r"\]"),
        ("COMMA", r","),
        ("COLON", r":"),
        ("SEMICOLON", r";"),
        ("IDENTIFIER", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("MISMATCH", r"."),
    ]

    KEYWORDS = {
        "fn": "FUNCTION",
        "let": "LET",
        "true": "TRUE",
        "false": "FALSE",
        "if": "IF",
        "else": "ELSE",
        "return": "RETURN",
        "print": "PRINT",
        "sin": "SIN",
        "cos": "COS",
    }

    def __init__(self) -> None:
        parts = []
        for token_name, token_regex in self.TOKEN_SPEC:
            parts.append(f"(?P<{token_name}>{token_regex})")
        self.master_pattern = re.compile("|".join(parts))

    def tokenize(self, source_code: str) -> List[Token]:
        tokens: List[Token] = []
        line = 1
        line_start = 0

        for match in self.master_pattern.finditer(source_code):
            token_type = match.lastgroup
            value = match.group()
            column = match.start() - line_start + 1

            if token_type == "NEWLINE":
                line += 1
                line_start = match.end()
                continue

            if token_type in {"WHITESPACE", "COMMENT"}:
                continue

            if token_type == "IDENTIFIER":
                token_type = self.KEYWORDS.get(value, "IDENTIFIER")

            if token_type == "MISMATCH":
                raise LexerError(
                    f"Unexpected character {value!r} at line {line}, column {column}"
                )

            tokens.append(Token(token_type, value, line, column))

        tokens.append(Token("EOF", "", line, 1))
        return tokens
