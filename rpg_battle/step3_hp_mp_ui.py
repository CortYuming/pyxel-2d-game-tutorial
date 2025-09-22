import pyxel
import random

class Character:
    def __init__(self, name, max_hp, max_mp, attack, defense):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mp = max_mp
        self.mp = max_mp
        self.attack = attack
        self.defense = defense
        self.is_defending = False
        
    def take_damage(self, damage):
        if self.is_defending:
            damage = max(1, damage // 2)
        self.hp = max(0, self.hp - damage)
        
    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)
        
    def use_mp(self, amount):
        self.mp = max(0, self.mp - amount)
        
    def recover_mp(self, amount):
        self.mp = min(self.max_mp, self.mp + amount)
        
    def is_alive(self):
        return self.hp > 0
        
    def get_hp_ratio(self):
        return self.hp / self.max_hp
        
    def get_mp_ratio(self):
        return self.mp / self.max_mp

class Player(Character):
    def __init__(self):
        super().__init__("Hero", 100, 50, 25, 8)
        
    def draw(self, x, y):
        pyxel.rect(x, y, 32, 48, 1)
        pyxel.rect(x + 4, y + 4, 24, 40, 12)
        
        pyxel.pset(x + 10, y + 12, 0)
        pyxel.pset(x + 22, y + 12, 0)
        pyxel.line(x + 12, y + 20, x + 20, y + 20, 0)

class Enemy(Character):
    def __init__(self, name, max_hp, max_mp, attack, defense):
        super().__init__(name, max_hp, max_mp, attack, defense)
        
    def ai_action(self):
        if random.random() < 0.7:
            return "attack"
        else:
            return "defend"
            
    def draw(self, x, y):
        pyxel.rect(x, y, 32, 48, 8)
        pyxel.rect(x + 4, y + 4, 24, 40, 9)
        
        pyxel.pset(x + 10, y + 12, 0)
        pyxel.pset(x + 22, y + 12, 0)
        pyxel.line(x + 12, y + 24, x + 20, y + 24, 0)

class BattleUI:
    def __init__(self):
        self.selected_action = 0
        self.actions = ["Attack", "Heal", "Defend"]
        
    def draw_character_status(self, character, x, y):
        pyxel.text(x, y, character.name, 7)
        pyxel.text(x, y + 10, f"HP: {character.hp}/{character.max_hp}", 7)
        pyxel.text(x, y + 20, f"MP: {character.mp}/{character.max_mp}", 7)
        
        bar_width = 60
        hp_ratio = character.get_hp_ratio()
        pyxel.rect(x, y + 30, bar_width, 6, 0)
        pyxel.rect(x + 1, y + 31, int((bar_width - 2) * hp_ratio), 4, 8)
        
        mp_ratio = character.get_mp_ratio()
        pyxel.rect(x, y + 38, bar_width, 6, 0)
        pyxel.rect(x + 1, y + 39, int((bar_width - 2) * mp_ratio), 4, 12)
        
    def draw_action_menu(self, player):
        pyxel.rect(20, 140, 200, 50, 0)
        pyxel.rectb(20, 140, 200, 50, 7)
        
        for i, action in enumerate(self.actions):
            color = 10 if i == self.selected_action else 7
            if action == "Heal" and player.mp < 10:
                color = 5
            pyxel.text(30 + i * 50, 155, action, color)
        
        pyxel.text(30, 170, "Arrow keys: Select  Space: Confirm", 7)
        
    def update_input(self, player):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.selected_action = max(0, self.selected_action - 1)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.selected_action = min(len(self.actions) - 1, self.selected_action + 1)
        elif pyxel.btnp(pyxel.KEY_SPACE):
            action = self.actions[self.selected_action]
            if action == "Heal" and player.mp < 10:
                return None
            return action
        return None

class Game:
    def __init__(self):
        pyxel.init(240, 200, title="RPG Battle - Step3")
        pyxel.mouse(True)
        self.player = Player()
        self.enemy = Enemy("Orc", 80, 30, 22, 7)
        self.ui = BattleUI()
        self.turn = "player"
        self.battle_log = []
        self.game_over = False
        self.winner = None
        pyxel.run(self.update, self.draw)
        
    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.restart_battle()
            return
            
        if self.turn == "player":
            action = self.ui.update_input(self.player)
            if action:
                self.execute_player_action(action)
                
        elif self.turn == "enemy":
            if pyxel.frame_count % 120 == 0:
                enemy_action = self.enemy.ai_action()
                self.execute_enemy_action(enemy_action)
                
    def execute_player_action(self, action):
        self.player.is_defending = False
        
        if action == "Attack":
            damage = max(1, self.player.attack - self.enemy.defense + random.randint(-3, 3))
            self.enemy.take_damage(damage)
            self.battle_log.append(f"Hero attacks! {damage} damage!")
            
        elif action == "Heal":
            if self.player.mp >= 10:
                self.player.use_mp(10)
                heal_amount = 25
                self.player.heal(heal_amount)
                self.battle_log.append(f"Hero recovered {heal_amount} HP!")
            else:
                self.battle_log.append("Not enough MP!")
                return
            
        elif action == "Defend":
            self.player.is_defending = True
            self.player.recover_mp(3)
            self.battle_log.append("Hero defends and recovers MP...")
            
        self.check_battle_end()
        if not self.game_over:
            self.turn = "enemy"
            
    def execute_enemy_action(self, action):
        self.enemy.is_defending = False
        
        if action == "attack":
            damage = max(1, self.enemy.attack - self.player.defense + random.randint(-3, 3))
            self.player.take_damage(damage)
            self.battle_log.append(f"{self.enemy.name} attacks! {damage} damage!")
            
        elif action == "defend":
            self.enemy.is_defending = True
            self.enemy.recover_mp(5)
            self.battle_log.append(f"{self.enemy.name} is defending...")
            
        if len(self.battle_log) > 3:
            self.battle_log.pop(0)
            
        self.check_battle_end()
        if not self.game_over:
            self.turn = "player"
            
    def check_battle_end(self):
        if not self.player.is_alive():
            self.game_over = True
            self.winner = "Enemy"
        elif not self.enemy.is_alive():
            self.game_over = True
            self.winner = "Player"
            
    def restart_battle(self):
        self.player = Player()
        self.enemy = Enemy("Orc", 80, 30, 22, 7)
        self.turn = "player"
        self.battle_log = []
        self.game_over = False
        self.winner = None
        
    def draw(self):
        pyxel.cls(1)
        
        self.player.draw(40, 80)
        self.enemy.draw(160, 80)
        
        self.ui.draw_character_status(self.player, 20, 20)
        self.ui.draw_character_status(self.enemy, 140, 20)
        
        turn_text = "Player's Turn" if self.turn == "player" else "Enemy's Turn"
        pyxel.text(90, 5, turn_text, 7)
        
        for i, log in enumerate(self.battle_log):
            pyxel.text(10, 100 + i * 10, log, 7)
        
        if self.turn == "player" and not self.game_over:
            self.ui.draw_action_menu(self.player)
            
        if self.game_over:
            pyxel.rect(60, 80, 120, 40, 0)
            pyxel.rectb(60, 80, 120, 40, 7)
            pyxel.text(85, 90, f"{self.winner} Wins!", 11)
            pyxel.text(70, 105, "SPACE: Restart", 7)

Game()