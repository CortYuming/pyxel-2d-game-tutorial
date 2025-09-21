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
        grid_x = int(x) // self.tile_size
        grid_y = int(y) // self.tile_size
        
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