import pyxel

class Character:
    def __init__(self, name, max_hp, attack, defense):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense
        
    def get_hp_ratio(self):
        return self.hp / self.max_hp

class Player(Character):
    def __init__(self):
        super().__init__("Hero", 100, 25, 8)
        
    def draw(self, x, y):
        pyxel.rect(x, y, 32, 48, 1)
        pyxel.rect(x + 4, y + 4, 24, 40, 12)
        
        pyxel.pset(x + 10, y + 12, 0)
        pyxel.pset(x + 22, y + 12, 0)
        pyxel.line(x + 12, y + 20, x + 20, y + 20, 0)

class Enemy(Character):
    def __init__(self, name, max_hp, attack, defense):
        super().__init__(name, max_hp, attack, defense)
        
    def draw(self, x, y):
        pyxel.rect(x, y, 32, 48, 8)
        pyxel.rect(x + 4, y + 4, 24, 40, 9)
        
        pyxel.pset(x + 10, y + 12, 0)
        pyxel.pset(x + 22, y + 12, 0)
        pyxel.line(x + 12, y + 24, x + 20, y + 24, 0)

class BattleUI:
    def __init__(self):
        pass
        
    def draw_character_status(self, character, x, y):
        pyxel.text(x, y, character.name, 7)
        pyxel.text(x, y + 10, f"HP: {character.hp}/{character.max_hp}", 7)
        
        bar_width = 80
        hp_ratio = character.get_hp_ratio()
        pyxel.rect(x, y + 20, bar_width, 8, 0)
        pyxel.rect(x + 1, y + 21, int((bar_width - 2) * hp_ratio), 6, 8)
        
    def draw_battle_field(self):
        pyxel.rect(20, 140, 200, 50, 0)
        pyxel.rectb(20, 140, 200, 50, 7)
        pyxel.text(30, 155, "Battle Screen Base", 7)
        pyxel.text(30, 170, "Step1: Basic Display", 7)

class Game:
    def __init__(self):
        pyxel.init(240, 200, title="RPG Battle - Step1")
        pyxel.mouse(True)
        self.player = Player()
        self.enemy = Enemy("Slime", 60, 18, 5)
        self.ui = BattleUI()
        pyxel.run(self.update, self.draw)
        
    def update(self):
        pass
        
    def draw(self):
        pyxel.cls(1)
        
        self.player.draw(40, 80)
        self.enemy.draw(160, 80)
        
        self.ui.draw_character_status(self.player, 20, 20)
        self.ui.draw_character_status(self.enemy, 140, 20)
        
        pyxel.text(90, 5, "Turn-based Battle", 7)
        
        self.ui.draw_battle_field()

Game()