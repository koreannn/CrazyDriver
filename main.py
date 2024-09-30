# REF : Do it! 게임 10개 만들며 배우는 파이썬
import pygame
import sys, time
from pygame.locals import * # pygame의 모든 지역 변수를 불러와서, 현재 작업 공간의 지역변수처럼 사용 가능

import random

import os

################# 게임 경로(path) 설정 #######################
# print(__file__) # 현재 작업 공간의 파일 이름까지 포함해서 출력
# print(os.path.dirname(__file__)) # 현재 작업 공간의 파일 이름은 제외하고, 상위 경로까지만 출력
GAME_ROOT_FOLDER = os.path.dirname(__file__)
IMAGE_FOLDER = os.path.join(GAME_ROOT_FOLDER, "GameImages")
SCORE_FILE = os.path.join(GAME_ROOT_FOLDER, "score.txt")

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

################# 게임 변수 초기화 ###########################
player_move_speed = 5
enemy_car_speed = random.randrange(3,6)
score = 0
paused = False
eNum = -1

################ 노래 추가 #################################
pygame.mixer.init()
pygame.mixer.music.load('Dontstopme.mp3')
pygame.mixer.music.play(-1, 0.0)

################# 최고 점수 파일 불러오기 ######################
def load_high_score():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, 'r') as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_high_score(high_score):
    with open(SCORE_FILE, 'w') as f :
        f.write(str(high_score))
        
high_score = load_high_score() # 최고 점수 불러오기

################# 텍스트의 폰트 및 사이즈 ######################
textFonts = ['comicsansms', 'arial']
textSize = 48


