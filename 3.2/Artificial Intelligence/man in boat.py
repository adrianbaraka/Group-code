from collections import deque

def is_valid(state):
    man, leopard, goat, grass = state
    
    if man != goat and (leopard == goat or goat == grass):
        return False
    
    return True

def get_next_states(state):
    man, leopard, goat, grass = state
    next_states = []
    
    new_man_pos = 'Right' if man == 'Left' else 'Left'
    
    # Move man alone
    new_state = list(state)
    new_state[0] = new_man_pos
    new_state = tuple(new_state)
    if is_valid(new_state):
        next_states.append(new_state)
    
    # Move man with leopard
    if leopard == man:
        new_state = list(state)
        new_state[0] = new_man_pos
        new_state[1] = new_man_pos
        new_state = tuple(new_state)
        if is_valid(new_state):
            next_states.append(new_state)
    
    # Move man with goat
    if goat == man:
        new_state = list(state)
        new_state[0] = new_man_pos
        new_state[2] = new_man_pos
        new_state = tuple(new_state)
        if is_valid(new_state):
            next_states.append(new_state)
    
    # Move man with grass
    if grass == man:
        new_state = list(state)
        new_state[0] = new_man_pos
        new_state[3] = new_man_pos
        new_state = tuple(new_state)
        if is_valid(new_state):
            next_states.append(new_state)
    
    return next_states

def bfs(initial_state, goal_state):
    queue = deque()
    queue.append((initial_state, []))
    
    visited = set()
    visited.add(initial_state)
    
    while queue:
        current_state, path = queue.popleft()
        
        if current_state == goal_state:
            return path + [current_state]
        
        for next_state in get_next_states(current_state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [current_state]))
    
    return None

def dfs(initial_state, goal_state):
    stack = [(initial_state, [])]
    
    visited = set()
    visited.add(initial_state)
    
    while stack:
        current_state, path = stack.pop()
        
        if current_state == goal_state:
            return path + [current_state]
        
        for next_state in get_next_states(current_state):
            if next_state not in visited:
                visited.add(next_state)
                stack.append((next_state, path + [current_state]))
    
    return None

# Define initial and goal states
initial_state = ('Left', 'Left', 'Left', 'Left')
goal_state = ('Right', 'Right', 'Right', 'Right')

# Find solution using BFS

bfs_path = bfs(initial_state, goal_state)
if bfs_path:
    print("BFS Solution Path:")
    print("man   | Leopard  | Goat  | Grass")
    for state in bfs_path:
        print(state)
else:
    print("BFS found no solution.")

# Find solution using DFS
dfs_path = dfs(initial_state, goal_state)
if dfs_path:
    print("\nDFS Solution Path:")
    print("man   | Leopard  | Goat | Grass")
    for state in dfs_path:
        print(state)
else:
    print("DFS found no solution.")