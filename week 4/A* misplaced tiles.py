import heapq

print("Saahya K S")

moves = {'U': -3, 'D': 3, 'L': -1, 'R': 1}

def is_valid(blank, move):
    if move == 'L' and blank % 3 == 0: return False
    if move == 'R' and blank % 3 == 2: return False
    if move == 'U' and blank < 3: return False
    if move == 'D' and blank > 5: return False
    return True

def neighbors(state):
    blank = state.index(0)
    result = []
    for off in moves.values():
        if is_valid(blank, [k for k,v in moves.items() if v == off][0]):
            new_state = list(state)
            swap = blank + off
            new_state[blank], new_state[swap] = new_state[swap], new_state[blank]
            result.append(tuple(new_state))
    return result

def h_misplaced(state, goal):
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != goal[i])

def astar(start, goal):
    open_heap = []
    heapq.heappush(open_heap, (h_misplaced(start, goal), 0, start, [start]))
    visited = set()
    while open_heap:
        f, g, state, path = heapq.heappop(open_heap)
        if state == goal:
            return path
        if state in visited:
            continue
        visited.add(state)
        for nxt in neighbors(state):
            if nxt not in visited:
                new_g = g + 1
                new_f = new_g + h_misplaced(nxt, goal)
                heapq.heappush(open_heap, (new_f, new_g, nxt, path + [nxt]))
    return None

if __name__ == "__main__":
    init = tuple(map(int, input("Enter initial state (9 numbers, 0 for blank): ").split()))
    goal = tuple(map(int, input("Enter goal state (9 numbers, 0 for blank): ").split()))
    solution = astar(init, goal)
    if solution:
        for i, s in enumerate(solution):
            print("Cost:", i)
            print(s[0:3])
            print(s[3:6])
            print(s[6:9])
            print()
    else:
        print("No solution found.")
