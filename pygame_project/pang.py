import os
import pygame
#초기화
pygame.init()

#화면 크기 설정

screen_width = 640 
screen_height = 480
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀
pygame.display.set_caption("Pang")
#FPS
clock = pygame.time.Clock()

#1. 사용자 게임 초기화
current_path = os.path.dirname(__file__) #현재파일 위치 반환
asset_path = os.path.join(current_path, "Asset") #asset folder return

#background
background = pygame.image.load(os.path.join(asset_path,"background.png"))
#stage

stage = pygame.image.load(os.path.join(asset_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #스테이지 위에 캐릭터를 두기 위해 
#[0]은 너비의 값


#character
character = pygame.image.load(os.path.join(asset_path,"character.png")) #이미지 로드
character_size = character.get_rect().size #캐릭터 사이즈
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2) #캐릭터의 초기 위치.
character_y_pos = screen_height - character_height - stage_height
#이동 방향
character_to_x = 0 #양수일 경우 오른쪽, 음수일 경우 왼쪽
#이동속도
character_speed = 5


#무기
weapon = pygame.image.load(os.path.join(asset_path,"weapon.png")) #이미지 로드
weapon_size = weapon.get_rect().size #무기의 사이즈
weapon_width = weapon_size[0]
#여러발 사용 가능
weapons = [] #리스트로 만들어서 관리
# 무기 이동속도
weapon_speed = 10 #위로 상승해야하기 때문에

#공 만들기 (4개)

ball_images = [
    pygame.image.load(os.path.join(asset_path, "baloon1.png")),
    pygame.image.load(os.path.join(asset_path, "baloon2.png")),
    pygame.image.load(os.path.join(asset_path, "baloon3.png")),
    pygame.image.load(os.path.join(asset_path, "baloon4.png"))
    ]
#공의 크기에 따라 공의 낙하속도가 다름 (최초속도)
ball_speed_y = [-18, -15, -12, -9]  # index 0, 1, 2, 3 에 해당하는 값

#공의 정보들
balls = []

#공들의 정보를 딕셔너리로 , 처음 공 셋팅
balls.append({
    "pos_x": 50, #공의 x좌표
    "pos_y" : 50, #y좌표
    "img_idx": 0, #공 이미지 인덱스
    "to_x": 3, #x축 이동방향 오른쪽이면 양수
    "to_y": -6 , #Y축 이동방향 위로
    "init_spd_y": ball_speed_y[0] #최초 속도
})

# 사라질 무기, 공 정보 저장 변수

weapon_to_remove = -1
ball_to_remove = -1

game_font = pygame.font.Font(None,40)
total_time = 100

start_ticks = pygame.time.get_ticks()
# 게임 종료 메세지 타임아웃, 미션 컴플리트, 게임오버
game_result = "Game Over"

running = True
while running:
    dt = clock.tick(30)


    # 2. 이벤트 처리

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN: #키 누를 때
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])

        if event.type == pygame.KEYUP: #키를 떼었을 때
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 캐릭터 위치 정의
    character_x_pos += character_to_x

        #경계값 처리

    if character_x_pos < 0 :
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    #무기 위치 조정

    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # 무기위치 위로 올림
    
        #천장에 닿으면 무기 없애기

    weapons = [ [w[0],  w[1]] for w in weapons if w[1] > 0 ]

        # 공 위치 정의

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"] 
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

         # 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        #세로위치
        #스테이지에 튕겼을 때

        if ball_pos_y >= screen_height -stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: #그 외 모든 경우에 속도를 감소
            ball_val["to_y"] += 0.5 #

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

            
     

    # 4.  충돌
     # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos


    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect) :
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),   # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),   # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x" : -3,     # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y" : -6,    # y출 이동방향,
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]})   # y 최초 속도

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),   # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),   # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1,  # 공의 이미지 인덱스
                        "to_x" : 3,     # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y" : -6,    # y출 이동방향,
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]})   # y 최초 속도

        
                break

        else:
            continue
        break


    #충돌된 공 or 무기 없애기

    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons [weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우 게임 종료 (성공)
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. add view

    screen.blit(background, (0,0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos,weapon_y_pos))


    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))


    screen.blit(stage, (0,screen_height - stage_height))
    screen.blit(character, (character_x_pos,character_y_pos))

    #경과 시간 계산

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #ms -> s
    timer = game_font.render("Time : {}" .format(int(total_time - elapsed_time)), True, (255,255,255))
    screen.blit(timer,(10,10))


    if total_time - elapsed_time <= 0 :
        game_result = "Time Over"
        running = False


    pygame.display.update()

# 게임 오버 메세지
msg = game_font.render(game_result, True, (255, 255, 0))    # 노란색
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)

pygame.quit()