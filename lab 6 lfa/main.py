from lexer import Lexer, LexerError, Token as LexerToken
from parser import Parser, Token as ParserToken, ParseError
from ast_printer import print_ast


def convert_lexer_tokens_to_parser_tokens(lexer_tokens: list) -> list:
    """Convert lexer tokens to parser tokens (adapting token type format)."""
    result = []
    for token in lexer_tokens:
        result.append(ParserToken(token.token_type.name, token.value, token.line, token.column))
    return result


def main() -> None:
    sample_program = """
# Small program demonstrating lexical and syntactic analysis
let x = 10;
let y = 3.14;
let z = sin(x) + cos(y) * 2;

fn add(first, second) {
    return first + second;
}

if (x == 10) {
    print(z);
} else {
    print("x is not 10");
}

let numbers = [1, 2, 3, 4, 5];
let data = {"name": "Alice", "age": 25};
""".strip()

    print("=" * 70)
    print("Laboratory Work 5 - Parser and AST")
    print("=" * 70)

    print("\nInput program:")
    print("-" * 70)
    print(sample_program)
    print("-" * 70)

    # Lexical analysis
    print("\n1. LEXICAL ANALYSIS (Tokenization)")
    print("-" * 70)
    lexer = Lexer()
    try:
        lexer_tokens = lexer.tokenize(sample_program)
        print(f"Generated {len(lexer_tokens)} tokens:\n")
        for i, token in enumerate(lexer_tokens[:30], start=1):  # Show first 30
            print(f"{i:2}. {token}")
        if len(lexer_tokens) > 30:
            print(f"... and {len(lexer_tokens) - 30} more tokens")
    except LexerError as error:
        print(f"Lexer error: {error}")
        return

    # Syntactic analysis
    print("\n2. SYNTACTIC ANALYSIS (Parsing)")
    print("-" * 70)
    parser_tokens = convert_lexer_tokens_to_parser_tokens(lexer_tokens)
    parser = Parser(parser_tokens)
    try:
        ast = parser.parse()
        print("Successfully parsed! Abstract Syntax Tree (AST) structure:\n")
        print_ast(ast)
    except ParseError as error:
        print(f"Parse error: {error}")
        return

    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
