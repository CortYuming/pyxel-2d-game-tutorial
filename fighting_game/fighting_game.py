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
        self.facing_right = True

    def update(self):
        # 攻撃タイマー更新
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.is_attacking = False

        # 向きの更新
        if self.vx > 0:
            self.facing_right = True
        elif self.vx < 0:
            self.facing_right = False

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
            if self.facing_right:
                return (self.x + self.width, self.y + 8, 20, 8)
            else:
                return (self.x - 20, self.y + 8, 20, 8)
        return None

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)
        # 攻撃エフェクト
        if self.is_attacking:
            if self.facing_right:
                pyxel.rect(self.x + self.width, self.y + 8, 20, 8, 10)
            else:
                pyxel.rect(self.x - 20, self.y + 8, 20, 8, 10)


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
