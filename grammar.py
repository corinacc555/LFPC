"""
Grammar implementation with Chomsky Hierarchy Classification
Laboratory 2
"""

class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        """
        Initialize Grammar
        :param non_terminals: Set of non-terminal symbols VN
        :param terminals: Set of terminal symbols VT
        :param productions: Production rules P as dict {non_terminal: [productions]}
        :param start_symbol: Start symbol S
        """
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
    
    def classify_chomsky(self):
        """
        Classify grammar according to Chomsky Hierarchy:
        Type 0: Unrestricted Grammar (no restrictions)
        Type 1: Context-Sensitive Grammar (|α| ≤ |β| for all α → β)
        Type 2: Context-Free Grammar (A → α where A is non-terminal)
        Type 3: Regular Grammar (A → aB or A → a where A, B are non-terminals, a is terminal)
        """
        is_regular = True
        is_context_free = True
        is_context_sensitive = True
        
        for lhs, productions_list in self.productions.items():
            # Check if left-hand side is a single non-terminal (for Type 2 and 3)
            if lhs not in self.non_terminals:
                is_context_free = False
                is_regular = False
            
            for production in productions_list:
                # Parse production
                parts = production.split()
                
                # Check for Regular Grammar (Type 3)
                # Right-linear: A → aB or A → a
                # where a is terminal, B is non-terminal
                if is_regular:
                    if len(parts) == 1:
                        # A → a (terminal only)
                        if parts[0] not in self.terminals:
                            is_regular = False
                    elif len(parts) == 2:
                        # A → aB (terminal followed by non-terminal)
                        if parts[0] not in self.terminals or parts[1] not in self.non_terminals:
                            is_regular = False
                    else:
                        # More than 2 symbols, not regular
                        is_regular = False
                
                # Check for Context-Sensitive Grammar (Type 1)
                # |α| ≤ |β| (left side length ≤ right side length)
                if is_context_sensitive:
                    if len(lhs) > len(production.replace(' ', '')):
                        is_context_sensitive = False
        
        # Determine the type
        if is_regular:
            return "Type 3 (Regular Grammar)"
        elif is_context_free:
            return "Type 2 (Context-Free Grammar)"
        elif is_context_sensitive:
            return "Type 1 (Context-Sensitive Grammar)"
        else:
            return "Type 0 (Unrestricted Grammar)"
    
    def display(self):
        """Display the grammar"""
        print("\n=== Grammar ===")
        print(f"VN (Non-terminals): {self.non_terminals}")
        print(f"VT (Terminals): {self.terminals}")
        print(f"S (Start symbol): {self.start_symbol}")
        print("\nP (Productions):")
        for lhs, productions_list in self.productions.items():
            for production in productions_list:
                print(f"  {lhs} → {production}")
        
        # Show classification
        classification = self.classify_chomsky()
        print(f"\nChomsky Classification: {classification}")
    
    @staticmethod
    def create_from_fa(fa_grammar_dict):
        """
        Create Grammar object from FA-to-Grammar conversion result
        """
        return Grammar(
            non_terminals=fa_grammar_dict['non_terminals'],
            terminals=fa_grammar_dict['terminals'],
            productions=fa_grammar_dict['productions'],
            start_symbol=fa_grammar_dict['start_symbol']
        )
    
    @staticmethod
    def create_variant_9_lab1():
        """
        Create Grammar from Lab 1 Variant 9:
        VN = {S, B, D, Q}
        VT = {a, b, c, d}
        P:
            S → aB | bB
            B → cD
            D → dQ | a
            Q → bB | dQ
        """
        non_terminals = {'S', 'B', 'D', 'Q'}
        terminals = {'a', 'b', 'c', 'd'}
        start_symbol = 'S'
        
        productions = {
            'S': ['a B', 'b B'],
            'B': ['c D'],
            'D': ['d Q', 'a'],
            'Q': ['b B', 'd Q']
        }
        
        return Grammar(non_terminals, terminals, productions, start_symbol)
