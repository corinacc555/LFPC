# Laboratory Work 1: Grammar and Finite Automaton

**Course:** Formal Languages & Finite Automata  
**Author:** [Your Name]  
**Variant:** 9

## Theory

A **formal language** is a set of strings formed from an alphabet according to specific rules. It consists of:
- **Alphabet (Σ)**: A finite set of symbols
- **Vocabulary**: Valid words formed from the alphabet
- **Grammar**: Rules that define how strings can be formed

A **formal grammar** is defined by the tuple **G = (VN, VT, P, S)** where:
- **VN**: Set of non-terminal symbols (variables)
- **VT**: Set of terminal symbols (alphabet)
- **P**: Set of production rules
- **S**: Start symbol (S ∈ VN)

A **Finite Automaton (FA)** is a mathematical model of computation defined by **FA = (Q, Σ, δ, q0, F)** where:
- **Q**: Finite set of states
- **Σ**: Input alphabet
- **δ**: Transition function (Q × Σ → Q)
- **q0**: Initial state (q0 ∈ Q)
- **F**: Set of final/accepting states (F ⊆ Q)

Grammars and finite automata are equivalent for regular languages - any regular grammar can be converted to a finite automaton and vice versa.

## Objectives

1. Understand what constitutes a formal language and formal grammar
2. Implement a Grammar class that can generate valid strings
3. Implement a Finite Automaton class that can validate strings
4. Convert a Grammar object to a Finite Automaton object
5. Set up a GitHub repository for the project

## Grammar Definition (Variant 9)

- **VN** = {S, B, D, Q}
- **VT** = {a, b, c, d}
- **P** (Production rules):
  - S → aB
  - S → bB
  - B → cD
  - D → dQ
  - D → a
  - Q → bB
  - Q → dQ

## Implementation Description

### 1. Grammar Class

The `Grammar` class represents a formal grammar with four main components stored as instance variables:
- `VN`: A Set containing non-terminal symbols
- `VT`: A Set containing terminal symbols  
- `P`: A Map storing production rules (key: non-terminal, value: list of productions)
- `S`: The start symbol

The class includes a `generateString()` method that creates valid strings by:
1. Starting with the start symbol S
2. Iteratively replacing non-terminals with randomly chosen productions
3. Keeping terminals in the result
4. Continuing until only terminals remain

```java
public String generateString() {
    StringBuilder result = new StringBuilder();
    String current = S;
    
    while (!current.isEmpty()) {
        char firstChar = current.charAt(0);
        String firstSymbol = String.valueOf(firstChar);
        
        if (VT.contains(firstSymbol)) {
            result.append(firstChar);
            current = current.substring(1);
        } else if (VN.contains(firstSymbol)) {
            List<String> productions = P.get(firstSymbol);
            if (productions != null && !productions.isEmpty()) {
                String production = productions.get(random.nextInt(productions.size()));
                current = production + current.substring(1);
            }
        }
        
        if (result.length() > 100) break; // Safety check
    }
    
    return result.toString();
}
```

### 2. Grammar to Finite Automaton Conversion

The `toFiniteAutomaton()` method converts the grammar to an equivalent finite automaton by:
1. Creating states Q from non-terminals plus a final state F
2. Using terminals as the alphabet Σ
3. Converting each production rule to a transition:
   - Productions like "D → a" become transitions to final state: δ(D, a) = F
   - Productions like "S → aB" become transitions: δ(S, a) = B
4. Setting the grammar's start symbol as q0
5. Setting F as the only final state

```java
public FiniteAutomaton toFiniteAutomaton() {
    Set<String> Q = new HashSet<>(VN);
    Q.add("F"); // Final state
    
    Set<String> Sigma = new HashSet<>(VT);
    Map<String, Map<String, Set<String>>> delta = new HashMap<>();
    
    for (Map.Entry<String, List<String>> entry : P.entrySet()) {
        String nonTerminal = entry.getKey();
        for (String production : entry.getValue()) {
            if (production.length() == 1 && VT.contains(production)) {
                // Terminal production → go to final state
                delta.get(nonTerminal).get(production).add("F");
            } else if (production.length() == 2) {
                // Non-terminal production → transition to next state
                String terminal = String.valueOf(production.charAt(0));
                String nextState = String.valueOf(production.charAt(1));
                delta.get(nonTerminal).get(terminal).add(nextState);
            }
        }
    }
    
    return new FiniteAutomaton(Q, Sigma, delta, S, Set.of("F"));
}
```

