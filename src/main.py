from maze_generator import generate_maze
import pathfinding
import renderer
import cv2
import numpy as np
import time
import random

clicked_algo_choice = None
clicked_home_start = False

current_hover_btn = None   
home_btn_hovered = False    

def mouse_click_handler(event, x, y, flags, param):
    global clicked_algo_choice, clicked_home_start, current_hover_btn, home_btn_hovered
    
    # ====================
    #  捕獲滑鼠懸浮移動事件
    # ====================
    if event == cv2.EVENT_MOUSEMOVE:
        if param == "HOME":
            if 380 <= x <= 630 and 430 <= y <= 490:
                home_btn_hovered = True
            else:
                home_btn_hovered = False
                
        elif param == "GAME":
            sidebar_x = x - 765
            sidebar_y = y
            if 20 <= sidebar_x <= 230:
                if 335 <= sidebar_y <= 365: current_hover_btn = '1'
                elif 380 <= sidebar_y <= 410: current_hover_btn = '2'
                elif 425 <= sidebar_y <= 455: current_hover_btn = '3'
                elif 470 <= sidebar_y <= 500: current_hover_btn = '4'
                else: current_hover_btn = None
            else:
                current_hover_btn = None

    # ==========================================
    # B. 捕獲滑鼠左鍵點擊事件 (LBUTTONDOWN)
    # ==========================================
    elif event == cv2.EVENT_LBUTTONDOWN:
        if param == "HOME":
            if 380 <= x <= 630 and 430 <= y <= 490:
                clicked_home_start = True
                
        elif param == "GAME":
            sidebar_x = x - 765
            sidebar_y = y
            if 20 <= sidebar_x <= 230:
                if 335 <= sidebar_y <= 365: clicked_algo_choice = '1'
                elif 380 <= sidebar_y <= 410: clicked_algo_choice = '2'
                elif 425 <= sidebar_y <= 455: clicked_algo_choice = '3'
                elif 470 <= sidebar_y <= 500: clicked_algo_choice = '4'

