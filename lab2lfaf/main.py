"""
Laboratory Work 2: Determinism and Grammar Classification
Course: Formal Languages & Finite Automata
Variant 9

This program demonstrates:
1. Grammar classification using Chomsky Hierarchy
2. FA to Regular Grammar conversion
3. Checking if FA is deterministic or non-deterministic
4. Converting NDFA to DFA
"""

from finite_automaton import FiniteAutomaton
from grammar import Grammar


def print_separator(title=""):
    """Print a formatted separator"""
    if title:
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print('=' * 60)
    else:
        print("\n" + "=" * 60)


def main():
    print("=" * 60)
    print("  Laboratory Work 2: FA and Grammar Classification")
    print("  Variant 9")
    print("=" * 60)
    
    # ========== Task 1: Grammar Classification (from Lab 1) ==========
    print_separator("Task 1: Chomsky Hierarchy Classification")
    print("\nUsing Grammar from Lab 1 (Variant 9):")
    
    grammar_lab1 = Grammar.create_variant_9_lab1()
    grammar_lab1.display()
    
    # ========== Task 2: Create Finite Automaton (Variant 9) ==========
    print_separator("Task 2: Finite Automaton (Variant 9)")
    
    fa = FiniteAutomaton.create_variant_9()
    fa.display()
    
    # ========== Task 3: Check if FA is Deterministic ==========
    print_separator("Task 3: Determinism Check")
    
    is_dfa = fa.is_deterministic()
    print(f"\nIs the FA deterministic? {'YES (DFA)' if is_dfa else 'NO (NDFA)'}")
    
    if not is_dfa:
        print("\nReason: State q1 has multiple transitions for symbol 'b':")
        print("  δ(q1, b) = q2")
        print("  δ(q1, b) = q3")
        print("This creates non-determinism!")
    
    # ========== Task 4: Convert NDFA to DFA ==========
    print_separator("Task 4: NDFA to DFA Conversion")
    
    if not is_dfa:
        print("\nConverting NDFA to DFA using subset construction...")
        dfa = fa.ndfa_to_dfa()
        dfa.display()
        
        print(f"\nNew DFA is deterministic? {dfa.is_deterministic()}")
        
        # Explain the conversion
        print("\nExplanation:")
        print("- Created new states as combinations of original states")
        print("- q1 with 'b' previously went to {q2, q3}")
        print("- In DFA, we create a new combined state {q2, q3}")
        print("- Each state now has exactly one transition per symbol")
    
    # ========== Task 5: Convert FA to Regular Grammar ==========
    print_separator("Task 5: FA to Regular Grammar Conversion")
    
    print("\nConverting original NDFA to Regular Grammar...")
    grammar_from_fa = fa.to_regular_grammar()
    
    grammar_obj = Grammar.create_from_fa(grammar_from_fa)
    grammar_obj.display()
    
    print("\nConversion Rules Applied:")
    print("- Each state becomes a non-terminal")
    print("- For δ(qi, a) = qj: add production qi → a qj")
    print("- If qj is final state: add production qi → a")
    
    # ========== Summary ==========
    print_separator("Summary")
    
    print("\n✓ Lab 1 Grammar Classification:")
    print(f"  {grammar_lab1.classify_chomsky()}")
    
    print("\n✓ FA Determinism:")
    print(f"  Original FA is {'Deterministic (DFA)' if is_dfa else 'Non-Deterministic (NDFA)'}")
    
    print("\n✓ NDFA to DFA Conversion:")
    print("  Successfully converted using subset construction algorithm")
    
    print("\n✓ FA to Grammar Conversion:")
    print(f"  Converted FA to {grammar_obj.classify_chomsky()}")
    
    print_separator()
    print("\nAll tasks completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