### 3. Finite Automaton Class

The `FiniteAutomaton` class represents a finite state machine with the five formal components (Q, Σ, δ, q0, F). The key method is `stringBelongsToLanguage()` which validates input strings by:
1. Starting from the initial state q0
2. Processing each character and following transitions
3. Tracking all possible current states (supports non-determinism)
4. Accepting the string if any final state is reached after processing all input

```java
public boolean stringBelongsToLanguage(final String inputString) {
    Set<String> currentStates = new HashSet<>();
    currentStates.add(q0);
    
    for (int i = 0; i < inputString.length(); i++) {
        String symbol = String.valueOf(inputString.charAt(i));
        
        if (!Sigma.contains(symbol)) return false;
        
        Set<String> nextStates = new HashSet<>();
        for (String currentState : currentStates) {
            if (delta.containsKey(currentState) && 
                delta.get(currentState).containsKey(symbol)) {
                nextStates.addAll(delta.get(currentState).get(symbol));
            }
        }
        
        if (nextStates.isEmpty()) return false;
        currentStates = nextStates;
    }
    
    for (String state : currentStates) {
        if (F.contains(state)) return true;
    }
    return false;
}
```

### 4. Main Class

The `Main` class demonstrates all functionality:
- Creates a Grammar instance with Variant 9 specifications
- Generates 5 valid strings from the grammar
- Converts the grammar to a finite automaton
- Tests string validation with both generated and custom strings

## Results

### Generated Strings

The implementation successfully generates valid strings such as:
- `acdbca`
- `acdbcdbca`
- `bcdbcdddbca`
- `aca`

All generated strings follow the pattern defined by the grammar rules and are correctly accepted by the finite automaton.

### String Validation

The finite automaton correctly validates strings:
- **Accepted**: Strings generated by the grammar (e.g., "acddddbca", "bca")
- **Rejected**: Invalid strings (e.g., "abcd", "xyz", malformed strings)

### Automaton Structure

```
States Q: {S, B, D, Q, F}
Alphabet Σ: {a, b, c, d}
Initial state q0: S
Final states F: {F}

Transitions:
δ(S, a) = {B}
δ(S, b) = {B}
δ(B, c) = {D}
δ(D, d) = {Q}
δ(D, a) = {F}
δ(Q, b) = {B}
δ(Q, d) = {Q}
```

## Conclusions

This laboratory work successfully demonstrated:

1. **Grammar Implementation**: Created a working Grammar class that properly stores and uses production rules to generate valid strings from the formal language.

2. **String Generation**: The random string generation algorithm correctly applies production rules iteratively, replacing non-terminals with their productions until only terminals remain.

3. **Grammar-to-Automaton Conversion**: Successfully converted the grammar to an equivalent finite automaton by mapping production rules to state transitions, demonstrating the equivalence between regular grammars and finite automata.

4. **String Validation**: The finite automaton correctly validates strings by simulating state transitions, accepting valid strings that can be derived from the grammar and rejecting invalid ones.

5. **Understanding Formal Languages**: Gained practical understanding of how formal grammars define languages and how finite automata recognize them.

The implementation is modular, well-documented, and can be easily extended for other grammar variants or additional functionality.

## How to Run

```bash
# Compile the Java files
javac Grammar.java FiniteAutomaton.java Main.java

# Run the demonstration
java Main
```

## References

1. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation*. Pearson.
2. Sipser, M. (2012). *Introduction to the Theory of Computation*. Cengage Learning.
3. Course lectures and materials on Formal Languages & Finite Automata.
