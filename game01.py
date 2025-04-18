import pyxel


# ゲームの初期設定
pyxel.init(160, 120, title="First Game")

player_x = 80  # プレイヤーのX座標
player_y = 100  # プレイヤーのY座標


# 画面の更新処理
def update():
    global player_x, player_y

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


# 画面の描画処理
def draw():
    pyxel.cls(0)
    # プレイヤーを描画（四角形で表現）
    pyxel.rect(player_x, player_y, 8, 8, 11)


# ゲーム開始
pyxel.run(update, draw)
