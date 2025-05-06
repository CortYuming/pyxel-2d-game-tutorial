import pyxel
from enum import Enum


class GameState(Enum):
    """ゲームの状態を表す列挙型"""
    PLAYING = 0
    GAME_OVER = 1


class GameObject:
    """ゲーム内のオブジェクトの基底クラス"""
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pyxel.rect(self.x, self.y, self.width, self.height, self.color)


class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 8, 8, 11)
        self.speed = 2

    def update(self):
        # 方向キーマッピング (キー: [x_direction, y_direction])
        key_map = {
            pyxel.KEY_LEFT: [-1, 0],
            pyxel.KEY_RIGHT: [1, 0],
            pyxel.KEY_UP: [0, -1],
            pyxel.KEY_DOWN: [0, 1]
        }

        # キー入力に応じてプレイヤーを移動
        for key, (dx, dy) in key_map.items():
            if pyxel.btn(key):
                self.x = max(0, min(152, self.x + dx * self.speed))
                self.y = max(0, min(112, self.y + dy * self.speed))


class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 8, 8, 8)
        self.dx = 1
        self.bullet_speed = 2

    def update(self):
        # 敵の移動
        self.x += self.dx

        # 画面端で跳ね返る (0と152はゲーム画面の端を考慮した値)
        if self.x < 0 or self.x > 152:
            self.dx = -self.dx

    def shoot(self):
        # 弾の発射位置を敵の中央下部に設定
        bullet_x = self.x + self.width // 2 - 1  # 弾の幅が2なので中心に配置
        bullet_y = self.y + self.height
        return Bullet(bullet_x, bullet_y, self.bullet_speed, False)


class Bullet(GameObject):
    def __init__(self, x, y, speed, is_player_bullet=True):
        # プレイヤーの弾か敵の弾かで色を変える
        color = 10 if is_player_bullet else 8
        super().__init__(x, y, 2, 6, color)
        self.speed = speed
        self.is_player_bullet = is_player_bullet
        self.screen_height = 120  # 画面の高さ

    def update(self):
        # 弾の移動方向を三項演算子で決定
        self.y += -self.speed if self.is_player_bullet else self.speed

    def is_out_of_screen(self):
        """画面外に出たかどうかの判定"""
        return self.y < 0 or self.y > self.screen_height

    def collides_with(self, obj):
        """オブジェクトとの衝突判定"""
        return (self.x < obj.x + obj.width and
                self.x + self.width > obj.x and
                self.y < obj.y + obj.height and
                self.y + self.height > obj.y)


