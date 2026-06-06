import cv2
import numpy as np


def apply_fog_of_war(frame, player_positions, cell_size, visible_radius=3):
    """
    支援多人的迷霧效果。
    :param player_positions: 裝著所有玩家座標的列表，例如 [player1_pos, player2_pos]
    """
    height, width, _ = frame.shape
    mask = np.zeros((height, width), dtype=np.uint8)
    r_pixels = int(visible_radius * cell_size)

    # 迴圈讀取每一個玩家的座標，並幫他們畫上專屬的光圈
    for pos in player_positions:
        # 如果光圈方向反了，一樣把中括號裡的 0 和 1 對調
        center_x = int(pos[1] * cell_size + cell_size / 2)
        center_y = int(pos[0] * cell_size + cell_size / 2)
        cv2.circle(mask, (center_x, center_y), r_pixels, 255, -1)

    foggy_frame = cv2.bitwise_and(frame, frame, mask=mask)
    return foggy_frame