# Pyxelでまるばつゲーム作成チュートリアル（小学4年生向け）

![スクリーンショット 2025-05-18 8 51 02](https://github.com/user-attachments/assets/52ccaf68-efca-4c11-8922-0326db791149)


## 概要
このチュートリアルでは、Pyxelというゲームエンジンを使って、まるばつゲーム（三目並べ）を作成します。レッスンは3回に分かれており、最終的にはコンピュータと対戦できるゲームを完成させます。

## レッスン1：基本的な画面表示とマス目の作成

### 目標
- Pyxelの基本的な使い方を理解する
- まるばつゲームの画面とマス目を表示する

### チュートリアル内容

1. まず、Pyxelをインポートして基本的なゲーム画面を作ります。

```python
import pyxel

class TicTacToe:
    def __init__(self):
        # 画面の大きさを設定（128x128ピクセル）
        pyxel.init(128, 128, title="まるばつゲーム")
        
        # マウスカーソルを表示する
        pyxel.mouse(True)
        
        # マス目の情報（0=空、1=○、2=×）
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        
        # ゲームの状態（0=続行中、1=○の勝ち、2=×の勝ち、3=引き分け）
        self.game_state = 0
        
        # 現在のプレイヤー（1=○、2=×）
        self.current_player = 1
        
        # pyxelの実行
        pyxel.run(self.update, self.draw)
    
    def update(self):
        # ゲームの更新処理（次のレッスンで実装）
        pass
    
    def draw(self):
        # 画面をクリア（黒色）
        pyxel.cls(0)
        
        # マス目を描く
        self.draw_grid()
    
    def draw_grid(self):
        # マス目の線を描く（白色）
        for i in range(1, 3):
            # 縦線
            pyxel.line(i * 40 + 10, 10, i * 40 + 10, 130, 7)
            # 横線
            pyxel.line(10, i * 40 + 10, 130, i * 40 + 10, 7)

# ゲームを起動
TicTacToe()
```

マス目は3×3の白い線で表示されます。このコードを実行すると、黒い背景に白い線で区切られた9つのマスが表示されます。

### 解説
- `pyxel.init(128, 128)`: 128×128ピクセルの画面を作ります
- `pyxel.mouse(True)`: マウスカーソルを表示します
- `self.board`: ゲームの盤面を表す2次元リストです。各マスの状態を記録します
- `self.current_player`: 今のプレイヤーが○か×かを示します
- `pyxel.cls(0)`: 画面を黒色でクリアします
- `pyxel.line()`: 線を描きます。始点(x, y)と終点(x, y)と色を指定します

## レッスン2：クリック操作と○×の表示

### 目標
- マウスクリックでマス目を選べるようにする
- ○と×を交互に表示できるようにする

### チュートリアル内容

```python
import pyxel

class TicTacToe:
    def __init__(self):
        pyxel.init(128, 128, title="まるばつゲーム")
        
        # マウスカーソルを表示する
        pyxel.mouse(True)
        
        # マス目の情報（0=空、1=○、2=×）
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        
        # ゲームの状態（0=続行中、1=○の勝ち、2=×の勝ち、3=引き分け）
        self.game_state = 0
        
        # 現在のプレイヤー（1=○、2=×）
        self.current_player = 1
        
        # pyxelの実行
        pyxel.run(self.update, self.draw)
    
    def update(self):
        # ゲームが終了していたら何もしない
        if self.game_state != 0:
            return
        
        # マウスがクリックされたか確認
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # クリックされた位置をマス目の座標に変換
            x = (pyxel.mouse_x - 10) // 40
            y = (pyxel.mouse_y - 10) // 40
            
            # 有効なマス目がクリックされたか確認
            if 0 <= x < 3 and 0 <= y < 3:
                # そのマスが空いているか確認
                if self.board[y][x] == 0:
                    # マスに現在のプレイヤーの印をつける
                    self.board[y][x] = self.current_player
                    
                    # プレイヤーを交代する
                    self.current_player = 3 - self.current_player  # 1→2, 2→1
    
    def draw(self):
        # 画面をクリア（黒色）
        pyxel.cls(0)
        
        # マス目を描く
        self.draw_grid()
        
        # ○と×を描く
        self.draw_marks()
    
    def draw_grid(self):
        # マス目の線を描く（白色）
        for i in range(1, 3):
            # 縦線
            pyxel.line(i * 40 + 10, 10, i * 40 + 10, 130, 7)
            # 横線
            pyxel.line(10, i * 40 + 10, 130, i * 40 + 10, 7)
    
    def draw_marks(self):
        for y in range(3):
            for x in range(3):
                # マスの中心座標
                center_x = x * 40 + 30
                center_y = y * 40 + 30
                
                # マスの状態によって○か×を描く
                if self.board[y][x] == 1:  # ○
                    pyxel.circb(center_x, center_y, 15, 11)  # 青い円
                elif self.board[y][x] == 2:  # ×
                    pyxel.line(center_x - 15, center_y - 15, center_x + 15, center_y + 15, 8)  # 赤い線
                    pyxel.line(center_x + 15, center_y - 15, center_x - 15, center_y + 15, 8)  # 赤い線

# ゲームを起動
TicTacToe()
```

### 解説
- `pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)`: マウスの左ボタンがクリックされたかチェックします
- `(pyxel.mouse_x - 10) // 40`: クリックされた座標をマス目の位置（0, 1, 2）に変換します
- `self.current_player = 3 - self.current_player`: プレイヤーを交代させる計算です（1→2, 2→1）
- `pyxel.circb()`: 円を描きます（○）
- `pyxel.line()`: 線を描きます（×）

## レッスン3：勝敗判定とコンピュータ対戦機能

### 目標
- 勝敗を判定できるようにする
- コンピュータと対戦できるようにする

### チュートリアル内容

```python
import pyxel
import random

class TicTacToe:
    def __init__(self):
        pyxel.init(128, 128, title="まるばつゲーム")
        
        # マウスカーソルを表示する
        pyxel.mouse(True)
        
        # マス目の情報（0=空、1=○、2=×）
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        
        # ゲームの状態（0=続行中、1=○の勝ち、2=×の勝ち、3=引き分け）
        self.game_state = 0
        
        # 現在のプレイヤー（1=○、2=×）
        self.current_player = 1
        
        # コンピュータがプレイヤー2（×）を担当
        self.computer_plays = True
        
        # pyxelの実行
        pyxel.run(self.update, self.draw)
    
    def update(self):
        # ゲームが終了していたらRボタンでリセット
        if self.game_state != 0:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return
        
        # プレイヤー1（人間）の番
        if self.current_player == 1:
            # マウスがクリックされたか確認
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                # クリックされた位置をマス目の座標に変換
                x = (pyxel.mouse_x - 10) // 40
                y = (pyxel.mouse_y - 10) // 40
                
                # 有効なマス目がクリックされたか確認
                if 0 <= x < 3 and 0 <= y < 3:
                    # そのマスが空いているか確認
                    if self.board[y][x] == 0:
                        # マスに現在のプレイヤーの印をつける
                        self.board[y][x] = self.current_player
                        
                        # 勝敗チェック
                        self.check_game_state()
                        
                        # プレイヤーを交代する
                        self.current_player = 3 - self.current_player  # 1→2, 2→1
        
        # プレイヤー2（コンピュータ）の番
        elif self.current_player == 2 and self.computer_plays and self.game_state == 0:
            # 少し間を置いてコンピュータの手を決める
            if pyxel.frame_count % 30 == 0:  # 約0.5秒待つ
                self.smart_computer_move()
                
                # 勝敗チェック
                self.check_game_state()
                
                # プレイヤーを交代する
                self.current_player = 3 - self.current_player  # 1→2, 2→1
    
    def draw(self):
        # 画面をクリア（黒色）
        pyxel.cls(0)
        
        # マス目を描く
        self.draw_grid()
        
        # ○と×を描く
        self.draw_marks()
        
        # ゲーム状態を表示
        self.draw_game_state()
    
    def draw_grid(self):
        # マス目の線を描く（白色）
        for i in range(1, 3):
            # 縦線
            pyxel.line(i * 40 + 10, 10, i * 40 + 10, 130, 7)
            # 横線
            pyxel.line(10, i * 40 + 10, 130, i * 40 + 10, 7)
    
    def draw_marks(self):
        for y in range(3):
            for x in range(3):
                # マスの中心座標
                center_x = x * 40 + 30
                center_y = y * 40 + 30
                
                # マスの状態によって○か×を描く
                if self.board[y][x] == 1:  # ○
                    pyxel.circb(center_x, center_y, 15, 11)  # 青い円
                elif self.board[y][x] == 2:  # ×
                    # 赤い×
                    pyxel.line(center_x - 15, center_y - 15, 
                               center_x + 15, center_y + 15, 8)
                    pyxel.line(center_x + 15, center_y - 15, 
                               center_x - 15, center_y + 15, 8)
    
    def draw_game_state(self):
        if self.game_state == 1:
            pyxel.text(10, 5, "You wins! Press R to reset", 11)
        elif self.game_state == 2:
            pyxel.text(10, 5, "PC wins! Press R to reset", 8)
        elif self.game_state == 3:
            pyxel.text(10, 5, "Draw! Press R to reset", 7)
    
    def check_game_state(self):
        # 横のラインをチェック
        for y in range(3):
            if (self.board[y][0] != 0 
                    and self.board[y][0] == self.board[y][1] == self.board[y][2]):
                self.game_state = self.board[y][0]
                return
        
        # 縦のラインをチェック
        for x in range(3):
            if (self.board[0][x] != 0 
                    and self.board[0][x] == self.board[1][x] == self.board[2][x]):
                self.game_state = self.board[0][x]
                return
        
        # 斜めのラインをチェック（左上→右下）
        if (self.board[0][0] != 0 
                and self.board[0][0] == self.board[1][1] == self.board[2][2]):
            self.game_state = self.board[0][0]
            return
        
        # 斜めのラインをチェック（右上→左下）
        if (self.board[0][2] != 0 
                and self.board[0][2] == self.board[1][1] == self.board[2][0]):
            self.game_state = self.board[0][2]
            return
        
        # 空きマスがあるかチェック
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == 0:
                    # まだゲームは続く
                    return
        
        # すべてのマスが埋まっていて勝者がいない場合は引き分け
        self.game_state = 3
    
    def get_empty_cells(self):
        """空いているマスのリストを返す"""
        empty_cells = []
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == 0:
                    empty_cells.append((x, y))
        return empty_cells
    
    def smart_computer_move(self):
        """コンピュータの手を決める（少し賢い）"""
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return
        
        # 勝てるマスがあれば選ぶ
        for x, y in empty_cells:
            self.board[y][x] = 2  # 試しに置いてみる
            if self.would_win(2):
                # このマスに置けば勝てる
                return
            self.board[y][x] = 0  # 元に戻す
        
        # プレイヤーが勝つのを防ぐ
        for x, y in empty_cells:
            self.board[y][x] = 1  # 試しに相手の手を置いてみる
            if self.would_win(1):
                # このマスに置かれると相手が勝つので防ぐ
                self.board[y][x] = 2
                return
            self.board[y][x] = 0  # 元に戻す
        
        # 中央が空いていれば選ぶ
        if self.board[1][1] == 0:
            self.board[1][1] = 2
            return
        
        # 隅が空いていれば選ぶ
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [corner for corner in corners 
                            if self.board[corner[1]][corner[0]] == 0]
        if available_corners:
            x, y = random.choice(available_corners)
            self.board[y][x] = 2
            return
        
        # それ以外はランダム
        x, y = random.choice(empty_cells)
        self.board[y][x] = 2
    
    def would_win(self, player):
        """指定したプレイヤーが現在の盤面で勝つかどうかをチェック"""
        # 横のラインをチェック
        for y in range(3):
            if self.board[y][0] == self.board[y][1] == self.board[y][2] == player:
                return True
        
        # 縦のラインをチェック
        for x in range(3):
            if self.board[0][x] == self.board[1][x] == self.board[2][x] == player:
                return True
        
        # 斜めのラインをチェック（左上→右下）
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        
        # 斜めのラインをチェック（右上→左下）
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True
        
        return False
    
    def reset_game(self):
        """ゲームをリセット"""
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.game_state = 0
        self.current_player = 1

# ゲームを起動
TicTacToe()
```

### 解説
- `check_game_state()`: 勝敗を判定する関数です
- `computer_move()`: コンピュータの手を決める関数です
- `smart_computer_move()`: 少し賢いコンピュータの思考ルーチンです
- `would_win()`: 特定のプレイヤーが勝つかどうかをチェックします
- `reset_game()`: ゲームをリセットする関数です
- `pyxel.text()`: 文字を表示します
- `pyxel.btnp(pyxel.KEY_R)`: Rキーが押されたかチェックします

## 最終的なコード

上記のコードが最終的な完成版です。このゲームは以下の機能を持っています：

1. マウスクリックで○を配置できます
2. コンピュータがプレイヤーとして×を配置します
3. 勝敗を判定し、勝者または引き分けを表示します
4. Rキーでゲームをリセットできます
5. コンピュータは賢い戦略を持っています：
   - 勝てるマスがあれば選びます
   - プレイヤーの勝利を防ぐマスを選びます
   - 中央を優先します
   - 隅を優先します
   - その他はランダムに選びます

## 発展課題

このゲームをさらに発展させる方法としては以下のような機能が考えられます：

1. 難易度設定（簡単・普通・難しい）
2. プレイヤーの名前入力
3. 勝敗の記録
4. 効果音の追加
5. 2人プレイモード
6. アニメーション効果

ぜひ、自分でアレンジしてみてください！
