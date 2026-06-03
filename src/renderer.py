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
            
    # 2.畫出 AI 探索過的足跡 (淡黃色)
    if visited:
        for vr, vc in visited:
            y1, x1 = vr * cell_size, vc * cell_size
            y2, x2 = y1 + cell_size, x1 + cell_size
            # 在通道上覆蓋一層淡黃色
            cv2.rectangle(canvas, (x1 + 1, y1 + 1), (x2 - 1, y2 - 1), (200, 240, 255), -1)

    # 3.畫出 A* 算出的正確路徑 (螢光綠)
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
    
    cv2.circle(
        canvas, 
        (center_x, center_y), 
        radius, 
        (255, 0, 0), 
        -1, 
        lineType=cv2.LINE_AA
    )
    
    return canvas