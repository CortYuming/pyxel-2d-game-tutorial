# Pyxelで作る簡単シューティングゲーム 01

## レッスン1：Pyxelとは何か（45分）

**目標:** Pyxelの基本を理解し、最初のプログラムを動かす

**必要なもの:**
- パソコン
  - Pyxel のインストール
  - エディタ

**授業の流れ:**

1. **導入（5分）**
- ゲームプログラミングについての簡単な説明
- 完成形のゲームデモを見せる

2. **Pyxelの紹介（10分）**
- Pyxelとは何か：シンプルなレトロゲーム作成ツール
- 色やピクセルについての基礎知識
- どんなゲームが作れるか例を見せる

3. **環境確認（5分）**
- Pyxel のサンプルコードが動くか確認
- エディタでpythonのコードに色が付くか確認

4. **最初のプログラム（15分）**


```python
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
```

- コードを一行ずつ説明
- 一緒に入力して実行

5. **簡単な図形を描く（10分）**
- 円、四角形を描く方法
- 色の変え方
- 位置の変え方

6. **まとめと次回予告（5分）**
- 今日学んだことの復習
- 次回は自機（キャラクター）を動かすことを予告


## レッスン2：キャラクターを動かそう（45分）

**目標:** キーボード入力でキャラクターを動かす方法を学ぶ

**必要なもの:**
- 前回のコード

**授業の流れ:**
1. **復習（5分）**
- 前回のコードを実行
- Pyxelの基本構造を思い出す

2. **自機の表示（10分）**

```python
# グローバル変数
player_x = 80  # プレイヤーのX座標
player_y = 100  # プレイヤーのY座標


def draw():
    pyxel.cls(0)
    # プレイヤーを描画
    pyxel.rect(player_x, player_y, 8, 8, 11)
```

- 変数の概念（プレイヤーの位置を記憶する箱）を説明

3. **キーボード入力の取得（15分）**

```python
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
```

- キーボード入力の検出方法
- if文（条件分岐）の使い方

4. **画面の端を超えない処理（10分）**

```python
# 画面外に出ないようにする
    if player_x < 0:
        player_x = 0
    if player_x > 152:
        player_x = 152
    if player_y < 0:
        player_y = 0
    if player_y > 112:
        player_y = 112
```

- 画面の範囲と座標の関係
- 境界チェックの考え方

5. **実践と調整（5分）**
- 速度の調整（数値を変えて動きを変える）
- 自機の大きさや色の変更


## レッスン3：敵と弾を作ろう（45分）

**目標:** 敵キャラクターと発射する弾の作成

**必要なもの:**
- 前回までのコード
- 配列の概念の説明（必要であれば）

**授業の流れ:**
1. **復習（5分）**
- 前回作成したプレイヤーの動きを確認

2. **敵の表示（10分）**

```python
# 敵の変数
enemy_x = 80
enemy_y = 20


def draw():
    # 前略
    # 敵を描画
    pyxel.rect(enemy_x, enemy_y, 8, 8, 8)
```

- 敵の初期位置の設定

3. **敵の動き（10分）**

```python
# 敵の移動方向
enemy_dx = 1


def update():
    # 前略
    global enemy_x, enemy_y, enemy_dx

    # 敵の移動
    enemy_x = enemy_x + enemy_dx

    # 画面端で跳ね返る
    if enemy_x < 0 or enemy_x > 152:
        enemy_dx = -enemy_dx
```

- 自動的に動く敵の作り方
- 左右に動いて壁で跳ね返る動き

4. **弾の発射（15分）**

```python
# 弾のリスト
bullets = []


def update():
    # 前略

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


def draw():
    # 前略

    # 弾の描画
    for bullet in bullets:
        pyxel.rect(bullet[0], bullet[1], 2, 6, 10)
```

- リスト（配列）の基本概念
- 複数の弾を管理する方法

5. **動作確認（5分）**
- 敵が動き、弾が発射されるか確認
- 必要に応じて調整

## レッスン4：当たり判定とゲームオーバー（45分）

**目標:** 当たり判定の仕組みを理解し、ゲームのルールを完成させる

**必要なもの:**
- 前回までのコード
- 当たり判定の図解資料

**授業の流れ:**
1. **復習（5分）**
- 前回までの進捗を確認

2. **当たり判定の説明（10分）**
- 四角形同士の衝突判定の考え方
- 座標と大きさを使った計算方法

3. **弾と敵の当たり判定（15分）**

```python
# スコア変数
score = 0


def update():
    # 前略
    global score

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
```

- 当たり判定のコード解説
- スコアの概念導入

4. **敵の弾の作成（10分）**

```python
# 敵の弾リスト
enemy_bullets = []


def update():
    # 前略

    # 一定間隔で敵が弾を発射
    if pyxel.frame_count % 30 == 0:
        enemy_bullets.append([enemy_x + 4, enemy_y + 8])

    # 敵の弾の移動
    for bullet in enemy_bullets:
        bullet[1] += 2  # 下に移動

    # 画面外の弾を削除
    for i in range(len(enemy_bullets)-1, -1, -1):
        if enemy_bullets[i][1] > 120:
            enemy_bullets.pop(i)


def draw():
    # 前略

    # 敵の弾の描画
    for bullet in enemy_bullets:
        pyxel.rect(bullet[0], bullet[1], 2, 6, 8)
```

