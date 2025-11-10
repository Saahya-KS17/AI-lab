import heapq

def uniform_cost_search(graph, start, goal):
    # Priority queue: (cost, node, path)
    pq = [(0, start, [start])]
    visited = set()

    while pq:
        cost, node, path = heapq.heappop(pq)

        # If node already visited, skip
        if node in visited:
            continue
        visited.add(node)

        # Goal test
        if node == goal:
            return cost, path

        # Explore neighbors
        for neighbor, edge_cost in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + edge_cost, neighbor, path + [neighbor]))

    return float("inf"), []  # No path found

# ------------------- USER INPUT -------------------
graph = {}

# Take number of edges
n = int(input("Enter number of edges: "))

print("Enter edges in the format: node1 node2 cost")
for _ in range(n):
    u, v, c = input().split()
    c = int(c)

    # Add edge (for undirected or directed graph)
    if u not in graph:
        graph[u] = []
    graph[u].append((v, c))

# If you want to make it undirected, uncomment the next 3 lines:
#    if v not in graph:
#        graph[v] = []
#    graph[v].append((u, c))

start = input("Enter start node: ")
goal = input("Enter goal node: ")

# ------------------- RUN UCS -------------------
cost, path = uniform_cost_search(graph, start, goal)

if path:
    print(f"\nLeast-cost path: {' -> '.join(path)}")
    print(f"Total cost: {cost}")
else:
    print("\nNo path found!")
