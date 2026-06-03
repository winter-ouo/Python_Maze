from maze_generator import generate_maze
from pathfinding import a_star_search  # 引入 A* 尋路大腦
import renderer
import cv2

def main():
    # 建立一個 51x51 高難度隨機迷宮
    maze = generate_maze(w=51, h=51, seed=None)
    player_pos = maze.start_pos
    
    # 儲存 A* 尋路的結果
    ai_path = None
    ai_visited = None
    
    print("====================================================")
    print("  【操作說明】")
    print("  - 手動移動：使用 W, A, S, D 或 鍵盤方向鍵")
    print("  - AI 尋路 ：按下『空白鍵 (Space)』讓 A* 幫你找路！")
    print("  - 離開遊戲：按 ESC 鍵")
    print("====================================================")
    
    while True:
        # 1. 產生畫布（將路徑與探索足跡傳入）
        canvas = renderer.draw_single(maze, player_pos, path=ai_path, visited=ai_visited)
        cv2.imshow("Python_maze MVP", canvas)
        
        key = cv2.waitKeyEx(30)
        if key == 27:  # ESC
            break
            
        char = chr(key & 0xFF).lower() if 32 <= (key & 0xFF) <= 126 else ""
        
        # 2. 觸發 A* 尋路機制 (按下空白鍵)
        if key == 32:  
            print("\n🤖 AI 大腦啟動中，計算 A* 最短路徑...")
            path, visited_order = a_star_search(maze)
            
            # 動畫特效
            print("展示 A* 擴散")
            step = max(1, len(visited_order) // 100) # 按比例決定播放速度
            for i in range(0, len(visited_order), step):
                current_visited = visited_order[:i]
                # 即時渲染當前探索進度
                temp_canvas = renderer.draw_single(maze, player_pos, visited=current_visited)
                cv2.imshow("Python_maze MVP", temp_canvas)
                cv2.waitKey(10) # 10毫秒微小延遲
                
            # 將最終路徑定格在畫面上
            ai_path = path
            ai_visited = visited_order
            print(f"✨ 尋路完成！共探索了 {len(visited_order)} 個格子，最短路徑為 {len(path)} 步！")

        # 3. 手動控制移動
        is_up    = (char == 'w' or key == 2490368)
        is_down  = (char == 's' or key == 2621440)
        is_left  = (char == 'a' or key == 2424832)
        is_right = (char == 'd' or key == 2555904)
        
        if is_up: player_pos = maze.move_player(player_pos, 'w')
        elif is_down: player_pos = maze.move_player(player_pos, 's')
        elif is_left: player_pos = maze.move_player(player_pos, 'a')
        elif is_right: player_pos = maze.move_player(player_pos, 'd')
            
        # 4. 檢查手動通關
        if player_pos == maze.end_pos:
            canvas = renderer.draw_single(maze, player_pos, path=ai_path, visited=ai_visited)
            cv2.imshow("Python_maze MVP", canvas)
            cv2.waitKey(1)
            print("\n🎉 恭喜通關！")
            break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()