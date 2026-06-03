import numpy as np
import random
from maze_model import Maze

def generate_maze(w, h, openness: float = 0.0, seed: int = None) -> Maze:
    """
    隨機 Prim (Randomized Prim's) 迷宮生成器
    生成特徵：分支極度破碎、短路徑多、毫無方向規律，挑戰性極高！
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # 1. 初始化資料模型 (預設全都是牆壁 1)
    maze = Maze(w, h)
    maze.grid.fill(1)

    start_pos = maze.start_pos
    end_pos = maze.end_pos

    # 2. 將起點打通為通道 (0)
    maze.grid[start_pos[0], start_pos[1]] = 0

    # 3. 初始化牆壁清單 (Wall List)
    walls = []
    
    def add_walls(r, c):
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 < nr < h - 1 and 0 < nc < w - 1:
                if maze.grid[nr, nc] == 1:
                    wr = r + dr // 2
                    wc = c + dc // 2
                    walls.append((wr, wc, nr, nc))

    # 將起點周圍的牆壁加入清單
    add_walls(start_pos[0], start_pos[1])

    # 4. Prim 核心隨機啃食迴圈
    while walls:
        wall_idx = random.randint(0, len(walls) - 1)
        wr, wc, nr, nc = walls.pop(wall_idx)

        if maze.grid[nr, nc] == 1:
            maze.grid[wr, wc] = 0
            maze.grid[nr, nc] = 0
            add_walls(nr, nc)

    # 5. 保障機制：強制挖通資料模型指定的終點格子
    maze.grid[end_pos[0], end_pos[1]] = 0

    return maze