################## 게임 종료 함수(사용자 정의) ####################
def GameOver():
    global high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)
        
    # 게임 끝내기 문자열 만들기
    fontGameOver = pygame.font.SysFont(textFonts, textSize)
    textGameOver = fontGameOver.render(f"Game Over!", True, RED)
    rectGameOver = textGameOver.get_rect()
    rectGameOver.center = (ROAD_IMG.get_width()//2,
                           ROAD_IMG.get_height()//2)
    
    fontGameOver2 = pygame.font.SysFont(textFonts, textSize//2)
    textGameOver2 = fontGameOver2.render("Score :" + str(score), True, RED)
    rectGameOver2 = textGameOver2.get_rect()
    rectGameOver2.center = (ROAD_IMG.get_width()//2,
                           ROAD_IMG.get_height()//2 + 80)
    
    fontGameOver3 = pygame.font.SysFont(textFonts, textSize//2)
    textGameOver3 = fontGameOver3.render("High Score :" + str(high_score), True, RED)
    rectGameOver3 = textGameOver3.get_rect()
    rectGameOver3.center = (ROAD_IMG.get_width()//2,
                           ROAD_IMG.get_height()//2 + 160)

    fontGameOver4 = pygame.font.SysFont(textFonts, textSize//2)
    textGameOver4 = fontGameOver4.render("To try again, press Enter", True, WHITE)
    rectGameOver4 = textGameOver4.get_rect()
    rectGameOver4.center = (ROAD_IMG.get_width()//2,
                           ROAD_IMG.get_height()//2 + 240)
    # 검은색 배경에 게임 오버 메시지 출력하기
    screen.fill(BLACK)
    screen.blit(textGameOver, rectGameOver)
    screen.blit(textGameOver2, rectGameOver2)
    screen.blit(textGameOver3, rectGameOver3)
    screen.blit(textGameOver4, rectGameOver4)

    # 출력 업데이트하기
    pygame.display.update()
    # 객체 없애기
    player_car.kill()
    enemy_car.kill()
    
    # 종료 조건 : 엔터 입력 기다림
    wait_for_enter()
    # # 일시 정지하기
    # time.sleep(3)
    # # 게임 끝내기 
    # pygame.quit()
    # sys.exit()

################## 게임 리셋 함수 #####################
def reset_game():
    global score, player_car, enemy_car, eNum, enemy_car_speed
    # 점수 초기화
    score = 0
    
    # 플레이어 초기 위치 설정
    h = ROAD_IMG.get_width()//2
    v = ROAD_IMG.get_height() - (PLAYER_CAR_IMG.get_height()//2)
    player_car = pygame.sprite.Sprite()
    player_car.image = PLAYER_CAR_IMG
    player_car.surf = pygame.Surface(PLAYER_CAR_IMG.get_size())
    player_car.rect = player_car.surf.get_rect(center = (h, v))

    # 적 초기화
    eNum = -1
    enemy_car_speed = random.randrange(3, 6)

################## 엔터 입력 대기 함수 ####################
def wait_for_enter():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_RETURN:
                reset_game()  # 게임 리셋
                return  # 메인 게임 루프로 돌아가기

################## 게임 시작 부분 #####################
pygame.init()

clock = pygame.time.Clock() # Frame rate를 설정하기 위한 '시간'에 대한 인스턴스 생성
clock.tick(60) # Frame rate 설정 : 1초당 화면을 업데이트하는 비율

################## 제목 표시줄 #######################
pygame.display.set_caption("Crazy Driver")

################## 게임에 나오는 이미지 불러오기 #############################
ROAD_IMG = pygame.image.load(os.path.join(IMAGE_FOLDER, "Road.png")) # 배경 이미지
PLAYER_CAR_IMG = pygame.image.load(os.path.join(IMAGE_FOLDER, "Player.png")) # 플레이어 이미지
ENEMY_CAR_IMG = []
ENEMY_CAR_IMG.append(pygame.image.load(os.path.join(IMAGE_FOLDER, "Enemy.png"))) # 적 자동차 이미지
ENEMY_CAR_IMG.append(pygame.image.load(os.path.join(IMAGE_FOLDER, "Enemy2.png")))
ENEMY_CAR_IMG.append(pygame.image.load(os.path.join(IMAGE_FOLDER, "Enemy3.png")))


################## 창(Window) #########################
# screen = pygame.display.set_mode((800, 800))
screen = pygame.display.set_mode(ROAD_IMG.get_size()) # Window를 내맘대로 하지 말고, 배경(ROAD_IMG)의 크기에 맞게 사이즈 설정하기
screen.fill(WHITE)
pygame.display.update()

################## 게임 객체(player_car, enemy_car) 만들기 #####################
##### 1. player 초기 위치 계산 및 sprite 정의
h = ROAD_IMG.get_width()//2 # 가로 : 도로 배경의 중간
v = ROAD_IMG.get_height() - (PLAYER_CAR_IMG.get_height()//2)
# 1-1. sprite
player_car = pygame.sprite.Sprite()
player_car.image = PLAYER_CAR_IMG
player_car.surf = pygame.Surface(PLAYER_CAR_IMG.get_size())
player_car.rect = player_car.surf.get_rect(center = (h, v))

# #####  2. enemy 초기 위치 계산 및 sprite 정의
# hl = ENEMY_CAR_IMG.get_width()//2 # horizontal left(hl) : 가로 왼쪽
# hr = ROAD_IMG.get_width() - (ENEMY_CAR_IMG.get_width()//2) # horizontal right(hr) : 가로 오른쪽
# h = random.randrange(hl, hr)
# v = 0

# # 2-2. sprite
# enemy_car = pygame.sprite.Sprite()
# enemy_car.image = ENEMY_CAR_IMG
# enemy_car.surf = pygame.Surface(ENEMY_CAR_IMG.get_size())
# enemy_car.rect = enemy_car.surf.get_rect(center = (h, v))



################## 메인 루프 ##################################
while True:
    ############# 윈도우 제목 Score랑 같이 나타내기 ##########
    pygame.display.set_caption("Crazy Driver - Score " + str(score))
    
    ############# 배경 확인하기 ###############
    screen.blit(ROAD_IMG, (0,0))
    
    ############# (초기)player_car 화면에 두기 #############
    screen.blit(player_car.image, player_car.rect)
    
    ############ 적이 있는지 확인하기
    if eNum == -1 :
        # 무작위로 적 발생시키기
        eNum = random.randrange(0, len(ENEMY_CAR_IMG))
        # 적 초기 위치 계산하기
        # enemy_car.rect.top = 0 # 적 자동차 다시 위로 올려보내기
        hl = ENEMY_CAR_IMG[eNum].get_width()//2 
        hr = ROAD_IMG.get_width() - (ENEMY_CAR_IMG[eNum].get_width()//2)
        h = random.randrange(hl, hr)
        v = 0
        # enemy sprite 만들기
        enemy_car = pygame.sprite.Sprite()
        enemy_car.image = ENEMY_CAR_IMG[eNum]
        enemy_car.surf = pygame.Surface(ENEMY_CAR_IMG[eNum].get_size())
        enemy_car.rect = enemy_car.surf.get_rect(center = (h, v))
        
        # enemy_car.rect.center = (h, v)
        # enemy_car_speed = random.randrange(4,7)
        # score += 1 # player가 enemy를 피한것으로 간주하고, score를 증가시키기
    
    
    
    # Player_car 움직이기
    keys = pygame.key.get_pressed()
    
    if keys[K_LEFT] and player_car.rect.left > 0 :
        player_car.rect.move_ip(-player_move_speed, 0) # 왼쪽으로 이동
        if player_car.rect.left < 0 :
            player_car.rect.left = 0 # 너무 왼쪽으로 갔다면, 되돌리기
    if keys[K_RIGHT] and player_car.rect.right < ROAD_IMG.get_width() :
        player_car.rect.move_ip(player_move_speed, 0) # 오른쪽으로 이동
        if player_car.rect.right > ROAD_IMG.get_width() :
            player_car.rect.right = ROAD_IMG.get_width() # 너무 오른쪽으로 갔다면, 되돌리기
    
    ############# enemy_car 화면에 두기 #############
    screen.blit(enemy_car.image, enemy_car.rect)
    enemy_car.rect.move_ip(0, enemy_car_speed) # Arguments : 각각 수평, 수직으로 움직일 픽셀의 숫자
    
    if (enemy_car.rect.bottom > ROAD_IMG.get_height()): # 적 자동차가 화면 밖으로 나갈 경우
        # # enemy_car.rect.top = 0 # 적 자동차 다시 위로 올려보내기
        # hl = ENEMY_CAR_IMG.get_width()//2 
        # hr = ROAD_IMG.get_width() - (ENEMY_CAR_IMG.get_width()//2) 
        # h = random.randrange(hl, hr)
        # v = 0
        # enemy_car.rect.center = (h, v)
        # enemy_car_speed = random.randrange(4,7)
        enemy_car.kill()
        eNum = -1
        score += 1 # player가 enemy를 피한것으로 간주하고, score를 증가시키기
        enemy_car_speed = random.randrange(4,8)
        
        
    ############# enemy ~ player 충돌 감지하기 #########
    if pygame.sprite.collide_rect(player_car, enemy_car):
        GameOver()
    
    # 이벤트(종료 이벤트 등)확인하기
    for event in pygame.event.get(): 
        if event.type == QUIT: # 일단 게임 종료(창 종료)조건은 사용자가 창을 닫을 경우에만 종료되는거로 (pygame의 지역 변수 사용)
            pygame.quit()
            sys.exit()
    
    pygame.display.update()

