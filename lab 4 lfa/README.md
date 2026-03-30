# Laboratory Work 4: Regular Expressions and Word Generation

**Course:** Formal Languages and Finite Automata  
**Author:** Cosneanu Corina

## Introduction: What Regular Expressions Are

A regular expression (regex) is a formal pattern that describes a set of strings over an alphabet. Rather than listing all valid words individually, a regular expression uses compact notation and special operators to define entire families of words with common patterns. The key insight is that instead of hardcoding which words are valid, we can write a short pattern that captures the entire language structure.

Regular expressions employ several fundamental operators to build patterns. The alternation operator `|` allows choice between alternatives, such as `(a|b)` to match either the symbol `a` or `b`. Concatenation, the default operation of placing symbols next to each other as in `ab`, specifies sequential matching. For repetition, the `*` operator stands for zero or more occurrences, `+` denotes one or more occurrences, and `?` marks an optional symbol occurring zero or once. Grouping with parentheses `(...)` allows complex subexpressions to be treated as a unit. Finally, the notation `{n}` specifies exactly `n` repetitions of a pattern.

## Practical Applications of Regular Expressions

Regular expressions are foundational in computer science because they appear in nearly every domain of software development. In compiler design, lexical analyzers use regex to tokenize source code by identifying keywords, identifiers, and literals. Web applications rely on regex for input validation, checking that email addresses follow expected format, usernames meet constraints, or credit card numbers have the correct length and digit pattern. Text processing tools like `grep`, `sed`, and `awk` depend on regex to search, filter, and extract information from large text files. Data science and log analysis frequently employ regex to parse unstructured logs and extract relevant fields. Underlying all these applications is the theoretical foundation: regular expressions define exactly the class of regular languages, which are fundamental in automata theory.

## Task Specification and Assignment Variant

This laboratory assigned Variant 1, which consists of three regular expressions that must be interpreted dynamically and used to generate valid words:

1. `(a|b) (c|d) E+ G?` — produces words from choices of `a` or `b`, followed by `c` or `d`, followed by one or more `E`, optionally ending with `G`.
2. `P (Q|R|S) T (UV|W|X)* Z+` — produces words starting with `P`, containing one choice from `Q`, `R`, or `S`, followed by `T`, zero or more occurrences of either `UV` or `W` or `X`, and ending with one or more `Z`.
3. `1 (0|1)* 2 (3|4){5} 36` — produces words starting with `1`, followed by any number of `0` or `1`, followed by `2`, followed by exactly five occurrences of either `3` or `4`, and ending with `36`.

The core requirement is that the generator must not hardcode these specific patterns. Instead, the solution must parse any regular expression dynamically and produce valid words by interpreting the regex structure at runtime.

## Implementation Approach

The solution consists of two main Python files that work together. The `regex_word_generator.py` module implements a complete regex engine comprised of three components: a parser that converts regex strings into an abstract syntax tree (AST), a set of node classes that represent different regex constructs, and a generator that traverses the AST to produce valid words.

The parser is implemented as a recursive-descent parser that respects operator precedence and grouping. It processes expressions left to right, first handling alternation (the lowest precedence operator), then concatenation, and finally factors with postfix operators like `*`, `+`, `?`, and `{n}`. This structure ensures that complex expressions like `P (Q|R|S) T` are correctly parsed as a sequence of a literal `P`, an alternation inside parentheses, a literal `T`, rather than misinterpreting the boundaries of operations.

The AST representation uses node classes such as `Literal` for single characters, `Concat` for sequential composition, `Alternation` for choice, and `Repeat` for bounded or unbounded repetition. Each node class implements a `generate` method that produces a valid string by recursively generating its subcomponents. The generator uses Python's `random` module to make non-deterministic choices (such as which branch to follow in an alternation or how many times to repeat a pattern), ensuring that multiple runs produce varied but correct outputs.

One subtle design decision addresses the lab requirement that unbounded repetitions like `*` and `+` must be limited. The parser automatically caps these to a maximum of 5 occurrences to prevent the generation of extremely long or infinite strings. This limit is reasonable because it still demonstrates the pattern without producing impractical output.

The `main.py` file demonstrates the generator on all three variant expressions, producing a set of unique valid words for each regex and also invoking the bonus feature to show the step-by-step processing sequence.

