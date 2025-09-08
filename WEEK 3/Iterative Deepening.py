moves = {'U': -3, 'D': 3, 'L': -1, 'R': 1}

print ("Saahya K S")

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

def depth_limited_dfs(state, goal, limit, visited):
    if state == goal:
        return [state]
    if limit == 0:
        return None
    visited.add(state)
    for nxt in neighbors(state):
        if nxt not in visited:
            path = depth_limited_dfs(nxt, goal, limit-1, visited)
            if path:
                return [state] + path
    visited.remove(state)
    return None

def iddfs(start, goal, max_depth=30):
    for depth in range(max_depth+1):
        visited = set()
        path = depth_limited_dfs(start, goal, depth, visited)
        if path:
            return path
    return None

if __name__ == "__main__":
    init = tuple(map(int, input("Enter initial state (9 numbers, 0 for blank): ").split()))
    goal = tuple(map(int, input("Enter goal state (9 numbers, 0 for blank): ").split()))
    solution = iddfs(init, goal, max_depth=30)
    if solution:
        for i, s in enumerate(solution):
            print("Cost:", i)
            print(s[0:3])
            print(s[3:6])
            print(s[6:9])
            print()
    else:
        print("No solution within depth limit.")
