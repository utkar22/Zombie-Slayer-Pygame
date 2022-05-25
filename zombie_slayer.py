import pygame
import random
import time
import math
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
pygame.font.init()

display_width=800
display_height=600

ground=500

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Jango the Zombie Slayer")

black=(0,0,0)
white=(255,255,255)

red=(255,0,0)
dark_red=(200,0,0)

green=(0,255,0)
dark_green=(0,200,0)

blue=(0,0,255)
dark_blue=(0,0,200)
sky_blue=(127, 255, 253)

gray=(223, 222, 221)
moon_gray=(119, 119, 119)

night_sky_0=(10, 3, 40)
night_sky_1=(1, 3, 35)
night_sky_2=(0, 2, 24)
night_sky_3=(0, 1, 16)
night_sky_4=(0, 0, 9)
night_sky_5=(0, 2, 24)
night_sky_6=(1, 3, 35)
night_sky_7=(10, 3, 40)
night_sky_8=(70, 9, 10)


player_skin=(209, 111, 13)
player_infected=(172, 225, 13)


font1=resource_path("data/arial.ttf")

shootSound=pygame.mixer.Sound(resource_path("music/shoot.wav"))
reloadSound=pygame.mixer.Sound(resource_path("music/reload.wav"))
bitingSound=pygame.mixer.Sound(resource_path("music/biting.wav"))
dyingSound=pygame.mixer.Sound(resource_path("music/dying.wav"))
screamSound=pygame.mixer.Sound(resource_path("music/scream.wav"))

clock=pygame.time.Clock()

paused=True
instructions_open=True
gameloop_run=False
music_playing=False

sky_color=night_sky_0

class player(object):
    def __init__(self,x,y,width,height,vel,status):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=vel
        self.status=status

    def draw(self, gameDisplay):
        if self.status=="Normal":
            color_skin=player_skin
        elif self.status=="Bitten":
            color_skin=player_infected
        elif self.status=="Zombie":
            color_skin=dark_green
            
        pygame.draw.rect(gameDisplay,color_skin,(self.x,self.y,self.width,self.height))
        

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=8*facing
        self.drop=0
        shootSound.play()

    def draw(self,gameDisplay):
        pygame.draw.circle(gameDisplay, self.color, (self.x,self.y), self.radius)

class enemy(object):
    def __init__(self,x,y,width,height,end,vel):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.path=[x,end]
        self.vel=vel

    def draw(self,gameDisplay,direction):
        self.move(direction)
        pygame.draw.rect(gameDisplay,dark_green,(self.x,self.y,self.width,self.height))

    def move(self,direction):
        if direction=="left":
            self.x-=self.vel
        else:
            self.x+=self.vel

def text_objects(text,font,color):
    textSurface=font.render(text, True, color)
    return (textSurface, textSurface.get_rect())

def message_display(text,font,size,x,y,color=gray):
    largeText=pygame.font.Font(font,size)
    TextSurf,TextRect=text_objects(text, largeText, color)
    TextRect.center=(x,y)
    gameDisplay.blit(TextSurf,TextRect)


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()

    if x<mouse[0]<x+w and y<mouse[1]<y+h:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))

        new_time=pygame.time.get_ticks()
        
        if click[0]==1 and action!=None:
            time.sleep(0.1)
            action()

    else:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))

    message_display(msg,font1,20,x+w/2,y+h/2)


def quitgame():
    pygame.quit()
    

music_toggle_oldtime=0

def music_toggle():
    global music_toggle_oldtime
    global music_playing

    music_toggle_newtime=pygame.time.get_ticks()

    if music_toggle_newtime-music_toggle_oldtime>450:
        if music_playing==True:
            pygame.mixer.music.pause()
            music_playing=False
        else:
            pygame.mixer.music.unpause()
            music_playing=True

        music_toggle_oldtime=music_toggle_newtime

    

