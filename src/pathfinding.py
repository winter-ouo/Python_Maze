import heapq

def heuristic(p1, p2):
    """計算兩點之間的曼哈頓距離"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def a_star_search(maze):
    """
    A* 尋路演算法
    回傳值：
        path: 從起點到終點的座標串列 [(r1, c1), (r2, c2), ...]
        visited_order: 演算法『探索格子』的先後順序（用來做酷炫的動態尋路特效！）
    """
    start = maze.start_pos
    end = maze.end_pos

    # 優先佇列（Min-Heap），儲存結構為: (f_score, (r, c))
    # 這樣每次 pop 都能自動拿到 F 值最小的節點
    open_set = []
    heapq.heappush(open_set, (0, start))

    # 紀錄每個格子是從哪一個前置格子走過來的，用於最後還原路徑
    came_from = {}

    # G_score: 起點到該格子的實際代價，未紀錄的預設為無限大
    g_score = {start: 0}
    
    # F_score: G_score + Heuristic 預估總代價
    f_score = {start: heuristic(start, end)}

    # 紀錄被丟進 Open Set 準備探索的格子集合，方便快速查詢
    open_set_hash = {start}
    
    # 紀錄已經被完全探索完畢的格子（Closed Set）
    closed_set = set()

    # 用來紀錄演算法依序走訪了哪些格子，展示時可以畫出 AI 的思維擴散過程
    visited_order = []

    while open_set:
        # 彈出當前 F 值最小的格子
        current_f, current = heapq.heappop(open_set)
        open_set_hash.remove(current)
        
        # 只要不是起點和終點，就記錄進走訪順序中
        if current != start and current != end:
            visited_order.append(current)

        # 成功抵達終點！開始回溯完整路徑
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()  # 翻轉過來變成從起點到終點
            return path, visited_order

        closed_set.add(current)
        r, c = current

        # 檢查上下左右距離為 1 的鄰居格子
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            neighbor = (r + dr, c + dc)

            # 利用 Model 的防禦機制檢查是否為合法通道
            if not maze.is_valid_move(neighbor[0], neighbor[1]):
                continue
                
            if neighbor in closed_set:
                continue

            # 迷宮每走一格代價都是 1
            tentative_g_score = g_score[current] + 1

            # 如果這條路的 G 值比之前紀錄的更短，代表發現了更好的走法
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    return None, visited_order  # 萬一沒找到路（雖然 Prim 必有解）