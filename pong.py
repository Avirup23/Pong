import pygame,sys,time
from variables import *
from pygame.locals import *

pygame.init()

class Game():
    def __init__(self,screen,player1,player2,ball):
        self.screen=screen
        self.player1=player1
        self.player2=player2
        self.ball=ball
        self.finish=0
        self.begin=0
        self.initialize=0
        self.music_start=1
        self.delay_ind=1
        self.collision_count=0
    def run(self):
        while True:
            clock.tick(fps)
            for event in pygame.event.get():
                keys_pressed=pygame.key.get_pressed()
                if event.type == QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and self.initialize == 1:
                    if keys_pressed[K_SPACE] and self.ball.rect.center == ball_start_pos:
                        click_sound.play()
                        self.begin=1
                        self.start()
            
            if self.player1.point==max_point or self.player2.point==max_point:
                self.finish = 1
            if self.collision_count==5 and abs(self.ball.speedx)<=9:
                self.collision_count=0
                self.ball.speedx+=ball_speed_increment*(self.ball.speedx/abs(self.ball.speedx))
            
            if self.initialize==0:
                # init window
                if keys_pressed[K_SPACE]:
                    click_sound.play()
                    self.initialize=1
            elif self.finish ==0 :
                # game window
                self.player_movements(keys_pressed,self.player1,pygame.K_UP,pygame.K_DOWN)
                self.player_movements(keys_pressed,self.player2,pygame.K_w,pygame.K_s)
                self.ball_movements()
            else:
                # restart game window
                self.player1.rect.centery=screen_length/2
                self.player2.rect.centery=screen_length/2
                if keys_pressed[K_SPACE]:
                    click_sound.play()
                    self.finish=0
                    self.player1.point=0
                    self.player2.point=0
                    self.out()
            self.screen_display()

    def ball_movements(self):
        if self.ball.rect.bottom >= screen_length or self.ball.rect.top <= 0:
            self.ball.speedy *=(-1)
        # win points  
        elif self.ball.rect.left <= margin:
            self.player1.point +=1
            out_sound.play()
            self.out()
        elif self.ball.rect.right >= screen_width-margin:
            self.player2.point +=1
            self.out()
            out_sound.play()

        # ball movements
        self.ball.rect.centerx += self.ball.speedx
        self.ball.rect.centery += self.ball.speedy
            
    def player_movements(self,keys_pressed,player,k1,k2):
        # key and player rellations 
        if keys_pressed[k1]and player.rect.top > 0: 
            player.speed = -pad_speed   
        elif keys_pressed[k2] and player.rect.bottom < screen_length: 
            player.speed = pad_speed
        else:
            player.speed = 0
        
        # player movements
        player.rect.y +=player.speed

        # collision of pad and ball    
        if player.rect.colliderect(self.ball.rect):
            if abs(self.ball.rect.left-player.rect.right)<collision_error and self.ball.speedx < 0:
                self.ball.speedx *= (-1)
                self.ball.speedy += player.speed/2
                ball_pad_sound.play()
                self.collision_count+=1
            elif abs(self.ball.rect.right-player.rect.left)<collision_error and self.ball.speedx > 0:
                self.ball.speedx *= (-1)
                self.ball.speedy += player.speed/2
                ball_pad_sound.play()
                self.collision_count+=1
            elif abs(self.ball.rect.top-player.rect.bottom)<collision_error and self.ball.speedy < 0:
                self.ball.speedy *= (-1)
                ball_pad_sound.play()
                self.collision_count+=1
            elif abs(self.ball.rect.bottom-player.rect.top)<collision_error and self.ball.speedx > 0:
                self.ball.speedy *= (-1)
                ball_pad_sound.play()
                self.collision_count+=1     

    def screen_display(self):
        if self.initialize==0:
            # initial window
            self.screen.blit(init_bgimage,(0,0))
            if self.music_start==1:
                pygame.mixer.music.load(bg_music)
                pygame.mixer.music.play(-1,1.5)
                self.music_start=0
            text=base_font1.render("PONG",True,light_violet)
            self.screen.blit(text,(screen_width/2-text.get_width()/2,2*margin))
            if self.delay_ind==1:
                pygame.display.update()
                time.sleep(1)
                self.delay_ind=0
            text=base_font2.render("Press 'SPACE' to play",True,white)
            self.screen.blit(text,(screen_width/2-text.get_width()/2,screen_length-text.get_height()-margin))
        
        elif self.finish == 0:
            # game window
            self.screen.blit(bgimage,(0,0))
            if self.music_start==0:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(bg_music)
                pygame.mixer.music.play(-1,1.5)
                self.music_start=1
            self.display_point(self.player1,screen_width/2+icon_length/2,light_blue)
            self.display_point(self.player2,screen_width/2-icon_length/2,light_red)

            # margins and boundary
            pygame.draw.line(self.screen,boundary_col,(screen_width/2,0),(screen_width/2,screen_length),line_w)
            pygame.draw.line(self.screen,boundary_col,(screen_width-margin,0),(screen_width-margin,screen_length),line_w)
            pygame.draw.line(self.screen,boundary_col,(margin,0),(margin,screen_length),line_w)
            
            if self.begin==0:
                # instructions
                self.screen.blit(updown,(screen_width-button_w-20*margin,screen_length/2-button_l/2),None,3) # blit flag=3
                self.screen.blit(ws,(20*margin,screen_length/2-button_l/2),None,3) # blit flag=3

                text1=base_font2.render("Press 'SPACE' to start",True,brown,bgimage_col)
                self.screen.blit(text1,(screen_width/2-text1.get_width()/2,screen_length-text1.get_height()-margin))
                text=base_font2.render(f"Get {max_point} points to win",True,brown,bgimage_col)
                self.screen.blit(text,(screen_width/2-text.get_width()/2,screen_length-text.get_height()-text1.get_height()-2*margin))
            
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            self.ball.draw(self.screen)
            
            #pad borders
            pygame.draw.rect(self.screen,dark_blue,self.player1.rect,margin,pad_curvature)
            pygame.draw.rect(self.screen,dark_red,self.player2.rect,margin,pad_curvature)
        else:
            # winner window
            self.screen.fill(screen_col)
            if self.music_start==1:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(winner_sound)
                pygame.mixer.music.play(0,1)
                self.music_start=0
            if self.player1.point==max_point:   
                pic=blue_win
                msg="Blue wins"
                col=light_blue
            else:
                pic=red_win
                msg="Red wins"
                col=light_red
            self.screen.blit(pic,(screen_width/2-icon_length/2,screen_length/2-icon_length/2-10*margin),None,4)
            text=base_font1.render(msg,True,col)
            self.screen.blit(text,(screen_width/2-text.get_width()/2,screen_length-text.get_height()-12*margin))
            text1=base_font2.render("Press 'SPACE' to restart",True,brown)
            self.screen.blit(text1,(screen_width/2-text1.get_width()/2,screen_length-text1.get_height()-2*margin))
        pygame.display.update()
    
    def display_point(self,player,xpos,col):
        text=base_font.render(str(player.point),True,col)
        self.screen.blit(text,(xpos-int(text.get_width()/2),4*margin))

    def start(self):
        global side
        self.collision_count=0
        self.ball.speedx = ball_speed *side
        self.ball.speedy = 0
        side*= -1
    
    def out(self):
        self.begin=0
        self.ball.speedx,self.ball.speedy=0,0
        self.ball.rect.center=(screen_width/2,screen_length/2)



game=Game(screen,player1,player2,ball)

if __name__ == '__main__':
    game.run()