def instructions():
    global instructions_open
    instructions_open=True

    old_time=pygame.time.get_ticks()

    no_of_tabs=3
    instructions_tab=1
    
    while instructions_open==True:
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        keys=pygame.key.get_pressed()

        if keys[pygame.K_m]:
            music_toggle()

        if keys[pygame.K_p]:
            unpause()


        if instructions_tab==1:
            gameDisplay.fill(sky_color)

            message_display("Jango, the legendary zombie slayer",font1,40,display_width/2,60)
            message_display("Stole a precious artifact",font1,40,display_width/2,105)
            message_display("From the mystical temple of",font1,40,display_width/2,150)
            message_display("Faletuza",font1,40,display_width/2,195)
            message_display("Now survive the most trechous trap",font1,40,display_width/2,240)
            message_display("Zombies",font1,40,display_width/2,285)
            message_display("Slay the zombies",font1,40,display_width/2,330)
            message_display("Survive until dawn",font1,40,display_width/2,375)
            message_display("And don't join them!",font1,40,display_width/2,420)

        if instructions_tab==2:
            gameDisplay.fill(sky_color)

            message_display("Use the WASD keys",font1,50,display_width/2,100)
            message_display("to move around",font1,50,display_width/2,160)
            
            message_display("Point in a direction",font1,50,display_width/2,250)
            message_display("and click to shoot",font1,50,display_width/2,310)

        if instructions_tab==3:
            gameDisplay.fill(sky_color)

            message_display("Keys",font1,70,display_width/2,100)

            message_display("WASD - Movement",font1,40,280,190)
            message_display("R - Reload",font1,40,200,240)
            message_display("P - Pause/Unpause",font1,40,280,310)
            message_display("M - Toggle Music",font1,40,260,360)

        if gameloop_run:
            button("Resume Game",(display_width/2)-90,485,180,50,dark_green,green,unpause)
        else:
            button("Play Now",(display_width/2)-90,485,180,50,dark_green,green,gameloop)

        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()

        new_time=pygame.time.get_ticks()

        if instructions_tab>1:
            pygame.draw.rect(gameDisplay,dark_blue,(30,550,70,30))
            message_display("Prev.",font1,20,65,565)

            if 30<mouse[0]<100 and 550<mouse[1]<580 and click[0]==1 and new_time-old_time>400:
                instructions_tab-=1
                old_time=new_time
            

        if instructions_tab<no_of_tabs:
            pygame.draw.rect(gameDisplay,dark_blue,(700,550,70,30))
            message_display("Next",font1,20,735,565)

            if 700<mouse[0]<770 and 550<mouse[1]<580 and click[0]==1 and new_time-old_time>100:
                instructions_tab+=1
                old_time=new_time
                

        pygame.display.update()


def unpause():
    global paused
    global instructions_open
    
    paused=False
    instructions_open=False

    pygame.mixer.music.unpause()


def pause():
    global paused

    gameDisplay.fill(sky_color)
    message_display("Game Paused",font1,100,display_width/2,display_height/2,gray)

    pygame.mixer.music.pause()

    paused_time=0
        
    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                paused=False

        paused_time+=1/60

        keys=pygame.key.get_pressed()

        music_newtime=pygame.time.get_ticks()

        if keys[pygame.K_m]:
            music_toggle()

        if keys[pygame.K_p] and paused_time>1:
            unpause()

        button("Unpause",135,450,130,50,dark_green,green,unpause)
        button("Instructions",335,450,130,50,dark_blue,dark_blue,instructions)
        button("Quit",535,450,130,50,dark_red,red,quitgame)
        pygame.display.update()


def end_screen(score):
    global gameloop_run
    gameloop_run=False
    
    gameDisplay.fill(sky_color)
    message_display("Score: "+str(int(score)),font1,100, display_width/2, display_height/2, gray)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        button("Play Again",150,450,120,50,dark_green,green,gameloop)
        button("Quit",550,450,120,50,dark_red,red,quitgame)

        pygame.display.update()


def you_died(score):
    message_display("YOU DIED!",font1, 150, display_width/2, display_height/2, red)
    pygame.display.update()
    time.sleep(5)
    screamSound.play()

    end_screen(score)

