import pygame
pygame.init() # initialize font

# various dimensions
margin=5
line_w=2
icon_length=200
button_w=100
button_l=200
collision_error=10
screen_width=800
screen_length=400
pad_width=20
pad_length=100
pad_curvature=100
ball_start_pos = (screen_width/2,screen_length/2)
ball_diameter=30
ball_speed=5
ball_speed_increment=2
pad_speed=4

# time variables
clock=pygame.time.Clock()
fps=60

# colors
white=(255,255,255)
brown=(100,50,20)
light_yellow=(255,255,150)
black=(0,0,0)
light_blue=(100,100,255)
dark_blue=(0,0,100)
light_red=(255,100,100)
dark_red=(100,0,0)
green=(50,200,50)
light_violet=(255,100,255)
bgimage_col=(252,221,122)

# colors used
screen_col=light_yellow
boundary_col=black
ball_col=green

# points
max_point = 3
side=1

# fonts
base_font=pygame.font.Font(None,80)
base_font1=pygame.font.Font("fonts/Calfinedemo.ttf",80) 
base_font2=pygame.font.Font("fonts/GameOfSquids-1GMVL.ttf",30)

# backgrounds
ws=pygame.transform.scale(pygame.image.load("assets/ws.png"),(button_w,button_l))
updown=pygame.transform.scale(pygame.image.load("assets/updown.png"),(button_w,button_l))
init_bgimage=pygame.transform.scale(pygame.image.load("assets/front_bg.png"),(screen_width,screen_length))
bgimage=pygame.transform.scale(pygame.image.load("assets/bg.png"),(screen_width,screen_length))
blue_win=pygame.transform.scale(pygame.image.load("assets/blue_wins.png"),(icon_length,icon_length))
red_win=pygame.transform.scale(pygame.image.load("assets/red_wins.png"),(icon_length,icon_length))

# music and sounds
bg_music="sound_music\Lobby-Time.mp3"
#bg_music="sound_music\Powerful-Trap-.mp3"
click_sound=pygame.mixer.Sound("sound_music\mixkit-modern-click-box-check-1120.wav")
ball_pad_sound=pygame.mixer.Sound("sound_music\mixkit-basketball-ball-hard-hit-2093.wav")
out_sound=pygame.mixer.Sound("sound_music\mixkit-game-click-1114.wav")
winner_sound="sound_music\mixkit-conference-audience-clapping-strongly-476.wav"

class Ball():
    def __init__(self,center_pos,col,speedx,speedy):
        self.col=col
        self.speedx=speedx
        self.speedy=speedy
        self.center_pos=center_pos
        self.rect=pygame.Rect(0,0,ball_diameter,ball_diameter)
        self.rect.center= ball_start_pos
    def draw(self,screen):
        pygame.draw.rect(screen,self.col,self.rect,0,100)

class Player():
    def __init__(self,y_pos,col,speed):
        self.width=pad_width
        self.length=pad_length
        self.y_pos=y_pos
        self.col=col
        self.speed=speed
        self.rect=pygame.Rect(0,0,self.width,self.length)
        self.rect.center=(self.y_pos+pad_width/2,screen_length/2)
        self.point=0
    def draw(self,screen):
        pygame.draw.rect(screen,self.col,self.rect,0,pad_curvature)

# required objects 
screen=pygame.display.set_mode((screen_width,screen_length))
pygame.display.set_caption("pong")
pygame.display.set_icon(init_bgimage)

player1=Player(screen_width-pad_width,light_blue,0)
player2=Player(0,light_red,0)
ball=Ball(ball_start_pos,ball_col,0,0)