# Laboratory Work 4: Regular Expressions and Word Generation

Course: Formal Languages and Finite Automata  
Author: Cosneanu Corina

## What Regular Expressions Are

A regular expression (regex) is a formal pattern that describes a set of strings over an alphabet. Instead of listing all valid words one by one, regex offers compact operators that define families of words.

Common operators used in this lab:
- `|` for alternation (choice), for example `(a|b)`
- concatenation for sequence, for example `ab`
- `*` for zero or more repetitions
- `+` for one or more repetitions
- `?` for optional symbol (zero or one)
- grouping with parentheses `(...)`

## What Regular Expressions Are Used For

Regular expressions are used in:
- lexical analysis and compiler design
- input validation (emails, IDs, formats)
- searching/filtering text
- data extraction and log processing
- language modeling for regular languages

## Task and Variant

Variant 1 expressions:
1. `(a|b) (c|d) E+ G?`
2. `P (Q|R|S) T (UV|W|X)* Z+`
3. `1 (0|1)* 2 (3|4){5} 36`

The project dynamically interprets regex input and generates valid words from each expression.

## Implementation Summary

Files:
- `regex_word_generator.py`: parser, AST, generator
- `main.py`: demonstration script for variant 1

Main design decisions:
- The solution does not hardcode variant structures.
- Expressions are written directly in standard regex notation.
- The generator also accepts legacy lab notation (for compatibility):
   - `^(+)` is interpreted as `+`
   - `^5` is interpreted as `{5}`
- The parser supports `()`, `|`, concatenation, `*`, `+`, `?`, `{n}`.
- For potentially unbounded repetition (`*`, `+`), the generator enforces the lab limit of 5.

## Bonus Requirement: Processing Sequence

The method `generate_one(..., with_trace=True)` records and prints generation steps:
- input and normalized expression
- structural decisions (alternation branch, repetition count)
- emitted literals

This provides a readable sequence of what is processed first, second, and so on.

## Faced Difficulties and Solutions

1. Legacy lab notation can differ from standard regex (`E^(+)`, `(3|4)^5`).  
   Solution: kept a compatibility normalization before parsing.

2. Need for dynamic interpretation without hardcoding each regex.  
   Solution: built a generic recursive-descent parser and AST-based generator.

3. Infinite-language risk with `*` and `+`.  
   Solution: hard cap of 5 repetitions, as required.

## How To Run

From folder `d:\LAB 2\LFA\lab4lfaf`:

```bash
python main.py
```

The script prints generated valid words for all three expressions and also a processing trace example.

## Example Output Style

- Regex 1 can generate words like: `acE`, `bdEEEG`, `adEE`
- Regex 2 can generate words like: `PQTUVUVZ`, `PRTWWWWZ`, `PSTXZ`
- Regex 3 can generate words like: `1023333336`, `1124444436`

Exact output differs between runs if seed is changed.
