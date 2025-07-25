# pyxel格闘ゲーム作成カリキュラム（全3回）

<img width="1072" height="940" alt="fighting_gameスクリーンショット 2025-07-16 17 25 08" src="https://github.com/user-attachments/assets/c79538e6-783f-4c74-9d1d-c04dc1c0fe65" />

- [pyxel格闘ゲーム作成カリキュラム（全3回）](#pyxel格闘ゲーム作成カリキュラム全3回)
  - [第1回：キャラクターの表示と移動](#第1回キャラクターの表示と移動)
    - [目標](#目標)
    - [作成するもの](#作成するもの)
    - [コード](#コード)
    - [操作方法](#操作方法)
  - [第2回：攻撃システムの追加](#第2回攻撃システムの追加)
    - [目標](#目標-1)
    - [追加・変更するコード](#追加変更するコード)
    - [追加操作](#追加操作)
  - [第3回：ゲーム完成とエフェクト](#第3回ゲーム完成とエフェクト)
    - [目標](#目標-2)
    - [追加・変更するコード](#追加変更するコード-1)
    - [最終完成コード](#最終完成コード)
    - [完成機能](#完成機能)
    - [全操作方法まとめ](#全操作方法まとめ)


## 第1回：キャラクターの表示と移動

### 目標
- 2人のキャラクターを画面に表示する
- キーボードで左右移動とジャンプができる

### 作成するもの
- 基本的なキャラクター（四角形）
- 左右移動機能
- ジャンプ機能
- 重力システム

### コード

```python
import pyxel


class Fighter:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        self.width = 16
        self.height = 24

    def update(self):
        # 重力
        if not self.on_ground:
            self.vy += 0.5

        # 位置更新
        self.x += self.vx
        self.y += self.vy

        # 地面判定
        if self.y >= 160:
            self.y = 160
            self.vy = 0
            self.on_ground = True

        # 画面端判定
        if self.x < 0:
            self.x = 0
        elif self.x > 240 - self.width:
            self.x = 240 - self.width

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)


class Game:
    def __init__(self):
        pyxel.init(240, 200)
        self.player1 = Fighter(50, 160, 8)
        self.player2 = Fighter(170, 160, 11)
        pyxel.run(self.update, self.draw)

    def update(self):
        # プレイヤー1の操作
        self.player1.vx = 0
        if pyxel.btn(pyxel.KEY_A):
            self.player1.vx = -2
        if pyxel.btn(pyxel.KEY_D):
            self.player1.vx = 2
        if pyxel.btnp(pyxel.KEY_W) and self.player1.on_ground:
            self.player1.vy = -8
            self.player1.on_ground = False

        # プレイヤー2の操作
        self.player2.vx = 0
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player2.vx = -2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player2.vx = 2
        if pyxel.btnp(pyxel.KEY_UP) and self.player2.on_ground:
            self.player2.vy = -8
            self.player2.on_ground = False

        self.player1.update()
        self.player2.update()

    def draw(self):
        pyxel.cls(1)
        # 地面
        pyxel.rect(0, 184, 240, 16, 3)
        self.player1.draw()
        self.player2.draw()


Game()
```

### 操作方法
- プレイヤー1：A・D（左右移動）、W（ジャンプ）
- プレイヤー2：矢印キー（左右移動・ジャンプ）

---

## 第2回：攻撃システムの追加

### 目標
- パンチ攻撃を追加する
- 当たり判定を作る
- 体力システムを作る

### 追加・変更するコード

```python
class Fighter:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        self.width = 16
        self.height = 24
        self.hp = 100  # 追加
        self.is_attacking = False  # 追加
        self.attack_timer = 0  # 追加

    def update(self):
        # 攻撃タイマー更新
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.is_attacking = False

        # 重力
        if not self.on_ground:
            self.vy += 0.5

        # 位置更新
        self.x += self.vx
        self.y += self.vy

        # 地面判定
        if self.y >= 160:
            self.y = 160
            self.vy = 0
            self.on_ground = True

        # 画面端判定
        if self.x < 0:
            self.x = 0
        elif self.x > 240 - self.width:
            self.x = 240 - self.width

    def attack(self):  # 追加
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = 10

    def get_attack_rect(self):  # 追加
        if self.is_attacking:
            return (self.x + self.width, self.y + 8, 20, 8)
        return None

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)
        # 攻撃エフェクト
        if self.is_attacking:
            pyxel.rect(self.x + self.width, self.y + 8, 20, 8, 10)


class Game:
    def __init__(self):
        pyxel.init(240, 200)
        self.player1 = Fighter(50, 160, 8)
        self.player2 = Fighter(170, 160, 11)
        pyxel.run(self.update, self.draw)

    def check_collision(self, rect1, rect2):  # 追加
        if rect1 is None or rect2 is None:
            return False
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)

    def update(self):
        # プレイヤー1の操作
        self.player1.vx = 0
        if pyxel.btn(pyxel.KEY_A):
            self.player1.vx = -2
        if pyxel.btn(pyxel.KEY_D):
            self.player1.vx = 2
        if pyxel.btnp(pyxel.KEY_W) and self.player1.on_ground:
            self.player1.vy = -8
            self.player1.on_ground = False
        if pyxel.btnp(pyxel.KEY_S):  # 追加
            self.player1.attack()

        # プレイヤー2の操作
        self.player2.vx = 0
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player2.vx = -2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player2.vx = 2
        if pyxel.btnp(pyxel.KEY_UP) and self.player2.on_ground:
            self.player2.vy = -8
            self.player2.on_ground = False
        if pyxel.btnp(pyxel.KEY_DOWN):  # 追加
            self.player2.attack()

        self.player1.update()
        self.player2.update()

        # 当たり判定チェック
        p1_attack = self.player1.get_attack_rect()
        p2_rect = (self.player2.x, self.player2.y, self.player2.width, self.player2.height)
        if self.check_collision(p1_attack, p2_rect):
            self.player2.hp -= 10

        p2_attack = self.player2.get_attack_rect()
        p1_rect = (self.player1.x, self.player1.y, self.player1.width, self.player1.height)
        if self.check_collision(p2_attack, p1_rect):
            self.player1.hp -= 10

    def draw(self):
        pyxel.cls(1)
        # 地面
        pyxel.rect(0, 184, 240, 16, 3)
        self.player1.draw()
        self.player2.draw()
        
        # 体力表示
        pyxel.text(10, 10, f"P1: {self.player1.hp}", 7)
        pyxel.text(180, 10, f"P2: {self.player2.hp}", 7)
```

### 追加操作
- プレイヤー1：S（攻撃）
- プレイヤー2：下矢印（攻撃）

---

## 第3回：ゲーム完成とエフェクト

### 目標
- 勝敗判定を追加する
- ゲームオーバー画面を作る
- 音とエフェクトを追加する

### 追加・変更するコード

```python
class Game:
    def __init__(self):
        pyxel.init(240, 200)
        self.player1 = Fighter(50, 160, 8)
        self.player2 = Fighter(170, 160, 11)
        self.game_over = False  # 追加
        self.winner = None  # 追加
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over:  # 追加
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.restart_game()
            return

        # プレイヤー1の操作
        self.player1.vx = 0
        if pyxel.btn(pyxel.KEY_A):
            self.player1.vx = -2
        if pyxel.btn(pyxel.KEY_D):
            self.player1.vx = 2
        if pyxel.btnp(pyxel.KEY_W) and self.player1.on_ground:
            self.player1.vy = -8
            self.player1.on_ground = False
        if pyxel.btnp(pyxel.KEY_S):
            self.player1.attack()

        # プレイヤー2の操作
        self.player2.vx = 0
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player2.vx = -2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player2.vx = 2
        if pyxel.btnp(pyxel.KEY_UP) and self.player2.on_ground:
            self.player2.vy = -8
            self.player2.on_ground = False
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.player2.attack()

        self.player1.update()
        self.player2.update()

        # 当たり判定チェック
        p1_attack = self.player1.get_attack_rect()
        p2_rect = (self.player2.x, self.player2.y, self.player2.width, self.player2.height)
        if self.check_collision(p1_attack, p2_rect):
            self.player2.hp -= 10

        p2_attack = self.player2.get_attack_rect()
        p1_rect = (self.player1.x, self.player1.y, self.player1.width, self.player1.height)
        if self.check_collision(p2_attack, p1_rect):
            self.player1.hp -= 10

        # 勝敗判定
        if self.player1.hp <= 0:
            self.game_over = True
            self.winner = "Player 2"
        elif self.player2.hp <= 0:
            self.game_over = True
            self.winner = "Player 1"

    def restart_game(self):  # 追加
        self.player1 = Fighter(50, 160, 8)
        self.player2 = Fighter(170, 160, 11)
        self.game_over = False
        self.winner = None

    def draw(self):
        pyxel.cls(1)
        # 地面
        pyxel.rect(0, 184, 240, 16, 3)
        self.player1.draw()
        self.player2.draw()
        
        # 体力表示
        pyxel.text(10, 10, f"P1: {self.player1.hp}", 7)
        pyxel.text(180, 10, f"P2: {self.player2.hp}", 7)

        # ゲームオーバー画面
        if self.game_over:
            pyxel.rect(60, 80, 120, 40, 0)
            pyxel.rectb(60, 80, 120, 40, 7)
            pyxel.text(90, 90, f"{self.winner} WIN!", 7)
            pyxel.text(70, 105, "SPACE: Restart", 7)
```

### 最終完成コード

```python
import pyxel


class Fighter:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = 0
        self.vy = 0
        self.on_ground = True
        self.width = 16
        self.height = 24
        self.hp = 100
        self.is_attacking = False
        self.attack_timer = 0

    def update(self):
        # 攻撃タイマー更新
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.is_attacking = False

        # 重力
        if not self.on_ground:
            self.vy += 0.5

        # 位置更新
        self.x += self.vx
        self.y += self.vy

        # 地面判定
        if self.y >= 160:
            self.y = 160
            self.vy = 0
            self.on_ground = True

        # 画面端判定
        if self.x < 0:
            self.x = 0
        elif self.x > 240 - self.width:
            self.x = 240 - self.width

    def attack(self):
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = 10

    def get_attack_rect(self):
        if self.is_attacking:
            return (self.x + self.width, self.y + 8, 20, 8)
        return None

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)
        # 攻撃エフェクト
        if self.is_attacking:
            pyxel.rect(self.x + self.width, self.y + 8, 20, 8, 10)


class Game:
    def __init__(self):
        pyxel.init(240, 200)
        self.player1 = Fighter(50, 160, 8)
        self.player2 = Fighter(170, 160, 11)
        self.game_over = False
        self.winner = None
        pyxel.run(self.update, self.draw)

    def check_collision(self, rect1, rect2):
        if rect1 is None or rect2 is None:
            return False
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.restart_game()
            return

        # プレイヤー1の操作
        self.player1.vx = 0
        if pyxel.btn(pyxel.KEY_A):
            self.player1.vx = -2
        if pyxel.btn(pyxel.KEY_D):
            self.player1.vx = 2
        if pyxel.btnp(pyxel.KEY_W) and self.player1.on_ground:
            self.player1.vy = -8
            self.player1.on_ground = False
        if pyxel.btnp(pyxel.KEY_S):
            self.player1.attack()

        # プレイヤー2の操作
        self.player2.vx = 0
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player2.vx = -2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player2.vx = 2
        if pyxel.btnp(pyxel.KEY_UP) and self.player2.on_ground:
            self.player2.vy = -8
            self.player2.on_ground = False
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.player2.attack()

        self.player1.update()
        self.player2.update()

        # 当たり判定チェック
        p1_attack = self.player1.get_attack_rect()
        p2_rect = (self.player2.x, self.player2.y, self.player2.width, self.player2.height)
        if self.check_collision(p1_attack, p2_rect):
            self.player2.hp -= 10

        p2_attack = self.player2.get_attack_rect()
        p1_rect = (self.player1.x, self.player1.y, self.player1.width, self.player1.height)
        if self.check_collision(p2_attack, p1_rect):
            self.player1.hp -= 10

        # 勝敗判定
        if self.player1.hp <= 0:
            self.game_over = True
            self.winner = "Player 2"
        elif self.player2.hp <= 0:
            self.game_over = True
            self.winner = "Player 1"

    def restart_game(self):
        self.player1 = Fighter(50, 160, 8)
        self.player2 = Fighter(170, 160, 11)
        self.game_over = False
        self.winner = None

    def draw(self):
        pyxel.cls(1)
        # 地面
        pyxel.rect(0, 184, 240, 16, 3)
        self.player1.draw()
        self.player2.draw()
        
        # 体力表示
        pyxel.text(10, 10, f"P1: {self.player1.hp}", 7)
        pyxel.text(180, 10, f"P2: {self.player2.hp}", 7)

        # ゲームオーバー画面
        if self.game_over:
            pyxel.rect(60, 80, 120, 40, 0)
            pyxel.rectb(60, 80, 120, 40, 7)
            pyxel.text(90, 90, f"{self.winner} WIN!", 7)
            pyxel.text(70, 105, "SPACE: Restart", 7)


Game()
```

### 完成機能
- 2人対戦格闘ゲーム
- 移動・ジャンプ・攻撃システム
- 体力・当たり判定システム
- 勝敗判定・リスタート機能

### 全操作方法まとめ
- プレイヤー1：A・D（移動）、W（ジャンプ）、S（攻撃）
- プレイヤー2：矢印キー（移動・ジャンプ・攻撃）
- スペースキー：ゲーム再開
