import cv2
import numpy as np

def draw_single(maze, player_pos):
    cell_size = 15  # 完美塞進筆電螢幕的精緻格子大小
    img_h = maze.height * cell_size
    img_w = maze.width * cell_size
    
    # 建立一個 BGR 彩色畫布
    canvas = np.zeros((img_h, img_w, 3), dtype=np.uint8)
    
    # 繪製迷宮本體
    for r in range(maze.height):
        for c in range(maze.width):
            y1, x1 = r * cell_size, c * cell_size
            y2, x2 = y1 + cell_size, x1 + cell_size
            
            if maze.grid[r, c] == 1:
                color = (50, 50, 50)  # 牆壁：深灰色
            else:
                color = (240, 240, 240)  # 通道：接近白色
                
            cv2.rectangle(canvas, (x1, y1), (x2, y2), color, -1)
            
    # --- 畫出終點 (紅色) ---
    # 精準讀取 Model 定義的 end_pos，並且 X 和 Y 在 OpenCV 裡正確對齊 (ex, ey)
    ey, ex = maze.end_pos
    padding = 2  # 固定內縮 2 像素
    cv2.rectangle(
        canvas, 
        (ex * cell_size + padding, ey * cell_size + padding), 
        ((ex + 1) * cell_size - padding, (ey + 1) * cell_size - padding), 
        (0, 0, 255), 
        -1
    )
    
    # --- 畫出玩家 (藍色圓球) ---
    py, px = player_pos
    center_x = px * cell_size + cell_size // 2
    center_y = py * cell_size + cell_size // 2
    radius = int(cell_size * 0.35)  # 黃金視覺比例
    
    cv2.circle(
        canvas, 
        (center_x, center_y), 
        radius, 
        (255, 0, 0), 
        -1, 
        lineType=cv2.LINE_AA  # 極致圓滑邊緣
    )
    
    return canvas

def update_display(canvas, delay=30):
    cv2.imshow("Python_maze MVP", canvas)
    key = cv2.waitKey(delay) & 0xFF
    return key