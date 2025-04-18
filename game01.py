import pyxel


# ゲームの初期設定
pyxel.init(160, 120, title="First Game")

player_x = 80  # プレイヤーのX座標
player_y = 100  # プレイヤーのY座標
# 敵の変数
enemy_x = 80
enemy_y = 20
# 敵の移動方向
enemy_dx = 1
# 弾のリスト
bullets = []


# 画面の更新処理
def update():
    global player_x, player_y
    global enemy_x, enemy_y, enemy_dx


    # 矢印キーで移動
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x = player_x - 2
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x = player_x + 2
    if pyxel.btn(pyxel.KEY_UP):
        player_y = player_y - 2
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y = player_y + 2

    if player_x < 0:
        player_x = 0
    if player_x > 152:
        player_x = 152
    if player_y < 0:
        player_y = 0
    if player_y > 112:
        player_y = 112

    # 敵の移動
    enemy_x = enemy_x + enemy_dx

    # 画面端で跳ね返る
    if enemy_x < 0 or enemy_x > 152:
        enemy_dx = -enemy_dx

    # スペースキーで弾を発射
    if pyxel.btnp(pyxel.KEY_SPACE):
        # 弾の位置（プレイヤーの中心から発射）
        bullets.append([player_x + 4, player_y])

    # 弾の移動
    for bullet in bullets:
        bullet[1] -= 4  # 上に移動

    # 画面外に出た弾を削除
    for i in range(len(bullets)-1, -1, -1):
        if bullets[i][1] < 0:
            bullets.pop(i)


# 画面の描画処理
def draw():
    pyxel.cls(0)
    # プレイヤーを描画（四角形で表現）
    pyxel.rect(player_x, player_y, 8, 8, 11)
    # 敵を描画
    pyxel.rect(enemy_x, enemy_y, 8, 8, 8)

    # 弾の描画
    for bullet in bullets:
        pyxel.rect(bullet[0], bullet[1], 2, 6, 10)


# ゲーム開始
pyxel.run(update, draw)
