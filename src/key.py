# key.py
import random
import pathfinding  # 引入尋路演算法來計算必經之路

KEY_MARK = 2  # 2 代表黃色鑰匙
WALKWAY = 0

# 核心狀態變數
has_key = False


def spawn_key_smart(maze_obj):
    """
    聰明地隨機生成鑰匙：確保鑰匙不在起點到終點的必經之路上。
    """
    global has_key
    has_key = False  # 重置狀態

    # 1. 跑一次 A* 尋路，找出起點到終點的「必經最短路徑」
    # 備註：請確保你的 pathfinding.a_star_search(maze_obj) 回傳的是一個包含 (y, x) 座標的 list
    try:
        main_path, _ = pathfinding.a_star_search(maze_obj)
        main_path_set = set(main_path)  # 轉成 set 方便快速比對
    except Exception:
        main_path_set = set()  # 如果尋路失敗，防禦性留空

    # 2. 在全地圖的「空地」中尋找一個不在必經之路上的格子放鑰匙
    rows = maze_obj.height
    cols = maze_obj.width

    key_placed = False
    attempts = 0

    while not key_placed and attempts < 2000:
        attempts += 1
        ry = random.randint(1, rows - 2)
        rx = random.randint(1, cols - 2)

        # 條件：必須是走道 (0)、不是起點、不是終點、且「絕對不在必經之路上」
        if maze_obj.grid[ry, rx] == 0:
            current_pos = (ry, rx)
            if current_pos != maze_obj.start_pos and current_pos != maze_obj.end_pos:
                if current_pos not in main_path_set:
                    maze_obj.grid[ry, rx] = KEY_MARK
                    key_placed = True
                    break

    # 萬一這張地圖太極端找不到（機率極低），退回一般隨機空格
    if not key_placed:
        while True:
            ry = random.randint(1, rows - 2)
            rx = random.randint(1, cols - 2)
            if maze_obj.grid[ry, rx] == 0 and (ry, rx) != maze_obj.start_pos and (ry, rx) != maze_obj.end_pos:
                maze_obj.grid[ry, rx] = KEY_MARK
                break


def check_key_logic(next_pos, maze_obj):
    """
    檢查玩家是否踩到鑰匙。
    如果是終點，檢查是否有鑰匙，沒鑰匙就不給通關。
    """
    global has_key
    ny, nx = next_pos

    # 狀況 A：踩到黃色鑰匙
    if maze_obj.grid[ny, nx] == KEY_MARK:
        has_key = True
        maze_obj.grid[ny, nx] = WALKWAY  # 鑰匙消失，變回普通走道
        print("\n【系統提示】你撿到了黃色鑰匙！🔑 現在可以前往終點通關了！")
        return True

    # 狀況 B：嘗試走向終點
    if (ny, nx) == maze_obj.end_pos:
        if not has_key:
            print("\n【系統提示】你雖然走到了終點，但沒有鑰匙無法開門通關！❌ 請回頭尋找鑰匙。")
            return False  # 沒鑰匙，當成牆壁擋住，不讓 player_pos 變成終點

    return True