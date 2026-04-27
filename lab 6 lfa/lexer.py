import re
from dataclasses import dataclass
from typing import List
from token_types import TokenType


@dataclass
class Token:
    """Token with enum-based token_type."""

    token_type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.token_type.name}, {self.value!r}, {self.line}, {self.column})"


class LexerError(Exception):
    pass


class Lexer:
    """Lexer for the small expression language, using regex to identify tokens."""

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
        "fn": TokenType.FUNCTION,
        "let": TokenType.LET,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "return": TokenType.RETURN,
        "print": TokenType.PRINT,
        "sin": TokenType.SIN,
        "cos": TokenType.COS,
    }

    def __init__(self) -> None:
        parts = []
        for token_name, token_regex in self.TOKEN_SPEC:
            parts.append(f"(?P<{token_name}>{token_regex})")
        self.master_pattern = re.compile("|".join(parts))

    def tokenize(self, source_code: str) -> List[Token]:
        """Tokenize source code and return list of tokens."""
        tokens: List[Token] = []
        line = 1
        line_start = 0

        for match in self.master_pattern.finditer(source_code):
            token_type_str = match.lastgroup
            value = match.group()
            column = match.start() - line_start + 1

            if token_type_str == "NEWLINE":
                line += 1
                line_start = match.end()
                continue

            if token_type_str in {"WHITESPACE", "COMMENT"}:
                continue

            if token_type_str == "IDENTIFIER":
                if value in self.KEYWORDS:
                    token_type = self.KEYWORDS[value]
                else:
                    token_type = TokenType.IDENTIFIER
            else:
                try:
                    token_type = TokenType[token_type_str]
                except KeyError:
                    if token_type_str == "MISMATCH":
                        raise LexerError(
                            f"Unexpected character {value!r} at line {line}, column {column}"
                        )
                    raise LexerError(f"Unknown token type {token_type_str}")

            tokens.append(Token(token_type, value, line, column))

        tokens.append(Token(TokenType.EOF, "", line, 1))
        return tokens
