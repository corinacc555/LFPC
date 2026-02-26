# Laboratory Work 2: Determinism and Grammar Classification

**Course:** Formal Languages & Finite Automata  
**Author:** [Your Name]  
**Variant:** 9

## Theory

### Finite Automaton
A **finite automaton (FA)** is a mathematical model that represents processes or computations. It consists of:
- **Q**: Finite set of states
- **Σ**: Input alphabet
- **δ**: Transition function
- **q0**: Initial state
- **F**: Set of final (accepting) states

### Determinism vs Non-Determinism
- **Deterministic FA (DFA)**: For each state and input symbol, there is exactly one transition
- **Non-Deterministic FA (NDFA)**: A state can have multiple transitions for the same input symbol

Any NDFA can be converted to an equivalent DFA using the **subset construction algorithm**.

### Chomsky Hierarchy
The **Chomsky Hierarchy** classifies grammars into four types:

1. **Type 0 (Unrestricted Grammar)**: No restrictions on production rules
2. **Type 1 (Context-Sensitive Grammar)**: Productions of form αAβ → αγβ where |α| ≤ |γ|
3. **Type 2 (Context-Free Grammar)**: Productions of form A → γ (single non-terminal on left)
4. **Type 3 (Regular Grammar)**: Productions of form A → aB or A → a (right-linear regular)

Regular grammars are equivalent to finite automata.

## Objectives

1. Classify grammars according to Chomsky Hierarchy
2. Convert a Finite Automaton to a Regular Grammar
3. Determine if an FA is deterministic or non-deterministic
4. Convert an NDFA to a DFA using subset construction

## Variant 9 Definition

### Finite Automaton
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

**Result**: The FA is **Non-Deterministic (NDFA)** because state q1 has two transitions for symbol 'b':
- δ(q1, b) = q2
- δ(q1, b) = q3

### 3. NDFA to DFA Conversion (Task 3)

The `ndfa_to_dfa()` method uses the **subset construction algorithm**:

1. Start with the initial state as a singleton set
2. For each unmarked state set and each symbol:
   - Compute the set of all reachable states
   - Create a new state for this set if it doesn't exist
3. Mark state sets containing final states as final

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

**Conversion Result**:
- Original NDFA state q1 with 'b' → {q2, q3}
- DFA creates combined state {q2, q3}
- New DFA has states: {q0}, {q1}, {q2, q3}, {q4}

### 4. FA to Regular Grammar Conversion (Task 4)

The `to_regular_grammar()` method converts transitions to production rules:

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

**Conversion Rules**:
- Each state becomes a non-terminal
- For δ(qi, a) = qj: add production qi → a qj
- If qj is final: also add production qi → a

## Results

### Task 1: Grammar Classification
The Lab 1 grammar is classified as **Type 3 (Regular Grammar)**.

Productions:
- S → a B | b B
- B → c D
- D → d Q | a
- Q → b B | d Q

All productions follow right-linear format: A → aB or A → a

### Task 2: Determinism Check
**Result**: NDFA (Non-Deterministic)

**Reason**: State q1 has multiple transitions for symbol 'b':
```
δ(q1, b) = q2
δ(q1, b) = q3
```

### Task 3: NDFA to DFA Conversion
Successfully converted to DFA with the following states:
```
{q0} → with 'a' → {q1}
{q1} → with 'b' → {q2, q3}
{q2, q3} → with 'a' → {q4}
{q2, q3} → with 'b' → {q0}
{q2, q3} → with 'c' → {q0}
```

The combined state {q2, q3} resolves the non-determinism.

### Task 4: FA to Grammar Conversion
Converted FA to Regular Grammar:

Productions:
- q0 → a q1
- q1 → b q2 | b q3
- q2 → c q0
- q3 → a q4 | a | b q0

Classification: **Type 3 (Regular Grammar)**

## Conclusions

1. **Chomsky Classification**: Successfully implemented grammar classification algorithm that correctly identifies the Lab 1 grammar as Type 3 (Regular Grammar).

2. **Determinism Analysis**: Correctly identified that the Variant 9 FA is non-deterministic due to multiple transitions from q1 on symbol 'b'.

3. **NDFA to DFA Conversion**: Successfully implemented the subset construction algorithm, converting the NDFA to an equivalent DFA by creating combined states for non-deterministic transitions.

4. **FA to Grammar Equivalence**: Demonstrated that finite automata and regular grammars are equivalent by converting the FA to a regular grammar where states become non-terminals and transitions become production rules.

5. **Simple Implementation**: The Python implementation is straightforward, well-structured, and easy to understand, making it suitable for educational purposes.

The laboratory successfully demonstrates the relationships between finite automata, determinism, and regular grammars in formal language theory.

## How to Run

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

1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation*.
2. Sipser, M. (2012). *Introduction to the Theory of Computation*.
3. Chomsky, N. (1956). "Three models for the description of language". *IRE Transactions on Information Theory*.
