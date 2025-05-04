#!/usr/bin/env python
#-*- cording: utf-8 -*-

import platform
if platform.system() == "Linux": #for Raspberry pi
    import RPi.GPIO as GPIO
else:                            #for PC,emulater
    class GPIO:
        HIGH = 1
        LOW = 0
        def output(port, highlow):
            print(port,highlow,"emulated")
import pygame
from pygame.locals import *
import sys
import signal
import random
import jtalk

(W,H) = (480,320) # display Size
inputPortList2 = (2,3)      #inputPort2
inputPortList = (4,17,27,22,10,9,11,5,6,13,19,26) #switch GPIO Port
outputPortList = (21,20,16,12,7,8,25,24,23,18,15,14)
timerCount = 0
scoreCount = 0
led_lighting=[]     #lighting LED state
state = [0,0]

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((W, H))
t1 = "Hero Academy"
pygame.display.set_caption(t1)              # タイトルバーに表示する文字
font = pygame.font.Font(None, 55)               # フォントの設定(55px)

# for GPIO raspberry pi
if platform.system() == "Linux":
    ok_sound = pygame.mixer.Sound("/home/pi/Desktop/pingpong.wav")
    ng_sound = pygame.mixer.Sound("/home/pi/Desktop/ng.wav")
    ng2_sound = pygame.mixer.Sound("/home/pi/Desktop/ng2.wav")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(outputPortList, GPIO.OUT)
    GPIO.output(outputPortList, GPIO.LOW)
    GPIO.setup(inputPortList, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(inputPortList2, GPIO.IN)
    def callBackGPIO(channel):
        global scoreCount
        inputPortIndex = inputPortList.index(channel)
        if inputPortIndex in led_lighting:
            GPIO.output(outputPortList[inputPortIndex], GPIO.LOW)
            led_lighting.remove(inputPortIndex)
            text[inputPortIndex][3] = False
            ok_sound.play()
            scoreCount +=1
            updateDisplay()
        else:
            ng2_sound.play()
            scoreCount -=1
        print("callback",channel,inputPortList.index(channel))

    def callBackGPIO2(channel):
        print("callback2",channel,inputPortList2.index(channel))
        state[inputPortList2.index(channel)] += 1
        updateDisplay()

    for inputPortNo in inputPortList:
        GPIO.add_event_detect(inputPortNo, GPIO.BOTH, callback=callBackGPIO, bouncetime=500)
    for inputPortNo in inputPortList2:
        GPIO.add_event_detect(inputPortNo, GPIO.FALLING, callback=callBackGPIO2, bouncetime=500)

else:
    ok_sound = pygame.mixer.Sound("pingpong.wav")
    ng_sound = pygame.mixer.Sound("ng.wav")
    ng2_sound = pygame.mixer.Sound("ng2.wav")
    fin_sound = pygame.mixer.Sound("FIN1020.wav")
    start_sound = pygame.mixer.Sound("START517.wav")

pygame.mixer.music.load("BGM1522.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

# for display
num_switch = 12
text = []           #for display
for index in range(num_switch):
    text.append([index+1,W*(int(index%4)/4 + 1/12),H*(int(index/4)/3+1/10),False])
# print(text)
def updateDisplay():
    screen.fill((255,255,255))        # 画面を白色(#FFFFFF)に塗りつぶし
    #　タイトルの表示
    tx1 = font.render(t1, True, (200,200,200))
    screen.blit(tx1, [W/6,H*3/12])# 文字列の表示位置
    #　スコア、時間の表示
    tx2 = font.render("score="+str(scoreCount)+", time="+str(timerCount)+", "+str(state), True, (200,200,200))
    screen.blit(tx2, [W/6,H*7/12])# 文字列の表示位置
    #　数字の表示
    for t in text:
        if t[3] :
            txt = font.render(str(t[0]), True, (255,0,0))   # 描画する文字列の設定
        else:
            txt = font.render(str(t[0]), True, (200,200,200))   # 描画する文字列の設定
        screen.blit(txt,[t[1],t[2]]) # 文字列の表示位置
    pygame.display.update()     # 画面を更新

#for timer
def timeFunc(arg1,arg2):
    global timerCount
    timerCount +=1
    #ランダムでリストled_lightingに無いものを追加
    while True:
        index = random.randrange(num_switch)    #0〜11
        if index not in led_lighting:
            led_lighting.append(index)      #リストに追加
            text[index][3] = True                           #文字を明転
            GPIO.output(outputPortList[index], GPIO.HIGH)   #LED　ON
            break
    #リストに4つ以上あれば、消去
    if len(led_lighting) >3:
        text[led_lighting[0]][3] = False               #文字を暗転
        GPIO.output(outputPortList[led_lighting[0]], GPIO.LOW)     #LED OFF
        led_lighting.pop(0) #削除
    print(led_lighting)
    updateDisplay()

signal.signal(signal.SIGALRM, timeFunc)     #タイマーで呼び出す関数設定
signal.setitimer(signal.ITIMER_REAL, 1, 1)  #1秒後に1秒間隔でタイマー開始

while (1):
    pygame.time.wait(100)        # キー読み取り時間間隔　100msec
    # イベント処理
    for event in pygame.event.get():
        if event.type == QUIT :  # 閉じるボタンが押されたら終了
            pygame.quit()       # Pygameの終了(画面閉じられる)
            sys.exit()
        # キーを押したとき
        if event.type == KEYDOWN:
            # ESCキーなら終了
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            else:
                print(event.key,chr(event.key),event.key-49,led_lighting)
                if event.key-49 in led_lighting:
                    scoreCount +=1
                    ok_sound.play()
                    led_lighting.remove(event.key-49)
                    text[event.key-49][3] = False
                    GPIO.output(outputPortList[event.key-49], GPIO.LOW)
                    print(event.key,chr(event.key),event.key-49,led_lighting)
                elif chr(event.key) =="0" and 9 in led_lighting:
                    scoreCount +=1
                    led_lighting.remove(9)
                    text[9][3] = False
                    GPIO.output(outputPortList[9], GPIO.LOW)
                    ok_sound.play()
                elif chr(event.key) =="-" and 10 in led_lighting:
                    scoreCount +=1
                    led_lighting.remove(10)
                    text[10][3] = False
                    GPIO.output(outputPortList[10], GPIO.LOW)
                    ok_sound.play()
                elif chr(event.key) =="=" and 11 in led_lighting:
                    scoreCount +=1
                    led_lighting.remove(11)
                    text[11][3] = False
                    GPIO.output(outputPortList[11], GPIO.LOW)
                    ok_sound.play()
                elif event.key ==K_SPACE:
                    print(event.key,"space")
                    signal.alarm(0)
                    pygame.mixer.music.pause()
                    fin_sound.play()
                    pygame.time.wait(3000)        # キー読み取り時間間隔　100msec
                    jtalk.jtalk(str(scoreCount))

                    state[0] =~state[0]
                elif event.key ==K_RETURN:
                    print(event.key,"return")
                    state[1] =~state[1]
                    start_sound.play()
                    pygame.time.wait(3000)        # キー読み取り時間間隔　100msec
                    signal.setitimer(signal.ITIMER_REAL, 1, 1)
                    pygame.mixer.music.play()
                else:
                    scoreCount -=1
                    ng_sound.play()
        updateDisplay()
