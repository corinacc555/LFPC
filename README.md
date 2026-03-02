# Laboratory Work 2: Determinism and Grammar Classification

**Course:** Formal Languages & Finite Automata  
**Author:** Cosneanu Corina 
**Variant:** 9

## Theory

### Finite Automaton
A **finite automaton (FA)** is a mathematical model that represents processes or computations. It is formally defined by five components: Q represents the finite set of states, Σ denotes the input alphabet, δ is the transition function that determines state changes, q0 indicates the initial state where computation begins, and F contains the set of final or accepting states where valid computations can terminate.

### Determinism vs Non-Determinism
The distinction between deterministic and non-deterministic finite automata lies in how transitions are defined. A **Deterministic FA (DFA)** has exactly one transition for each state and input symbol combination, making the automaton's behavior entirely predictable. In contrast, a **Non-Deterministic FA (NDFA)** allows a state to have multiple transitions for the same input symbol, introducing multiple possible computational paths. Despite this difference, any NDFA can be converted to an equivalent DFA using the **subset construction algorithm**, proving that both models have equal computational power.

### Chomsky Hierarchy
The **Chomsky Hierarchy** provides a theoretical framework for classifying grammars into four distinct types based on their production rule restrictions. **Type 0**, known as Unrestricted Grammar, imposes no constraints on production rules and can generate any recursively enumerable language. **Type 1**, or Context-Sensitive Grammar, requires that productions follow the form αAβ → αγβ where the length of the left side is less than or equal to the right side, ensuring that the string never shrinks during derivation. **Type 2**, called Context-Free Grammar, restricts productions to the form A → γ where a single non-terminal appears on the left side, making these grammars useful for programming language syntax. Finally, **Type 3**, or Regular Grammar, has the most restrictive form with productions like A → aB or A → a, where A and B are non-terminals and a is a terminal, following right-linear patterns. This type is particularly important because regular grammars are equivalent to finite automata in their expressive power.

## Objectives

This laboratory work focuses on understanding the fundamental relationships between finite automata and formal grammars. The primary objectives include classifying grammars according to the Chomsky Hierarchy to understand their computational complexity, converting a Finite Automaton to an equivalent Regular Grammar to demonstrate their theoretical equivalence, determining whether a given FA is deterministic or non-deterministic by analyzing its transition structure, and implementing the subset construction algorithm to convert an NDFA to a DFA while preserving the accepted language.

## Variant 9 Definition

### Finite Automaton
The finite automaton for Variant 9 is defined with the following components:
- **Q** = {q0, q1, q2, q3, q4}
- **Σ** = {a, b, c}
- **F** = {q4}
- **Transitions**:
  - δ(q0, a) = q1
  - δ(q1, b) = q2
  - δ(q1, b) = q3 ← **Non-deterministic!**
  - δ(q2, c) = q0
  - δ(q3, a) = q4
  - δ(q3, b) = q0

The automaton exhibits non-deterministic behavior at state q1, where symbol 'b' leads to two different states (q2 and q3), making this a non-deterministic finite automaton. State q2 creates a potential loop by transitioning back to q0, while q3 provides paths to both the final state q4 and back to the initial state q0.

## Implementation

### 1. Grammar Classification (Task 1)

The `Grammar` class includes a `classify_chomsky()` method that analyzes production rules to determine the grammar type:

```python
def classify_chomsky(self):
    is_regular = True
    is_context_free = True
    is_context_sensitive = True
    
    for lhs, productions_list in self.productions.items():
        if lhs not in self.non_terminals:
            is_context_free = False
            is_regular = False
        
        for production in productions_list:
            parts = production.split()
            
            # Check Regular Grammar: A → aB or A → a
            if is_regular:
                if len(parts) == 1:
                    if parts[0] not in self.terminals:
                        is_regular = False
                elif len(parts) == 2:
                    if parts[0] not in self.terminals or parts[1] not in self.non_terminals:
                        is_regular = False
                else:
                    is_regular = False
    
    if is_regular:
        return "Type 3 (Regular Grammar)"
    elif is_context_free:
        return "Type 2 (Context-Free Grammar)"
    # ... other types
```

The Lab 1 grammar (Variant 9) is classified as **Type 3 (Regular Grammar)** because all productions follow the pattern A → aB or A → a.

### 2. Determinism Check (Task 2)

The `is_deterministic()` method checks if each state has at most one transition per symbol:

```python
def is_deterministic(self):
    for state in self.transitions:
        for symbol in self.transitions[state]:
            if len(self.transitions[state][symbol]) > 1:
                return False  # Multiple transitions found
    return True
```

**Result**: The FA is **Non-Deterministic (NDFA)** because state q1 has two transitions for symbol 'b', namely δ(q1, b) = q2 and δ(q1, b) = q3, creating ambiguity in which state to transition to when processing the symbol 'b' from state q1.

### 3. NDFA to DFA Conversion (Task 3)

The `ndfa_to_dfa()` method uses the **subset construction algorithm**, which begins by starting with the initial state as a singleton set. For each unmarked state set and each symbol in the alphabet, the algorithm computes the set of all reachable states and creates a new state for this set if it doesn't already exist. Finally, any state sets containing original final states are marked as final in the new DFA.

