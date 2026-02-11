import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/**
 * Finite Automaton class representing a finite state machine with:
 * Q - Set of states
 * Sigma - Input alphabet
 * delta - Transition function
 * q0 - Initial state
 * F - Set of final states
 */
public class FiniteAutomaton {
    // Set of states
    private Set<String> Q;
    
    // Input alphabet
    private Set<String> Sigma;
    
    // Transition function: delta(state, symbol) -> set of next states
    // Map<CurrentState, Map<InputSymbol, Set<NextStates>>>
    private Map<String, Map<String, Set<String>>> delta;
    
    // Initial state
    private String q0;
    
    // Set of final states
    private Set<String> F;
    
    /**
     * Constructor for Finite Automaton
     * @param Q Set of states
     * @param Sigma Input alphabet
     * @param delta Transition function
     * @param q0 Initial state
     * @param F Set of final states
     */
    public FiniteAutomaton(Set<String> Q, Set<String> Sigma, 
                          Map<String, Map<String, Set<String>>> delta, 
                          String q0, Set<String> F) {
        this.Q = Q;
        this.Sigma = Sigma;
        this.delta = delta;
        this.q0 = q0;
        this.F = F;
    }
    
    /**
     * Check if an input string belongs to the language accepted by this automaton
     * @param inputString The string to check
     * @return true if the string is accepted, false otherwise
     */
    public boolean stringBelongsToLanguage(final String inputString) {
        // Start from the initial state
        Set<String> currentStates = new HashSet<>();
        currentStates.add(q0);
        
        // Process each character in the input string
        for (int i = 0; i < inputString.length(); i++) {
            String symbol = String.valueOf(inputString.charAt(i));
            
            // Check if symbol is in alphabet
            if (!Sigma.contains(symbol)) {
                return false;
            }
            
            // Compute next states
            Set<String> nextStates = new HashSet<>();
            for (String currentState : currentStates) {
                if (delta.containsKey(currentState) && 
                    delta.get(currentState).containsKey(symbol)) {
                    nextStates.addAll(delta.get(currentState).get(symbol));
                }
            }
            
            // If no valid transitions, reject the string
            if (nextStates.isEmpty()) {
                return false;
            }
            
            currentStates = nextStates;
        }
        
        // Accept if any current state is a final state
        for (String state : currentStates) {
            if (F.contains(state)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Print the automaton structure for debugging
     */
    public void printAutomaton() {
        System.out.println("Finite Automaton:");
        System.out.println("Q (States): " + Q);
        System.out.println("Σ (Alphabet): " + Sigma);
        System.out.println("q0 (Initial state): " + q0);
        System.out.println("F (Final states): " + F);
        System.out.println("\nδ (Transition function):");
        for (Map.Entry<String, Map<String, Set<String>>> stateEntry : delta.entrySet()) {
            String state = stateEntry.getKey();
            for (Map.Entry<String, Set<String>> transEntry : stateEntry.getValue().entrySet()) {
                String symbol = transEntry.getKey();
                Set<String> nextStates = transEntry.getValue();
                System.out.println("  δ(" + state + ", " + symbol + ") = " + nextStates);
            }
        }
    }
    
    // Getters
    public Set<String> getQ() {
        return Q;
    }
    
    public Set<String> getSigma() {
        return Sigma;
    }
    
    public Map<String, Map<String, Set<String>>> getDelta() {
        return delta;
    }
    
    public String getQ0() {
        return q0;
    }
    
    public Set<String> getF() {
        return F;
    }
}
