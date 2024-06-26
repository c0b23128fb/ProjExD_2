import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1000, 600
DELTA  = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect，または，爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect，または，爆弾Rect
    戻り値：横方向判定結果，縦方向判定結果（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: 
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def GameOver1():
    """
    フォントサイズを80に設定する
    白字で"GameOver"と書く
    """
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("GameOver", True, (255, 255, 255))
    return txt


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) 
    clock = pg.time.Clock()
    ki_img = pg.image.load("fig/8.png") # 泣いてる工科トン
    ki_rct = ki_img.get_rect()
    ki_rct.center = 680, 300
    ko_img = pg.image.load("fig/7.png") # 工科トン
    ko_rct = ko_img.get_rect()
    ko_rct.center = 300, 300

    tmr = 0
    txt = GameOver1()
    vx, vy = +5, +5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct): # 工科トンと爆弾がぶつかったら
            pg.draw.rect(bg_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT)) # 四角を描画
            alpha = 128 # 透明度
            bg_img.set_alpha(alpha)
            screen.blit(bg_img, [0, 0]) # 半透明の背景を表示
            screen.blit(txt, [350, 250]) # テキストを表示
            screen.blit(ki_img, ki_rct) # 泣いてる工科トン
            screen.blit(ko_img, ko_rct) # 工科トン
            pg.display.update()
            time.sleep(5) # 5秒止まる
            return

        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed() # 
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]: # キーを押したとき
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]

        kk_rct.move_ip(sum_mv) # こうかとんの判定
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct) # こうかとんを表示
        bd_rct.move_ip(vx, vy)  # バクダンの動き
        screen.blit(bd_img, bd_rct) # バクダンを表示
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