```python
def ndfa_to_dfa(self):
    initial_set = frozenset([self.initial_state])
    unmarked_states = [initial_set]
    dfa_states.append(initial_set)
    
    while unmarked_states:
        current_set = unmarked_states.pop(0)
        
        for symbol in self.alphabet:
            next_states = set()
            
            for state in current_set:
                if state in self.transitions and symbol in self.transitions[state]:
                    next_states.update(self.transitions[state][symbol])
            
            if next_states:
                next_set = frozenset(next_states)
                # Add new state if not seen before
                if next_set not in dfa_states:
                    dfa_states.append(next_set)
                    unmarked_states.append(next_set)
```

**Conversion Result**: The original NDFA state q1, which had non-deterministic transitions with 'b' going to both q2 and q3, is resolved in the DFA by creating a combined state {q2, q3}. The resulting DFA has four distinct states: {q0}, {q1}, {q2, q3}, and {q4}, where the combined state effectively captures both possible paths that could have been taken in the NDFA.

### 4. FA to Regular Grammar Conversion (Task 4)

The `to_regular_grammar()` method converts transitions to production rules following a systematic approach. Each state becomes a non-terminal symbol in the grammar, and for every transition δ(qi, a) = qj, the method adds a production qi → a qj. Additionally, if qj is a final state, the method also adds a simpler production qi → a to allow the derivation to terminate at that point.

```python
def to_regular_grammar(self):
    productions = {}
    
    for state in self.transitions:
        productions[state] = []
        
        for symbol in self.transitions[state]:
            next_states = self.transitions[state][symbol]
            
            for next_state in next_states:
                # Add: state → symbol next_state
                productions[state].append(f"{symbol} {next_state}")
                
                # If next_state is final: state → symbol
                if next_state in self.final_states:
                    productions[state].append(symbol)
```

## Results

### Task 1: Grammar Classification
The Lab 1 grammar is classified as **Type 3 (Regular Grammar)**. This classification is based on the production rules which all follow the right-linear format where each production takes the form A → aB or A → a, satisfying the requirements for regular grammars.

**Productions**:
- S → a B | b B
- B → c D
- D → d Q | a
- Q → b B | d Q

### Task 2: Determinism Check
The analysis reveals that the finite automaton is **Non-Deterministic (NDFA)**. The reason for this classification is that state q1 has multiple transitions for symbol 'b', specifically δ(q1, b) = q2 and δ(q1, b) = q3, creating ambiguity in the transition function.

### Task 3: NDFA to DFA Conversion
The conversion to DFA was successfully completed. The original NDFA state q1, which had non-deterministic transitions with 'b' going to both q2 and q3, is resolved in the DFA by creating a combined state {q2, q3}. The resulting DFA has four distinct states where the combined state effectively captures both possible paths that could have been taken in the NDFA.

**DFA States and Transitions**:
- {q0} → with 'a' → {q1}
- {q1} → with 'b' → {q2, q3}
- {q2, q3} → with 'a' → {q4} (final state)
- {q2, q3} → with 'b' → {q0}
- {q2, q3} → with 'c' → {q0}

### Task 4: FA to Grammar Conversion
The finite automaton was successfully converted to a Regular Grammar. This grammar is classified as **Type 3 (Regular Grammar)**, confirming the theoretical equivalence between finite automata and regular grammars.

**Productions**:
- q0 → a q1
- q1 → b q2 | b q3
- q2 → c q0
- q3 → a q4 | a | b q0

## Conclusions

This laboratory work successfully demonstrated several fundamental concepts in formal language theory and automata. The implementation of a grammar classification algorithm correctly identifies grammars according to the Chomsky Hierarchy, as evidenced by the successful classification of the Lab 1 grammar as Type 3 (Regular Grammar). The determinism analysis component effectively identified that the Variant 9 finite automaton is non-deterministic, specifically due to the multiple transitions from state q1 on symbol 'b', demonstrating a clear understanding of what distinguishes deterministic from non-deterministic automata.

The subset construction algorithm was successfully implemented to convert the NDFA to an equivalent DFA. This conversion process creates combined states for non-deterministic transitions, preserving the language accepted by the automaton while eliminating non-determinism. The resulting DFA maintains the same computational power as the original NDFA but with deterministic transition behavior.

Furthermore, the laboratory demonstrated the theoretical equivalence between finite automata and regular grammars through bidirectional conversion. By converting the FA to a regular grammar where states become non-terminals and transitions become production rules, the implementation confirms that both formalisms can express exactly the same class of languages. The Python implementation is straightforward, well-structured, and easy to understand, making it suitable for educational purposes while maintaining correctness in its algorithmic approach.

Overall, this laboratory successfully illustrates the relationships between finite automata, determinism, and regular grammars in formal language theory, providing practical experience with fundamental concepts that underpin compiler design, pattern matching, and formal verification.

## How to Run

To execute this laboratory work:

```bash
# Navigate to the lab2lfaf directory
cd "d:\LAB 2\lab2lfaf"

# Run the program
python main.py
```

**Requirements**: Python 3.x (no external libraries needed)

## Files Structure

```
lab2lfaf/
├── finite_automaton.py  # FiniteAutomaton class with all FA operations
├── grammar.py           # Grammar class with Chomsky classification
├── main.py             # Main demonstration program
└── README.md           # This file
```

## References

1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation*. Pearson.
2. Sipser, M. (2012). *Introduction to the Theory of Computation*. Cengage Learning.
3. Chomsky, N. (1956). "Three models for the description of language". *IRE Transactions on Information Theory*.
