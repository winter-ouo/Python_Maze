import cv2
import numpy as np


def apply_fog_of_war(frame, player_pos, cell_size, visible_radius=3):
    """
    在迷宮畫面上加上迷霧效果，只保留玩家周圍的視線。
    :param frame: 原本已經畫好迷宮的 OpenCV 畫面
    :param player_pos: 玩家目前的座標 (y, x) 或是 (row, col)
    :param cell_size: 迷宮每一格的大小 (像素)
    :param visible_radius: 可以看見的格子數量
    :return: 加上迷霧後的畫面
    """
    # 取得畫面的長寬
    height, width, _ = frame.shape

    # 建立一個全黑的遮罩 (Mask)
    mask = np.zeros((height, width), dtype=np.uint8)

    # 計算玩家在畫面上的實際像素中心點
    # 假設 player_pos 格式是 [y, x]，如果你的專案是 [x, y] 可以調換 0 和 1
    center_x = int(player_pos[1] * cell_size + cell_size / 2)
    center_y = int(player_pos[0] * cell_size + cell_size / 2)

    # 計算視線半徑的像素大小
    r_pixels = int(visible_radius * cell_size)

    # 在全黑的遮罩上，以玩家為中心畫一個白色的實心圓 (代表看得到的地方)
    cv2.circle(mask, (center_x, center_y), r_pixels, 255, -1)

    # 將原本的畫面和遮罩疊加，只保留白色圓圈內的畫面，其他變成黑色
    foggy_frame = cv2.bitwise_and(frame, frame, mask=mask)

    return foggy_frame