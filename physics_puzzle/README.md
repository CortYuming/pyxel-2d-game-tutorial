# 物理パズルゲーム作成チュートリアル（全3回）

<img width="1072" height="860" alt="スクリーンショット 2025-09-21 9 02 57" src="https://github.com/user-attachments/assets/3978dc4f-a09f-4edc-87fa-e5944938970b" />

## 第1回：基本的な画面とボールを作ろう

### 学習内容
- pyxelの基本的な使い方を覚える
- ボールを画面に表示して動かす
- 重力の仕組みを理解する

### 完成コード

```python
import pyxel
import math


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0  # 横の速度
        self.vy = 0  # 縦の速度
        self.radius = 4
        self.color = 8  # 赤色

    def update(self):
        # 重力を加える
        self.vy += 0.2
        
        # 位置を更新
        self.x += self.vx
        self.y += self.vy
        
        # 地面との当たり判定
        if self.y > 120 - self.radius:
            self.y = 120 - self.radius
            self.vy *= -0.7  # 跳ね返り
            self.vx *= 0.9   # 摩擦
    def draw(self):
        pyxel.circb(self.x, self.y, self.radius, self.color)


class Game:
    def __init__(self):
        pyxel.init(160, 120)
        self.ball = Ball(80, 20)
        pyxel.run(self.update, self.draw)

    def update(self):
        # スペースキーでボールをリセット
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.ball = Ball(80, 20)
        
        self.ball.update()

    def draw(self):
        pyxel.cls(12)  # 薄い青色の背景
        
        # 地面を描く
        pyxel.rect(0, 120, 160, 8, 3)  # 緑色の地面
        
        self.ball.draw()


Game()
```

### 理解しよう
1. **Ball クラス**: ボールの位置と動きを管理
2. **重力**: `self.vy += 0.2` で下向きの力を加える
3. **跳ね返り**: 地面に当たったら速度を反転させる

---

## 第2回：ボールを飛ばして的を作ろう

### 学習内容
- マウスでボールを飛ばす仕組みを作る
- 的（ブロック）を置く
- 当たり判定を実装する

### 追加・変更部分

```python
# Ball クラスに追加
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = 4
        self.color = 8
        self.launched = False  # 追加：発射されたかどうか

    def launch(self, target_x, target_y):
        # 発射の力を計算
        dx = target_x - self.x
        dy = target_y - self.y
        power = min(math.sqrt(dx * dx + dy * dy) / 10, 8)
        
        angle = math.atan2(dy, dx)
        self.vx = math.cos(angle) * power
        self.vy = math.sin(angle) * power
        self.launched = True

    def reset(self):
        self.x = 30
        self.y = 100
        self.vx = 0
        self.vy = 0
        self.launched = False


# 新しいクラス
class Block:
    def __init__(self, x, y, width=16, height=16):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = 9  # オレンジ色
        self.alive = True

    def check_collision(self, ball):
        if not self.alive:
            return False
            
        # 長方形と円の当たり判定
        closest_x = max(self.x, min(ball.x, self.x + self.width))
        closest_y = max(self.y, min(ball.y, self.y + self.height))
        
        distance = math.sqrt((ball.x - closest_x) ** 2 + 
                           (ball.y - closest_y) ** 2)
        
        if distance < ball.radius:
            self.alive = False
            return True
        return False

    def draw(self):
        if self.alive:
            pyxel.rect(self.x, self.y, self.width, self.height, self.color)


# Game クラスの変更部分
class Game:
    def __init__(self):
        pyxel.init(160, 120)
        self.ball = Ball(30, 100)
        self.blocks = [
            Block(120, 80),
            Block(120, 64),
            Block(136, 80),
            Block(136, 64)
        ]
        pyxel.run(self.update, self.draw)

    def update(self):
        # マウスクリックで発射
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and not self.ball.launched:
            self.ball.launch(pyxel.mouse_x, pyxel.mouse_y)
        
        # スペースキーでリセット
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.ball.reset()
            for block in self.blocks:
                block.alive = True
        
        if self.ball.launched:
            self.ball.update()
            
            # ブロックとの当たり判定
            for block in self.blocks:
                if block.check_collision(self.ball):
                    self.ball.vx *= -0.5
                    self.ball.vy *= -0.5

    def draw(self):
        pyxel.cls(12)
        pyxel.rect(0, 120, 160, 8, 3)
        
        # 発射前の軌道予測線
        if not self.ball.launched:
            pyxel.line(self.ball.x, self.ball.y, 
                      pyxel.mouse_x, pyxel.mouse_y, 7)
        
        self.ball.draw()
        
        for block in self.blocks:
            block.draw()
```

### 理解しよう
1. **発射システム**: マウスの位置までの距離と角度を計算
2. **当たり判定**: 円と長方形の距離を測って判定
3. **軌道予測**: 発射前にマウスまでの線を表示

---

## 第3回：完成版を作ろう

### 学習内容
- スコアシステムを追加
- ゲームオーバーとクリア判定
- 画面外判定の追加

### 追加・変更部分

