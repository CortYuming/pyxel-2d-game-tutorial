# 小学4年生向け Pyxel ラインドロップ作成カリキュラム

![スクリーンショット 2025-06-07 23 28 32](https://github.com/user-attachments/assets/abe516fb-49b8-4688-a068-9382cd58b345)

## レッスン1：基本の画面とブロック表示

### 目標
- ゲーム画面を作る
- ラインドロップゲームのブロックを表示する

### 事前準備
```
pip install pyxel
```

### コード
```python
import pyxel

# 画面とブロックのサイズ設定
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160
BLOCK_SIZE = 10

# ブロックの形（I型）
block = [
    [1, 1, 1, 1]
]

# ブロックの位置
block_x = 3
block_y = 0

class App:
    def __init__(self):
        # 画面の初期化
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="かんたんラインドロップゲーム")
        pyxel.run(self.update, self.draw)
    
    def update(self):
        # ESCキーでゲーム終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
    
    def draw(self):
        # 画面を黒でクリア
        pyxel.cls(0)
        
        # 画面の枠を描く
        pyxel.rectb(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 7)
        
        # ブロックを描く
        self.draw_block()
    
    def draw_block(self):
        # ブロックの描画
        for y in range(len(block)):
            for x in range(len(block[0])):
                if block[y][x] == 1:
                    pyxel.rect(
                        (block_x + x) * BLOCK_SIZE,
                        (block_y + y) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                        11  # 色は水色(11)
                    )

App()
```

### 解説
1. `pyxel.init()` でゲーム画面を作ります
2. `pyxel.run()` でゲームループを開始します
3. `update()` 関数ではキー入力などの処理をします
4. `draw()` 関数では画面に絵を描きます
5. ブロックは二次元リストで表現しています

今回はI型のブロック（一直線の形）を表示しました。実行すると、水色のブロックが画面上部に表示されます。

## レッスン2：ブロックの移動と回転

### 目標
- キー操作でブロックを動かす
- ブロックを回転させる
- ブロックを自動で下に落とす

### コード（レッスン1からの追加部分）

```python
import pyxel
import time

# 画面とブロックのサイズ設定
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160
BLOCK_SIZE = 10

# ブロックの形（複数種類）
BLOCKS = [
    [[1, 1, 1, 1]],  # I型
    [[1, 1], [1, 1]],  # O型
    [[0, 1, 0], [1, 1, 1]],  # T型
]

# 現在のブロック
current_block = BLOCKS[0]  # 最初はI型
block_x = 3
block_y = 0

# 最後に下に動いた時間
last_drop_time = time.time()

class App:
    def __init__(self):
        # 画面の初期化
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="かんたんラインドロップゲーム")
        pyxel.run(self.update, self.draw)
    
    def update(self):
        global current_block, block_x, block_y, last_drop_time, current_block
        
        # ESCキーでゲーム終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # 左右移動
        if pyxel.btnp(pyxel.KEY_LEFT):
            if self.can_move(block_x - 1, block_y):
                block_x -= 1
        
        if pyxel.btnp(pyxel.KEY_RIGHT):
            if self.can_move(block_x + 1, block_y):
                block_x += 1
        
        # 下に移動
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.can_move(block_x, block_y + 1):
                block_y += 1
        
        # 回転（スペースキー）
        if pyxel.btnp(pyxel.KEY_SPACE):
            rotated = self.rotate_block(current_block)
            # 回転後の位置が有効かチェック
            if self.can_place(rotated, block_x, block_y):
                current_block = rotated
        
        # 一定時間ごとに自動で落下
        current_time = time.time()
        if current_time - last_drop_time >= 1.0:  # 1秒ごとに落下
            if self.can_move(block_x, block_y + 1):
                block_y += 1
            last_drop_time = current_time
    
    def can_move(self, new_x, new_y):
        # 移動先が有効かチェック
        width = len(current_block[0])
        height = len(current_block)
        
        # 左右の壁判定
        if new_x < 0 or new_x + width > SCREEN_WIDTH // BLOCK_SIZE:
            return False
        
        # 下の壁判定
        if new_y + height > SCREEN_HEIGHT // BLOCK_SIZE:
            return False
        
        return True
    
    def can_place(self, block, x, y):
        # ブロックを置けるかチェック
        width = len(block[0])
        height = len(block)
        
        if x < 0 or x + width > SCREEN_WIDTH // BLOCK_SIZE:
            return False
        
        if y + height > SCREEN_HEIGHT // BLOCK_SIZE:
            return False
        
        return True
    
    def rotate_block(self, block):
        # ブロックを90度回転
        height = len(block)
        width = len(block[0])
        
        # 回転後の新しい形を作る
        rotated = [[0 for _ in range(height)] for _ in range(width)]
        
        for y in range(height):
            for x in range(width):
                rotated[x][height - 1 - y] = block[y][x]
        
        return rotated
    
    def draw(self):
        # 画面を黒でクリア
        pyxel.cls(0)
        
        # 画面の枠を描く
        pyxel.rectb(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 7)
        
        # ブロックを描く
        self.draw_block()
    
    def draw_block(self):
        # ブロックの描画
        for y in range(len(current_block)):
            for x in range(len(current_block[0])):
                if current_block[y][x] == 1:
                    pyxel.rect(
                        (block_x + x) * BLOCK_SIZE,
                        (block_y + y) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                        11  # 色は水色(11)
                    )

App()
```

### 解説
1. 矢印キー「←」「→」でブロックを左右に動かせます
2. 矢印キー「↓」でブロックを下に動かせます
3. スペースキーでブロックを回転できます
4. 自動で1秒ごとにブロックが下に落ちます
5. `can_move()` 関数で画面の外に出ないかチェックします
6. `rotate_block()` 関数でブロックを90度回転させます

ブロックの動きを確認してみましょう。画面の端を超えて移動できないようになっています。

## レッスン3：ゲームのルール実装

### 目標
- ブロックが積み重なるようにする
- ラインがそろったら消す
- ゲームオーバーの判定をする

### 最終コード

```python
import pyxel
import time
import random

# 画面とブロックのサイズ設定
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160
BLOCK_SIZE = 10
FIELD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
FIELD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# ブロックの形（複数種類）
BLOCKS = [
    [[1, 1, 1, 1]],  # I型
    [[1, 1], [1, 1]],  # O型
    [[0, 1, 0], [1, 1, 1]],  # T型
    [[1, 0], [1, 0], [1, 1]],  # L型
]

# ブロックの色
COLORS = [11, 10, 9, 8]

# フィールド（積み重なったブロック）
field = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]

# 現在のブロック
current_block = None
block_x = 0
block_y = 0
block_color = 0

# 最後に下に動いた時間
last_drop_time = time.time()

# ゲームオーバーフラグ
game_over = False

# スコア
score = 0

class App:
    def __init__(self):
        # 画面の初期化
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="かんたんラインドロップゲーム")
        self.new_block()  # 最初のブロックを作成
        pyxel.run(self.update, self.draw)
    
    def new_block(self):
        global current_block, block_x, block_y, block_color
        
        # ランダムにブロックを選ぶ
        idx = random.randint(0, len(BLOCKS) - 1)
        current_block = BLOCKS[idx]
        block_color = COLORS[idx]
        
        # 開始位置を設定
        block_x = FIELD_WIDTH // 2 - len(current_block[0]) // 2
        block_y = 0
        
        # ブロックを置けない場合はゲームオーバー
        if not self.can_place(current_block, block_x, block_y):
            global game_over
            game_over = True
    
    def update(self):
        global current_block, block_x, block_y, last_drop_time, game_over, score
        
        # ゲームオーバーなら何もしない
        if game_over:
            if pyxel.btnp(pyxel.KEY_R):  # Rキーでリスタート
                self.restart_game()
            return
        
        # ESCキーでゲーム終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        # 左右移動
        if pyxel.btnp(pyxel.KEY_LEFT):
            if self.can_move(block_x - 1, block_y):
                block_x -= 1
        
        if pyxel.btnp(pyxel.KEY_RIGHT):
            if self.can_move(block_x + 1, block_y):
                block_x += 1

        # 下に移動
        if pyxel.btnp(pyxel.KEY_DOWN):
            if self.can_move(block_x, block_y + 1):
                block_y += 1
            else:
                self.place_block()
        
        # 回転（スペースキー）
        if pyxel.btnp(pyxel.KEY_SPACE):
            rotated = self.rotate_block(current_block)
            # 回転後の位置が有効かチェック
            if self.can_place(rotated, block_x, block_y):
                current_block = rotated
        
        # 一定時間ごとに自動で落下
        current_time = time.time()
        if current_time - last_drop_time >= 1.0:  # 1秒ごとに落下
            if self.can_move(block_x, block_y + 1):
                block_y += 1
            else:
                self.place_block()
            last_drop_time = current_time
    
    def restart_game(self):
        global field, game_over, score
        field = [[0 for _ in range(FIELD_WIDTH)] for _ in range(FIELD_HEIGHT)]
        game_over = False
        score = 0
        self.new_block()
    
    def can_move(self, new_x, new_y):
        return self.can_place(current_block, new_x, new_y)
    
    def can_place(self, block, x, y):
        # ブロックを置けるかチェック
        height = len(block)
        width = len(block[0])
        
        for ty in range(height):
            for tx in range(width):
                if block[ty][tx] == 0:
                    continue
                
                pos_x = x + tx
                pos_y = y + ty
                
                # 画面外チェック
                if pos_x < 0 or pos_x >= FIELD_WIDTH or pos_y >= FIELD_HEIGHT:
                    return False
                
                # 既存ブロックとの衝突チェック
                if pos_y >= 0 and field[pos_y][pos_x] != 0:
                    return False
        
        return True
    
    def rotate_block(self, block):
        # ブロックを90度回転
        height = len(block)
        width = len(block[0])
        
        # 回転後の新しい形を作る
        rotated = [[0 for _ in range(height)] for _ in range(width)]
        
        for y in range(height):
            for x in range(width):
                rotated[x][height - 1 - y] = block[y][x]
        
        return rotated
    
    def place_block(self):
        # ブロックをフィールドに固定
        height = len(current_block)
        width = len(current_block[0])
        
        for y in range(height):
            for x in range(width):
                if current_block[y][x] == 0:
                    continue
                
                pos_y = block_y + y
                pos_x = block_x + x
                
                # フィールド内ならブロックを配置
                if 0 <= pos_y < FIELD_HEIGHT and 0 <= pos_x < FIELD_WIDTH:
                    field[pos_y][pos_x] = block_color
        
        # ラインの削除チェック
        self.check_lines()
        
        # 新しいブロックを作成
        self.new_block()
    
    def check_lines(self):
        global field, score
        lines_cleared = 0
        
        # 下から順にチェック
        y = FIELD_HEIGHT - 1
        while y >= 0:
            is_line_full = True
            
            # 1行が全て埋まっているかチェック
            for x in range(FIELD_WIDTH):
                if field[y][x] == 0:
                    is_line_full = False
                    break
            
            if is_line_full:
                # ラインを消して上のブロックを下に移動
                lines_cleared += 1
                
                # 消したラインより上を1行下に移動
                for y2 in range(y, 0, -1):
                    for x in range(FIELD_WIDTH):
                        field[y2][x] = field[y2-1][x]
                
                # 一番上の行をクリア
                for x in range(FIELD_WIDTH):
                    field[0][x] = 0
            else:
                y -= 1
        
        # スコア加算（消したライン数に応じて）
        if lines_cleared > 0:
            score += lines_cleared * 100
    
    def draw(self):
        # 画面を黒でクリア
        pyxel.cls(0)
        
        # 画面の枠を描く
        pyxel.rectb(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 7)
        
        # フィールドのブロックを描く
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                if field[y][x] != 0:
                    pyxel.rect(
                        x * BLOCK_SIZE,
                        y * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                        field[y][x]
                    )
        
        # ブロックを描く
        if not game_over:
            self.draw_block()
        
        # スコア表示
        pyxel.text(2, 2, f"SCORE: {score}", 7)
        
        # ゲームオーバー表示
        if game_over:
            pyxel.text(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 10, "GAME OVER", 8)
            pyxel.text(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 10, "R: RESTART", 7)
    
    def draw_block(self):
        # ブロックの描画
        for y in range(len(current_block)):
            for x in range(len(current_block[0])):
                if current_block[y][x] == 1:
                    pyxel.rect(
                        (block_x + x) * BLOCK_SIZE,
                        (block_y + y) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE,
                        block_color
                    )

App()
```

### 解説
1. ブロックが下に落ちたら `place_block()` でフィールドに固定します
2. `check_lines()` で揃ったラインを消し、上のブロックを下に下げます
3. `new_block()` で新しいブロックを作成します
4. ブロックを置けない場合は「GAME OVER」になります
5. Rキーでゲームを再スタートできます
6. スコアが表示されます（ライン消去で100点×消した行数）

これで基本的なラインドロップゲームゲームの完成です！上手くブロックを操作して、たくさんのラインを消しましょう。
