import cv2
import numpy as np
import time
import random
from maze_generator import generate_maze
import pathfinding
import renderer
from fog_effect import apply_fog_of_war

# === 全域引入與設定 ===
import key as key_sys

clicked_algo_choice = None
clicked_home_start = False
clicked_fog_start = False

current_hover_btn = None
home_btn_hovered = False
fog_btn_hovered = False

# === 全域變數，讓滑鼠可以跨功能知道目前的模式與人數按鈕狀態 ===
CURRENT_MODE = "DEFAULT"
clicked_fog_p_choice = None  # 儲存點擊了 '1' (1P) 還是 '2' (2P)
hover_fog_p = None  # 儲存滑鼠正懸浮在 '1' 還是 '2' 上


# =============================================================

def mouse_click_handler(event, x, y, flags, param):
    global clicked_algo_choice, clicked_home_start, clicked_fog_start
    global current_hover_btn, home_btn_hovered, fog_btn_hovered
    global CURRENT_MODE, clicked_fog_p_choice, hover_fog_p

    # ====================
    #  捕獲滑鼠懸浮移動事件
    # ====================
    if event == cv2.EVENT_MOUSEMOVE:
        if param == "HOME":
            if 380 <= x <= 630 and 400 <= y <= 460:
                home_btn_hovered = True
                fog_btn_hovered = False
            elif 380 <= x <= 630 and 480 <= y <= 540:
                fog_btn_hovered = True
                home_btn_hovered = False
            else:
                home_btn_hovered = False
                fog_btn_hovered = False

        elif param == "GAME":
            sidebar_x = x - 765
            sidebar_y = y

            # 根據不同模式，讓滑鼠懸浮偵測不同的按鈕
            if CURRENT_MODE == "DEFAULT":
                if 20 <= sidebar_x <= 230:
                    if 335 <= sidebar_y <= 365:
                        current_hover_btn = '1'
                    elif 380 <= sidebar_y <= 410:
                        current_hover_btn = '2'
                    elif 425 <= sidebar_y <= 455:
                        current_hover_btn = '3'
                    elif 470 <= sidebar_y <= 500:
                        current_hover_btn = '4'
                    else:
                        current_hover_btn = None
                else:
                    current_hover_btn = None

            elif CURRENT_MODE == "FOG":
                # 偵測迷霧模式側邊欄的 1P/2P 按鈕懸浮
                if 20 <= sidebar_x <= 230:
                    if 180 <= sidebar_y <= 220:
                        hover_fog_p = '1'
                    elif 240 <= sidebar_y <= 280:
                        hover_fog_p = '2'
                    else:
                        hover_fog_p = None
                else:
                    hover_fog_p = None

    # ==========================================
    # B. 捕獲滑鼠左鍵點擊事件 (LBUTTONDOWN)
    # ==========================================
    elif event == cv2.EVENT_LBUTTONDOWN:
        if param == "HOME":
            if 380 <= x <= 630 and 400 <= y <= 460:
                clicked_home_start = True
            elif 380 <= x <= 630 and 480 <= y <= 540:
                clicked_fog_start = True

        elif param == "GAME":
            sidebar_x = x - 765
            sidebar_y = y

            if CURRENT_MODE == "DEFAULT":
                if 20 <= sidebar_x <= 230:
                    if 335 <= sidebar_y <= 365:
                        clicked_algo_choice = '1'
                    elif 380 <= sidebar_y <= 410:
                        clicked_algo_choice = '2'
                    elif 425 <= sidebar_y <= 455:
                        clicked_algo_choice = '3'
                    elif 470 <= sidebar_y <= 500:
                        clicked_algo_choice = '4'

            elif CURRENT_MODE == "FOG":
                # 偵測點擊 1P 還是 2P 按鈕
                if 20 <= sidebar_x <= 230:
                    if 180 <= sidebar_y <= 220:
                        clicked_fog_p_choice = '1'
                    elif 240 <= sidebar_y <= 280:
                        clicked_fog_p_choice = '2'


