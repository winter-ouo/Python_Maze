# Maze
## 目前要求
1. 記得開自己的分支進行程式碼的增減及修改
2. 程式碼放於src資料夾中
3. (待增...)

## 運行
### 環境
#### 使用的python環境 3.10
```bash
pip install numpy
pip install opencv-python
```
### 如何執行
#### 先確定套件清單 `pip list`
```text
Package       Version
------------- ---------
numpy         2.2.6
opencv-python 4.13.0.92
pip           23.0.1
setuptools    65.5.0
```
### 如何執行
#### 輸入 `python src/main.py`
## 目前專案架構
```text
PYTHON_MAZE/
│
├── src/                         # 程式碼資料夾
│   ├── __pycache__/             # Python 自動生成的編譯快取檔（不需手動修改）
│   ├── main.py                  # 遊戲主程式（控制層 Controller / 遊戲調度中樞）
│   ├── maze_generator.py        # 迷宮生成器（演算法層 / 負責隨機 Prim 演算法）
│   ├── maze_model.py            # 基礎資料模型（模型層 Model / 封裝矩陣與座標防禦）
│   ├── pathfinding.py           # 尋路邏輯（演算法層 / 整合 A*、BFS、DFS）
│   └── renderer.py              # 畫面渲染器（視圖層 View / 負責 OpenCV 畫布與側欄）
│
├── venv/                         # Python 虛擬環境資料夾（隔離並存放套件如 OpenCV、NumPy）
├── .gitignore                    # Git 忽略設定檔（排除 venv、__pycache__ 等不需推上 GitHub 的檔案）
└── README.md                     # 專案說明文件

```
## 目前已完成之項目
- #### 基礎迷宮生成
- #### A*演算法找最佳路徑
- #### BFS找最佳路徑
- #### DFS找最佳路徑
- #### 沿牆法找路徑
- #### 計時系統
- #### 基礎GUI(遊戲畫面、首頁)