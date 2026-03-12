from lexer import Lexer, LexerError


def main() -> None:
    sample_program = """
# small script with lexer-oriented syntax examples
let x = 10;
let y = 3.14;
let z = sin(x) + cos(y) * 2;
let name = "String";
let myArray = [0, 1, 2, 3];
let map = {"name": "First_Name", "age": 28};

fn add(first, second) {
    return first + second;
}

if x == 10 {
    print(z);
} else {
    print(name);
}

print(z);
""".strip()

    lexer = Lexer()

    print("=" * 58)
    print("Laboratory Work 3 - Simple Lexer Demo")
    print("=" * 58)
    print("\nInput program:\n")
    print(sample_program)

    print("\n\nGenerated tokens:\n")
    try:
        tokens = lexer.tokenize(sample_program)
        for token in tokens:
            print(
                f"{token.token_type:<12} value={token.value!r:<8} "
                f"line={token.line:<2} col={token.column}"
            )
    except LexerError as error:
        print(f"Lexer error: {error}")


if __name__ == "__main__":
    main()