def main():
    global clicked_algo_choice, clicked_home_start, clicked_fog_start
    global current_hover_btn, home_btn_hovered, fog_btn_hovered
    global CURRENT_MODE, clicked_fog_p_choice, hover_fog_p

    WINDOW_WIDTH = 1015
    WINDOW_HEIGHT = 765
    window_name = "Python maze game"

    cv2.namedWindow(window_name)
    game_state = 0

    maze = None
    player_pos = None
    player2_pos = None
    CURRENT_SEED = 0
    current_algo = "None"
    stats = {}
    ai_path, ai_visited = None, None
    player_has_moved, player_start_time, player_game_over = False, None, False

    fog_players = 1
    CURRENT_MODE = "DEFAULT"

    print("====================================================")
    print("              Python_maze【操作說明】     ")
    print("      - 預設模式：可於右側側欄選擇演算法觀看尋路（無鑰匙限制）")
    print("      - 迷霧模式：可在右側即時切換單人(1P)或雙人(2P)合作挑戰")
    print("      - 鑰匙機制：【僅限迷霧模式】每 8 秒現行 2 秒，需取得方可通關！")
    print("      - 通關結算：可按 'R' 鍵再來一局，或按 'ESC' 返回主選單")
    print("====================================================")

    while True:
        # ==========================================
        # 【首頁選單畫面】
        # ==========================================
        if game_state == 0:
            cv2.setMouseCallback(window_name, mouse_click_handler, param="HOME")
            home_frame = renderer.draw_home_screen(WINDOW_WIDTH, WINDOW_HEIGHT, home_btn_hovered)

            btn_color = (60, 60, 80) if not fog_btn_hovered else (90, 90, 120)
            cv2.rectangle(home_frame, (380, 480), (630, 540), btn_color, -1)
            cv2.rectangle(home_frame, (380, 480), (630, 540), (200, 200, 200), 2)
            cv2.putText(home_frame, "FOG MODE", (455, 518), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2,
                        cv2.LINE_AA)

            cv2.imshow(window_name, home_frame)

            key = cv2.waitKey(15) & 0xFF
            if key == 27: break

            if clicked_home_start or clicked_fog_start:
                if clicked_home_start:
                    CURRENT_MODE = "DEFAULT"
                else:
                    CURRENT_MODE = "FOG"

                clicked_home_start = False
                clicked_fog_start = False

                # === 抽離出初始化關卡的獨立區塊 (方便通關後再來一次呼叫) ===
                CURRENT_SEED = random.randint(0, 2147483647)
                maze = generate_maze(w=51, h=51, seed=CURRENT_SEED)

                if CURRENT_MODE == "FOG":
                    key_sys.spawn_key_smart(maze)
                else:
                    key_sys.has_key = True

                player_pos = maze.start_pos
                player2_pos = maze.start_pos
                fog_players = 1

                stats = {"explored": 0, "path_len": 0, "a_star_time": 0.0, "bfs_time": 0.0, "dfs_time": 0.0,
                         "wall_time": 0.0, "player_time": 0.0}
                ai_path, ai_visited = None, None
                player_has_moved, player_start_time, player_game_over = False, None, False
                current_algo = "None"

                game_state = 1

        # ==========================================
        # 【遊戲與側欄畫面】
        # ==========================================
        elif game_state == 1:
            cv2.setMouseCallback(window_name, mouse_click_handler, param="GAME")

            if player_has_moved and not player_game_over:
                stats["player_time"] = time.time() - player_start_time

            if CURRENT_MODE == "FOG" and clicked_fog_p_choice is not None:
                if clicked_fog_p_choice == '1' and not player_has_moved:
                    fog_players = 1
                elif clicked_fog_p_choice == '2' and not player_has_moved:
                    fog_players = 2
                clicked_fog_p_choice = None

            maze_canvas = renderer.draw_single(maze, player_pos, path=ai_path, visited=ai_visited,
                                               player2_pos=player2_pos if fog_players == 2 else None)

            if CURRENT_MODE == "DEFAULT":
                sidebar_canvas = renderer.draw_sidebar(maze_canvas.shape[0], current_algo, stats, CURRENT_SEED,
                                                       player_game_over, current_hover_btn)

                # === [優化] 在 DEFAULT 模式通關時，於側邊欄最下方增添操作選單提示 ===
                if player_game_over:
                    cv2.rectangle(sidebar_canvas, (15, 620), (235, 710), (50, 40, 40), -1)
                    cv2.rectangle(sidebar_canvas, (15, 620), (235, 710), (0, 255, 0), 1)
                    cv2.putText(sidebar_canvas, "PLAY AGAIN?", (30, 645), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                                (100, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(sidebar_canvas, "Press 'R' : Restart", (25, 675), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                                (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(sidebar_canvas, "Press 'ESC': Main Menu", (25, 695), cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                                (200, 200, 200), 1, cv2.LINE_AA)

                full_window = np.hstack((maze_canvas, sidebar_canvas))

            elif CURRENT_MODE == "FOG":
                if fog_players == 1:
                    maze_canvas = apply_fog_of_war(maze_canvas, [player_pos], cell_size=15, visible_radius=4)
                else:
                    maze_canvas = apply_fog_of_war(maze_canvas, [player_pos, player2_pos], cell_size=15,
                                                   visible_radius=4)

                # 強制讓現行的鑰匙「穿透迷霧」直接渲染在畫布最上層 (每 8 秒的前 2 秒)
                current_time_mod = time.time() % 8.0
                if current_time_mod <= 2.0:
                    cell_size = 15
                    for r in range(maze.height):
                        for c in range(maze.width):
                            if maze.grid[r, c] == 2:
                                y1, x1 = r * cell_size, c * cell_size
                                y2, x2 = y1 + cell_size, x1 + cell_size
                                padding_key = 3
                                cv2.rectangle(maze_canvas, (x1 + padding_key, y1 + padding_key),
                                              (x2 - padding_key, y2 - padding_key), (0, 220, 255), -1)
                                cv2.rectangle(maze_canvas, (x1 + padding_key, y1 + padding_key),
                                              (x2 - padding_key, y2 - padding_key), (0, 150, 200), 1)

                sidebar_width = WINDOW_WIDTH - maze_canvas.shape[1]
                sidebar_canvas = np.zeros((maze_canvas.shape[0], sidebar_width, 3), dtype=np.uint8)
                sidebar_canvas[:] = (35, 30, 30)

                cv2.line(sidebar_canvas, (0, 0), (0, maze_canvas.shape[0]), (70, 70, 70), 2)

                cv2.putText(sidebar_canvas, "FOG MODE", (25, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2,
                            cv2.LINE_AA)
                cv2.line(sidebar_canvas, (20, 48), (230, 48), (100, 100, 100), 1)
                cv2.putText(sidebar_canvas, "Survive the dark.", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (150, 150, 150), 1, cv2.LINE_AA)

                cv2.putText(sidebar_canvas, "SELECT PLAYERS:", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (255, 255, 255), 1, cv2.LINE_AA)

                # 1P 按鈕
                if fog_players == 1:
                    c_p1, b_p1 = (50, 120, 50), (100, 255, 100)
                elif hover_fog_p == '1':
                    c_p1, b_p1 = (90, 90, 120), (255, 255, 255)
                else:
                    c_p1, b_p1 = (60, 60, 80), (150, 150, 150)

                cv2.rectangle(sidebar_canvas, (20, 180), (230, 220), c_p1, -1)
                cv2.rectangle(sidebar_canvas, (20, 180), (230, 220), b_p1,
                              2 if fog_players == 1 or hover_fog_p == '1' else 1)
                cv2.putText(sidebar_canvas, "1P: Single Player", (45, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (255, 255, 255), 1, cv2.LINE_AA)

                # 2P 按鈕
                if fog_players == 2:
                    c_p2, b_p2 = (50, 120, 50), (100, 255, 100)
                elif hover_fog_p == '2':
                    c_p2, b_p2 = (90, 90, 120), (255, 255, 255)
                else:
                    c_p2, b_p2 = (60, 60, 80), (150, 150, 150)

                cv2.rectangle(sidebar_canvas, (20, 240), (230, 280), c_p2, -1)
                cv2.rectangle(sidebar_canvas, (20, 240), (230, 280), b_p2,
                              2 if fog_players == 2 or hover_fog_p == '2' else 1)
                cv2.putText(sidebar_canvas, "2P: CO-OP Mode", (45, 265), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (255, 255, 255), 1, cv2.LINE_AA)

                cv2.putText(sidebar_canvas, "CONTROLS:", (20, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (170, 170, 170), 1,
                            cv2.LINE_AA)
                if fog_players == 1:
                    cv2.putText(sidebar_canvas, "Player: W, A, S, D", (20, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                                (255, 255, 255), 1, cv2.LINE_AA)
                else:
                    cv2.putText(sidebar_canvas, "P1 (Blue) : W, A, S, D", (20, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                                (255, 150, 50), 1, cv2.LINE_AA)
                    cv2.putText(sidebar_canvas, "P2 (Green): Arrow Keys", (20, 390), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                                (100, 255, 100), 1, cv2.LINE_AA)

                # 迷霧模式側欄的鑰匙狀態
                key_str = "KEY: RECEIVED 🔑" if key_sys.has_key else "KEY: NEEDED ❌"
                key_color = (100, 255, 100) if key_sys.has_key else (100, 100, 255)
                cv2.putText(sidebar_canvas, key_str, (20, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.45, key_color, 1,
                            cv2.LINE_AA)

                cv2.putText(sidebar_canvas, f"Map Seed: {CURRENT_SEED}", (20, 700), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (0, 200, 200), 1, cv2.LINE_AA)
                cv2.putText(sidebar_canvas, "ESC: Return to Menu", (20, 740), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (100, 100, 100), 1, cv2.LINE_AA)

                # === [優化] 迷霧模式結算與「再來一次 / 離開」介面整合 ===
                if player_game_over:
                    cv2.putText(sidebar_canvas, "GAME OVER!", (30, 480), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
                                cv2.LINE_AA)
                    if fog_players == 1:
                        cv2.putText(sidebar_canvas, "You Escaped!", (30, 520), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    (255, 255, 255), 1, cv2.LINE_AA)
                    else:
                        cv2.putText(sidebar_canvas, "TEAM ESCAPED!", (30, 520), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                    (100, 255, 255), 2, cv2.LINE_AA)
                    cv2.putText(sidebar_canvas, f"Time: {stats['player_time']:.2f} s", (30, 555),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

                    # 增添再來局的快捷指示文字
                    cv2.line(sidebar_canvas, (20, 580), (230, 580), (100, 100, 100), 1)
                    cv2.putText(sidebar_canvas, "R : Play Again", (30, 610), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                                (0, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(sidebar_canvas, "ESC: Return to Menu", (30, 635), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                                (200, 200, 200), 1, cv2.LINE_AA)

                full_window = np.hstack((maze_canvas, sidebar_canvas))

            cv2.imshow(window_name, full_window)

            key = cv2.waitKeyEx(1)
            if key == 27:  # 無論何時按 ESC 都能退回主畫面
                game_state = 0
                current_hover_btn = None
                continue

            char = chr(key & 0xFF).lower() if 32 <= (key & 0xFF) <= 126 else ""

            # === [新增] 當遊戲結束時，攔截玩家按下的功能鍵 (R 鍵重新開始) ===
            if player_game_over and char == 'r':
                CURRENT_SEED = random.randint(0, 2147483647)
                maze = generate_maze(w=51, h=51, seed=CURRENT_SEED)
                if CURRENT_MODE == "FOG":
                    key_sys.spawn_key_smart(maze)
                else:
                    key_sys.has_key = True
                player_pos = maze.start_pos
                player2_pos = maze.start_pos
                stats = {"explored": 0, "path_len": 0, "a_star_time": 0.0, "bfs_time": 0.0, "dfs_time": 0.0,
                         "wall_time": 0.0, "player_time": 0.0}
                ai_path, ai_visited = None, None
                player_has_moved, player_start_time, player_game_over = False, None, False
                current_algo = "None"
                continue

            algo_trigger = None
            if CURRENT_MODE == "DEFAULT":
                if char in ['1', '2', '3', '4']:
                    algo_trigger = char
                elif clicked_algo_choice is not None:
                    algo_trigger = clicked_algo_choice
                    clicked_algo_choice = None
            else:
                clicked_algo_choice = None

            if algo_trigger:
                search_func = None
                algo_key = ""
                if algo_trigger == '1':
                    search_func, current_algo, algo_key = pathfinding.a_star_search, "A* Search ", "a_star_time"
                elif algo_trigger == '2':
                    search_func, current_algo, algo_key = pathfinding.bfs_search, "BFS ", "bfs_time"
                elif algo_trigger == '3':
                    search_func, current_algo, algo_key = pathfinding.dfs_search, "DFS ", "dfs_time"
                elif algo_trigger == '4':
                    search_func, current_algo, algo_key = pathfinding.wall_follower_search, "Wall Follower", "wall_time"

                if search_func:
                    t_start = time.perf_counter()
                    path, visited_order = search_func(maze)
                    t_end = time.perf_counter()
                    stats[algo_key] = (t_end - t_start) * 1000.0

                    step = max(1, len(visited_order) // 80)
                    for i in range(0, len(visited_order), step):
                        temp_maze = renderer.draw_single(maze, player_pos, visited=visited_order[:i],
                                                         player2_pos=player2_pos if fog_players == 2 else None)
                        temp_sidebar = renderer.draw_sidebar(temp_maze.shape[0], current_algo, stats, CURRENT_SEED,
                                                             player_game_over, current_hover_btn)
                        cv2.imshow(window_name, np.hstack((temp_maze, temp_sidebar)))
                        cv2.waitKey(4)

                    ai_path, ai_visited = path, visited_order
                    stats["explored"], stats["path_len"] = len(visited_order), len(path)

            # 移動判定
            if not player_game_over:
                p1_moved = p2_moved = False

                # 玩家一 (藍色): W, A, S, D
                if char in ['w', 's', 'a', 'd']:
                    next_p1 = maze.move_player(player_pos, char)
                    if CURRENT_MODE == "DEFAULT" or key_sys.check_key_logic(next_p1, maze):
                        player_pos = next_p1
                        p1_moved = True

                # 玩家二 (綠色): 鍵盤方向鍵 (只有在切換到 2P 合作模式時開機)
                if fog_players == 2:
                    move_dir = None
                    if key == 2490368:
                        move_dir = 'w'
                    elif key == 2621440:
                        move_dir = 's'
                    elif key == 2424832:
                        move_dir = 'a'
                    elif key == 2555904:
                        move_dir = 'd'

                    if move_dir:
                        next_p2 = maze.move_player(player2_pos, move_dir)
                        if CURRENT_MODE == "DEFAULT" or key_sys.check_key_logic(next_p2, maze):
                            player2_pos = next_p2
                            p2_moved = True

                if p1_moved or p2_moved:
                    if not player_has_moved:
                        player_has_moved = True
                        player_start_time = time.time()

                # 判定合作勝利：任一玩家抵達終點，即全隊破關
                if player_pos == maze.end_pos or (fog_players == 2 and player2_pos == maze.end_pos):
                    player_game_over = True
                    stats["player_time"] = time.time() - player_start_time

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()