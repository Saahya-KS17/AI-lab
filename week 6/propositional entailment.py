import itertools

def eval_expr(expr: str, model: dict) -> bool:
    e = expr
    for sym, val in model.items():
        e = e.replace(sym, str(val))
    e = e.replace("&", " and ")
    e = e.replace("|", " or ")
    e = e.replace("~", " not ")
    return eval(e)

def pl_true(expr: str, model: dict) -> bool:
    return eval_expr(expr, model)

def tt_check_all(KB: str, alpha: str, symbols: list, model: dict) -> bool:
    if not symbols:
        if pl_true(KB, model):
            return pl_true(alpha, model)
        else:
            return True
    P, rest = symbols[0], symbols[1:]
    model_true = model.copy()
    model_true[P] = True
    model_false = model.copy()
    model_false[P] = False
    return (tt_check_all(KB, alpha, rest, model_true) and
            tt_check_all(KB, alpha, rest, model_false))

def tt_entails(KB: str, alpha: str, symbols: list) -> bool:
    return tt_check_all(KB, alpha, symbols, {})

def print_truth_table(KB: str, alpha: str, symbols: list):
    print("Truth Table:")
    header = symbols + [KB, alpha]
    print(" | ".join(f"{h:^5}" for h in header))
    print("-" * (7 * len(header)))

    for values in itertools.product([False, True], repeat=len(symbols)):
        model = {sym: val for sym, val in zip(symbols, values)}
        kb_val = pl_true(KB, model)
        alpha_val = pl_true(alpha, model)
        row = list(values) + [kb_val, alpha_val]
        print(" | ".join(f"{str(x):^5}" for x in row))

if __name__ == "__main__":
    KB = "(A | C) & (B | ~C)" 
    alpha = "(A | B)"         
    symbols = ["A", "B", "C"]

    print_truth_table(KB, alpha, symbols)
    result = tt_entails(KB, alpha, symbols)
    print("\nKB entails alpha?", "YES" if result else "NO")
