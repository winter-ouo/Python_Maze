import cv2
import numpy as np

def draw_single(maze, player_pos, path=None, visited=None):
    cell_size = 15  
    img_h = maze.height * cell_size
    img_w = maze.width * cell_size
    
    canvas = np.zeros((img_h, img_w, 3), dtype=np.uint8)
    
    # 1. 繪製迷宮本體
    for r in range(maze.height):
        for c in range(maze.width):
            y1, x1 = r * cell_size, c * cell_size
            y2, x2 = y1 + cell_size, x1 + cell_size
            
            if maze.grid[r, c] == 1:
                color = (50, 50, 50)  # 牆壁：深灰色
            else:
                color = (240, 240, 240)  # 通道：白色
                
            cv2.rectangle(canvas, (x1, y1), (x2, y2), color, -1)
            
    # 2. 畫出 AI 探索過的足跡 (淡黃色)
    if visited:
        for vr, vc in visited:
            y1, x1 = vr * cell_size, vc * cell_size
            y2, x2 = y1 + cell_size, x1 + cell_size
            cv2.rectangle(canvas, (x1 + 1, y1 + 1), (x2 - 1, y2 - 1), (200, 240, 255), -1)

    # 3. 畫出 A* 最終算出的正確路徑 (螢光綠)
    if path:
        for pr, pc in path:
            if (pr, pc) != maze.start_pos and (pr, pc) != maze.end_pos:
                y1, x1 = pr * cell_size, pc * cell_size
                y2, x2 = y1 + cell_size, x1 + cell_size
                cv2.rectangle(canvas, (x1 + 1, y1 + 1), (x2 - 1, y2 - 1), (50, 220, 50), -1)

    # 4. 畫出終點 (紅色)
    ey, ex = maze.end_pos
    padding = 2  
    cv2.rectangle(
        canvas, 
        (ex * cell_size + padding, ey * cell_size + padding), 
        ((ex + 1) * cell_size - padding, (ey + 1) * cell_size - padding), 
        (0, 0, 255), 
        -1
    )
    
    # 5. 畫出玩家 (藍色圓球)
    py, px = player_pos
    center_x = px * cell_size + cell_size // 2
    center_y = py * cell_size + cell_size // 2
    radius = int(cell_size * 0.35)
    
    cv2.circle(canvas, (center_x, center_y), radius, (255, 0, 0), -1, lineType=cv2.LINE_AA)
    
    return canvas

def draw_sidebar(height, current_algo, stats):
    """
    全新功能：繪製右側的 250 像素 UI 側欄面版
    """
    width = 250
    # 側欄底色
    sidebar = np.zeros((height, width, 3), dtype=np.uint8)
    sidebar[:] = (35, 30, 30)
    
    cv2.line(sidebar, (0, 0), (0, height), (70, 70, 70), 2)
    
    # 標題區
    cv2.putText(sidebar, "MAZE AI PANEL", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.line(sidebar, (20, 55), (230, 55), (100, 100, 100), 1)
    
    # 目前狀態
    algo_text = f"Active: {current_algo}"
    cv2.putText(sidebar, algo_text, (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 255, 50), 1)
    
    # 數據統計
    cv2.putText(sidebar, f"Explored: {stats['explored']} cells", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
    cv2.putText(sidebar, f"Path Length: {stats['path_len']} steps", (20, 145), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
    
    cv2.line(sidebar, (20, 175), (230, 175), (100, 100, 100), 1)
    cv2.putText(sidebar, "SELECT ALGORITHM:", (20, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # 繪製三個演算法虛擬按鈕 (按鈕寬度: 210, 高度: 40)
    # 按鈕 1: A*
    cv2.rectangle(sidebar, (20, 230), (230, 270), (80, 60, 50), -1)
    cv2.rectangle(sidebar, (20, 230), (230, 270), (150, 150, 150), 1)
    cv2.putText(sidebar, "[1] A* Search", (45, 255), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # 按鈕 2: BFS
    cv2.rectangle(sidebar, (20, 290), (230, 330), (80, 60, 50), -1)
    cv2.rectangle(sidebar, (20, 290), (230, 330), (150, 150, 150), 1)
    cv2.putText(sidebar, "[2] BFS", (45, 315), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # 按鈕 3: DFS
    cv2.rectangle(sidebar, (20, 350), (230, 390), (80, 60, 50), -1)
    cv2.rectangle(sidebar, (20, 350), (230, 390), (150, 150, 150), 1)
    cv2.putText(sidebar, "[3] DFS", (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # 操作說明
    cv2.line(sidebar, (20, 420), (230, 420), (100, 100, 100), 1)
    cv2.putText(sidebar, "CONTROLS:", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(sidebar, "- Click Sidebar Buttons", (20, 480), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
    cv2.putText(sidebar, "- Or Press 1, 2, 3 on Keyboard", (20, 505), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
    cv2.putText(sidebar, "- WASD / Arrows to Move", (20, 530), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
    cv2.putText(sidebar, "- ESC to Quit", (20, 555), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
    
    return sidebar