import heapq
from collections import deque
import time

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
# 2. BFS (廣度優先 / 洪水法)
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
        current = stack.pop()
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
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (r + dr, c + dc)
            if maze.is_valid_move(neighbor[0], neighbor[1]) and neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
    return None, visited_order

# ==========================================
# 4. 左手沿牆法 (Wall Follower)
# ==========================================
def wall_follower_search(maze):
    start, end = maze.start_pos, maze.end_pos
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    current_dir = 2 
    current_pos = start
    
    visited_order = []
    raw_path = [start] # 包含重複回頭路的原始足跡
    
    # 最大步數防禦
    max_steps = maze.width * maze.height * 2
    steps = 0
    
    while current_pos != end and steps < max_steps:
        steps += 1
        r, c = current_pos
        
        # 決定左手、前方、右手邊的方向索引
        left_dir = (current_dir - 1) % 4
        front_dir = current_dir
        right_dir = (current_dir + 1) % 4
        back_dir = (current_dir + 2) % 4
        
        chosen_dir = None
        
        # 優先級 1：嘗試往左手轉彎
        lr, lc = r + directions[left_dir][0], c + directions[left_dir][1]
        if maze.is_valid_move(lr, lc):
            chosen_dir = left_dir
        else:
            # 優先級 2：左邊撞牆，嘗試往前走
            fr, fc = r + directions[front_dir][0], c + directions[front_dir][1]
            if maze.is_valid_move(fr, fc):
                chosen_dir = front_dir
            else:
                # 優先級 3：左邊、前方都撞牆，嘗試右手轉彎
                rr, rc = r + directions[right_dir][0], c + directions[right_dir][1]
                if maze.is_valid_move(rr, rc):
                    chosen_dir = right_dir
                else:
                    # 優先級 4：三面撞牆（死胡同），只能向後轉原路倒車
                    chosen_dir = back_dir
                    
        # 執行移動
        dr, dc = directions[chosen_dir]
        current_pos = (r + dr, c + dc)
        current_dir = chosen_dir
        
        raw_path.append(current_pos)
        if current_pos != end:
            visited_order.append(current_pos)
            
    # 【路徑修剪】
    clean_path = []
    for node in raw_path:
        if node in clean_path:
            idx = clean_path.index(node)
            clean_path = clean_path[:idx + 1] # 砍掉死胡同回頭路
        else:
            clean_path.append(node)
            
    return clean_path, visited_order