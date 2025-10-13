class Term:
    """Base class for terms in first-order logic"""
    pass

class Constant(Term):
    """Represents a constant"""
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, other):
        return isinstance(other, Constant) and self.name == other.name
    
    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(('Constant', self.name))

class Variable(Term):
    """Represents a variable"""
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name
    
    def __repr__(self):
        return self.name
    
    def __hash__(self):
        return hash(('Variable', self.name))

class Predicate(Term):
    """Represents a predicate with arguments"""
    def __init__(self, name, args):
        self.name = name
        self.args = args if isinstance(args, list) else [args]
    
    def __eq__(self, other):
        return (isinstance(other, Predicate) and 
                self.name == other.name and 
                len(self.args) == len(other.args) and
                all(a == b for a, b in zip(self.args, other.args)))
    
    def __repr__(self):
        return f"{self.name}({', '.join(str(arg) for arg in self.args)})"
    
    def __hash__(self):
        return hash((self.name, tuple(self.args)))

class Rule:
    """Represents an implication rule: premises => conclusion"""
    def __init__(self, premises, conclusion):
        self.premises = premises if isinstance(premises, list) else [premises]
        self.conclusion = conclusion
    
    def __repr__(self):
        premises_str = ' ∧ '.join(str(p) for p in self.premises)
        return f"{premises_str} => {self.conclusion}"

# Variable counter for standardization
_var_counter = 0

def get_new_variable():
    """Generate a new unique variable"""
    global _var_counter
    _var_counter += 1
    return Variable(f"v{_var_counter}")

def standardize_variables(rule):
    """Replace all variables in rule with new unique variables"""
    var_mapping = {}
    
    def replace_vars(term):
        if isinstance(term, Variable):
            if term not in var_mapping:
                var_mapping[term] = get_new_variable()
            return var_mapping[term]
        elif isinstance(term, Predicate):
            new_args = [replace_vars(arg) for arg in term.args]
            return Predicate(term.name, new_args)
        else:
            return term
    
    new_premises = [replace_vars(p) for p in rule.premises]
    new_conclusion = replace_vars(rule.conclusion)
    return Rule(new_premises, new_conclusion)

def occurs_check(var, term, subst):
    """Check if variable occurs in term"""
    if var == term:
        return True
    elif isinstance(term, Variable) and term in subst:
        return occurs_check(var, subst[term], subst)
    elif isinstance(term, Predicate):
        return any(occurs_check(var, arg, subst) for arg in term.args)
    return False

def apply_substitution(term, subst):
    """Apply substitution to a term"""
    if isinstance(term, Variable):
        if term in subst:
            return apply_substitution(subst[term], subst)
        return term
    elif isinstance(term, Predicate):
        new_args = [apply_substitution(arg, subst) for arg in term.args]
        return Predicate(term.name, new_args)
    else:
        return term

def unify(term1, term2, subst=None):
    """Unification algorithm"""
    if subst is None:
        subst = {}
    
    term1 = apply_substitution(term1, subst)
    term2 = apply_substitution(term2, subst)
    
    if term1 == term2:
        return subst
    elif isinstance(term1, Variable):
        if occurs_check(term1, term2, subst):
            return None
        else:
            new_subst = subst.copy()
            new_subst[term1] = term2
            return new_subst
    elif isinstance(term2, Variable):
        if occurs_check(term2, term1, subst):
            return None
        else:
            new_subst = subst.copy()
            new_subst[term2] = term1
            return new_subst
    elif isinstance(term1, Constant) or isinstance(term2, Constant):
        return None
    elif isinstance(term1, Predicate) and isinstance(term2, Predicate):
        if term1.name != term2.name or len(term1.args) != len(term2.args):
            return None
        
        current_subst = subst.copy()
        for arg1, arg2 in zip(term1.args, term2.args):
            current_subst = unify(arg1, arg2, current_subst)
            if current_subst is None:
                return None
        return current_subst
    else:
        return None

def unify_all(premises, kb_facts, subst=None):
    """Try to unify all premises with facts in KB"""
    if subst is None:
        subst = {}
    
    if not premises:
        return [subst]
    
    first_premise = premises[0]
    remaining_premises = premises[1:]
    
    all_substitutions = []
    
    for fact in kb_facts:
        theta = unify(first_premise, fact, subst.copy())
        if theta is not None:
            # Apply substitution to remaining premises
            substituted_remaining = [apply_substitution(p, theta) for p in remaining_premises]
            # Recursively unify remaining premises
            result_substs = unify_all(substituted_remaining, kb_facts, theta)
            all_substitutions.extend(result_substs)
    
    return all_substitutions

