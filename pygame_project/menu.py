import pygame
from pygame import surface
from pygame import mouse
from pygame.constants import QUIT
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum 
import subprocess
import os


BLUE = (106,159,181)    # 배경 색
WHITE = (255,255,255)   # 텍스트 색

def create_surface_with_text(text,font_size, text_rgb, bg_rgb):         # 매개변수 텍스트, 폰트 크기, 텍스트 색, 배경 색
    font = pygame.freetype.SysFont("Courier", font_size,bold=True)      # 폰트 설정
    surface, _ = font.render(text= text, fgcolor=text_rgb, bgcolor = bg_rgb) # 뷰에 텍스트를 렌더링
    return surface.convert_alpha() # 뷰 리턴


class UIElement(Sprite): #Sprite , 독립된 이미지의 단위 여러장으로 쓰면 애니메이션 구현 가능, class를 이용하여 컴포넌트화.
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb,action=None):  #매개변수 center_position = 위치 action은 어떤 버튼을 클릭하는 지에 따라 작동
        super().__init__()

        self.mouse_over = False # 기본상태 -> Button에 마우스를 올리면 True 값이 되고 글자가 하이라이팅 됨.

        defalut_image = create_surface_with_text(text,font_size,text_rgb,bg_rgb) # 마우스 안 올렸을 때 defalut image

        highlighted_image = create_surface_with_text(text, font_size * 1.2, text_rgb,bg_rgb) #마우스 올렸을 때 highlighted_image 
        

        self.images = [defalut_image,highlighted_image]     

        self.rects = [                                              #위치 정보
            defalut_image.get_rect(center = center_position),
            highlighted_image.get_rect(center = center_position)
        ]
        self.action = action
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0] # 버튼에 mouse가 올라가있을 때, 하이라이트 이미지 리턴. 아닐 시 defalut


    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0] # 버튼에 mouse가 올라가있을 때, 하이라이트 위치정보. 아닐 시 defalut 


    def update(self,mouse_pos, mouse_up):  # 화면에 변화가 있을 시 업데이트
        if self.rect.collidepoint(mouse_pos): # mouse_pos는 마우스 위치를 튜플 값으로 받아오는데, rect와 충돌하면 mouse_over = True -> highlighted_image return
            self.mouse_over = True
            if mouse_up:            #클릭을 했을 경우
                return self.action #각 버튼 액션 실행
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image,self.rect)


class GameState(Enum):  #Game State를 Enum으로 저장
    QUIT = -1  #종료
    TITLE = 0 #메뉴
    Pang = 1 #팡 게임 실행
    Tetris = 2 #테트리스 실행
    Square = 3  #2048 실행


def main(): #메인 함수
    pygame.init() #pygame을 초기화

    screen = pygame.display.set_mode((800,800)) #스크린 사이즈 설정.

    game_state = GameState.TITLE #초기 state는 메뉴

    while True: #Quit 버튼을 누를 때까지 계속 실행.
        if game_state == GameState.TITLE: #메뉴
            game_state = title_screen(screen)

        if game_state == GameState.Pang: # Pang 버튼을 누를 시 
            game_state = GameState.TITLE # 게임 상태를 메뉴로 바꿔주고 (안바꿔주면 무한실행.)
            subprocess.call(['python', './pang.py']) #subprocess를 이용해서, 경로 상에 있는 pang.py 실행

        if game_state == GameState.Tetris:
            game_state = GameState.TITLE
            subprocess.call(['python', './tetris.py']) #subprocess를 이용해서, 경로 상에 있는 tetris.py 실행

        if game_state == GameState.Square:
            game_state = GameState.TITLE
            subprocess.call(['python', './2048.py']) #subprocess를 이용해서, 경로 상에 있는 2048.py 실행

        if game_state == GameState.QUIT:
            pygame.quit()
            return



def title_screen(screen): #메뉴 구성

    pang_btn = UIElement(               # class를 이용한 Button 생성
        center_position= (400, 300), #위치
        font_size= 30,
        bg_rgb= BLUE,
        text_rgb= WHITE,
        text = 'Pang',
        action=GameState.Pang #선택시 GameState가 Pang으로 바뀌고, 위에 main함수에 의해 팡 게임 실행.
        )

    tetris_btn = UIElement(
        center_position= (400, 400),
        font_size= 30,
        bg_rgb= BLUE,
        text_rgb= WHITE,
        text = 'Tetris',
        action=GameState.Tetris    #선택시 GameState가 Tetris로 바뀌고, 위에 main함수에 의해 테트리스 게임 실행.
        )
        
    square_btn = UIElement(
        center_position= (400, 500),
        font_size= 30,
        bg_rgb= BLUE,
        text_rgb= WHITE,
        text = '2048',
        action=GameState.Square #선택시 GameState가 Square로 바뀌고, 위에 main함수에 의해 2048 게임 실행.
        )

    quit_btn = UIElement(
        center_position= (400, 600),
        font_size= 30,
        bg_rgb= BLUE,
        text_rgb= WHITE,
        text = 'Quit',
        action=GameState.QUIT #선택시 GameState가 QUIT으로 바뀌고, 게임종료
        )
    

    buttons = [pang_btn, tetris_btn,square_btn, quit_btn] #버튼들을 리스트에 넣고

    while True: 
        mouse_up = False #초기값 버튼 클릭 안했을 때,
        for event in pygame.event.get(): #event들을 받고 
            if event.type == pygame.MOUSEBUTTONUP and (event.button ==1): # 마우스 버튼을 누른 후 뗄 때
                mouse_up = True     #클릭!

        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(),mouse_up) #클릭액션 발생
            if ui_action is not None:
                return ui_action #클릭액션
            button.draw(screen) #모든 버튼 스크린에 그려주기
        pygame.display.flip()



print(os.getcwd())





main() #메인 함수 실행.



