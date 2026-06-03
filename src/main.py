from maze_generator import generate_maze
import renderer
import cv2

def main():
    # 建立一個 51x51 完美奇數的高難度隨機迷宮
    maze = generate_maze(w=51, h=51, seed=None)
    player_pos = maze.start_pos
    
    print("====================================================")
    print("  【操作說明】")
    print("  - 移動：使用 W, A, S, D 或 鍵盤方向鍵 (↑ ↓ ← →)")
    print("  - 離開：按 ESC 鍵")
    print("====================================================")
    
    while True:
        # 1. 產生當前迷宮與玩家的畫布
        canvas = renderer.draw_single(maze, player_pos)
        
        # 2. 直接在主迴圈將畫布推上視窗，保障雙緩衝機制不衝突
        cv2.imshow("Python_maze MVP", canvas)
        
        # 3. 讀取完整的 32 位元原始按鍵碼
        key = cv2.waitKeyEx(30)
        
        if key == 27:  # ESC 鍵直接退出
            break
            
        # 4. 提取標準 ASCII 字元（用於 WASD）
        char = chr(key & 0xFF).lower() if 32 <= (key & 0xFF) <= 126 else ""
        
        # 5. 精準對齊你的筆電專屬方向鍵原始編碼
        is_up    = (char == 'w' or key == 2490368)
        is_down  = (char == 's' or key == 2621440)
        is_left  = (char == 'a' or key == 2424832)
        is_right = (char == 'd' or key == 2555904)
        
        # 6. 執行移動
        if is_up:
            player_pos = maze.move_player(player_pos, 'w')
        elif is_down:
            player_pos = maze.move_player(player_pos, 's')
        elif is_left:
            player_pos = maze.move_player(player_pos, 'a')
        elif is_right:
            player_pos = maze.move_player(player_pos, 'd')
            
        # 7. 精準檢查是否通關
        if player_pos == maze.end_pos:
            # 通關時最後刷新一次畫面，讓藍球重疊在紅色終點上
            canvas = renderer.draw_single(maze, player_pos)
            cv2.imshow("Python_maze MVP", canvas)
            cv2.waitKey(1)
            print("\n🎉 恭喜通關！成功突破 51x51 高難度隨機 Prim 迷宮！")
            break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()