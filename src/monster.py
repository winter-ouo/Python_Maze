import time


class Monster:
    def __init__(self):
        self.pos = None
        self.spawned = False

        # 怪物巡邏路線
        self.path = []

        # 目前走到哪個點
        self.idx = 0

        # 1=往下
        # -1=往上
        self.direction = 1

        self.spawn_time = None

    # =========================
    # 生成怪物
    # =========================
    def spawn(self, path):

        if not path:
            return

        vertical_path = []

        # 找出同一欄位的連續點
        for i in range(1, len(path)):

            r0, c0 = path[i - 1]
            r1, c1 = path[i]

            if c0 == c1:
                vertical_path.append((r0, c0))
                vertical_path.append((r1, c1))

        # 如果沒有垂直路段
        if len(vertical_path) < 2:
            vertical_path = path

        # 去除重複
        vertical_path = list(dict.fromkeys(vertical_path))

        self.path = vertical_path

        # 從中間生成
        self.idx = len(self.path) // 2

        self.pos = self.path[self.idx]

        self.spawned = True

        self.spawn_time = time.time()

    # =========================
    # 上下巡邏
    # =========================
    def update(self):

        if not self.spawned:
            return

        if len(self.path) <= 1:
            return

        self.idx += self.direction

        # 到底反彈
        if self.idx >= len(self.path):

            self.idx = len(self.path) - 2

            self.direction = -1

        # 到頂反彈
        elif self.idx < 0:

            self.idx = 1

            self.direction = 1

        self.pos = self.path[self.idx]

    # =========================
    # 碰撞判定
    # =========================
    def check_collision(self, player_pos):

        if not self.spawned:
            return False

        return self.pos == player_pos

    # =========================
    # 重置
    # =========================
    def reset(self):

        self.pos = None
        self.spawned = False
        self.path = []
        self.idx = 0
        self.direction = 1
        self.spawn_time = None
