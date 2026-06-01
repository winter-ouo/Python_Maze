import cv2
import numpy as np

def draw_single(maze, player_pos):
    cell_size = 40  # 每個格子 40x40 像素
    img_h = maze.height * cell_size
    img_w = maze.width * cell_size
    
    # 建立一個彩色畫布
    canvas = np.zeros((img_h, img_w, 3), dtype=np.uint8)
    
    for r in range(maze.height):
        for c in range(maze.width):
            # 計算格子的左上角與右下角座標
            y1, x1 = r * cell_size, c * cell_size
            y2, x2 = y1 + cell_size, x1 + cell_size
            
            if maze.grid[r, c] == 1:
                color = (50, 50, 50)  # 牆壁：深灰色
            else:
                color = (240, 240, 240)  # 通道：接近白色
                
            cv2.rectangle(canvas, (x1, y1), (x2, y2), color, -1)
            
    # 畫出終點 (紅色)
    ey, ex = maze.end_pos
    cv2.rectangle(canvas, (ex*cell_size+5, ey*cell_size+5), ((ex+1)*cell_size-5, (ey+1)*cell_size-5), (0, 0, 255), -1)
    
    # 畫出玩家 (藍色)
    py, px = player_pos
    cv2.circle(canvas, (px * cell_size + cell_size//2, py * cell_size + cell_size//2), cell_size//3, (255, 0, 0), -1)
    
    return canvas

def update_display(canvas, delay=30):
    cv2.imshow("Python_maze MVP", canvas)
    # 讀取鍵盤輸入
    key = cv2.waitKey(delay) & 0xFF
    return key