class Game:
    # 画面サイズの定数
    WIDTH = 160
    HEIGHT = 120

    def __init__(self):
        # ゲームの初期設定
        pyxel.init(self.WIDTH, self.HEIGHT, title="First Game")

        # 音の設定
        self.setup_sounds()

        # ゲームの初期化
        self.reset_game()

        # ゲームループの開始
        pyxel.run(self.update, self.draw)

    def setup_sounds(self):
        """音の設定"""
        # 弾の発射音
        pyxel.sound(0).set("c3e3g3c4", "t", "7", "n", 20)
        # 敵を倒した音
        pyxel.sound(1).set("f3f2f1", "n", "7", "f", 10)

    def reset_game(self):
        """ゲームの初期状態をセットアップ"""
        # プレイヤーの初期位置（画面下部中央）
        player_x = self.WIDTH // 2 - 4  # プレイヤーの幅が8なので中央に配置
        player_y = self.HEIGHT - 20
        self.player = Player(player_x, player_y)

        # 敵の初期位置（画面上部中央）
        enemy_x = self.WIDTH // 2 - 4  # 敵の幅が8なので中央に配置
        enemy_y = 20
        self.enemy = Enemy(enemy_x, enemy_y)

        # 弾のリストを初期化
        self.player_bullets = []
        self.enemy_bullets = []

        # スコアとゲーム状態を初期化
        self.score = 0
        self.state = GameState.PLAYING

    def update(self):
        """ゲームの状態更新"""
        # 状態に応じた処理の分岐
        if self.state == GameState.PLAYING:
            self.update_gameplay()
        elif self.state == GameState.GAME_OVER:
            self.handle_game_over()

    def update_gameplay(self):
        """ゲームプレイ中の処理"""
        self.update_game_objects()
        self.handle_player_input()
        self.enemy_shoot()
        self.update_bullets()
        self.check_collisions()

    def handle_game_over(self):
        """ゲームオーバー時の処理"""
        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()

    def update_game_objects(self):
        """ゲーム内のオブジェクトを更新"""
        self.player.update()
        self.enemy.update()

    def handle_player_input(self):
        """プレイヤーの入力処理"""
        # スペースキーで弾を発射
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 弾の位置（プレイヤーの中心上部から発射）
            bullet_x = self.player.x + self.player.width // 2 - 1  # 弾の幅が2なので中央に配置
            bullet_y = self.player.y
            self.player_bullets.append(Bullet(bullet_x, bullet_y, 4))
            pyxel.play(0, 0)  # 音を鳴らす

    def update_bullets(self):
        """すべての弾を更新"""
        # すべての弾を更新
        for bullets in [self.player_bullets, self.enemy_bullets]:
            for bullet in bullets:
                bullet.update()

        # 画面外の弾を削除 - リスト内包表記で簡潔に
        self.player_bullets = [b for b in self.player_bullets if not b.is_out_of_screen()]
        self.enemy_bullets = [b for b in self.enemy_bullets if not b.is_out_of_screen()]

    def enemy_shoot(self):
        """敵の弾発射処理"""
        # 一定間隔（30フレーム）で敵が弾を発射
        shooting_interval = 30
        if pyxel.frame_count % shooting_interval == 0:
            self.enemy_bullets.append(self.enemy.shoot())

    def check_collisions(self):
        """衝突判定の処理"""
        self.check_player_bullets_enemy_collision()
        self.check_enemy_bullets_player_collision()

    def check_player_bullets_enemy_collision(self):
        """プレイヤーの弾と敵の衝突判定"""
        # 当たった弾のインデックスを集める
        bullets_to_remove = [
            i for i, bullet in enumerate(self.player_bullets)
            if bullet.collides_with(self.enemy)
        ]

        # 当たった弾があればスコア加算と効果音
        if bullets_to_remove:
            self.score += 10 * len(bullets_to_remove)
            pyxel.play(0, 1)  # 効果音

        # インデックスの大きい順に削除して位置ズレを防ぐ
        for i in sorted(bullets_to_remove, reverse=True):
            self.player_bullets.pop(i)

    def check_enemy_bullets_player_collision(self):
        """敵の弾とプレイヤーの衝突判定"""
        # 当たり判定のチェック
        collision = any(bullet.collides_with(self.player) for bullet in self.enemy_bullets)

        # 衝突があればゲームオーバー
        if collision:
            self.state = GameState.GAME_OVER
            # 弾をクリア（オプション）
            self.enemy_bullets.clear()

    def draw(self):
        """ゲーム画面の描画"""
        # 背景をクリア
        pyxel.cls(0)

        # ゲームオブジェクトの描画
        self.draw_game_objects()

        # UI要素の描画
        self.draw_ui()

    def draw_game_objects(self):
        """ゲーム内のオブジェクトを描画"""
        # プレイヤーと敵の描画
        self.player.draw()
        self.enemy.draw()

        # すべての弾を描画
        for bullet_list in [self.player_bullets, self.enemy_bullets]:
            for bullet in bullet_list:
                bullet.draw()

    def draw_ui(self):
        """UI要素の描画"""
        # スコア表示
        pyxel.text(5, 5, f"SCORE:{self.score}", 7)

        # ゲームオーバー表示
        if self.state == GameState.GAME_OVER:
            # 中央に表示
            center_x = self.WIDTH // 2
            game_over_text = "GAME OVER"
            restart_text = "PRESS R TO RESTART"

            # テキストの長さに基づいて中央揃え
            game_over_x = center_x - len(game_over_text) * 2
            restart_x = center_x - len(restart_text) * 2

            pyxel.text(game_over_x, 50, game_over_text, 8)
            pyxel.text(restart_x, 70, restart_text, 7)


# ゲーム開始
if __name__ == "__main__":
    Game()