## Bonus Feature: Processing Sequence Trace

To meet the bonus requirement, the generator includes a tracing mechanism that records the sequence of decisions made during word generation. When the `generate_one()` method is called with `with_trace=True`, it records each step of the process: the input expression, the normalized form, and all parsing and generation decisions in order. This produces output like "Parse to AST", "Concatenation with 4 parts", "Alternation: choose option 2 of 2", "Emit literal 'b'", and so on. The sequence of steps provides insight into how the regex engine processes the pattern, making the internal mechanics transparent to the user. This feature helps debug complex expressions and understand the order in which different parts of a regex are evaluated during word generation.

## Implementation Challenges and Solutions

During implementation, several challenges emerged. The first challenge stemmed from the fact that the lab specification used non-standard regex notation like `E^(+)` and `(3|4)^5`, which differ from common regex syntax where these would be written as `E+` and `(3|4){5}`. The solution was to implement a normalization function that converts the lab notation to standard syntax before parsing. The system was designed flexibly to accept both notations for maximum compatibility.

The second challenge was architectural: the requirement demanded dynamic interpretation, not hardcoding. This meant the solution could not contain a series of if-statements checking which specific regex had been given. Instead, a generic recursive-descent parser was built that can parse any regex with the supported operators. This approach scales to additional operators or variants without modification.

The third challenge concerned managing infinite languages. Regular expressions with `*` or `+` technically describe infinite languages, since repetition has no inherent upper bound. If the generator naively followed the spec, it could produce astronomically long strings (imagine `(3|4){5}` repeated fifty times). The solution applies the lab's specified limit of 5 repetitions maximum, ensuring output remains reasonable while still demonstrating the pattern correctly.

## How To Run the Program

Navigate to the folder `d:\LAB 2\LFA\lab4lfaf` in a terminal. Execute the command `python main.py`. The program will display generated valid words for all three variant expressions, showing approximately 15 unique words for each regex. It also includes a bonus section that shows the step-by-step processing sequence for the first regex, illustrating exactly how the generator interprets and processes the pattern. If you modify the seed parameter when creating the `RegexWordGenerator`, you will see different word generation sequences while still maintaining correctness.

## Example Output

For reference, the program generates words such as the following:
- From regex 1: `acE`, `bdEEEG`, `adEE`, `bcEEEEEG`
- From regex 2: `PQTUVUVZ`, `PRTWWWWZ`, `PSTXZ`, `PQTWZZ`
- From regex 3: `1023333336`, `1124444436`, `100124444436`, `101123433336`

The exact words vary based on randomization, but all adhere to their respective regex patterns.

## Conclusion

Completing this laboratory was insightful in several ways. At first, the requirement to "dynamically interpret" regex seemed abstract, but building the parser clarified what it means: the system must handle regex as data, not as code. By implementing a recursive-descent parser, I gained a concrete understanding of how compilers and interpreters process structured input. The design decision to separate parsing from generation also highlighted the value of abstraction—the AST representation serves as a clean bridge between syntax (the textual regex) and semantics (what words it generates).

One key learning was recognizing that regular expressions, despite their power and prevalence, have well-defined computational limits. The requirement to cap unbounded repetitions forced me to confront the difference between the mathematical ideal (infinite language) and practical implementation (finite output). This tension between theory and practice appears throughout computer science.

The tracing feature proved particularly educating. Initially, I implemented word generation as a simple recursive function, but adding traces required capturing why each decision was made. This experience demonstrated that observability and transparency in algorithms are not afterthoughts but integral to understanding. Seeing the step-by-step sequence of parsing and generation helped me verify correctness and debug edge cases.

On reflection, this lab addressed objectives that seemed theoretical but revealed practical importance. Regular expressions power many tools I use daily without thinking about their internal mechanisms. Now, having built a regex engine from scratch, I understand both their elegance and limitations. The exercise reinforced that foundational computer science concepts—parsing, code generation, language design—are not merely academic but underpin the systems we build every day.

The combination of theory and implementation was well-balanced. The lab required understanding what a regular expression is and why it matters, then translating that understanding into working code. This end-to-end approach—from motivation through design to demonstration—left me with both conceptual clarity and practical confidence in regex and parsing techniques.
