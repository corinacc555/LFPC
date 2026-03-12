"""
Finite Automaton implementation for Laboratory 2
Variant 9
"""

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        """
        Initialize Finite Automaton
        :param states: Set of states Q
        :param alphabet: Input alphabet Σ
        :param transitions: Transition function δ as dict: {state: {symbol: [next_states]}}
        :param initial_state: Initial state q0
        :param final_states: Set of final states F
        """
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
    
    def is_deterministic(self):
        """
        Check if the FA is deterministic (DFA) or non-deterministic (NDFA)
        A FA is deterministic if:
        1. Each state has at most one transition for each symbol
        2. No epsilon transitions exist
        """
        for state in self.transitions:
            for symbol in self.transitions[state]:
                # Check if there are multiple transitions for same symbol
                if len(self.transitions[state][symbol]) > 1:
                    return False
        return True
    
    def ndfa_to_dfa(self):
        """
        Convert NDFA to DFA using subset construction algorithm
        """
        if self.is_deterministic():
            print("Already deterministic!")
            return self
        
        # New DFA components
        dfa_states = []
        dfa_transitions = {}
        dfa_final_states = []
        
        # Start with the initial state as a set
        initial_set = frozenset([self.initial_state])
        unmarked_states = [initial_set]
        dfa_states.append(initial_set)
        
        while unmarked_states:
            current_set = unmarked_states.pop(0)
            dfa_transitions[current_set] = {}
            
            # For each symbol in alphabet
            for symbol in self.alphabet:
                next_states = set()
                
                # Get all states reachable from current_set with symbol
                for state in current_set:
                    if state in self.transitions and symbol in self.transitions[state]:
                        next_states.update(self.transitions[state][symbol])
                
                if next_states:
                    next_set = frozenset(next_states)
                    dfa_transitions[current_set][symbol] = [next_set]
                    
                    # Add new state if not seen before
                    if next_set not in dfa_states:
                        dfa_states.append(next_set)
                        unmarked_states.append(next_set)
        
        # Determine final states (any set containing an original final state)
        for state_set in dfa_states:
            if any(state in self.final_states for state in state_set):
                dfa_final_states.append(state_set)
        
        return FiniteAutomaton(
            states=set(dfa_states),
            alphabet=self.alphabet,
            transitions=dfa_transitions,
            initial_state=initial_set,
            final_states=set(dfa_final_states)
        )
    
    def to_regular_grammar(self):
        """
        Convert Finite Automaton to Regular Grammar
        Rules:
        - For transition δ(qi, a) = qj: add production qi → a qj
        - If qj is final state: add production qi → a
        """
        # Non-terminals are the states
        non_terminals = self.states.copy()
        
        # Terminals are the alphabet
        terminals = self.alphabet.copy()
        
        # Start symbol is the initial state
        start_symbol = self.initial_state
        
        # Production rules
        productions = {}
        
        for state in self.transitions:
            productions[state] = []
            
            for symbol in self.transitions[state]:
                next_states = self.transitions[state][symbol]
                
                for next_state in next_states:
                    # Add production: state → symbol next_state
                    productions[state].append(f"{symbol} {next_state}")
                    
                    # If next_state is final, also add: state → symbol
                    if next_state in self.final_states:
                        if symbol not in productions[state]:  # Avoid duplicates
                            productions[state].append(symbol)
        
        return {
            'non_terminals': non_terminals,
            'terminals': terminals,
            'start_symbol': start_symbol,
            'productions': productions
        }
    
    def display(self):
        """Display the finite automaton"""
        print("\n=== Finite Automaton ===")
        print(f"Q (States): {self.states}")
        print(f"Σ (Alphabet): {self.alphabet}")
        print(f"q0 (Initial state): {self.initial_state}")
        print(f"F (Final states): {self.final_states}")
        print("\nδ (Transitions):")
        for state in sorted(self.transitions.keys(), key=str):
            for symbol in sorted(self.transitions[state].keys()):
                next_states = self.transitions[state][symbol]
                for next_state in next_states:
                    print(f"  δ({state}, {symbol}) = {next_state}")
    
    @staticmethod
    def create_variant_9():
        """
        Create FA for Variant 9:
        Q = {q0, q1, q2, q3, q4}
        Σ = {a, b, c}
        F = {q4}
        δ(q0, a) = q1
        δ(q1, b) = q2
        δ(q2, c) = q0
        δ(q1, b) = q3  (non-deterministic!)
        δ(q3, a) = q4
        δ(q3, b) = q0
        """
        states = {'q0', 'q1', 'q2', 'q3', 'q4'}
        alphabet = {'a', 'b', 'c'}
        initial_state = 'q0'
        final_states = {'q4'}
        
        # Transitions with non-determinism at q1 with 'b'
        transitions = {
            'q0': {'a': ['q1']},
            'q1': {'b': ['q2', 'q3']},  # Non-deterministic!
            'q2': {'c': ['q0']},
            'q3': {'a': ['q4'], 'b': ['q0']}
        }
        
        return FiniteAutomaton(states, alphabet, transitions, initial_state, final_states)
