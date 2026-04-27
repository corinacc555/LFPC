from enum import Enum, auto


class TokenType(Enum):
    """Enumeration of all possible token types."""

    # Literals
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    TRUE = auto()
    FALSE = auto()

    # Identifiers
    IDENTIFIER = auto()

    # Keywords
    LET = auto()
    FUNCTION = auto()
    IF = auto()
    ELSE = auto()
    RETURN = auto()
    PRINT = auto()
    SIN = auto()
    COS = auto()

    # Operators
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EQ = auto()
    NOT_EQ = auto()
    LT = auto()
    GT = auto()
    BANG = auto()

    # Punctuation
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()

    # End of file
    EOF = auto()


def string_to_token_type(token_type_str: str) -> TokenType:
    """Convert a string token type to TokenType enum."""
    try:
        return TokenType[token_type_str]
    except KeyError:
        raise ValueError(f"Unknown token type: {token_type_str}")
