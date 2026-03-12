import java.util.*;

/**
 * Grammar class representing a formal grammar with:
 * VN = {S, B, D, Q} - Non-terminal symbols
 * VT = {a, b, c, d} - Terminal symbols
 * P - Production rules
 * S - Start symbol
 */
public class Grammar {
    // Non-terminal symbols
    private Set<String> VN;
    
    // Terminal symbols
    private Set<String> VT;
    
    // Production rules: Map<NonTerminal, List<Possible Productions>>
    private Map<String, List<String>> P;
    
    // Start symbol
    private String S;
    
    // Random generator for string generation
    private Random random;
    
    /**
     * Constructor for Grammar (Variant 9)
     */
    public Grammar() {
        this.random = new Random();
        
        // Initialize non-terminal symbols
        this.VN = new HashSet<>(Arrays.asList("S", "B", "D", "Q"));
        
        // Initialize terminal symbols
        this.VT = new HashSet<>(Arrays.asList("a", "b", "c", "d"));
        
        // Initialize production rules
        this.P = new HashMap<>();
        P.put("S", Arrays.asList("aB", "bB"));
        P.put("B", Arrays.asList("cD"));
        P.put("D", Arrays.asList("dQ", "a"));
        P.put("Q", Arrays.asList("bB", "dQ"));
        
        // Set start symbol
        this.S = "S";
    }
    
    /**
     * Generate a valid string from the grammar
     * @return A string that belongs to the language defined by this grammar
     */
    public String generateString() {
        StringBuilder result = new StringBuilder();
        String current = S;
        
        // Keep expanding until we have only terminal symbols
        while (!current.isEmpty()) {
            char firstChar = current.charAt(0);
            String firstSymbol = String.valueOf(firstChar);
            
            // If it's a terminal symbol, add it to result and move to next
            if (VT.contains(firstSymbol)) {
                result.append(firstChar);
                current = current.substring(1);
            }
            // If it's a non-terminal, replace it with one of its productions
            else if (VN.contains(firstSymbol)) {
                List<String> productions = P.get(firstSymbol);
                if (productions != null && !productions.isEmpty()) {
                    // Choose a random production
                    String production = productions.get(random.nextInt(productions.size()));
                    // Replace the non-terminal with the production
                    current = production + current.substring(1);
                } else {
                    // No production found, remove the symbol
                    current = current.substring(1);
                }
            } else {
                // Unknown symbol, skip it
                current = current.substring(1);
            }
            
            // Safety check to avoid infinite loops
            if (result.length() > 100) {
                break;
            }
        }
        
        return result.toString();
    }
    
    /**
     * Convert this Grammar to a Finite Automaton
     * @return FiniteAutomaton equivalent to this grammar
     */
    public FiniteAutomaton toFiniteAutomaton() {
        // States Q: all non-terminals + a final state
        Set<String> Q = new HashSet<>(VN);
        Q.add("F"); // Final state
        
        // Alphabet Sigma: all terminal symbols
        Set<String> Sigma = new HashSet<>(VT);
        
        // Transition function delta
        Map<String, Map<String, Set<String>>> delta = new HashMap<>();
        
        // Initialize delta for all states
        for (String state : Q) {
            delta.put(state, new HashMap<>());
        }
        
        // Convert production rules to transitions
        for (Map.Entry<String, List<String>> entry : P.entrySet()) {
            String nonTerminal = entry.getKey();
            List<String> productions = entry.getValue();
            
            for (String production : productions) {
                if (production.length() == 1 && VT.contains(production)) {
                    // Production like D → a (goes to final state)
                    if (!delta.get(nonTerminal).containsKey(production)) {
                        delta.get(nonTerminal).put(production, new HashSet<>());
                    }
                    delta.get(nonTerminal).get(production).add("F");
                } else if (production.length() == 2) {
                    // Production like S → aB
                    String terminal = String.valueOf(production.charAt(0));
                    String nextState = String.valueOf(production.charAt(1));
                    
                    if (VT.contains(terminal) && VN.contains(nextState)) {
                        if (!delta.get(nonTerminal).containsKey(terminal)) {
                            delta.get(nonTerminal).put(terminal, new HashSet<>());
                        }
                        delta.get(nonTerminal).get(terminal).add(nextState);
                    }
                }
            }
        }
        
        // Initial state q0: start symbol of grammar
        String q0 = S;
        
        // Final states F: the final state we added
        Set<String> F = new HashSet<>(Arrays.asList("F"));
        
        return new FiniteAutomaton(Q, Sigma, delta, q0, F);
    }
    
    // Getters
    public Set<String> getVN() {
        return VN;
    }
    
    public Set<String> getVT() {
        return VT;
    }
    
    public Map<String, List<String>> getP() {
        return P;
    }
    
    public String getS() {
        return S;
    }
}
