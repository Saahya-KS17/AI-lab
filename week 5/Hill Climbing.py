import random

def calculate_attacks(state):
    """Heuristic: count number of attacking pairs."""
    attacks = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

def print_board(state):
    """Print board row by row with '_' for empty and 'Q' for queen."""
    n = len(state)
    for row in range(n):
        print(' '.join('Q' if state[col] == row else '_' for col in range(n)))
    print()

def get_neighbors(state):
    """Generate all possible neighbor states."""
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if row != state[col]:
                neighbor = list(state)
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors

def hill_climbing_verbose(n, initial_state=None, max_iter=1000):
    if initial_state is None:
        current = [random.randint(0, n - 1) for _ in range(n)]
    else:
        current = list(initial_state)

    current_attacks = calculate_attacks(current)
    step = 0

    print(f"\nInitial state (Step {step}): cost = {current_attacks}")
    print_board(current)

    while step < max_iter:
        neighbors = get_neighbors(current)
        if not neighbors:
            break

        best = min(neighbors, key=calculate_attacks)
        best_attacks = calculate_attacks(best)

        if best_attacks >= current_attacks:
            print("\nNo better neighbor found. Local optimum reached.")
            break

        step += 1
        current, current_attacks = best, best_attacks

        print(f"Step {step}: cost = {current_attacks}")
        print_board(current)

        if current_attacks == 0:
            print("Found a solution!\n")
            break

    print("Final state (array form):", current)
    print("Final attacking pairs (cost):", current_attacks)

if __name__ == "__main__":
    N = int(input("Enter N (number of queens): ").strip())
    s = input("Enter initial state as N space-separated integers (rows 0..N-1), or press Enter for random initial state:\n").strip()
    initial = None
    if s:
        parts = list(map(int, s.split()))
        if len(parts) == N and all(0 <= x < N for x in parts):
            initial = parts
        else:
            print("Invalid initial state, using random.")
    hill_climbing_verbose(N, initial_state=initial)
