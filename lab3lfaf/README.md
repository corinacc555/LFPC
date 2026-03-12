# Laboratory Work 3: Lexer

Course: Formal Languages & Finite Automata  
Author: Coșneanu Corina
## Overview

This laboratory introduces lexical analysis, which is one of the first stages in a compiler or interpreter. A lexer reads a stream of characters and transforms it into tokens. Tokens are categories such as keywords, identifiers, numbers, or operators, while lexemes are the actual text fragments from the source code.

## Objectives

The purpose of this implementation is to understand how a lexer works internally and to build a small but practical tokenizer. The lexer was designed to be slightly more complex than a calculator example by supporting both integers and floating-point numbers, variables, assignment, arithmetic operators, and trigonometric function names (`sin` and `cos`).

## Implementation Description

The project contains a simple `Lexer` class in Python. It uses regular expressions to scan source code and produce tokens in order. The lexer recognizes keywords (`fn`, `let`, `true`, `false`, `if`, `else`, `return`, `print`, `sin`, `cos`), identifiers, numeric literals (`INT`, `FLOAT`), string literals, operators (`=`, `==`, `!=`, `+`, `-`, `*`, `/`, `!`, `<`, `>`), punctuation (`(`, `)`, `{`, `}`, `[`, `]`, `,`, `:`, `;`), and comments. It also tracks line and column positions for each token.

If the lexer finds an unknown character, it raises a `LexerError` with position information. At the end of scanning, it appends an `EOF` token.

## Example Input

```txt
let x = 10;
let y = 3.14;
let z = sin(x) + cos(y) * 2;
let name = "String";
let myArray = [0, 1, 2, 3];
let map = {"name": "First_Name", "age": 28};
fn add(first, second) { return first + second; }
if x == 10 { print(z); } else { print(name); }
print(z);
```

## Example Output (Token Stream)

A sample of produced tokens:

```txt
LET          value='let'    line=1  col=1
IDENTIFIER   value='x'      line=1  col=5
ASSIGN       value='='      line=1  col=7
INT          value='10'     line=1  col=9
SEMICOLON    value=';'      line=1  col=11
...
EOF          value=''       line=4  col=1
```

## Files

- `lexer.py` - token definitions, lexer logic, and error handling
- `main.py` - demonstration script that tokenizes a sample input
- `README.md` - short report for the laboratory

## How To Run

```bash
cd "d:\LAB 2\lab3lfaf"
python main.py
```

## Conclusion

This lab demonstrates a clean and simple lexer implementation. The solution is intentionally lightweight, but it still supports useful language elements including float values and trigonometric function names, which satisfies the lab requirement for a slightly richer tokenizer example.

## References

- Lexer / Scanner (tokenization concept and token categories)
- Lexical analysis notes and sample scanner flow (`gettok`, identifiers, numbers, comments)
- Divide et impera approach for splitting source text into lexemes and token types