- 敵からの攻撃の実装

5. **ゲームオーバー条件（5分）**

```python
# ゲーム状態
game_over = False


def update():
    # 前略
    global game_over

    # ゲームオーバーなら操作を受け付けない
    if game_over:
        return

    # 略

    # 画面外の弾を削除
    # プレイヤーと敵の弾の当たり判定
    for i in range(len(enemy_bullets)-1, -1, -1):
        if enemy_bullets[i][1] > 120:
            enemy_bullets.pop(i)

        bullet = enemy_bullets[i]
        if (bullet[0] < player_x + 8 and
                bullet[0] + 2 > player_x and
                bullet[1] < player_y + 8 and
                bullet[1] + 6 > player_y):
            # プレイヤーがやられた
            game_over = True
            enemy_bullets.pop(i)


def draw():
    # 前略

    # ゲームオーバー表示
    if game_over:
        pyxel.text(55, 50, "GAME OVER", 8)
        pyxel.text(40, 70, "PRESS R TO RESTART", 7)
```

**次回予告**

- ゲームオーバー状態の管理
- リスタート機能の追加

## レッスン5：ゲームの完成とカスタマイズ（45分）

**目標:** ゲームを完成させ、自分だけのオリジナル要素を追加する

**必要なもの:**
- 前回までのコード
- カスタマイズアイデアのワークシート

**授業の流れ:**
1. **復習と前回の続き（10分）**
- 前回の実装の確認と調整
- リスタート機能の完成

```python
def update():
    # 略

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
```

- リスタートの仕組みを説明

2. **スコア表示の追加（5分）**


```python
def draw():
    # 前略

    # スコア表示
    pyxel.text(5, 5, f"SCORE:{score}", 7)
```

- 文字列とスコア変数の表示方法

3. **音楽・効果音の追加（10分）**

```python
# 音の設定
pyxel.sound(0).set("c3e3g3c4", "t", "7", "n", 20)  # 弾の発射音
pyxel.sound(1).set("f3f2f1", "n", "7", "f", 10)   # 敵を倒した音


def update():
    # 略（下記if文の中で「音を鳴らす」の行を追加する）
    # スペースキーで弾を発射
    if pyxel.btnp(pyxel.KEY_SPACE):
        bullets.append([player_x + 4, player_y])
        pyxel.play(0, 0)  # 音を鳴らす

    # 略

    # 弾と敵の当たり判定（効果音を追加する）
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

```

- 簡単な効果音の追加方法

4. **リファクタリング（5分）**

``` diff
-    global player_x, player_y
-    global enemy_x, enemy_y, enemy_dx
-    global score
-    global game_over
+    global player_x, player_y, enemy_x, enemy_y, enemy_dx, score, game_over
```

``` diff
     # 矢印キーで移動
     if pyxel.btn(pyxel.KEY_LEFT):
-        player_x = player_x - 2
+        player_x = max(0, player_x - 2)
     if pyxel.btn(pyxel.KEY_RIGHT):
-        player_x = player_x + 2
+        player_x = min(152, player_x + 2)
     if pyxel.btn(pyxel.KEY_UP):
-        player_y = player_y - 2
+        player_y = max(0, player_y - 2)
     if pyxel.btn(pyxel.KEY_DOWN):
-        player_y = player_y + 2
-
-    if player_x < 0:
-        player_x = 0
-    if player_x > 152:
-        player_x = 152
-    if player_y < 0:
-        player_y = 0
-    if player_y > 112:
-        player_y = 112
+        player_y = min(112, player_y + 2)
```

``` diff
     # 敵の移動
-    enemy_x = enemy_x + enemy_dx
+    enemy_x += enemy_dx
```

- コードの改善の例

5. **個人カスタマイズ時間（15分）**
- 自分だけのゲーム要素を考える
- 色の変更、キャラクターデザインの変更
- 難易度調整（敵の速さ、弾の速さなど）
- オリジナル機能の追加（可能な範囲で）

6. **発表会と振り返り（5分）**
- 数人の生徒に完成したゲームを発表してもらう
- 学んだことの振り返り
- 次のステップの紹介
  - 弾のクールダウンで連射制限
  - プレイヤーのライフ制（3回まではOK）
  - 敵のスピードを変えて難易度調整
  - アイテム要素やスコア倍率
  - グラフィック適用


## 指導者向け補足情報

**事前準備**
- 各パソコンにPyxelをインストール（`pip install pyxel`）
- サンプルコードを用意して、すぐに実行できるようにしておく
- トラブルシューティングの準備（一般的なエラーへの対処法）

**評価ポイント**
- 基本概念の理解度（変数、条件分岐、ループ）
- プログラムの動作（指示通りに動くか）
- 創造性（オリジナル要素の追加）
- 課題への取り組み姿勢

**発展課題**
- 複数の敵を作る（リストを使用）
- レベルデザイン（難易度が徐々に上がる）
- パワーアップアイテムの追加
- 背景のデザイン

## 完成したコードの例（flake8準拠）


```python
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
    global player_x, player_y, enemy_x, enemy_y, enemy_dx, score, game_over

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
        player_x = max(0, player_x - 2)
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x = min(152, player_x + 2)
    if pyxel.btn(pyxel.KEY_UP):
        player_y = max(0, player_y - 2)
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y = min(112, player_y + 2)

    # 敵の移動
    enemy_x += enemy_dx

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
```
