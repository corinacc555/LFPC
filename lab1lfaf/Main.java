/**
 * Main class to demonstrate Grammar and Finite Automaton functionality
 * Laboratory Work 1 - Formal Languages & Finite Automata
 * Variant 9
 */
public class Main {
    public static void main(String[] args) {
        System.out.println("=== Laboratory Work 1: Grammar and Finite Automaton ===");
        System.out.println("Variant 9\n");
        
        // Create grammar instance
        Grammar grammar = new Grammar();
        
        // Display grammar definition
        System.out.println("Grammar Definition:");
        System.out.println("VN (Non-terminals): " + grammar.getVN());
        System.out.println("VT (Terminals): " + grammar.getVT());
        System.out.println("S (Start symbol): " + grammar.getS());
        System.out.println("P (Production rules):");
        for (var entry : grammar.getP().entrySet()) {
            for (String production : entry.getValue()) {
                System.out.println("  " + entry.getKey() + " → " + production);
            }
        }
        
        // Task 1: Generate 5 valid strings
        System.out.println("\n=== Task 1: Generate 5 Valid Strings ===");
        for (int i = 1; i <= 5; i++) {
            String generatedString = grammar.generateString();
            System.out.println("String " + i + ": " + generatedString);
        }
        
        // Task 2: Convert Grammar to Finite Automaton
        System.out.println("\n=== Task 2: Convert Grammar to Finite Automaton ===");
        FiniteAutomaton fa = grammar.toFiniteAutomaton();
        fa.printAutomaton();
        
        // Task 3: Check if strings belong to the language
        System.out.println("\n=== Task 3: String Validation ===");
        
        // Test with generated strings
        System.out.println("\nTesting generated strings:");
        for (int i = 1; i <= 5; i++) {
            String testString = grammar.generateString();
            boolean isValid = fa.stringBelongsToLanguage(testString);
            System.out.println("String: \"" + testString + "\" → " + 
                             (isValid ? "ACCEPTED ✓" : "REJECTED ✗"));
        }
        
        // Test with custom strings
        System.out.println("\nTesting custom strings:");
        String[] testStrings = {
            "abcda",      // Valid: S→aB→acD→acdQ→acdbB→abcdcD→abcdca
            "bcda",       // Valid: S→bB→bcD→bcdQ→bcdbB→bcdcD→bcdca
            "acdddda",    // Valid: multiple dQ loops
            "abcd",       // Invalid: doesn't end in final state
            "xyz",        // Invalid: not in alphabet
            "a",          // Invalid: too short
            "acddda"      // Valid
        };
        
        for (String testString : testStrings) {
            boolean isValid = fa.stringBelongsToLanguage(testString);
            System.out.println("String: \"" + testString + "\" → " + 
                             (isValid ? "ACCEPTED ✓" : "REJECTED ✗"));
        }
        
        System.out.println("\n=== End of Demonstration ===");
    }
}
