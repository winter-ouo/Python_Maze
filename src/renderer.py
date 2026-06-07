import cv2
import numpy as np
import time  # === [新增] 引入 time 模組來計算每 10 秒現行 0.5 秒的時間差 ===


def draw_single(maze, player_pos, path=None, visited=None, player2_pos=None, monster_pos=None):
    cell_size = 15
    img_h = maze.height * cell_size
    img_w = maze.width * cell_size

    canvas = np.zeros((img_h, img_w, 3), dtype=np.uint8)

    # ========================================================
    # === [新增] 閃爍邏輯計算 ===
    # 取當前時間（秒）對 10 取餘數。如果餘數小於 0.5 秒，代表進入「現行時間」
    # ========================================================
    current_time_mod = time.time() % 8.0
    show_key_pulsing = (current_time_mod <= 2.0)

    # 繪製迷宮
    for r in range(maze.height):
        for c in range(maze.width):
            y1, x1 = r * cell_size, c * cell_size
            y2, x2 = y1 + cell_size, x1 + cell_size

            grid_val = maze.grid[r, c]

            if grid_val == 1:  # 牆壁
                color = (50, 50, 50)
                cv2.rectangle(canvas, (x1, y1), (x2, y2), color, -1)
            elif grid_val == 2:  # === [新增] 鑰匙 (KEY_MARK) ===
                # 先鋪底色（普通走道）
                cv2.rectangle(canvas, (x1, y1), (x2, y2), (240, 240, 240), -1)

                # 如果是「現行時間」，在走道上畫出耀眼的黃色鑰匙方塊/圖示
                if show_key_pulsing:
                    # 內縮一點讓鑰匙看起來像個道具 (黃色 BGR: 0, 220, 255)
                    padding_key = 3
                    cv2.rectangle(canvas,
                                  (x1 + padding_key, y1 + padding_key),
                                  (x2 - padding_key, y2 - padding_key),
                                  (0, 220, 255), -1)
                    # 加個小框框讓它更明顯
                    cv2.rectangle(canvas,
                                  (x1 + padding_key, y1 + padding_key),
                                  (x2 - padding_key, y2 - padding_key),
                                  (0, 150, 200), 1)
            else:  # 普通走道 (0)
                color = (240, 240, 240)
                cv2.rectangle(canvas, (x1, y1), (x2, y2), color, -1)

    # 畫出演算法足跡與正確路徑
    if visited:
        for vr, vc in visited:
            y1, x1 = vr * cell_size, vc * cell_size
            cv2.rectangle(canvas, (x1 + 1, y1 + 1), (x1 + cell_size - 1, y1 + cell_size - 1), (200, 240, 255), -1)
    if path:
        for pr, pc in path:
            if (pr, pc) != maze.start_pos and (pr, pc) != maze.end_pos:
                y1, x1 = pr * cell_size, pc * cell_size
                cv2.rectangle(canvas, (x1 + 1, y1 + 1), (x1 + cell_size - 1, y1 + cell_size - 1), (50, 220, 50), -1)

    # 畫出終點 (紅色)
    ey, ex = maze.end_pos
    padding = 2
    cv2.rectangle(canvas, (ex * cell_size + padding, ey * cell_size + padding),
                  ((ex + 1) * cell_size - padding, (ey + 1) * cell_size - padding), (0, 0, 255), -1)

    # 畫出玩家一 (藍色圓球)
    py, px = player_pos
    radius = int(cell_size * 0.35)
    cv2.circle(canvas, (px * cell_size + cell_size // 2, py * cell_size + cell_size // 2), radius, (255, 0, 0), -1,
               lineType=cv2.LINE_AA)

    # 畫出玩家二 (綠色圓球)
    if player2_pos:
        p2y, p2x = player2_pos
        cv2.circle(canvas, (p2x * cell_size + cell_size // 2, p2y * cell_size + cell_size // 2), radius, (0, 255, 0),
                   -1, lineType=cv2.LINE_AA)
    # ======================
    # 畫出怪物 (紅色)
    # ======================
    if monster_pos:
        my, mx = monster_pos

        cv2.circle(
            canvas,
            (
                mx * cell_size + cell_size // 2,
                my * cell_size + cell_size // 2
            ),
            radius,
            (0, 0, 255),
            -1,
            lineType=cv2.LINE_AA
        )

    return canvas


def draw_sidebar(height, current_algo, stats, seed_val, is_cleared, hover_btn=None):
    width = 250
    sidebar = np.zeros((height, width, 3), dtype=np.uint8)
    sidebar[:] = (35, 30, 30)

    cv2.line(sidebar, (0, 0), (0, height), (70, 70, 70), 2)
    cv2.putText(sidebar, "MAZE GAME", (25, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.line(sidebar, (20, 48), (230, 48), (100, 100, 100), 1)

    cv2.putText(sidebar, f"Active: {current_algo}", (20, 73), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (50, 255, 50), 1)
    cv2.putText(sidebar, f"Explored: {stats['explored']} cells", (20, 98), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                (200, 200, 200), 1)
    cv2.putText(sidebar, f"Path Length: {stats['path_len']} steps", (20, 123), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                (200, 200, 200), 1)
    cv2.line(sidebar, (20, 140), (230, 140), (100, 100, 100), 1)

    cv2.putText(sidebar, "PERFORMANCE TIME:", (20, 163), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    cv2.putText(sidebar, f"A* Finish Time : {stats['a_star_time']:.2f} ms" if stats[
                                                                                  'a_star_time'] > 0 else "A* Finish Time : ...",
                (20, 188), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (100, 200, 255), 1)
    cv2.putText(sidebar,
                f"BFS Finish Time: {stats['bfs_time']:.2f} ms" if stats['bfs_time'] > 0 else "BFS Finish Time: ...",
                (20, 211), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (100, 255, 200), 1)
    cv2.putText(sidebar,
                f"DFS Finish Time: {stats['dfs_time']:.2f} ms" if stats['dfs_time'] > 0 else "DFS Finish Time: ...",
                (20, 234), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 100, 255), 1)
    cv2.putText(sidebar,
                f"Wall Finish Time: {stats['wall_time']:.2f} ms" if stats['wall_time'] > 0 else "Wall Finish Time: ...",
                (20, 257), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 130), 1)
    cv2.putText(sidebar, f"player Finish Time : {stats['player_time']:.1f} s" if stats[
                                                                                     'player_time'] > 0 else "player Finish Time : ...",
                (20, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 150, 100), 1)

    cv2.line(sidebar, (20, 295), (230, 295), (100, 100, 100), 1)
    cv2.putText(sidebar, "SELECT ALGORITHM:", (20, 318), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    c_normal = (80, 60, 50)
    c_hover = (130, 95, 75)
    b_normal = (150, 150, 150)
    b_hover = (255, 255, 255)

    btns = [("1", "[1] A* Search", 335), ("2", "[2] BFS ", 380), ("3", "[3] DFS ", 425),
            ("4", "[4] Wall Follower", 470)]
    for key, text, y in btns:
        is_h = (hover_btn == key)
        cv2.rectangle(sidebar, (20, y), (230, y + 30), c_hover if is_h else c_normal, -1)
        cv2.rectangle(sidebar, (20, y), (230, y + 30), b_hover if is_h else b_normal, 2 if is_h else 1)
        cv2.putText(sidebar, text, (50, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    cv2.line(sidebar, (20, 515), (230, 515), (100, 100, 100), 1)
    cv2.putText(sidebar, "SYSTEM INFO:", (20, 538), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (170, 170, 170), 1)
    cv2.putText(sidebar, f"Map Seed: {seed_val}", (20, 565), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 100), 1)
    cv2.putText(sidebar, "Game Status: ", (20, 595), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)

    if is_cleared:
        cv2.putText(sidebar, "CLEARED !!! ", (120, 595), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (50, 255, 50), 1)
        cv2.putText(sidebar, f"Finish Time: {stats['player_time']:.2f}", (70, 630), cv2.FONT_HERSHEY_SIMPLEX, 0.48,
                    (50, 255, 50), 1)
    else:
        cv2.putText(sidebar, "PLAYING", (120, 595), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 180, 255), 1)

    cv2.putText(sidebar, "ESC: Exit Game", (20, 670), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (120, 120, 120), 1)
    return sidebar


def draw_home_screen(width, height, is_btn_hover=False):
    home_canvas = np.zeros((height, width, 3), dtype=np.uint8)
    home_canvas[:] = (30, 25, 25)

    cv2.rectangle(home_canvas, (40, 40), (width - 40, height - 40), (60, 60, 60), 2)
    cv2.rectangle(home_canvas, (50, 50), (width - 50, height - 50), (40, 40, 40), 1)

    cv2.putText(home_canvas, "PYTHON MAZE GAME", (280, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 4,
                lineType=cv2.LINE_AA)
    cv2.putText(home_canvas, "Final Project v1.0", (430, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 1)

    c_btn = (130, 95, 75) if is_btn_hover else (80, 60, 50)
    b_btn = (255, 255, 255) if is_btn_hover else (150, 150, 150)

    cv2.rectangle(home_canvas, (380, 400), (630, 460), c_btn, -1)
    cv2.rectangle(home_canvas, (380, 400), (630, 460), b_btn, 3 if is_btn_hover else 2)
    cv2.putText(home_canvas, "DEFAULT MODE", (415, 438), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2,
                lineType=cv2.LINE_AA)
    cv2.putText(home_canvas, "[ Click Button to choose mode ]", (380, 590), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (130, 130, 130), 1)
    cv2.putText(home_canvas, "Press 'ESC' to Exit this Platform", (400, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                (80, 80, 80), 1)

    return home_canvas