import numpy as np

class Maze:
    def __init__(self, width=31, height=31):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self.start_pos = (1, 1)
        self.end_pos = (height - 2, width - 2)

    def is_valid_move(self, row, col):
        # 檢查是否越界或撞牆
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return False
        if self.grid[row, col] == 1:
            return False
        return True

    def move_player(self, current_pos, direction):
        r, c = current_pos
        if direction == 'w': r -= 1
        elif direction == 's': r += 1
        elif direction == 'a': c -= 1
        elif direction == 'd': c += 1
        
        if self.is_valid_move(r, c):
            return (r, c)
        return current_pos