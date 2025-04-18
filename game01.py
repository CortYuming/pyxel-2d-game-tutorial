import pyxel


# ゲームの初期設定
pyxel.init(160, 120, title="First Game")


# 画面の更新処理
def update():
    pass


# 画面の描画処理
def draw():
    pyxel.cls(0)
    pyxel.text(55, 55, "Hello!", 7)


# ゲーム開始
pyxel.run(update, draw)
