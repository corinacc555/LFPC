# Laboratory 5: Chomsky Normal Form

## 1. Introduction
This project implements a normalizer that converts a Context-Free Grammar (CFG) into its equivalent Chomsky Normal Form (CNF) according to the algorithms of Formal Languages and Automata. It handles epsilon productions, unit productions, inaccessible symbols, non-productive symbols, and finally factors productions into standard binary and terminal variables.

## 2. Theory
Chomsky Normal Form requires every production step in a Context-Free Grammar (CFG) to be of the form:
- $A \rightarrow BC$ (where A, B, C are non-terminals)
- $A \rightarrow a$ (where a is a terminal)

To achieve this, the following pipeline is executed:
1.  **Eliminate Epsilon Productions:** Find nullable symbols and remove transitions resolving to $\epsilon$ while preserving generating paths.
2.  **Eliminate Unit Productions:** Remove productions of the form $A \rightarrow B$, replacing $B$ with its generating set to flatten derivation trees.
3.  **Eliminate Inaccessible Symbols:** Remove symbols which cannot be reached from the Start non-terminal ($S$).
4.  **Eliminate Non-Productive Symbols:** Remove symbols that cannot generate any terminal string.
5.  **Transform to CNF:** Factor remaining long non-terminal sequences and replace explicitly specified terminal sequences with their associated variables ($X_a \rightarrow a$) and newly created intermediate symbols ($Z_n \rightarrow A B$).

## 3. Implementation Details
The conversion algorithm is cleanly encapsulated within the `Grammar` class located in `grammar_normalizer/grammar.py`.
The process exposes the public method `to_cnf()`, which orchestrates each step sequentially and modifies the grammar's internal state mappings (`self.p` for productions, `self.vn` for Non-terminals, `self.vt` for Terminals).

The system accepts an initial dictionary definition parameter allowing for arbitrary grammar parsing - satisfying the bonus requirements.

### Grammar Input (Variant 9)
```
Vn = {S, A, B, C, D}
Vt = {a, b}
P = {
    S -> B | BC | bA
    A -> a | aS | bAaAb
    B -> A | aAa | bS
    C -> ε | AB
    D -> AB
}
```

## 4. Output Example
Running `python main.py` provides the step-by-step resolution:

```text
Original Grammar:
A -> a | aS | bAaAb
B -> A | aAa | bS
C -> ε | AB
D -> AB
S -> BC | bA

Step 1: After Eliminating Epsilon Productions:
A -> a | aS | bAaAb
B -> A | aAa | bS
C -> AB
D -> AB
S -> B | BC | bA

Step 2: After Eliminating Unit (Renaming) Productions:
A -> a | aS | bAaAb
B -> a | aAa | aS | bAaAb | bS
C -> AB
D -> AB
S -> BC | a | aAa | aS | bA | bAaAb | bS

Step 3: After Eliminating Inaccessible Symbols:
A -> a | aS | bAaAb
B -> a | aAa | aS | bAaAb | bS
C -> AB
S -> BC | a | aAa | aS | bA | bAaAb | bS

Step 4: After Eliminating Non-Productive Symbols:
A -> a | aS | bAaAb
B -> a | aAa | aS | bAaAb | bS
C -> AB
S -> BC | a | aAa | aS | bA | bAaAb | bS

Step 5: Chomsky Normal Form (CNF):
A -> X_aS | X_bZ_5 | a
B -> X_aS | X_aZ_4 | X_bS | X_bZ_3 | a
C -> AB
S -> BC | X_aS | X_aZ_2 | X_bA | X_bS | X_bZ_1 | a
X_a -> a
X_b -> b
```

## 5. Conclusion
Through carefully modularizing the Chomsky pipeline, it is verified that each transformation independently restricts the structural deviations of the formal grammar, successfully bounding the derivation tree to the required Chomsky binary depth structure without altering the language originally generated.

*Important Note on Repository Submission Format:*
Please note that you should consider moving the code out of the `lab5lfaf` naming convention prior to pushing it to a public GitHub branch, to avoid point penalties (per lab evaluation instructions: "Please don't name your folders based on the lab work e.g. Lab1").
