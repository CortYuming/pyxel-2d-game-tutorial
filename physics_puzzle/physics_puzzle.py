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
