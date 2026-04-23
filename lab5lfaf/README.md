# Laboratory Work 5: Chomsky Normal Form

**Course:** Formal Languages & Finite Automata  
**Author:** Cosneanu Corina  
**Variant:** 9  

## Theory
Chomsky Normal Form (CNF) requires every production step in a Context-Free Grammar (CFG) to strictly produce either exactly two non-terminal symbols or exactly one terminal symbol ( \rightarrow BC$ or  \rightarrow a$). Rather than allowing arbitrary derivation pathways, CNF enforces a strict binary tree structure on the grammar's derivations. This normalization bounds parsing depth and guarantees predictable logic for parsing algorithms.

## Objectives
1. Implement a normalizer that converts a Context-Free Grammar (CFG) into its equivalent Chomsky Normal Form (CNF).
2. Apply the five algorithmic steps: eliminating epsilon productions, unit productions, inaccessible symbols, and non-productive symbols, followed by the final CNF factorization.
3. Encapsulate the implementation logic into a reusable method.
4. Ensure the program accepts any grammar definition dynamically, not just the hardcoded Variant 9.

## Implementation description
The transformation pipeline is cleanly encapsulated inside the Grammar class. It manages internal dictionaries and sets for productions, terminals, and non-terminals.

`python
class Grammar:
    def __init__(self, vn, vt, p, start_symbol):
        self.vn = set(vn)
        self.vt = set(vt)
        self.p = p
        self.start = start_symbol
`

The algorithm systematically addresses structural deviations in five distinct stages, orchestrated by the 	o_cnf() method. First, it identifies nullable symbols and eliminates epsilon productions while preserving alternate generating paths. Next, it resolves unit productions by replacing the target non-terminal with its generative set to flatten derivation trees. 

`python
    def to_cnf(self):
        self.eliminate_epsilon()
        self.eliminate_unit()
        self.eliminate_inaccessible()
        self.eliminate_non_productive()
        self.factor_to_cnf()
`

In the third step, the module computes the reachable set of symbols from the start non-terminal and removes any inaccessible rules. After that, it iteratively identifies productive symbols that can eventually derive terminal strings, pruning any path trapped in an infinite loop. Finally, the algorithm transforms the remaining rules into strict CNF by substituting inline terminals with dedicated non-terminal wrappers ( \rightarrow a$) and breaking down lengthy rule sequences using newly generated intermediate variables ($).

## How to run the program
To execute the normalizer, navigate to its directory and run the main script. From the terminal, change to the folder d:\LAB 2\lfa\lab5lfaf\grammar_normalizer and execute:
python main.py

This will trigger the normalization of the given Variant 9 grammar and display the state of the production rules step-by-step in the console.

## Conclusions / Screenshots / Results
Through carefully modularizing the Chomsky pipeline, each transformation independently restricts the structural deviations of the formal grammar, successfully bounding the derivation tree to the required Chomsky binary depth strictures without altering the language originally generated.

Below is the terminal output demonstrating the execution sequence leading up to the final Chomsky Normal Form state:

`	ext
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
`
"@
Set-Content -Path 'd:\LAB 2\lfa\lab5lfaf\README.md' -Value  -Encoding UTF8
cd d:\ ; git clone https://github.com/corinacc555/LFPC.git LFPC_clone3 ; cd LFPC_clone3 ; Copy-Item -Force 'd:\LAB 2\lfa\lab5lfaf\README.md' '.\lab5lfaf\' ; git add . ; git commit -m "Update formatting of Lab 5 README to match template" ; git push origin main


cd d:\ ; git clone https://github.com/corinacc555/LFPC.git LFPC_clone3 ; cd LFPC_clone3 ; Copy-Item -Force 'd:\LAB 2\lfa\lab5lfaf\README.md' '.\lab5lfaf\' ; git add . ; git commit -m "Update formatting of Lab 5 README to match template" ; git push origin main
