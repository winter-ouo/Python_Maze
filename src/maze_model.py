import numpy as np

class Maze:
    def __init__(self):
        # 寫死一個 7x7 的最簡迷宮 (0: 通道, 1: 牆壁)
        self.grid = np.array([
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ], dtype=np.uint8)
        
        self.height, self.width = self.grid.shape
        self.start_pos = (1, 1)  # 起點 (列, 行)
        self.end_pos = (5, 5)    # 終點 (列, 行)

    def is_valid_move(self, row, col):
        # 檢查是否越界或撞牆
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return False
        if self.grid[row, col] == 1:
            return False
        return True

    def move_player(self, current_pos, direction):
        # 接收 WASD 方向，計算新座標
        r, c = current_pos
        if direction == 'w': r -= 1
        elif direction == 's': r += 1
        elif direction == 'a': c -= 1
        elif direction == 'd': c += 1
        
        # 呼叫防禦檢查
        if self.is_valid_move(r, c):
            return (r, c)
        return current_pos  # 撞牆就留在原地