from grammar import Grammar

def main():
    # Variant 9
    vn = {'S', 'A', 'B', 'C', 'D'}
    vt = {'a', 'b'}
    p = {
        'S': {'bA', 'BC'},
        'A': {'a', 'aS', 'bAaAb'},
        'B': {'A', 'bS', 'aAa'},
        'C': {'', 'AB'},
        'D': {'AB'}
    }
    s = 'S'
    
    g = Grammar(vn, vt, p, s)
    print("Original Grammar:")
    g.print_grammar()
    
    g.eliminate_epsilon()
    print("\nStep 1: After Eliminating Epsilon Productions:")
    g.print_grammar()
    
    g.eliminate_unit()
    print("\nStep 2: After Eliminating Unit (Renaming) Productions:")
    g.print_grammar()
    
    g.eliminate_inaccessible()
    print("\nStep 3: After Eliminating Inaccessible Symbols:")
    g.print_grammar()
    
    g.eliminate_non_productive()
    print("\nStep 4: After Eliminating Non-Productive Symbols:")
    g.print_grammar()
    
    g.to_cnf()
    print("\nStep 5: Chomsky Normal Form (CNF):")
    g.print_grammar()

if __name__ == '__main__':
    main()
