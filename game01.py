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
# スコア変数
score = 0
# 敵の弾リスト
enemy_bullets = []
# ゲーム状態
game_over = False

# 音の設定
pyxel.sound(0).set("c3e3g3c4", "t", "7", "n", 20)  # 弾の発射音
pyxel.sound(1).set("f3f2f1", "n", "7", "f", 10)   # 敵を倒した音


# 画面の更新処理
def update():
    global player_x, player_y
    global enemy_x, enemy_y, enemy_dx
    global score
    global game_over

    # ゲームオーバーならリスタート処理のみ
    if game_over:
        if pyxel.btnp(pyxel.KEY_R):
            # ゲームをリセット
            player_x = 80
            player_y = 100
            enemy_x = 80
            enemy_y = 20
            enemy_dx = 1
            bullets.clear()
            enemy_bullets.clear()
            score = 0
            game_over = False
        return

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
        pyxel.play(0, 0)  # 音を鳴らす

    # 弾の移動
    for bullet in bullets:
        bullet[1] -= 4  # 上に移動

    # 画面外に出た弾を削除
    # 弾と敵の当たり判定
    for i in range(len(bullets)-1, -1, -1):
        bullet_x = bullets[i][0]
        bullet_y = bullets[i][1]

        # 弾と敵が重なっているか
        if (bullet_x < enemy_x + 8 and
                bullet_x + 2 > enemy_x and
                bullet_y < enemy_y + 8 and
                bullet_y + 6 > enemy_y):
            # 敵に当たった
            bullets.pop(i)  # 弾を消す
            score += 10     # スコア加算
            pyxel.play(0, 1)  # 効果音

    # 一定間隔で敵が弾を発射
    if pyxel.frame_count % 30 == 0:
        enemy_bullets.append([enemy_x + 4, enemy_y + 8])

    # 敵の弾の移動
    for bullet in enemy_bullets:
        bullet[1] += 2  # 下に移動

    # 画面外の弾を削除
    # プレイヤーと敵の弾の当たり判定
    for i in range(len(enemy_bullets)-1, -1, -1):
        bullet = enemy_bullets[i]
        if (bullet[0] < player_x + 8 and
                bullet[0] + 2 > player_x and
                bullet[1] < player_y + 8 and
                bullet[1] + 6 > player_y):
            # プレイヤーがやられた
            game_over = True
            enemy_bullets.pop(i)


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

    # 敵の弾の描画
    for bullet in enemy_bullets:
        pyxel.rect(bullet[0], bullet[1], 2, 6, 8)

    # ゲームオーバー表示
    if game_over:
        pyxel.text(55, 50, "GAME OVER", 8)
        pyxel.text(40, 70, "PRESS R TO RESTART", 7)

    # スコア表示
    pyxel.text(5, 5, f"SCORE:{score}", 7)


# ゲーム開始
pyxel.run(update, draw)