def fol_fc_ask(kb_facts, kb_rules, query, max_iterations=100):
    """
    Forward Chaining Algorithm for First-Order Logic
    
    Args:
        kb_facts: List of atomic sentences (facts) in KB
        kb_rules: List of implication rules in KB
        query: The query to prove (atomic sentence)
        max_iterations: Maximum number of iterations to prevent infinite loops
    
    Returns:
        Substitution if query can be proved, None otherwise
    """
    print("=== Forward Chaining Algorithm ===\n")
    print(f"Query: {query}\n")
    print("Initial KB Facts:")
    for fact in kb_facts:
        print(f"  {fact}")
    print("\nKB Rules:")
    for rule in kb_rules:
        print(f"  {rule}")
    print("\n" + "="*50 + "\n")
    
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        new = []
        
        print(f"Iteration {iteration}:")
        
        # For each rule in KB
        for rule in kb_rules:
            # Standardize variables in the rule
            std_rule = standardize_variables(rule)
            
            # Try to find substitutions that satisfy all premises
            substitutions = unify_all(std_rule.premises, kb_facts)
            
            # For each valid substitution
            for theta in substitutions:
                # Apply substitution to conclusion
                inferred = apply_substitution(std_rule.conclusion, theta)
                
                # Check if this fact is new
                if inferred not in kb_facts and inferred not in new:
                    new.append(inferred)
                    print(f"  Inferred: {inferred}")
                    print(f"    From rule: {std_rule}")
                    print(f"    With substitution: {theta}")
                    
                    # Check if inferred fact unifies with query
                    result = unify(inferred, query)
                    if result is not None:
                        print(f"\n*** Query proved! ***")
                        print(f"Substitution: {result}")
                        return result
        
        # If no new facts inferred, we're done
        if not new:
            print("  No new facts inferred.")
            print("\nForward chaining completed. Query cannot be proved.")
            return None
        
        # Add new facts to KB
        kb_facts.extend(new)
        print()
    
    print(f"Maximum iterations ({max_iterations}) reached.")
    return None

def parse_term(term_str):
    """Parse a string into a Term object"""
    term_str = term_str.strip()
    
    if '(' in term_str:
        paren_idx = term_str.index('(')
        pred_name = term_str[:paren_idx].strip()
        args_str = term_str[paren_idx+1:term_str.rindex(')')].strip()
        
        args = []
        depth = 0
        current_arg = ""
        for char in args_str:
            if char == ',' and depth == 0:
                args.append(parse_term(current_arg))
                current_arg = ""
            else:
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                current_arg += char
        
        if current_arg.strip():
            args.append(parse_term(current_arg))
        
        return Predicate(pred_name, args)
    elif term_str[0].islower():
        return Variable(term_str)
    else:
        return Constant(term_str)

def parse_rule(rule_str):
    """Parse a rule string like 'P(x) ∧ Q(x) => R(x)'"""
    if '=>' in rule_str:
        parts = rule_str.split('=>')
        conclusion_str = parts[1].strip()
        premises_str = parts[0].strip()
        
        # Split premises by ∧ or AND
        premise_parts = [p.strip() for p in premises_str.replace('AND', '∧').split('∧')]
        
        premises = [parse_term(p) for p in premise_parts]
        conclusion = parse_term(conclusion_str)
        
        return Rule(premises, conclusion)
    else:
        # It's just a fact
        return parse_term(rule_str)

# Example usage
if __name__ == "__main__":
    print("Choose mode:")
    print("1. Run example (Animal reasoning)")
    print("2. Interactive mode")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    print()
    
    if choice == '1':
        # Example: Animal reasoning
        # Facts
        kb_facts = [
            Predicate('Animal', [Constant('Dog')]),
            Predicate('Animal', [Constant('Cat')]),
            Predicate('Loves', [Constant('John'), Constant('Dog')]),
            Predicate('Owns', [Constant('John'), Constant('Dog')])
        ]
        
        # Rules
        kb_rules = [
            # Animal(x) ∧ Loves(y, x) => Loves(x, y)
            Rule([Predicate('Animal', [Variable('x')]), 
                  Predicate('Loves', [Variable('y'), Variable('x')])],
                 Predicate('Loves', [Variable('x'), Variable('y')])),
            
            # Owns(x, y) ∧ Animal(y) => KeepsAsPet(x, y)
            Rule([Predicate('Owns', [Variable('x'), Variable('y')]),
                  Predicate('Animal', [Variable('y')])],
                 Predicate('KeepsAsPet', [Variable('x'), Variable('y')]))
        ]
        
        # Query: Does Dog love John?
        query = Predicate('Loves', [Constant('Dog'), Constant('John')])
        
        result = fol_fc_ask(kb_facts, kb_rules, query)
        
    elif choice == '2':
        print("=== Interactive Forward Chaining ===")
        print("Enter facts and rules for the knowledge base.\n")
        
        kb_facts = []
        kb_rules = []
        
        # Input facts
        print("Enter facts (one per line, empty line to finish):")
        print("Example: Animal(Dog), Loves(John, Dog)")
        while True:
            fact_str = input("Fact: ").strip()
            if not fact_str:
                break
            try:
                fact = parse_term(fact_str)
                kb_facts.append(fact)
            except Exception as e:
                print(f"Error parsing fact: {e}")
        
        # Input rules
        print("\nEnter rules (one per line, empty line to finish):")
        print("Example: Animal(x) ∧ Loves(y,x) => Loves(x,y)")
        print("You can also use 'AND' instead of ∧")
        while True:
            rule_str = input("Rule: ").strip()
            if not rule_str:
                break
            try:
                rule = parse_rule(rule_str)
                kb_rules.append(rule)
            except Exception as e:
                print(f"Error parsing rule: {e}")
        
        # Input query
        print("\nEnter query:")
        query_str = input("Query: ").strip()
        try:
            query = parse_term(query_str)
            result = fol_fc_ask(kb_facts, kb_rules, query)
        except Exception as e:
            print(f"Error parsing query: {e}")
    
    else:
        print("Invalid choice.")