def game_win(score):
    message_display("You survived!", font1, 120, display_width/2, display_height/2, green)
    pygame.display.update()
    time.sleep(5)

    end_screen(score)


def gameintro():
    intro=True

    pygame.mixer.music.load(resource_path("music/intro_music.wav"))
    pygame.mixer.music.play(0)

    global music_playing
    music_playing=True

    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()

        gameDisplay.fill(sky_color)
        message_display("Zombie Slayer",font1,100,display_width/2,175,green)

        button("Start Game",(display_width/2)-65,250,130,50,dark_green,green,gameloop)
        button("Instructions",(display_width/2)-65,350,130,50,dark_blue,blue,instructions)
        button("Quit",(display_width/2)-65,450,130,50,dark_red,red,quitgame)
        pygame.display.update()
               
        
def gameloop():
    score=0
    kills=0
    
    bullets=[]
    zombies=[]
    
    width=40
    height=60
    
    x=(display_width-width)/2
    y=(ground-height)
    
    vel=5

    jump_allowed=28

    man=player(x,y,width,height,vel,"Normal")

    spawn_gap=2.5

    zombie_count=0

    oldtime=0
    zombie_oldtime=0

    total_health=1000
    health=total_health

    bullet_capacity=6
    bullet_available=bullet_capacity

    reload=False
    reload_oldtime=0

    bullet_display_color=blue
    

    manual_time=0

    clock_time="8:00 PM"
    clock_dictionary={0:"8:00 PM",1:"9:00 PM",2:"10:00 PM",3:"11:00 PM",4:"12:00 PM",5:"1:00 AM",6:"2:00 AM",7:"3:00 AM",8:"4:00 AM"}
    color_dictionary={0:night_sky_0, 1:night_sky_1, 2:night_sky_2, 3:night_sky_3, 4:night_sky_4,
                      5:night_sky_5, 6:night_sky_6, 7:night_sky_7, 8:night_sky_7}

    win_time=250

    global gameloop_run
    gameloop_run=True

    paused_oldtime=0

    pygame.mixer.music.load(resource_path("music/background_music.wav"))
    pygame.mixer.music.play(0)

    global music_playing
    music_playing=True

    while gameloop_run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameloop_run=False

        manual_time+=(1/60)

        score=int(health+kills+manual_time)

        clock_hour=manual_time//30
        clock_time=clock_dictionary[clock_hour]

        global sky_color
        sky_color=color_dictionary[clock_hour]

        if manual_time>win_time:
            game_win(score)

        if man.status=="Bitten":
            man.vel=4
            if manual_time%2==0:
                health-=1
            if clock_time==8:
                man.status="Normal"
                man.vel=5

        if health<1:
            man.status="Zombie"
            man.draw
            bitingSound.set_volume(0)
            dyingSound.play()
            you_died(score)

        if clock_hour==4:
            zombie_width=30
            zombie_height=45
            zombie_damage=2.5
            zombie_velocity=4
            spawn_gap=1.2
        else:
            zombie_width=30
            zombie_height=40
            zombie_damage=1.5
            zombie_velocity=3

        if clock_hour>4:
            spawn_gap=1.5
            
            

        for bullet in bullets:
            hit=False
            if 0<bullet.x<display_width:
                bullet.x+=bullet.vel
                if bullet.drop==8:
                    bullet.y+=1
                    bullet.drop=0
                else:
                    bullet.drop+=1
                for zombie in zombies:
                    if zombie.y+zombie.height>bullet.y-bullet.radius>zombie.y:
                        if bullet.x+bullet.radius>zombie.x and bullet.x-bullet.radius<zombie.x+zombie.width:
                            zombies.pop(zombies.index(zombie))
                            kills+=1
                            if spawn_gap>1.6:
                                spawn_gap-=0.2
                            hit=True
            else:
                bullets.pop(bullets.index(bullet))
            if hit:
                bullets.pop(bullets.index(bullet))


        for zombie in zombies:
            if zombie.y<man.y+man.height:
                if zombie.x+zombie.width>man.x and zombie.x<man.x+man.width:
                    health-=zombie_damage
                    bitingSound.play()
                    if health>1:
                        bitten_random=random.randint(0,health*100)
                        if bitten_random==65:
                            man.status="Bitten"

        keys=pygame.key.get_pressed()

        if keys[pygame.K_w] and jump_count<jump_allowed:
            man.y-=man.vel
            jump_count+=1

        if keys[pygame.K_s]:
            man.y+=man.vel

        if keys[pygame.K_a]:
            man.x-=man.vel

        if keys[pygame.K_d]:
            man.x+=man.vel

        if keys[pygame.K_j]: #Jetpack cheat
            jump_allowed=10000

        if keys[pygame.K_r]:
            reload=True
            reload_oldtime=manual_time
            bullet_display_color=red
            reloadSound.play()

        paused_newtime=manual_time

        if keys[pygame.K_p] and paused_newtime-paused_oldtime>0.5:
            global paused
            paused=True
            pause()
            paused_oldtime=paused_newtime

        if keys[pygame.K_m]:
            music_toggle()

        man.y+=2 #gravity

        if man.x<0:
            man.x=0
        elif man.x+man.width>display_width:
            man.x=display_width-man.width

        if man.y<0:
            man.y=0
        elif man.y+man.height==ground or man.y+man.height>ground:
            man.y=ground-man.height
            jump_count=0

        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()

        reload_newtime=manual_time

        if reload and reload_newtime-reload_oldtime>1.8:
            reload=False
            bullet_available=bullet_capacity
            bullet_display_color=blue

        newtime=manual_time

        if (click[0]==1 or keys[pygame.K_SPACE]) and newtime-oldtime>0.5 and paused_newtime-paused_oldtime>0.5 and bullet_available and not reload:
            if mouse[0]<man.x:
                facing=-1
            else:
                facing=1

            if len(bullets)<5:
                bullets.append(projectile(int(man.x+man.width/2),int(man.y+man.height/2),6,red,facing))
                bullet_available-=1
                if not bullet_available:
                    bullet_display_color=red

                oldtime=newtime

        zombie_newtime=manual_time

        if zombie_newtime-zombie_oldtime>spawn_gap:
            zombie_count=random.randint(1,99)
            if man.x<display_width/2:
                zombies.append(enemy(0,ground-zombie_height,zombie_width,zombie_height,display_width,zombie_velocity))
            else:
                zombies.append(enemy(display_width,ground-zombie_height,zombie_width,zombie_height,0,zombie_velocity))
            zombie_oldtime=zombie_newtime


        moon_x=int((manual_time/240)*display_width)
        moon_y=ground-int((display_height/2)*math.sin(math.pi*(moon_x/display_width)))


        gameDisplay.fill(sky_color)
        pygame.draw.circle(gameDisplay, moon_gray, (moon_x,moon_y), 75)
        pygame.draw.line(gameDisplay, green, (0,ground), (display_width,ground), 2)
        
        man.draw(gameDisplay)
        
        for bullet in bullets:
            bullet.draw(gameDisplay)
            
        for zombie in zombies:
            if zombie.x>man.x:
                zombie_direction="left"
            else:
                zombie_direction="right"
            zombie.draw(gameDisplay,zombie_direction)

        pygame.draw.rect(gameDisplay,red,(300,15,total_health//5,50))
        if health>0:
            pygame.draw.rect(gameDisplay,green,(300,15,health//5,50))

        message_display(clock_time,font1, 75, 400, 110, gray)

        message_display("Kills: "+str(kills),font1, 40, 700, 40, gray)

        message_display(str(bullet_available)+"/"+str(bullet_capacity),font1, 25, 700, 550, bullet_display_color)

        if man.status=="Bitten":
            message_display("Bitten", font1, 30, 70, 50, player_infected)

        if clock_hour==4:
            message_display("Hour of the moon", font1, 50, display_width/2, 160, gray)
     
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

gameintro()
