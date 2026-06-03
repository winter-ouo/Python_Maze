import heapq
from collections import deque

def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# ==========================================
# 1. A* 尋路演算法
# ==========================================
def a_star_search(maze):
    start, end = maze.start_pos, maze.end_pos
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    open_set_hash = {start}
    closed_set = set()
    visited_order = []

    while open_set:
        current_f, current = heapq.heappop(open_set)
        open_set_hash.remove(current)
        if current != start and current != end:
            visited_order.append(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, visited_order

        closed_set.add(current)
        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (r + dr, c + dc)
            if not maze.is_valid_move(neighbor[0], neighbor[1]) or neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
    return None, visited_order

# ==========================================
# 2. BFS (廣度優先)
# ==========================================
def bfs_search(maze):
    start, end = maze.start_pos, maze.end_pos
    queue = deque([start])
    came_from = {}
    visited = {start}
    visited_order = []

    while queue:
        current = queue.popleft()
        if current != start and current != end:
            visited_order.append(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, visited_order

        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (r + dr, c + dc)
            if maze.is_valid_move(neighbor[0], neighbor[1]) and neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
    return None, visited_order

# ==========================================
# 3. DFS (深度優先搜尋)
# ==========================================
def dfs_search(maze):
    start, end = maze.start_pos, maze.end_pos
    stack = [start]
    came_from = {}
    visited = {start}
    visited_order = []

    while stack:
        current = stack.pop()  # 後進先出 (LIFO)
        if current != start and current != end:
            visited_order.append(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, visited_order

        r, c = current
        # 為了順序好看，故意反向加入 stack
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (r + dr, c + dc)
            if maze.is_valid_move(neighbor[0], neighbor[1]) and neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
    return None, visited_order