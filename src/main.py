from maze_model import Maze
import renderer
import cv2

def main():
    # 初始化資料模型
    maze = Maze()
    player_pos = maze.start_pos
    
    print("遊戲開始！請點擊 OpenCV 視窗，並使用 W, A, S, D 控制移動。按 ESC 鍵離開。")
    
    while True:
        # 渲染畫面
        canvas = renderer.draw_single(maze, player_pos)
        
        # 更新顯示並偵測鍵盤 (刷新率 30ms)
        key = renderer.update_display(canvas, delay=30)
        
        # 鍵盤
        char = chr(key) if 32 <= key <= 126 else ""
        
        if key == 27:  # ESC 鍵
            break
        elif char in ['w', 'a', 's', 'd']:
            # 呼叫模型移動玩家
            player_pos = maze.move_player(player_pos, char)
            
        # 4. 檢查是否通關
        if player_pos == maze.end_pos:
            print("# 恭喜通關！")
            break
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()