from regex_word_generator import RegexWordGenerator


def print_block(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def main() -> None:
    variant_1_regexes = [
        "(a|b) (c|d) E+ G?",
        "P (Q|R|S) T (UV|W|X)* Z+",
        "1 (0|1)* 2 (3|4){5} 36",
    ]

    generator = RegexWordGenerator(repetition_limit=5, seed=42)

    print_block("Laboratory Work 4 - Regular Expression Word Generator")
    print("Goal: dynamically interpret regex input and generate valid words.")
    print("Rule: unbounded repeats are capped to 5 occurrences.\n")

    for index, expression in enumerate(variant_1_regexes, start=1):
        print_block(f"Regex {index}: {expression}")

        words = generator.generate_many(expression, count=15)
        print("Generated valid words:")
        print("{" + ", ".join(words) + "}")

    print_block("Bonus - Processing Sequence Example")
    sample_expression = variant_1_regexes[0]
    sample_word, trace = generator.generate_one(sample_expression, with_trace=True)

    print(f"Sample expression: {sample_expression}")
    print(f"Generated word: {sample_word}")
    print("Processing steps:")
    for step_number, step in enumerate(trace, start=1):
        print(f"{step_number}. {step}")


if __name__ == "__main__":
    main()
