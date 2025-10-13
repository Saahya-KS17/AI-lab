from collections import deque

def print_table(state):
    for i in range(3):
        row = []
        for val in state[3*i:3*i+3]:
            if val == 0:
                row.append(' ')  # show blank as space
            else:
                row.append(str(val))
        print(' '.join(row))
    print()

def get_neighbors(state):
    neighbors = []
    zero_pos = state.index(0)
    row, col = zero_pos // 3, zero_pos % 3

    moves = [(-1,0),(1,0),(0,-1),(0,1)]  # up, down, left, right

    for dr, dc in moves:
        new_r, new_c = row + dr, col + dc
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            new_pos = new_r * 3 + new_c
            new_state = list(state)
            new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
            neighbors.append(tuple(new_state))
    return neighbors

def bfs(start, goal):
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            # Found goal, reconstruct path
            path = []
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, visited, queue

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None, visited, queue  # no solution found

def input_state(name):
    print(f"Enter the {name} state row by row (3 numbers each row, space separated). Use 0 or leave blank for empty cell:")
    vals = []
    for i in range(3):
        while True:
            row_input = input(f"Row {i+1}: ").strip().split()
            # Allow blank input for zero
            if len(row_input) != 3:
                print("Please enter exactly 3 numbers or blanks.")
                continue
            try:
                row = []
                for v in row_input:
                    if v == '' or v == '0':
                        row.append(0)
                    else:
                        val = int(v)
                        if val < 1 or val > 8:
                            raise ValueError
                        row.append(val)
                vals.extend(row)
                break
            except:
                print("Invalid input. Use numbers 1-8 or 0/blank for empty.")
    if set(vals) != set(range(9)):
        print("Invalid state: numbers must be from 0 to 8 without repetition.")
        return input_state(name)
    return tuple(vals)

# Input from user
start_state = input_state("start")
goal_state = input_state("goal")

# Run BFS
path, visited, remaining = bfs(start_state, goal_state)

print(f"\nTotal states visited: {len(visited)}\n")

if path:
    print("Final path length:", len(path))
    print("Final state:")
    print_table(path[-1])
else:
    print("No solution found.")

print("Remaining states in queue (positions of zero):")
for state in remaining:
    print(state.index(0), end=" ")
