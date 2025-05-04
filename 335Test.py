import pygame
from pygame.locals import *
import sys

ScreenWidth = 800
ScreenHeight = 600
pygame.init()                                 # Pygameの初期化おはようございます
screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))  # 800*600の画面
pygame.display.set_caption("3-3&3-5 Presents")    # タイトルを作成

#STEP1.フォントの用意  
# for index, fontname in enumerate(sorted(pygame.font.get_fonts())):
#     try:
#         font = pygame.font.SysFont(fontname, 30)
#         print(f"{index+1}\t{fontname}")
#     except:
#         print(f"{index+1}\t{fontname} is not available!!")

font1 = pygame.font.SysFont("ヒラキノ丸コpronw4", 150)
font2 = pygame.font.SysFont(None, 150)
text1 = font1.render("日本語", True, (255,0,0))
text2 = font2.render("Default", True, (255,0,0))

px=120
py=100
directionX = 1
directionY = 1


running = True
while running:
    px+=directionX
    py+=directionY
    if (px >= ScreenWidth) or (px <= 0):
        directionX *= -1
    if (py >= ScreenHeight) or (py <= 0):
        directionY *= -1


    screen.fill((255,255,255))                                    # 背景を白
    pygame.draw.circle(screen,(10,10,10),(px,py),50)              # ●
    pygame.draw.rect(screen, (255,0,0), Rect(10,100,50,50), 1)    # ■
    pygame.draw.line(screen, (0,255,0), (0,200), (100,300), 2)    # 線
    screen.blit(text1, (px,py))
    screen.blit(text2, (px,py*2))
    pygame.display.update()                                       # 画面更新

    # keys = pygame.key.get_pressed()                               # キー入力を取得

    # イベント処理
    for event in pygame.event.get():  # イベントを取得
        if event.type == pygame.KEYDOWN:    # キー押下
            if event.key == pygame.K_r: px = 0; py = 0    # Rでリセット
            if event.key == pygame.K_q: running = False    # Qで終了
        if event.type == QUIT:        # 閉じるボタンが押されたら
            running = False          # ループを抜ける
    keys = pygame.key.get_pressed() # キー保持
    if keys[pygame.K_LEFT]:  directionX += -0.5   # 左
    if keys[pygame.K_RIGHT]: directionX += 0.5   # 右
    if keys[pygame.K_UP]:    directionY += -0.5   # 上
    if keys[pygame.K_DOWN]:  directionY += 0.5   # 下

pygame.quit()             # 全てのpygameモジュールの初期化を解除
sys.exit()                # 終了（ないとエラーで終了することになる）
