# Laboratory Work 5: Chomsky Normal Form

**Course:** Formal Languages & Finite Automata  
**Author:** Cosneanu Corina  
**Variant:** 9  

## Theory
Chomsky Normal Form (CNF) requires every production step in a Context-Free Grammar (CFG) to strictly produce either exactly two non-terminal symbols or exactly one terminal symbol ($A \rightarrow BC$ or $A \rightarrow a$). Rather than allowing arbitrary derivation pathways, CNF enforces a strict binary tree structure on the grammar's derivations. This normalization bounds parsing depth and guarantees predictable logic for parsing algorithms.

## Objectives
1. Implement a normalizer that converts a Context-Free Grammar (CFG) into its equivalent Chomsky Normal Form (CNF).
2. Apply the five algorithmic steps: eliminating epsilon productions, unit productions, inaccessible symbols, and non-productive symbols, followed by the final CNF factorization.
3. Encapsulate the implementation logic into a reusable method.
4. Ensure the program accepts any grammar definition dynamically, not just the hardcoded Variant 9.

## Implementation description
The transformation pipeline is cleanly encapsulated inside the `Grammar` class. It manages internal dictionaries and sets for productions, terminals, and non-terminals.

```python
class Grammar:
    def __init__(self, vn, vt, p, start_symbol):
        self.vn = set(vn)
        self.vt = set(vt)
        self.p = p
        self.start = start_symbol
```

The algorithm systematically addresses structural deviations in five distinct stages, orchestrated by the `to_cnf()` method. First, it identifies nullable symbols and eliminates epsilon productions while preserving alternate generating paths. Next, it resolves unit productions by replacing the target non-terminal with its generative set to flatten derivation trees. 

```python
    def to_cnf(self):
        self.eliminate_epsilon()
        self.eliminate_unit()
        self.eliminate_inaccessible()
        self.eliminate_non_productive()
        self.factor_to_cnf()
```

In the third step, the module computes the reachable set of symbols from the start non-terminal and removes any inaccessible rules. After that, it iteratively identifies productive symbols that can eventually derive terminal strings, pruning any path trapped in an infinite loop. Finally, the algorithm transforms the remaining rules into strict CNF by substituting inline terminals with dedicated non-terminal wrappers ($X_a \rightarrow a$) and breaking down lengthy rule sequences using newly generated intermediate variables ($Z_n$).

## How to run the program
To execute the normalizer, navigate to its directory and run the main script. From the terminal, change to the folder `grammar_normalizer` and execute:
```bash
python main.py
```
This will trigger the normalization of the given Variant 9 grammar and display the state of the production rules step-by-step in the console.

## Conclusions
In this laboratory work, I successfully implemented a system capable of transforming a given Context-Free Grammar into its equivalent Chomsky Normal Form. Through the incremental application of the algorithmic stages—eliminating nullable symbols, resolving cycle-prone unit mappings, and purging unreachable or unproductive branches—I learned how theoretical grammar constraints translate logically into code. Specifically, the final step of breaking down long sequences into strict binary structures demonstrated how complex production trees can be uniformly bounded without altering the language itself. This provided practical experience with graph traversal, set theory, and string manipulation within formally constructed systems.
