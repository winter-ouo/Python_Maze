from maze_generator import generate_maze
import pathfinding
import renderer
import cv2
import numpy as np
import time

clicked_algo_choice = None

def mouse_click_handler(event, x, y, flags, param):
    global clicked_algo_choice
    if event == cv2.EVENT_LBUTTONDOWN:
        sidebar_x = x - 765
        sidebar_y = y
        if 20 <= sidebar_x <= 230:
            if 365 <= sidebar_y <= 405:
                clicked_algo_choice = '1'
            elif 425 <= sidebar_y <= 465:
                clicked_algo_choice = '2'
            elif 485 <= sidebar_y <= 525:
                clicked_algo_choice = '3'

def main():
    global clicked_algo_choice
    
    maze = generate_maze(w=51, h=51, seed=None)
    player_pos = maze.start_pos
    
    # 初始化時間
    current_algo = "None"
    stats = {
        "explored": 0, 
        "path_len": 0, 
        "a_star_time": 0.0, 
        "bfs_time": 0.0, 
        "dfs_time": 0.0, 
        "player_time": 0.0
    }
    ai_path = None
    ai_visited = None
    
    player_has_moved = False
    player_start_time = None
    player_game_over = False
    
    window_name = "Python_maze MVP - AI Panel"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_click_handler)
    
    print("====================================================")
    print("              Python_maze【操作說明】     ")
    print("      - 手動移動：使用 W, A, S, D 或 鍵盤方向鍵")
    print("      - 使用演算法：於右側側欄選擇欲使用的演算法    ")
    print("====================================================")
    
    while True:
        # 即時更新手動時間
        if player_has_moved and not player_game_over:
            stats["player_time"] = time.time() - player_start_time
            
        maze_canvas = renderer.draw_single(maze, player_pos, path=ai_path, visited=ai_visited)
        sidebar_canvas = renderer.draw_sidebar(maze_canvas.shape[0], current_algo, stats)
        full_window = np.hstack((maze_canvas, sidebar_canvas))
        cv2.imshow(window_name, full_window)
        
        key = cv2.waitKeyEx(30)
        if key == 27:
            print("使用者按 ESC ，結束程式。")
            break
            
        char = chr(key & 0xFF).lower() if 32 <= (key & 0xFF) <= 126 else ""
        
        algo_trigger = None
        if char in ['1', '2', '3']:
            algo_trigger = char
        elif clicked_algo_choice is not None:
            algo_trigger = clicked_algo_choice
            clicked_algo_choice = None
            
        # 處理演算法尋路與時間紀錄
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
                
            if search_func:
                t_start = time.perf_counter()
                path, visited_order = search_func(maze)
                t_end = time.perf_counter()
                
                stats[algo_key] = (t_end - t_start) * 1000.0
                
                # 動畫
                step = max(1, len(visited_order) // 80)
                for i in range(0, len(visited_order), step):
                    current_visited = visited_order[:i]
                    temp_maze = renderer.draw_single(maze, player_pos, visited=current_visited)
                    temp_sidebar = renderer.draw_sidebar(temp_maze.shape[0], current_algo, stats)
                    temp_full = np.hstack((temp_maze, temp_sidebar))
                    cv2.imshow(window_name, temp_full)
                    cv2.waitKey(4)
                
                ai_path = path
                ai_visited = visited_order
                stats["explored"] = len(visited_order)
                stats["path_len"] = len(path)
        
        # 手動移動控制
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
                
            # 檢查是否抵達終點
            if player_pos == maze.end_pos:
                player_game_over = True
                # 抵達終點時定格
                stats["player_time"] = time.time() - player_start_time
                print(f"抵達終點！手動通關時間：{stats['player_time']:.2f} 秒")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()