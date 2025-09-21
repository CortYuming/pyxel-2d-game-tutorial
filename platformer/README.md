# pyxelプラットフォーマー作成カリキュラム（全4回）

<img width="1072" height="940" alt="スクリーンショット 2025-09-21 15 08 17" src="https://github.com/user-attachments/assets/32176032-a34c-4b78-802d-23e0e0e5df61" />

- [pyxelプラットフォーマー作成カリキュラム（全4回）](#pyxelプラットフォーマー作成カリキュラム全4回)
  - [第1回：基本移動とジャンプ](#第1回基本移動とジャンプ)
    - [目標](#目標)
    - [作成するもの](#作成するもの)
    - [コード](#コード)
    - [操作方法](#操作方法)
    - [ポイント解説](#ポイント解説)
  - [第2回：マップタイルと衝突判定](#第2回マップタイルと衝突判定)
    - [目標](#目標-1)
    - [追加・変更するコード](#追加変更するコード)
    - [ポイント解説](#ポイント解説-1)
  - [第3回：敵・アイテム・アニメーション](#第3回敵アイテムアニメーション)
    - [目標](#目標-2)
    - [追加・変更するコード](#追加変更するコード-1)
    - [ポイント解説](#ポイント解説-2)
  - [第4回：マルチステージとゲーム完成](#第4回マルチステージとゲーム完成)
    - [目標](#目標-3)
    - [追加・変更するコード](#追加変更するコード-2)
    - [最終完成コード](#最終完成コード)
    - [完成機能](#完成機能)
    - [全操作方法まとめ](#全操作方法まとめ)


## 第1回：基本移動とジャンプ

### 目標
- プレイヤーキャラクターを作成する
- 左右移動とジャンプを実装する
- 重力システムを理解する

### 作成するもの
- プレイヤーキャラクター（四角形）
- 左右移動システム
- ジャンプと重力の物理演算
- 地面との衝突判定

### コード

```python
import pyxel


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = 12
        self.height = 16
        self.on_ground = False
        self.speed = 2
        self.jump_power = -6
        self.gravity = 0.3
        self.ground_y = 180
        
    def update(self):
        # 左右移動
        self.vx = 0
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.vx = -self.speed
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.vx = self.speed
        
        # ジャンプ
        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_UP) or 
            pyxel.btnp(pyxel.KEY_W)) and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False
        
        # 重力適用
        self.vy += self.gravity
        
        # 位置更新
        self.x += self.vx
        self.y += self.vy
        
        # 地面との衝突判定
        if self.y + self.height >= self.ground_y:
            self.y = self.ground_y - self.height
            self.vy = 0
            self.on_ground = True
        
        # 画面端判定
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > 240:
            self.x = 240 - self.width
    
    def draw(self):
        # プレイヤー本体
        pyxel.rect(self.x, self.y, self.width, self.height, 8)
        # 顔
        pyxel.pset(self.x + 3, self.y + 4, 7)
        pyxel.pset(self.x + 8, self.y + 4, 7)
        pyxel.rect(self.x + 4, self.y + 8, 4, 2, 7)


class Game:
    def __init__(self):
        pyxel.init(240, 200, title="Platformer")
        self.player = Player(120, 160)
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.player.update()
    
    def draw(self):
        pyxel.cls(12)  # 空色の背景
        
        # 地面
        pyxel.rect(0, 180, 240, 20, 3)
        
        # プレイヤー描画
        self.player.draw()
        
        # UI表示
        pyxel.text(5, 5, "Move: Arrow keys or WASD", 7)
        pyxel.text(5, 15, "Jump: Space/Up/W", 7)


Game()
```

### 操作方法
- 移動：矢印キー または WASD
- ジャンプ：スペース / 上矢印 / W

### ポイント解説
1. **物理演算**: 重力、速度、加速度の概念
2. **入力処理**: 複数キーでの同じ操作
3. **衝突判定**: 地面との接触判定
4. **状態管理**: `on_ground`フラグでジャンプ制御

---

## 第2回：マップタイルと衝突判定

### 目標
- タイルベースのマップシステムを作成
- プラットフォームとの衝突判定を実装
- より複雑なレベルデザインを可能にする

### 追加・変更するコード

```python
import pyxel


class TileMap:
    def __init__(self):
        self.tile_size = 16
        self.width = 15
        self.height = 12
        
        # マップデータ（0:空気, 1:地面, 2:プラットフォーム）
        self.map_data = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,2,2,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,2,2,0,0,0,0,0,2,2,2,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,2,2,0],
            [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,2,2,2,2,2,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
    
    def get_tile(self, x, y):
        grid_x = x // self.tile_size
        grid_y = y // self.tile_size
        
        if (0 <= grid_x < self.width and 0 <= grid_y < self.height):
            return self.map_data[grid_y][grid_x]
        return 0
    
    def is_solid(self, x, y):
        return self.get_tile(x, y) in [1, 2]
    
    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.map_data[y][x]
                pixel_x = x * self.tile_size
                pixel_y = y * self.tile_size
                
                if tile == 1:  # 地面
                    pyxel.rect(pixel_x, pixel_y, self.tile_size, self.tile_size, 3)
                elif tile == 2:  # プラットフォーム
                    pyxel.rect(pixel_x, pixel_y, self.tile_size, self.tile_size, 9)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = 12
        self.height = 16
        self.on_ground = False
        self.speed = 2
        self.jump_power = -6
        self.gravity = 0.3
        
    def update(self, tile_map):
        # 左右移動
        self.vx = 0
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.vx = -self.speed
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.vx = self.speed
        
        # ジャンプ
        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_UP) or 
            pyxel.btnp(pyxel.KEY_W)) and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False
        
        # 重力適用
        self.vy += self.gravity
        
        # 水平移動と衝突判定
        self.x += self.vx
        if self.check_collision_horizontal(tile_map):
            if self.vx > 0:  # 右移動
                self.x = (self.x // 16) * 16 + 16 - self.width
            else:  # 左移動
                self.x = ((self.x + self.width) // 16) * 16
        
        # 垂直移動と衝突判定
        self.y += self.vy
        if self.check_collision_vertical(tile_map):
            if self.vy > 0:  # 下移動（落下）
                self.y = (self.y // 16) * 16 + 16 - self.height
                self.vy = 0
                self.on_ground = True
            else:  # 上移動（ジャンプ）
                self.y = ((self.y + self.height) // 16) * 16
                self.vy = 0
        else:
            self.on_ground = False
        
        # 画面端判定
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > 240:
            self.x = 240 - self.width
    
    def check_collision_horizontal(self, tile_map):
        # 左右の角をチェック
        return (tile_map.is_solid(self.x, self.y) or
                tile_map.is_solid(self.x + self.width - 1, self.y) or
                tile_map.is_solid(self.x, self.y + self.height - 1) or
                tile_map.is_solid(self.x + self.width - 1, self.y + self.height - 1))
    
    def check_collision_vertical(self, tile_map):
        # 上下の角をチェック
        return (tile_map.is_solid(self.x, self.y) or
                tile_map.is_solid(self.x + self.width - 1, self.y) or
                tile_map.is_solid(self.x, self.y + self.height - 1) or
                tile_map.is_solid(self.x + self.width - 1, self.y + self.height - 1))
    
    def draw(self):
        # プレイヤー本体
        pyxel.rect(self.x, self.y, self.width, self.height, 8)
        # 顔
        pyxel.pset(self.x + 3, self.y + 4, 7)
        pyxel.pset(self.x + 8, self.y + 4, 7)
        pyxel.rect(self.x + 4, self.y + 8, 4, 2, 7)


class Game:
    def __init__(self):
        pyxel.init(240, 200, title="Platformer")
        self.tile_map = TileMap()
        self.player = Player(32, 160)
        pyxel.run(self.update, self.draw)
    
    def update(self):
        self.player.update(self.tile_map)
    
    def draw(self):
        pyxel.cls(12)  # 空色の背景
        
        # マップ描画
        self.tile_map.draw()
        
        # プレイヤー描画
        self.player.draw()
        
        # UI表示
        pyxel.text(5, 5, "Move: Arrow keys or WASD", 7)
        pyxel.text(5, 15, "Jump: Space/Up/W", 7)


Game()
```

### ポイント解説
1. **タイルマップ**: 2次元配列でレベルを管理
2. **衝突判定**: プレイヤーの4つの角で判定
3. **分離判定**: 水平・垂直を別々に処理
4. **グリッド整列**: タイルの境界に正確に配置

---

## 第3回：敵・アイテム・アニメーション

### 目標
- 移動する敵キャラクターを追加
- 収集可能なアイテムを配置
- プレイヤーアニメーションを実装

### 追加・変更するコード

```python
import pyxel


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = -1
        self.vy = 0
        self.width = 12
        self.height = 12
        self.alive = True
        self.gravity = 0.3
        self.on_ground = False
        
    def update(self, tile_map):
        if not self.alive:
            return
            
        # 重力適用
        self.vy += self.gravity
        
        # 水平移動
        self.x += self.vx
        
        # 壁との衝突で方向転換
        if (tile_map.is_solid(self.x, self.y) or 
            tile_map.is_solid(self.x + self.width - 1, self.y)):
            self.vx = -self.vx
            self.x += self.vx
        
        # 垂直移動と衝突判定
        self.y += self.vy
        if (tile_map.is_solid(self.x, self.y + self.height - 1) or
            tile_map.is_solid(self.x + self.width - 1, self.y + self.height - 1)):
            self.y = (self.y // 16) * 16 + 16 - self.height
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False
        
        # 崖で方向転換
        if (self.on_ground and not 
            (tile_map.is_solid(self.x + self.width if self.vx > 0 else self.x - 1, 
                              self.y + self.height))):
            self.vx = -self.vx
    
    def draw(self):
        if self.alive:
            pyxel.rect(self.x, self.y, self.width, self.height, 8)
            pyxel.pset(self.x + 3, self.y + 3, 7)
            pyxel.pset(self.x + 8, self.y + 3, 7)


class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.anim_timer = 0
        
    def update(self):
        self.anim_timer += 1
        
    def draw(self):
        if not self.collected:
            # アニメーション効果
            offset = (self.anim_timer // 10) % 3 - 1
            pyxel.rect(self.x + 2, self.y + 2 + offset, 12, 12, 10)
            pyxel.rect(self.x + 4, self.y + 4 + offset, 8, 8, 9)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = 12
        self.height = 16
        self.on_ground = False
        self.speed = 2
        self.jump_power = -6
        self.gravity = 0.3
        self.facing_right = True
        self.anim_timer = 0
        self.lives = 3
        self.score = 0
        
    def update(self, tile_map, enemies, items):
        # アニメーションタイマー
        self.anim_timer += 1
        
        # 左右移動
        self.vx = 0
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.vx = -self.speed
            self.facing_right = False
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.vx = self.speed
            self.facing_right = True
        
        # ジャンプ
        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_UP) or 
            pyxel.btnp(pyxel.KEY_W)) and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False
        
        # 重力適用
        self.vy += self.gravity
        
        # 水平移動と衝突判定
        self.x += self.vx
        if self.check_collision_horizontal(tile_map):
            if self.vx > 0:  # 右移動
                self.x = (self.x // 16) * 16 + 16 - self.width
            else:  # 左移動
                self.x = ((self.x + self.width) // 16) * 16
        
        # 垂直移動と衝突判定
        self.y += self.vy
        if self.check_collision_vertical(tile_map):
            if self.vy > 0:  # 下移動（落下）
                self.y = (self.y // 16) * 16 + 16 - self.height
                self.vy = 0
                self.on_ground = True
            else:  # 上移動（ジャンプ）
                self.y = ((self.y + self.height) // 16) * 16
                self.vy = 0
        else:
            self.on_ground = False
        
        # 画面端判定
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > 240:
            self.x = 240 - self.width
        
        # 敵との衝突判定
        for enemy in enemies:
            if (enemy.alive and 
                self.x < enemy.x + enemy.width and
                self.x + self.width > enemy.x and
                self.y < enemy.y + enemy.height and
                self.y + self.height > enemy.y):
                # 上から踏んだ場合
                if self.vy > 0 and self.y < enemy.y:
                    enemy.alive = False
                    self.vy = -3  # 小さく跳ねる
                    self.score += 100
                else:
                    self.take_damage()
        
        # アイテムとの衝突判定
        for item in items:
            if (not item.collected and
                self.x < item.x + 16 and
                self.x + self.width > item.x and
                self.y < item.y + 16 and
                self.y + self.height > item.y):
                item.collected = True
                self.score += 50
        
        # 落下死判定
        if self.y > 220:
            self.take_damage()
    
    def take_damage(self):
        self.lives -= 1
        self.x = 32
        self.y = 160
        self.vx = 0
        self.vy = 0
    
    def check_collision_horizontal(self, tile_map):
        return (tile_map.is_solid(self.x, self.y) or
                tile_map.is_solid(self.x + self.width - 1, self.y) or
                tile_map.is_solid(self.x, self.y + self.height - 1) or
                tile_map.is_solid(self.x + self.width - 1, self.y + self.height - 1))
    
    def check_collision_vertical(self, tile_map):
        return (tile_map.is_solid(self.x, self.y) or
                tile_map.is_solid(self.x + self.width - 1, self.y) or
                tile_map.is_solid(self.x, self.y + self.height - 1) or
                tile_map.is_solid(self.x + self.width - 1, self.y + self.height - 1))
    
    def draw(self):
        # プレイヤー本体（アニメーション）
        color = 8 if (self.anim_timer // 10) % 2 == 0 or self.vx == 0 else 14
        pyxel.rect(self.x, self.y, self.width, self.height, color)
        
        # 顔（向きに応じて変化）
        eye_offset = 2 if self.facing_right else 6
        pyxel.pset(self.x + eye_offset, self.y + 4, 7)
        pyxel.pset(self.x + eye_offset + 4, self.y + 4, 7)
        pyxel.rect(self.x + 4, self.y + 8, 4, 2, 7)


class TileMap:
    def __init__(self):
        self.tile_size = 16
        self.width = 15
        self.height = 12
        
        self.map_data = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,2,2,2,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,2,2,0,0,0,0,0,2,2,2,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,2,2,0],
            [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,2,2,2,2,2,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
    
    def get_tile(self, x, y):
        grid_x = x // self.tile_size
        grid_y = y // self.tile_size
        
        if (0 <= grid_x < self.width and 0 <= grid_y < self.height):
            return self.map_data[grid_y][grid_x]
        return 0
    
    def is_solid(self, x, y):
        return self.get_tile(x, y) in [1, 2]
    
    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.map_data[y][x]
                pixel_x = x * self.tile_size
                pixel_y = y * self.tile_size
                
                if tile == 1:  # 地面
                    pyxel.rect(pixel_x, pixel_y, self.tile_size, self.tile_size, 3)
                elif tile == 2:  # プラットフォーム
                    pyxel.rect(pixel_x, pixel_y, self.tile_size, self.tile_size, 9)


class Game:
    def __init__(self):
        pyxel.init(240, 200, title="Platformer")
        self.tile_map = TileMap()
        self.player = Player(32, 160)
        self.enemies = [
            Enemy(80, 160),
            Enemy(160, 144),
            Enemy(200, 112)
        ]
        self.items = [
            Item(96, 48),
            Item(144, 80),
            Item(192, 112),
            Item(128, 144)
        ]
        self.game_over = False
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.restart_game()
            return
            
        self.player.update(self.tile_map, self.enemies, self.items)
        
        for enemy in self.enemies:
            enemy.update(self.tile_map)
            
        for item in self.items:
            item.update()
        
        # ゲームオーバー判定
        if self.player.lives <= 0:
            self.game_over = True
    
    def restart_game(self):
        self.player = Player(32, 160)
        self.enemies = [
            Enemy(80, 160),
            Enemy(160, 144),
            Enemy(200, 112)
        ]
        for enemy in self.enemies:
            enemy.alive = True
        self.items = [
            Item(96, 48),
            Item(144, 80),
            Item(192, 112),
            Item(128, 144)
        ]
        for item in self.items:
            item.collected = False
        self.game_over = False
    
    def draw(self):
        pyxel.cls(12)  # 空色の背景
        
        # マップ描画
        self.tile_map.draw()
        
        # アイテム描画
        for item in self.items:
            item.draw()
        
        # 敵描画
        for enemy in self.enemies:
            enemy.draw()
        
        # プレイヤー描画
        self.player.draw()
        
        # UI表示
        pyxel.text(5, 5, f"Lives: {self.player.lives}", 7)
        pyxel.text(5, 15, f"Score: {self.player.score}", 7)
        
        if self.game_over:
            pyxel.rect(60, 80, 120, 40, 0)
            pyxel.rectb(60, 80, 120, 40, 7)
            pyxel.text(90, 90, "GAME OVER", 8)
            pyxel.text(70, 105, "SPACE: Restart", 7)


Game()
```

### ポイント解説
1. **敵AI**: 壁と崖で方向転換する簡単なAI
2. **アニメーション**: タイマーを使った色変化
3. **ゲームループ**: ライフ・スコアシステム
4. **状態管理**: collected、aliveフラグの活用

---

## 第4回：マルチステージとゲーム完成

### 目標
- 複数のステージを実装
- ステージクリア条件を追加
- 完全なゲーム体験を提供

### 追加・変更するコード

最終完成版のコードに統合します。

### 最終完成コード

```python
import pyxel


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = -1
        self.vy = 0
        self.width = 12
        self.height = 12
        self.alive = True
        self.gravity = 0.3
        self.on_ground = False
        
    def update(self, tile_map):
        if not self.alive:
            return
            
        # 重力適用
        self.vy += self.gravity
        
        # 水平移動
        self.x += self.vx
        
        # 壁との衝突で方向転換
        if (tile_map.is_solid(self.x, self.y) or 
            tile_map.is_solid(self.x + self.width - 1, self.y)):
            self.vx = -self.vx
            self.x += self.vx
        
        # 垂直移動と衝突判定
        self.y += self.vy
        if (tile_map.is_solid(self.x, self.y + self.height - 1) or
            tile_map.is_solid(self.x + self.width - 1, self.y + self.height - 1)):
            self.y = (self.y // 16) * 16 + 16 - self.height
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False
        
        # 崖で方向転換
        if (self.on_ground and not 
            (tile_map.is_solid(self.x + self.width if self.vx > 0 else self.x - 1, 
                              self.y + self.height))):
            self.vx = -self.vx
    
    def draw(self):
        if self.alive:
            pyxel.rect(self.x, self.y, self.width, self.height, 8)
            pyxel.pset(self.x + 3, self.y + 3, 7)
            pyxel.pset(self.x + 8, self.y + 3, 7)


class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.anim_timer = 0
        
    def update(self):
        self.anim_timer += 1
        
    def draw(self):
        if not self.collected:
            # アニメーション効果
            offset = (self.anim_timer // 10) % 3 - 1
            pyxel.rect(self.x + 2, self.y + 2 + offset, 12, 12, 10)
            pyxel.rect(self.x + 4, self.y + 4 + offset, 8, 8, 9)


class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.anim_timer = 0
        
    def update(self):
        self.anim_timer += 1
        
    def draw(self):
        # ゴールフラグ
        color = 11 if (self.anim_timer // 15) % 2 == 0 else 3
        pyxel.rect(self.x, self.y, 4, 32, 6)  # ポール
        pyxel.rect(self.x + 4, self.y, 12, 8, color)  # フラグ


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.width = 12
        self.height = 16
        self.on_ground = False
        self.speed = 2
        self.jump_power = -6
        self.gravity = 0.3
        self.facing_right = True
        self.anim_timer = 0
        self.lives = 3
        self.score = 0
        
    def update(self, tile_map, enemies, items, goal):
        # アニメーションタイマー
        self.anim_timer += 1
        
        # 左右移動
        self.vx = 0
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.vx = -self.speed
            self.facing_right = False
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.vx = self.speed
            self.facing_right = True
        
        # ジャンプ
        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_UP) or 
            pyxel.btnp(pyxel.KEY_W)) and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False
        
        # 重力適用
        self.vy += self.gravity
        
        # 水平移動と衝突判定
        self.x += self.vx
        if self.check_collision_horizontal(tile_map):
            if self.vx > 0:  # 右移動
                self.x = (self.x // 16) * 16 + 16 - self.width
            else:  # 左移動
                self.x = ((self.x + self.width) // 16) * 16
        
        # 垂直移動と衝突判定
        self.y += self.vy
        if self.check_collision_vertical(tile_map):
            if self.vy > 0:  # 下移動（落下）
                self.y = (self.y // 16) * 16 + 16 - self.height
                self.vy = 0
                self.on_ground = True
            else:  # 上移動（ジャンプ）
                self.y = ((self.y + self.height) // 16) * 16
                self.vy = 0
        else:
            self.on_ground = False
        
        # 画面端判定
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > 240:
            self.x = 240 - self.width
        
        # 敵との衝突判定
        for enemy in enemies:
            if (enemy.alive and 
                self.x < enemy.x + enemy.width and
                self.x + self.width > enemy.x and
                self.y < enemy.y + enemy.height and
                self.y + self.height > enemy.y):
                # 上から踏んだ場合
                if self.vy > 0 and self.y < enemy.y:
                    enemy.alive = False
                    self.vy = -3  # 小さく跳ねる
                    self.score += 100
                else:
                    self.take_damage()
        
        # アイテムとの衝突判定
        for item in items:
            if (not item.collected and
                self.x < item.x + 16 and
                self.x + self.width > item.x and
                self.y < item.y + 16 and
                self.y + self.height > item.y):
                item.collected = True
                self.score += 50
        
        # ゴールとの衝突判定
        goal_reached = (self.x < goal.x + 16 and
                       self.x + self.width > goal.x and
                       self.y < goal.y + 32 and
                       self.y + self.height > goal.y)
        
        # 落下死判定
        if self.y > 220:
            self.take_damage()
            
        return goal_reached
    
    def take_damage(self):
        self.lives -= 1
        self.x = 32
        self.y = 160
        self.vx = 0
        self.vy = 0
    
    def check_collision_horizontal(self, tile_map):
        return (tile_map.is_solid(self.x, self.y) or
                tile_map.is_solid(self.x + self.width - 1, self.y) or
                tile_map.is_solid(self.x, self.y + self.height - 1) or
                tile_map.is_solid(self.x + self.width - 1, self.y + self.height - 1))
    
    def check_collision_vertical(self, tile_map):
        return (tile_map.is_solid(self.x, self.y) or
                tile_map.is_solid(self.x + self.width - 1, self.y) or
                tile_map.is_solid(self.x, self.y + self.height - 1) or
                tile_map.is_solid(self.x + self.width - 1, self.y + self.height - 1))
    
    def draw(self):
        # プレイヤー本体（アニメーション）
        color = 8 if (self.anim_timer // 10) % 2 == 0 or self.vx == 0 else 14
        pyxel.rect(self.x, self.y, self.width, self.height, color)
        
        # 顔（向きに応じて変化）
        eye_offset = 2 if self.facing_right else 6
        pyxel.pset(self.x + eye_offset, self.y + 4, 7)
        pyxel.pset(self.x + eye_offset + 4, self.y + 4, 7)
        pyxel.rect(self.x + 4, self.y + 8, 4, 2, 7)


class TileMap:
    def __init__(self, stage=1):
        self.tile_size = 16
        self.width = 15
        self.height = 12
        
        # ステージごとのマップデータ
        if stage == 1:
            self.map_data = [
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,2,2,2,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,2,2,0,0,0,0,0,2,2,2,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,2,2,0],
                [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,2,2,2,2,2,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ]
        elif stage == 2:
            self.map_data = [
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,2,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,2,0,0,0,0,2,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0],
                [0,2,0,0,0,0,2,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,2,0,0,0,0,0,2,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [2,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ]
        else:  # stage 3
            self.map_data = [
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,2,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,2,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0],
                [0,0,2,2,2,0,0,0,0,0,2,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,2,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ]
    
    def get_tile(self, x, y):
        grid_x = x // self.tile_size
        grid_y = y // self.tile_size
        
        if (0 <= grid_x < self.width and 0 <= grid_y < self.height):
            return self.map_data[grid_y][grid_x]
        return 0
    
    def is_solid(self, x, y):
        return self.get_tile(x, y) in [1, 2]
    
    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.map_data[y][x]
                pixel_x = x * self.tile_size
                pixel_y = y * self.tile_size
                
                if tile == 1:  # 地面
                    pyxel.rect(pixel_x, pixel_y, self.tile_size, self.tile_size, 3)
                elif tile == 2:  # プラットフォーム
                    pyxel.rect(pixel_x, pixel_y, self.tile_size, self.tile_size, 9)


class Game:
    def __init__(self):
        pyxel.init(240, 200, title="Platformer")
        self.current_stage = 1
        self.max_stage = 3
        self.load_stage()
        self.game_over = False
        self.stage_clear = False
        self.game_clear = False
        pyxel.run(self.update, self.draw)
    
    def load_stage(self):
        self.tile_map = TileMap(self.current_stage)
        self.player = Player(32, 160)
        
        if self.current_stage == 1:
            self.enemies = [
                Enemy(80, 160),
                Enemy(160, 144)
            ]
            self.items = [
                Item(96, 48),
                Item(144, 80),
                Item(192, 112)
            ]
        elif self.current_stage == 2:
            self.enemies = [
                Enemy(96, 160),
                Enemy(144, 160),
                Enemy(192, 160)
            ]
            self.items = [
                Item(48, 80),
                Item(112, 112),
                Item(176, 144),
                Item(208, 16)
            ]
        else:  # stage 3
            self.enemies = [
                Enemy(96, 160),
                Enemy(128, 160),
                Enemy(160, 160),
                Enemy(192, 160)
            ]
            self.items = [
                Item(48, 80),
                Item(80, 80),
                Item(112, 112),
                Item(176, 144),
                Item(208, 16)
            ]
        
        self.goal = Goal(208, 144)
    
    def next_stage(self):
        self.current_stage += 1
        if self.current_stage > self.max_stage:
            self.game_clear = True
        else:
            self.load_stage()
            self.stage_clear = False
    
    def update(self):
        if self.game_over or self.game_clear:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.restart_game()
            return
        
        if self.stage_clear:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.next_stage()
            return
            
        goal_reached = self.player.update(self.tile_map, self.enemies, self.items, self.goal)
        
        if goal_reached:
            self.stage_clear = True
            self.player.score += 200
        
        for enemy in self.enemies:
            enemy.update(self.tile_map)
            
        for item in self.items:
            item.update()
            
        self.goal.update()
        
        # ゲームオーバー判定
        if self.player.lives <= 0:
            self.game_over = True
    
    def restart_game(self):
        self.current_stage = 1
        self.player = Player(32, 160)
        self.load_stage()
        self.game_over = False
        self.stage_clear = False
        self.game_clear = False
    
    def draw(self):
        pyxel.cls(12)  # 空色の背景
        
        # マップ描画
        self.tile_map.draw()
        
        # ゴール描画
        self.goal.draw()
        
        # アイテム描画
        for item in self.items:
            item.draw()
        
        # 敵描画
        for enemy in self.enemies:
            enemy.draw()
        
        # プレイヤー描画
        self.player.draw()
        
        # UI表示
        pyxel.text(5, 5, f"Stage: {self.current_stage}", 7)
        pyxel.text(5, 15, f"Lives: {self.player.lives}", 7)
        pyxel.text(5, 25, f"Score: {self.player.score}", 7)
        
        # ゲーム状態表示
        if self.game_clear:
            pyxel.rect(50, 70, 140, 60, 0)
            pyxel.rectb(50, 70, 140, 60, 7)
            pyxel.text(90, 85, "GAME CLEAR!", 11)
            pyxel.text(70, 100, f"Final Score: {self.player.score}", 7)
            pyxel.text(70, 115, "SPACE: Play Again", 7)
        elif self.stage_clear:
            pyxel.rect(60, 80, 120, 40, 0)
            pyxel.rectb(60, 80, 120, 40, 7)
            pyxel.text(85, 90, "STAGE CLEAR!", 11)
            pyxel.text(75, 105, "SPACE: Next Stage", 7)
        elif self.game_over:
            pyxel.rect(60, 80, 120, 40, 0)
            pyxel.rectb(60, 80, 120, 40, 7)
            pyxel.text(90, 90, "GAME OVER", 8)
            pyxel.text(70, 105, "SPACE: Restart", 7)


Game()
```

### 完成機能
- 3つのステージで構成されたプラットフォーマーゲーム
- プレイヤーの移動・ジャンプ・アニメーション
- 敵キャラクターのAIと衝突判定
- 収集可能なアイテムシステム
- ライフ・スコア・ステージ進行システム
- ゲームオーバー・クリア判定とリスタート機能

### 全操作方法まとめ
- 移動：矢印キー または WASD
- ジャンプ：スペース / 上矢印 / W
- スペースキー：ゲーム再開・ステージ進行

**学習ポイント:**
1. **物理演算**: 重力・速度・衝突判定の実装
2. **タイルシステム**: 2次元配列によるマップ管理
3. **ゲーム状態**: ステージ・ライフ・スコア管理
4. **オブジェクト管理**: プレイヤー・敵・アイテムの相互作用
5. **アニメーション**: フレームベースの動的表現
