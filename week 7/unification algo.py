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

def occurs_check(var, term, subst):
    """Check if variable occurs in term (prevents infinite structures)"""
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
    """
    Unification Algorithm
    Returns substitution set if unification succeeds, None if it fails
    """
    if subst is None:
        subst = {}
    
    # Apply existing substitutions
    term1 = apply_substitution(term1, subst)
    term2 = apply_substitution(term2, subst)
    
    # Step 1: If term1 or term2 is a variable or constant
    # Step 1a: If both are identical
    if term1 == term2:
        return subst
    
    # Step 1b: If term1 is a variable
    elif isinstance(term1, Variable):
        if occurs_check(term1, term2, subst):
            return None  # FAILURE
        else:
            new_subst = subst.copy()
            new_subst[term1] = term2
            return new_subst
    
    # Step 1c: If term2 is a variable
    elif isinstance(term2, Variable):
        if occurs_check(term2, term1, subst):
            return None  # FAILURE
        else:
            new_subst = subst.copy()
            new_subst[term2] = term1
            return new_subst
    
    # Step 1d: Both are constants but not equal
    elif isinstance(term1, Constant) or isinstance(term2, Constant):
        return None  # FAILURE
    
    # Step 2: Check if both are predicates with same name
    elif isinstance(term1, Predicate) and isinstance(term2, Predicate):
        if term1.name != term2.name:
            return None  # FAILURE
        
        # Step 3: Check if they have same number of arguments
        if len(term1.args) != len(term2.args):
            return None  # FAILURE
        
        # Step 4 & 5: Unify arguments recursively
        current_subst = subst.copy()
        for arg1, arg2 in zip(term1.args, term2.args):
            current_subst = unify(arg1, arg2, current_subst)
            if current_subst is None:  # If unification fails
                return None
        
        return current_subst
    
    else:
        return None  # FAILURE

def print_substitution(subst):
    """Pretty print substitution set"""
    if subst is None:
        print("FAILURE: Unification failed")
    elif not subst:
        print("NIL: Terms are already unified")
    else:
        print("Substitution:")
        for var, term in subst.items():
            print(f"  {var} -> {term}")

def parse_term(term_str):
    """Parse a string representation of a term into Term objects"""
    term_str = term_str.strip()
    
    # Check if it's a predicate (contains parentheses)
    if '(' in term_str:
        paren_idx = term_str.index('(')
        pred_name = term_str[:paren_idx].strip()
        
        # Extract arguments between parentheses
        args_str = term_str[paren_idx+1:term_str.rindex(')')].strip()
        
        # Split arguments by comma (handle nested predicates)
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
    
    # Check if it's a variable (lowercase first letter or starts with ?)
    elif term_str[0].islower() or term_str[0] == '?':
        return Variable(term_str)
    
    # Otherwise it's a constant (uppercase first letter)
    else:
        return Constant(term_str)

def run_interactive():
    """Interactive mode for user input"""
    print("=== Unification Algorithm (Interactive Mode) ===")
    print("Enter terms to unify. Use:")
    print("  - Variables: lowercase letters (x, y, z) or ?x, ?y")
    print("  - Constants: uppercase letters (John, Mary, A)")
    print("  - Predicates: Name(arg1, arg2, ...) e.g., P(x, y)")
    print("  - Type 'quit' to exit\n")
    
    while True:
        print("-" * 50)
        term1_str = input("Enter first term: ").strip()
        
        if term1_str.lower() == 'quit':
            print("Exiting...")
            break
        
        term2_str = input("Enter second term: ").strip()
        
        if term2_str.lower() == 'quit':
            print("Exiting...")
            break
        
        try:
            term1 = parse_term(term1_str)
            term2 = parse_term(term2_str)
            
            print(f"\nUnifying: {term1} and {term2}")
            result = unify(term1, term2)
            print_substitution(result)
            print()
            
        except Exception as e:
            print(f"Error parsing terms: {e}")
            print("Please check your input format.\n")

def run_examples():
    """Run predefined examples"""
    print("=== Unification Algorithm Examples ===\n")
    
    # Example 1: Unifying variables
    print("Example 1: Unify(x, y)")
    x = Variable('x')
    y = Variable('y')
    result = unify(x, y)
    print_substitution(result)
    print()
    
    # Example 2: Unifying variable with constant
    print("Example 2: Unify(x, John)")
    x = Variable('x')
    john = Constant('John')
    result = unify(x, john)
    print_substitution(result)
    print()
    
    # Example 3: Unifying predicates
    print("Example 3: Unify(P(x, y), P(John, z))")
    p1 = Predicate('P', [Variable('x'), Variable('y')])
    p2 = Predicate('P', [Constant('John'), Variable('z')])
    result = unify(p1, p2)
    print_substitution(result)
    print()
    
    # Example 4: Unifying complex predicates
    print("Example 4: Unify(P(x, f(y)), P(a, f(b)))")
    p1 = Predicate('P', [Variable('x'), Predicate('f', [Variable('y')])])
    p2 = Predicate('P', [Constant('a'), Predicate('f', [Constant('b')])])
    result = unify(p1, p2)
    print_substitution(result)
    print()
    
    # Example 5: Failure case - occurs check
    print("Example 5: Unify(x, f(x)) - Occurs Check")
    x = Variable('x')
    fx = Predicate('f', [x])
    result = unify(x, fx)
    print_substitution(result)
    print()
    
    # Example 6: Failure case - different predicates
    print("Example 6: Unify(P(x), Q(x)) - Different Predicates")
    p1 = Predicate('P', [Variable('x')])
    p2 = Predicate('Q', [Variable('x')])
    result = unify(p1, p2)
    print_substitution(result)
    print()
    
    # Example 7: Failure case - different constants
    print("Example 7: Unify(John, Mary) - Different Constants")
    john = Constant('John')
    mary = Constant('Mary')
    result = unify(john, mary)
    print_substitution(result)

# Main program
if __name__ == "__main__":
    print("Choose mode:")
    print("1. Run predefined examples")
    print("2. Interactive mode (enter your own terms)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    print()
    
    if choice == '1':
        run_examples()
    elif choice == '2':
        run_interactive()
    else:
        print("Invalid choice. Running examples by default...\n")
        run_examples()
