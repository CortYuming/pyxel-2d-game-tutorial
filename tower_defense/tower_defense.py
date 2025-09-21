import pyxel
import math


class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 60
        self.damage = 15
        self.attack_speed = 60
        self.attack_timer = 0
        self.target = None
        
    def update(self, enemies):
        self.attack_timer -= 1
        
        # ターゲット検索
        self.target = None
        min_distance = self.range
        
        for enemy in enemies:
            if not enemy.alive:
                continue
                
            distance = math.sqrt((enemy.x - self.x) ** 2 + (enemy.y - self.y) ** 2)
            if distance <= min_distance:
                min_distance = distance
                self.target = enemy
        
        # 攻撃
        if self.target and self.attack_timer <= 0:
            self.target.hp -= self.damage
            self.attack_timer = self.attack_speed
            return True
        
        return False
    
    def draw(self):
        # タワー本体
        pyxel.rect(self.x - 6, self.y - 6, 12, 12, 6)
        pyxel.rectb(self.x - 6, self.y - 6, 12, 12, 5)


class AttackEffect:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.start_x = start_x
        self.start_y = start_y
        self.target_x = target_x
        self.target_y = target_y
        self.timer = 10
        
    def update(self):
        self.timer -= 1
        return self.timer > 0
    
    def draw(self):
        if self.timer > 0:
            pyxel.line(self.start_x, self.start_y, self.target_x, self.target_y, 10)


class Enemy:
    def __init__(self, path, wave_num=1):
        self.path = path
        self.path_index = 0
        self.x = path[0][0] * 16 + 8
        self.y = path[0][1] * 16 + 28
        self.speed = 0.5 + (wave_num - 1) * 0.1
        self.hp = 30 + (wave_num - 1) * 10
        self.max_hp = self.hp
        self.radius = 6
        self.alive = True
        self.reward = 10 + (wave_num - 1) * 2
        
    def update(self):
        if not self.alive or self.path_index >= len(self.path) - 1:
            return
            
        # 次の目標地点
        target_x = self.path[self.path_index + 1][0] * 16 + 8
        target_y = self.path[self.path_index + 1][1] * 16 + 28
        
        # 移動方向計算
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance < 2:
            self.path_index += 1
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def draw(self):
        if not self.alive:
            return
            
        # 敵本体
        pyxel.circb(self.x, self.y, self.radius, 8)
        pyxel.circ(self.x, self.y, self.radius - 2, 9)
        
        # HP表示
        hp_ratio = self.hp / self.max_hp
        pyxel.rect(self.x - 8, self.y - 12, 16, 3, 0)
        pyxel.rect(self.x - 7, self.y - 11, int(14 * hp_ratio), 1, 8)
    
    def reached_goal(self):
        return self.path_index >= len(self.path) - 1


class Wave:
    def __init__(self, wave_num, enemy_count, spawn_interval):
        self.wave_num = wave_num
        self.enemy_count = enemy_count
        self.spawn_interval = spawn_interval
        self.spawned = 0
        self.spawn_timer = 0
        self.completed = False
        
    def update(self, game_map):
        if self.spawned >= self.enemy_count:
            return None
            
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.spawned += 1
            return Enemy(game_map.path, self.wave_num)
        
        return None
    
    def is_complete(self, enemies_alive):
        return self.spawned >= self.enemy_count and enemies_alive == 0


