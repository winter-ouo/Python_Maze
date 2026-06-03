import cv2
import numpy as np

def draw_single(maze, player_pos, path=None, visited=None):
    cell_size = 15  
    img_h = maze.height * cell_size
    img_w = maze.width * cell_size
    
    canvas = np.zeros((img_h, img_w, 3), dtype=np.uint8)
    
    # 繪製迷宮本體
    for r in range(maze.height):
        for c in range(maze.width):
            y1, x1 = r * cell_size, c * cell_size
            y2, x2 = y1 + cell_size, x1 + cell_size
            if maze.grid[r, c] == 1:
                color = (50, 50, 50)
            else:
                color = (240, 240, 240)
            cv2.rectangle(canvas, (x1, y1), (x2, y2), color, -1)
            
    # 畫出 AI 探索過的足跡 (淡黃色)
    if visited:
        for vr, vc in visited:
            y1, x1 = vr * cell_size, vc * cell_size
            y2, x2 = y1 + cell_size, x1 + cell_size
            cv2.rectangle(canvas, (x1 + 1, y1 + 1), (x2 - 1, y2 - 1), (200, 240, 255), -1)

    # 畫出 最終算出的正確路徑 (螢光綠)
    if path:
        for pr, pc in path:
            if (pr, pc) != maze.start_pos and (pr, pc) != maze.end_pos:
                y1, x1 = pr * cell_size, pc * cell_size
                y2, x2 = y1 + cell_size, x1 + cell_size
                cv2.rectangle(canvas, (x1 + 1, y1 + 1), (x2 - 1, y2 - 1), (50, 220, 50), -1)

    # 畫出終點 (紅色)
    ey, ex = maze.end_pos
    padding = 2  
    cv2.rectangle(canvas, (ex * cell_size + padding, ey * cell_size + padding), ((ex + 1) * cell_size - padding, (ey + 1) * cell_size - padding), (0, 0, 255), -1)
    
    # 畫出玩家 (藍色圓球)
    py, px = player_pos
    center_x = px * cell_size + cell_size // 2
    center_y = py * cell_size + cell_size // 2
    radius = int(cell_size * 0.35)
    cv2.circle(canvas, (center_x, center_y), radius, (255, 0, 0), -1, lineType=cv2.LINE_AA)
    
    return canvas

def draw_sidebar(height, current_algo, stats):
    width = 250
    sidebar = np.zeros((height, width, 3), dtype=np.uint8)
    sidebar[:] = (35, 30, 30)
    
    cv2.line(sidebar, (0, 0), (0, height), (70, 70, 70), 2)
    
    # 標題區
    cv2.putText(sidebar, "MAZE GAME", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.line(sidebar, (20, 55), (230, 55), (100, 100, 100), 1)
    
    # 目前動態數據
    algo_text = f"Active: {current_algo}"
    cv2.putText(sidebar, algo_text, (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 255, 50), 1)
    cv2.putText(sidebar, f"Explored: {stats['explored']} cells", (20, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
    cv2.putText(sidebar, f"Path Length: {stats['path_len']} steps", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
    
    cv2.line(sidebar, (20, 165), (230, 165), (100, 100, 100), 1)
    
    # ─── 【全新升級】各自獨立計時看板 ───
    cv2.putText(sidebar, "PERFORMANCE TIME:", (20, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # A* 時間 (未執行顯示 ...，執行後顯示毫秒)
    a_star_str = f"A* Finish Time : {stats['a_star_time']:.2f} ms" if stats['a_star_time'] > 0 else "A* Finish Time : ..."
    cv2.putText(sidebar, a_star_str, (20, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 200, 255), 1)
    
    # BFS 時間
    bfs_str = f"BFS Finish Time: {stats['bfs_time']:.2f} ms" if stats['bfs_time'] > 0 else "BFS Finish Time: ..."
    cv2.putText(sidebar, bfs_str, (20, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 255, 200), 1)
    
    # DFS 時間
    dfs_str = f"DFS Finish Time: {stats['dfs_time']:.2f} ms" if stats['dfs_time'] > 0 else "DFS Finish Time: ..."
    cv2.putText(sidebar, dfs_str, (20, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 100, 255), 1)
    
    # Player 手動時間 (以秒為單位)
    player_str = f"player Finish Time : {stats['player_time']:.1f} s" if stats['player_time'] > 0 else "player Finish Time : ..."
    cv2.putText(sidebar, player_str, (20, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 150, 100), 1)
    
    cv2.line(sidebar, (20, 320), (230, 320), (100, 100, 100), 1)
    
    # 3個演算法按鈕
    cv2.putText(sidebar, "SELECT ALGORITHM:", (20, 345), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # A*按鈕 
    cv2.rectangle(sidebar, (20, 365), (230, 405), (80, 60, 50), -1)
    cv2.rectangle(sidebar, (20, 365), (230, 405), (150, 150, 150), 1)
    cv2.putText(sidebar, "[1] A* Search", (45, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # BFS按鈕
    cv2.rectangle(sidebar, (20, 425), (230, 465), (80, 60, 50), -1)
    cv2.rectangle(sidebar, (20, 425), (230, 465), (150, 150, 150), 1)
    cv2.putText(sidebar, "[2] BFS / Flood", (45, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # DFS按鈕
    cv2.rectangle(sidebar, (20, 485), (230, 525), (80, 60, 50), -1)
    cv2.rectangle(sidebar, (20, 485), (230, 525), (150, 150, 150), 1)
    cv2.putText(sidebar, "[3] DFS (Snake)", (45, 510), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return sidebar