```python
# Game クラスに追加
class Game:
    def __init__(self):
        pyxel.init(160, 120)
        self.ball = Ball(30, 100)
        self.blocks = [
            Block(120, 80),
            Block(120, 64),
            Block(136, 80),
            Block(136, 64)
        ]
        self.score = 0
        self.shots = 3  # 残り発射回数
        self.game_over = False
        self.game_clear = False
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over or self.game_clear:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return
        
        # マウスクリックで発射
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and not self.ball.launched:
            if self.shots > 0:
                self.ball.launch(pyxel.mouse_x, pyxel.mouse_y)
                self.shots -= 1
        
        # スペースキーでリセット
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.ball.reset()
        
        if self.ball.launched:
            self.ball.update()
            
            # 画面外判定
            if (self.ball.x < 0 or self.ball.x > 160 or 
                self.ball.y > 120):
                self.ball.reset()
            
            # ブロックとの当たり判定
            for block in self.blocks:
                if block.check_collision(self.ball):
                    self.ball.vx *= -0.5
                    self.ball.vy *= -0.5
                    self.score += 10
        
        # クリア判定
        if all(not block.alive for block in self.blocks):
            self.game_clear = True
        
        # ゲームオーバー判定
        if self.shots == 0 and not self.ball.launched:
            if any(block.alive for block in self.blocks):
                self.game_over = True

    def reset_game(self):
        self.ball.reset()
        self.score = 0
        self.shots = 3
        self.game_over = False
        self.game_clear = False
        for block in self.blocks:
            block.alive = True

    def draw(self):
        pyxel.cls(12)
        pyxel.rect(0, 120, 160, 8, 3)
        
        # UI表示
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(5, 15, f"Shots: {self.shots}", 7)
        
        # ゲーム状態表示
        if self.game_clear:
            pyxel.text(50, 50, "GAME CLEAR!", 10)
            pyxel.text(40, 65, "Press R to Restart", 7)
        elif self.game_over:
            pyxel.text(50, 50, "GAME OVER!", 8)
            pyxel.text(40, 65, "Press R to Restart", 7)
        else:
            # 発射前の軌道予測線
            if not self.ball.launched and self.shots > 0:
                pyxel.line(self.ball.x, self.ball.y, 
                          pyxel.mouse_x, pyxel.mouse_y, 7)
        
        self.ball.draw()
        
        for block in self.blocks:
            block.draw()
```

### 最終完成コード

```python
import pyxel
import math


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = 4
        self.color = 8
        self.launched = False

    def update(self):
        self.vy += 0.2
        self.x += self.vx
        self.y += self.vy
        
        if self.y > 120 - self.radius:
            self.y = 120 - self.radius
            self.vy *= -0.7
            self.vx *= 0.9

    def launch(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        power = min(math.sqrt(dx * dx + dy * dy) / 10, 8)
        
        angle = math.atan2(dy, dx)
        self.vx = math.cos(angle) * power
        self.vy = math.sin(angle) * power
        self.launched = True

    def reset(self):
        self.x = 30
        self.y = 100
        self.vx = 0
        self.vy = 0
        self.launched = False

    def draw(self):
        pyxel.circb(self.x, self.y, self.radius, self.color)


class Block:
    def __init__(self, x, y, width=16, height=16):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = 9
        self.alive = True

    def check_collision(self, ball):
        if not self.alive:
            return False
            
        closest_x = max(self.x, min(ball.x, self.x + self.width))
        closest_y = max(self.y, min(ball.y, self.y + self.height))
        
        distance = math.sqrt((ball.x - closest_x) ** 2 + 
                           (ball.y - closest_y) ** 2)
        
        if distance < ball.radius:
            self.alive = False
            return True
        return False

    def draw(self):
        if self.alive:
            pyxel.rect(self.x, self.y, self.width, self.height, self.color)


class Game:
    def __init__(self):
        pyxel.init(160, 120)
        self.ball = Ball(30, 100)
        self.blocks = [
            Block(120, 80),
            Block(120, 64),
            Block(136, 80),
            Block(136, 64)
        ]
        self.score = 0
        self.shots = 3
        self.game_over = False
        self.game_clear = False
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over or self.game_clear:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and not self.ball.launched:
            if self.shots > 0:
                self.ball.launch(pyxel.mouse_x, pyxel.mouse_y)
                self.shots -= 1
        
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.ball.reset()
        
        if self.ball.launched:
            self.ball.update()
            
            if (self.ball.x < 0 or self.ball.x > 160 or 
                self.ball.y > 120):
                self.ball.reset()
            
            for block in self.blocks:
                if block.check_collision(self.ball):
                    self.ball.vx *= -0.5
                    self.ball.vy *= -0.5
                    self.score += 10
        
        if all(not block.alive for block in self.blocks):
            self.game_clear = True
        
        if self.shots == 0 and not self.ball.launched:
            if any(block.alive for block in self.blocks):
                self.game_over = True

    def reset_game(self):
        self.ball.reset()
        self.score = 0
        self.shots = 3
        self.game_over = False
        self.game_clear = False
        for block in self.blocks:
            block.alive = True

    def draw(self):
        pyxel.cls(12)
        pyxel.rect(0, 120, 160, 8, 3)
        
        pyxel.text(5, 5, f"Score: {self.score}", 7)
        pyxel.text(5, 15, f"Shots: {self.shots}", 7)
        
        if self.game_clear:
            pyxel.text(50, 50, "GAME CLEAR!", 10)
            pyxel.text(40, 65, "Press R to Restart", 7)
        elif self.game_over:
            pyxel.text(50, 50, "GAME OVER!", 8)
            pyxel.text(40, 65, "Press R to Restart", 7)
        else:
            if not self.ball.launched and self.shots > 0:
                pyxel.line(self.ball.x, self.ball.y, 
                          pyxel.mouse_x, pyxel.mouse_y, 7)
        
        self.ball.draw()
        
        for block in self.blocks:
            block.draw()


Game()
```

### 完成！
おめでとうございます！物理パズルゲームが完成しました。

**操作方法:**
- マウスクリック：ボールを発射
- スペースキー：ボールをリセット
- Rキー：ゲーム再開

**学んだこと:**
1. オブジェクト指向プログラミング
2. 物理計算（重力、当たり判定）
3. ゲームループの仕組み
4. UIとゲーム状態の管理
