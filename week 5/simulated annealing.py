import random
import math

def calculate_attacks(state):
    """Heuristic: number of attacking queen pairs."""
    attacks = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

def random_neighbor(state):
    """Generate a random neighbor by moving one queen."""
    n = len(state)
    neighbor = list(state)
    col = random.randint(0, n - 1)
    row = random.randint(0, n - 1)
    while row == state[col]: 
        row = random.randint(0, n - 1)
    neighbor[col] = row
    return neighbor

def simulated_annealing(n, max_steps=10000, initial_temp=100, cooling_rate=0.99):
    """Solve N-Queens using simulated annealing."""
    current = [random.randint(0, n - 1) for _ in range(n)]
    current_attacks = calculate_attacks(current)

    temperature = initial_temp

    for step in range(max_steps):
        if current_attacks == 0:
            return current, current_attacks 

        neighbor = random_neighbor(current)
        neighbor_attacks = calculate_attacks(neighbor)

        delta_e = current_attacks - neighbor_attacks

        if delta_e > 0 or random.random() < math.exp(delta_e / temperature):
            current, current_attacks = neighbor, neighbor_attacks

        temperature *= cooling_rate
        if temperature < 1e-6:
            break

    return current, current_attacks

if __name__ == "__main__":
    N = 8
    solution, attacks = simulated_annealing(N)
    print("Final State:", solution)
    print("Attacking pairs:", attacks)
    if attacks == 0:
        print("Found a solution!")
    else:
        print("Did not find solution (stuck).")