class GameMap:
    def __init__(self):
        self.width = 15
        self.height = 10
        self.tile_size = 16
        self.path = [
            (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5),
            (5, 4), (5, 3), (5, 2), (6, 2), (7, 2), (8, 2),
            (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (9, 7),
            (10, 7), (11, 7), (12, 7), (13, 7), (14, 7)
        ]
        
    def is_path(self, grid_x, grid_y):
        return (grid_x, grid_y) in self.path
        
    def draw(self):
        # 背景（草地）
        for x in range(self.width):
            for y in range(self.height):
                pyxel.rect(
                    x * self.tile_size, 
                    y * self.tile_size + 20, 
                    self.tile_size, 
                    self.tile_size, 
                    3
                )
        
        # 道の表示
        for x, y in self.path:
            pyxel.rect(
                x * self.tile_size, 
                y * self.tile_size + 20, 
                self.tile_size, 
                self.tile_size, 
                13
            )
        
        # スタート地点
        start_x, start_y = self.path[0]
        pyxel.rect(
            start_x * self.tile_size + 2, 
            start_y * self.tile_size + 22, 
            12, 12, 11
        )
        
        # ゴール地点
        end_x, end_y = self.path[-1]
        pyxel.rect(
            end_x * self.tile_size + 2, 
            end_y * self.tile_size + 22, 
            12, 12, 8
        )


class Game:
    def __init__(self):
        pyxel.init(240, 180, title="Tower Defense")
        pyxel.mouse(True)  # マウスカーソルを表示
        self.game_map = GameMap()
        self.enemies = []
        self.towers = []
        self.effects = []
        self.waves = [
            Wave(1, 5, 90),   # ウェーブ1: 5体、1.5秒間隔
            Wave(2, 8, 75),   # ウェーブ2: 8体、1.25秒間隔
            Wave(3, 12, 60),  # ウェーブ3: 12体、1秒間隔
            Wave(4, 15, 45),  # ウェーブ4: 15体、0.75秒間隔
            Wave(5, 20, 30),  # ウェーブ5: 20体、0.5秒間隔
        ]
        self.current_wave_index = 0
        self.current_wave = self.waves[0] if self.waves else None
        self.life = 20
        self.gold = 100
        self.tower_cost = 50
        self.score = 0
        self.game_over = False
        self.game_clear = False
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over or self.game_clear:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.restart_game()
            return

        # タワー設置
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x = pyxel.mouse_x
            mouse_y = pyxel.mouse_y
            
            if mouse_y > 20 and self.gold >= self.tower_cost:
                grid_x = mouse_x // 16
                grid_y = (mouse_y - 20) // 16
                
                if not self.game_map.is_path(grid_x, grid_y):
                    tower_x = grid_x * 16 + 8
                    tower_y = grid_y * 16 + 28
                    
                    can_place = True
                    for tower in self.towers:
                        if abs(tower.x - tower_x) < 16 and abs(tower.y - tower_y) < 16:
                            can_place = False
                            break
                    
                    if can_place:
                        self.towers.append(Tower(tower_x, tower_y))
                        self.gold -= self.tower_cost

        # ウェーブ管理
        if self.current_wave:
            new_enemy = self.current_wave.update(self.game_map)
            if new_enemy:
                self.enemies.append(new_enemy)
            
            # ウェーブ完了チェック
            if self.current_wave.is_complete(len(self.enemies)):
                self.gold += 50  # ウェーブクリアボーナス
                self.current_wave_index += 1
                if self.current_wave_index < len(self.waves):
                    self.current_wave = self.waves[self.current_wave_index]
                else:
                    self.current_wave = None
                    if len(self.enemies) == 0:
                        self.game_clear = True

        # タワーの更新
        for tower in self.towers:
            if tower.update(self.enemies):
                if tower.target:
                    self.effects.append(AttackEffect(
                        tower.x, tower.y, 
                        tower.target.x, tower.target.y
                    ))

        # 敵の更新
        for enemy in self.enemies[:]:
            enemy.update()
            
            if enemy.reached_goal():
                self.life -= 1
                self.enemies.remove(enemy)
                if self.life <= 0:
                    self.game_over = True
            
            elif enemy.hp <= 0:
                self.gold += enemy.reward
                self.score += enemy.reward
                enemy.alive = False
                self.enemies.remove(enemy)

        # エフェクトの更新
        self.effects = [effect for effect in self.effects if effect.update()]

    def restart_game(self):
        # ゲーム状態をリセット（pyxel.init()は呼ばない）
        self.enemies = []
        self.towers = []
        self.effects = []
        self.current_wave_index = 0
        self.current_wave = self.waves[0] if self.waves else None
        self.life = 20
        self.gold = 100
        self.score = 0
        self.game_over = False
        self.game_clear = False

    def draw(self):
        pyxel.cls(1)
        
        # UI背景
        pyxel.rect(0, 0, 240, 20, 0)
        
        # ステータス表示
        pyxel.text(5, 5, f"Life: {self.life}", 7)
        pyxel.text(70, 5, f"Gold: {self.gold}", 7)
        pyxel.text(5, 12, f"Wave: {self.current_wave_index + 1 if self.current_wave else 'Complete'}", 7)
        pyxel.text(150, 5, f"Score: {self.score}", 7)
        pyxel.text(150, 12, f"Enemies: {len(self.enemies)}", 7)
        
        # マップ描画
        self.game_map.draw()
        
        # タワー描画
        for tower in self.towers:
            tower.draw()
        
        # 敵描画
        for enemy in self.enemies:
            enemy.draw()
        
        # エフェクト描画
        for effect in self.effects:
            effect.draw()
        
        # ゲーム終了画面
        if self.game_over:
            pyxel.rect(60, 70, 120, 40, 0)
            pyxel.rectb(60, 70, 120, 40, 7)
            pyxel.text(95, 80, "GAME OVER", 8)
            pyxel.text(75, 95, "SPACE: Restart", 7)
        elif self.game_clear:
            pyxel.rect(60, 70, 120, 40, 0)
            pyxel.rectb(60, 70, 120, 40, 7)
            pyxel.text(95, 80, "GAME CLEAR!", 11)
            pyxel.text(85, 95, f"Score: {self.score}", 7)
            pyxel.text(75, 103, "SPACE: Restart", 7)


Game()