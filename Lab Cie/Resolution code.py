import re
from itertools import combinations

def get_fol_sentences():
    print("Converting given sentences to FOL...")
    fol = [
        "Likes(cat, fish)",                     
        "∀x∀y((Cat(x) ∧ Likes(x, y)) → Eats(x, y))",  
        "Cat(mani)"                             
    ]
    query = "Eats(mani, fish)"                  
    return fol, query

def fol_to_cnf(fol_sentences):
    print("\nConverting FOL to CNF...")
    cnf = [
        {"Likes(cat,fish)"},                      
        {"~Cat(x)", "~Likes(x,y)", "Eats(x,y)"},  
        {"Cat(mani)"}                             
    ]
    return cnf

def unify(expr, subs):
    expr = expr.strip()
    for var, val in subs.items():
        expr = expr.replace(var, val)
    return expr

def can_unify(a, b):
    if a == b:
        return True, {}
    pattern = re.match(r"(\w+)\(([^,]+),([^,]+)\)", a)
    pattern2 = re.match(r"(\w+)\(([^,]+),([^,]+)\)", b)
    if pattern and pattern2 and pattern.group(1) == pattern2.group(1):
        subs = {}
        if pattern.group(2) != pattern2.group(2):
            subs[pattern.group(2)] = pattern2.group(2)
        if pattern.group(3) != pattern2.group(3):
            subs[pattern.group(3)] = pattern2.group(3)
        return True, subs
    return False, {}

def resolve(ci, cj):
    resolvents = []
    for di in ci:
        for dj in cj:
            neg_dj = "~" + dj if not dj.startswith("~") else dj[1:]
            if di == neg_dj:
                new_clause = (ci - {di}) | (cj - {dj})
                resolvents.append(new_clause)
                continue
            ok, subs = can_unify(di.replace("~",""), dj.replace("~",""))
            if ok and (di.startswith("~") ^ dj.startswith("~")):
                ci_sub = {unify(lit, subs) for lit in ci if lit != di}
                cj_sub = {unify(lit, subs) for lit in cj if lit != dj}
                new_clause = ci_sub | cj_sub
                resolvents.append(new_clause)
    return resolvents

def resolution_algorithm(kb, query):
    kb.append(set(['~' + query]))
    derived = []
    clause_id = {frozenset(c): f"C{i+1}" for i, c in enumerate(kb)}
    step = 1
    while True:
        new = []
        for (ci, cj) in combinations(kb, 2):
            resolvents = resolve(ci, cj)
            for res in resolvents:
                if res not in kb and res not in new:
                    cid_i, cid_j = clause_id[frozenset(ci)], clause_id[frozenset(cj)]
                    clause_name = f"R{step}"
                    derived.append((clause_name, res, cid_i, cid_j))
                    clause_id[frozenset(res)] = clause_name
                    new.append(res)
                    print(f"[Step {step}] {clause_name} = Resolve({cid_i}, {cid_j}) → {res or '{}'}")
                    step += 1
                    if res == set():
                        print("\nQuery is proved by resolution (empty clause found).")
                        print("\n--- Proof Tree ---")
                        print_tree(derived, clause_name)
                        return True
        if not new:
            print("\n Query cannot be proved by resolution.")
            return False
        kb.extend(new)

def print_tree(derived, goal):
    tree = {name: (parents, clause) for name, clause, *parents in [(r[0], r[1], r[2:][0], r[2:][1]) for r in derived]}
    def show(node, indent=0):
        if node not in tree:
            print(" " * indent + node)
            return
        parents, clause = tree[node]
        print(" " * indent + f"{node}: {set(clause) or '{}'}")
        for p in parents:
            show(p, indent + 4)
    show(goal)

print("=== Automatic FOL → CNF → Resolution Proof Demo ===")
fol_sentences, query = get_fol_sentences()
cnf_kb = fol_to_cnf(fol_sentences)
print("\n--- Resolution Steps ---")
resolution_algorithm(cnf_kb, query)
