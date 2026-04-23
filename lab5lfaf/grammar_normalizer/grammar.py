import itertools

class Grammar:
    def __init__(self, vn, vt, p, s):
        self.vn = set(vn)
        self.vt = set(vt)
        self.s = s
        
        # Convert string RHS into tuples for easier manipulation
        # For the original grammar, single capitals are VN, single lowercases are VT
        self.p_tuples = {k: set() for k in self.vn}
        for lhs, rhs_set in p.items():
            for rhs in rhs_set:
                if rhs == '':
                    self.p_tuples[lhs].add(tuple())
                else:
                    self.p_tuples[lhs].add(tuple(c for c in rhs))
                    
    def _print_rhs(self, rhs):
        if not rhs:
            return 'ε'
        return "".join(str(x) for x in rhs)

    def print_grammar(self):
        for lhs in sorted(self.vn):
            if lhs in self.p_tuples and self.p_tuples[lhs]:
                rhs_strings = [self._print_rhs(rhs) for rhs in sorted(self.p_tuples[lhs])]
                rhs_joined = ' | '.join(rhs_strings)
                print(f"{lhs} -> {rhs_joined}")

    def eliminate_epsilon(self):
        """Step 1: Eliminate epsilon productions"""
        nullable = set()
        changed = True
        while changed:
            changed = False
            for lhs, rhs_set in self.p_tuples.items():
                if lhs in nullable:
                    continue
                for rhs in rhs_set:
                    if not rhs or all(c in nullable for c in rhs):
                        nullable.add(lhs)
                        changed = True
                        break

        new_p_tuples = {k: set() for k in self.vn}
        for lhs, rhs_set in self.p_tuples.items():
            for rhs in rhs_set:
                if not rhs:
                    continue
                # Generate all combinations of removing nullable symbols
                nullable_indices = [i for i, c in enumerate(rhs) if c in nullable]
                for i in range(len(nullable_indices) + 1):
                    for combo in itertools.combinations(nullable_indices, i):
                        new_rhs = tuple(c for j, c in enumerate(rhs) if j not in combo)
                        if new_rhs or lhs == self.s: # Allow S -> epsilon if it was there originally, but normally we ignore it for CNF
                            if new_rhs: # We just ignore epsilon productions for CNF
                                new_p_tuples[lhs].add(new_rhs)
                                
        self.p_tuples = new_p_tuples

    def eliminate_unit(self):
        """Step 2: Eliminate unit productions (renaming)"""
        # A unit production is of the form A -> B where A, B in VN
        unit_pairs = set()
        for A in self.vn:
            unit_pairs.add((A, A))

        changed = True
        while changed:
            changed = False
            new_pairs = set(unit_pairs)
            for A, B in unit_pairs:
                if B in self.p_tuples:
                    for rhs in self.p_tuples[B]:
                        if len(rhs) == 1 and rhs[0] in self.vn:
                            C = rhs[0]
                            if (A, C) not in new_pairs:
                                new_pairs.add((A, C))
                                changed = True
            unit_pairs = new_pairs

        new_p_tuples = {k: set() for k in self.vn}
        for A, B in unit_pairs:
            if B in self.p_tuples:
                for rhs in self.p_tuples[B]:
                    if not (len(rhs) == 1 and rhs[0] in self.vn):
                        new_p_tuples[A].add(rhs)

        self.p_tuples = new_p_tuples

    def eliminate_non_productive(self):
        """Step 3: Eliminate non-productive symbols"""
        productive = set()
        changed = True
        while changed:
            changed = False
            for lhs in self.vn:
                if lhs in productive:
                    continue
                if lhs in self.p_tuples:
                    for rhs in self.p_tuples[lhs]:
                        if all(c in self.vt or c in productive for c in rhs):
                            productive.add(lhs)
                            changed = True
                            break

        # Remove non-productive symbols and their productions
        self.vn = productive
        new_p_tuples = {}
        for k in self.vn:
            if k in self.p_tuples:
                new_p_tuples[k] = {rhs for rhs in self.p_tuples[k] if all(c in self.vt or c in productive for c in rhs)}
        self.p_tuples = new_p_tuples

    def eliminate_inaccessible(self):
        """Step 4: Eliminate inaccessible symbols"""
        accessible = {self.s}
        changed = True
        while changed:
            changed = False
            for A in list(accessible):
                if A in self.p_tuples:
                    for rhs in self.p_tuples[A]:
                        for c in rhs:
                            if c in self.vn and c not in accessible:
                                accessible.add(c)
                                changed = True

        # Remove inaccessible symbols
        self.vn = accessible
        self.p_tuples = {k: v for k, v in self.p_tuples.items() if k in self.vn}

    def to_cnf(self):
        """Step 5: Obtain Chomsky Normal Form"""
        term_to_nt = {}
        new_p_tuples = {k: set() for k in self.vn}
        
        # 5.1: Replace terminals in mixed or long RHS with new non-terminals
        for lhs, rhs_set in self.p_tuples.items():
            for rhs in rhs_set:
                if len(rhs) >= 2:
                    new_rhs = []
                    for c in rhs:
                        if c in self.vt:
                            if c not in term_to_nt:
                                new_nt = f"X_{c}"
                                term_to_nt[c] = new_nt
                                self.vn.add(new_nt)
                                new_p_tuples[new_nt] = {(c,)}
                            new_rhs.append(term_to_nt[c])
                        else:
                            new_rhs.append(c)
                    new_p_tuples[lhs].add(tuple(new_rhs))
                else:
                    new_p_tuples[lhs].add(rhs)
                    
        self.p_tuples = new_p_tuples

        # 5.2: Reduce long RHS (>2) down to 2 symbols by introducing variables
        alias_counter = 1
        while True:
            needs_reduction = False
            new_p_tuples = {k: set() for k in self.vn}
            for lhs, rhs_set in list(self.p_tuples.items()):
                for rhs in rhs_set:
                    if len(rhs) > 2:
                        needs_reduction = True
                        new_nt = f"Z_{alias_counter}"
                        alias_counter += 1
                        self.vn.add(new_nt)
                        
                        # Replace first two symbols with new_nt, keep the rest
                        # Alternatively, A -> B C D ... becomes A -> B new_nt, new_nt -> C D ...
                        new_p_tuples[lhs].add((rhs[0], new_nt))
                        if new_nt not in self.p_tuples:
                            self.p_tuples[new_nt] = set()
                        self.p_tuples[new_nt].add(tuple(rhs[1:]))
                    else:
                        new_p_tuples[lhs].add(rhs)
            self.p_tuples = new_p_tuples
            if not needs_reduction:
                break