def main():
    global clicked_algo_choice, clicked_home_start, current_hover_btn, home_btn_hovered
    
    WINDOW_WIDTH = 1015
    WINDOW_HEIGHT = 765
    window_name = "Python maze game"
    
    cv2.namedWindow(window_name)
    game_state = 0 
    
    maze = None
    player_pos = None
    CURRENT_SEED = 0
    current_algo = "None"
    stats = {}
    ai_path, ai_visited = None, None
    player_has_moved, player_start_time, player_game_over = False, None, False
    
    print("====================================================")
    print("              Python_maze【操作說明】     ")
    print("      - 手動移動：使用 W, A, S, D 或 鍵盤方向鍵")
    print("      - 使用演算法：於右側側欄選擇欲使用的演算法    ")
    print("====================================================")
    while True:
        # ==========================================
        # 【狀態 0：首頁選單畫面】
        # ==========================================
        if game_state == 0:
            cv2.setMouseCallback(window_name, mouse_click_handler, param="HOME")
            
            # 懸浮狀態首頁渲染
            home_frame = draw_home_screen = renderer.draw_home_screen(WINDOW_WIDTH, WINDOW_HEIGHT, home_btn_hovered)
            cv2.imshow(window_name, home_frame)
            
            key = cv2.waitKey(15) & 0xFF
            if key == 27: # Esc
                break
                
            if clicked_home_start:
                clicked_home_start = False
                CURRENT_SEED = random.randint(0, 2147483647)
                maze = generate_maze(w=51, h=51, seed=CURRENT_SEED)
                player_pos = maze.start_pos
                
                stats = {
                    "explored": 0, "path_len": 0, 
                    "a_star_time": 0.0, "bfs_time": 0.0, "dfs_time": 0.0, "wall_time": 0.0, 
                    "player_time": 0.0
                }
                ai_path, ai_visited = None, None
                player_has_moved, player_start_time, player_game_over = False, None, False
                current_algo = "None"
                
                print(f"\n 預設模式加載成功！地圖 Seed：【{CURRENT_SEED}】")
                game_state = 1
                
        # ==========================================
        # 【狀態 1：核心遊戲與 AI 側欄畫面】
        # ==========================================
        elif game_state == 1:
            cv2.setMouseCallback(window_name, mouse_click_handler, param="GAME")
            
            if player_has_moved and not player_game_over:
                stats["player_time"] = time.time() - player_start_time
                
            maze_canvas = renderer.draw_single(maze, player_pos, path=ai_path, visited=ai_visited)
            # 側欄渲染
            sidebar_canvas = renderer.draw_sidebar(maze_canvas.shape[0], current_algo, stats, CURRENT_SEED, player_game_over, current_hover_btn)
            full_window = np.hstack((maze_canvas, sidebar_canvas))
            cv2.imshow(window_name, full_window)
            
            key = cv2.waitKeyEx(15)  # 縮短 UI 更新率
            if key == 27:
                print(" ↩ 返回主首頁選單。")
                game_state = 0
                current_hover_btn = None # 重設懸浮狀態
                continue
                
            char = chr(key & 0xFF).lower() if 32 <= (key & 0xFF) <= 126 else ""
            
            algo_trigger = None
            if char in ['1', '2', '3', '4']:
                algo_trigger = char
            elif clicked_algo_choice is not None:
                algo_trigger = clicked_algo_choice
                clicked_algo_choice = None
                
            if algo_trigger:
                search_func = None
                algo_key = ""
                if algo_trigger == '1':
                    search_func = pathfinding.a_star_search
                    current_algo = "A* Search"
                    algo_key = "a_star_time"
                elif algo_trigger == '2':
                    search_func = pathfinding.bfs_search
                    current_algo = "BFS / Flood Fill"
                    algo_key = "bfs_time"
                elif algo_trigger == '3':
                    search_func = pathfinding.dfs_search
                    current_algo = "DFS (Snake)"
                    algo_key = "dfs_time"
                elif algo_trigger == '4':
                    search_func = pathfinding.wall_follower_search
                    current_algo = "Wall Follower"
                    algo_key = "wall_time"
                    
                if search_func:
                    t_start = time.perf_counter()
                    path, visited_order = search_func(maze)
                    t_end = time.perf_counter()
                    
                    stats[algo_key] = (t_end - t_start) * 1000.0
                    
                    step = max(1, len(visited_order) // 80)
                    for i in range(0, len(visited_order), step):
                        current_visited = visited_order[:i]
                        temp_maze = renderer.draw_single(maze, player_pos, visited=current_visited)
                        temp_sidebar = renderer.draw_sidebar(temp_maze.shape[0], current_algo, stats, CURRENT_SEED, player_game_over, current_hover_btn)
                        temp_full = np.hstack((temp_maze, temp_sidebar))
                        cv2.imshow(window_name, temp_full)
                        cv2.waitKey(4)
                    
                    ai_path = path
                    ai_visited = visited_order
                    stats["explored"] = len(visited_order)
                    stats["path_len"] = len(path)
            
            if not player_game_over:
                is_up    = (char == 'w' or key == 2490368)
                is_down  = (char == 's' or key == 2621440)
                is_left  = (char == 'a' or key == 2424832)
                is_right = (char == 'd' or key == 2555904)
                
                if is_up or is_down or is_left or is_right:
                    if not player_has_moved:
                        player_has_moved = True
                        player_start_time = time.time()
                        
                    if is_up: player_pos = maze.move_player(player_pos, 'w')
                    elif is_down: player_pos = maze.move_player(player_pos, 's')
                    elif is_left: player_pos = maze.move_player(player_pos, 'a')
                    elif is_right: player_pos = maze.move_player(player_pos, 'd')
                    
                if player_pos == maze.end_pos:
                    player_game_over = True
                    stats["player_time"] = time.time() - player_start_time
                    print(f"# 通關！手動時間：{stats['player_time']:.2f} 秒。")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()