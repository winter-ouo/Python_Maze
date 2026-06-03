from maze_generator import generate_maze
import pathfinding
import renderer
import cv2
import numpy as np

# 全域變數用來傳遞滑鼠點擊事件
clicked_algo_choice = None

def mouse_click_handler(event, x, y, flags, param):
    """
    滑鼠監聽器：專門捕獲玩家點擊右側側欄按鈕的事件
    """
    global clicked_algo_choice
    if event == cv2.EVENT_LBUTTONDOWN:
        # 換算成側欄內部的相對座標
        sidebar_x = x - 765
        sidebar_y = y
        
        # 檢查點擊是否落在按鈕的 X 軸有效寬度內 (20 到 230)
        if 20 <= sidebar_x <= 230:
            # 按鈕 1: A* (Y 軸 230 到 270)
            if 230 <= sidebar_y <= 270:
                clicked_algo_choice = '1'
            # 按鈕 2: BFS (Y 軸 290 到 330)
            elif 290 <= sidebar_y <= 330:
                clicked_algo_choice = '2'
            # 按鈕 3: DFS (Y 軸 350 到 390)
            elif 350 <= sidebar_y <= 390:
                clicked_algo_choice = '3'

def main():
    global clicked_algo_choice
    
    # 建立一個 51x51 的隨機迷宮
    maze = generate_maze(w=51, h=51, seed=None)
    player_pos = maze.start_pos
    
    # 介面狀態資料
    current_algo = "None"
    stats = {"explored": 0, "path_len": 0}
    ai_path = None
    ai_visited = None
    
    # 初始化 OpenCV 視窗並綁定滑鼠事件
    window_name = "Python_maze MVP - AI Panel"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_click_handler)
    
    print("====================================================")
    print("                  【操作說明】                       ")
    print("    - 手動移動：使用 W, A, S, D 或 鍵盤方向鍵         ")
    print("    - 使用演算法：於右側次欄選擇欲使用的演算法         ")
    print("====================================================")
    
    while True:
        # 產生左側迷宮畫布
        maze_canvas = renderer.draw_single(maze, player_pos, path=ai_path, visited=ai_visited)
        
        # 產生右側 UI 側欄畫布
        sidebar_canvas = renderer.draw_sidebar(maze_canvas.shape[0], current_algo, stats)
        
        # 核心拼接：將迷宮與側欄水平黏合
        full_window = np.hstack((maze_canvas, sidebar_canvas))
        cv2.imshow(window_name, full_window)
        
        # 讀取按鍵
        key = cv2.waitKeyEx(30)
        if key == 27:  # ESC
            break
            
        char = chr(key & 0xFF).lower() if 32 <= (key & 0xFF) <= 126 else ""
        
        # 整合按鍵與滑鼠的輸入來源
        algo_trigger = None
        if char in ['1', '2', '3']:
            algo_trigger = char
        elif clicked_algo_choice is not None:
            algo_trigger = clicked_algo_choice
            clicked_algo_choice = None  # 消費掉滑鼠點擊事件
            
        # 處理演算法尋路與動畫展示
        if algo_trigger:
            search_func = None
            if algo_trigger == '1':
                search_func = pathfinding.a_star_search
                current_algo = "A* Search"
            elif algo_trigger == '2':
                search_func = pathfinding.bfs_search
                current_algo = "BFS / Flood Fill"
            elif algo_trigger == '3':
                search_func = pathfinding.dfs_search
                current_algo = "DFS (Snake)"
                
            if search_func:
                path, visited_order = search_func(maze)
                
                # 動態播放
                step = max(1, len(visited_order) // 80)
                for i in range(0, len(visited_order), step):
                    current_visited = visited_order[:i]
                    temp_maze = renderer.draw_single(maze, player_pos, visited=current_visited)
                    temp_sidebar = renderer.draw_sidebar(temp_maze.shape[0], current_algo, stats)
                    temp_full = np.hstack((temp_maze, temp_sidebar))
                    cv2.imshow(window_name, temp_full)
                    cv2.waitKey(6)
                
                # 更新定格狀態與側欄面板數據
                ai_path = path
                ai_visited = visited_order
                stats["explored"] = len(visited_order)
                stats["path_len"] = len(path)
        
        # 7. 手動移動控制
        is_up    = (char == 'w' or key == 2490368)
        is_down  = (char == 's' or key == 2621440)
        is_left  = (char == 'a' or key == 2424832)
        is_right = (char == 'd' or key == 2555904)
        
        if is_up: player_pos = maze.move_player(player_pos, 'w')
        elif is_down: player_pos = maze.move_player(player_pos, 's')
        elif is_left: player_pos = maze.move_player(player_pos, 'a')
        elif is_right: player_pos = maze.move_player(player_pos, 'd')
            
        # 8. 檢查通關
        if player_pos == maze.end_pos:
            maze_canvas = renderer.draw_single(maze, player_pos, path=ai_path, visited=ai_visited)
            sidebar_canvas = renderer.draw_sidebar(maze_canvas.shape[0], current_algo, stats)
            full_window = np.hstack((maze_canvas, sidebar_canvas))
            cv2.imshow(window_name, full_window)
            cv2.waitKey(1)
            print("\n🎉 恭喜通關！")
            break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()