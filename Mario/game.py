import pygame,sys
from pygame.locals import *
pygame.init()

#Global Variables
width=1200  #width of the screen
height=600   #height of the screen
level=0
fps=25
addnewflamerate=20

#Colors section
black=(0,0,0)   #background is black
green=(0,255,0)
white=(255,255,255)
red=(255,0,0)
#Colors section end



#Class Dragon
class dragon:
    global canvas
    up=False
    down=True
    velocity=15

    def __init__(self):
        self.image=load_image("ImagesSprites/dragon.png")
        self.imagerect=self.image.get_rect()
        self.imagerect.right=width   #where to place the dragon i.e  from left 1200
        self.imagerect.top=height/2   #from where the dragon will start
  
    def update(self): 
        if(self.imagerect.top<cacbrick.bottom):
            self.down=True
            self.up=False
        if(self.imagerect.bottom>firebrick.top):
            self.up=True
            self.down=False
        if(self.up):
            self.imagerect.top-=self.velocity
        if(self.down):
            self.imagerect.bottom+=self.velocity
        canvas.blit(self.image,self.imagerect)

    def return_height(self):
        #print(self.imagerect.top)
        return self.imagerect.top

#Class flames
class flames:
    flamespeed=20

    def __init__(self):
        self.image=load_image("ImagesSprites/fireball.png")
        self.imagerect=self.image.get_rect()
        self.height=Dragon.return_height()+20 #+20 refers to the mouth of the dragon
        self.surface=pygame.transform.scale(self.image,(20,20)) #reshape the flame into 20x20 pixel
        self.imagerect=pygame.Rect(width-106,self.height,20,20) #Rect(left, top, width, height)

        #width-106 refers to the width of the dragon or starting point of the flame

    def update(self):
        self.imagerect.left-=self.flamespeed
        
#Class Mario
class mario:  
    global moveup,movedown,gravity
    speed=10
    downspeed=20
    def __init__(self):
        self.image=load_image("ImagesSprites/maryo.png")
        self.imagerect=self.image.get_rect()
        self.imagerect.topleft=(100,height/2)  #
        self.score=0

    def update(self):
        if(moveup and (self.imagerect.top>cacbrick.bottom)):   #upper thi niche so mario has to be bottom ave moveup true or false
            self.imagerect.top-=self.speed  #decrement
            self.score+=1
        if(movedown and (self.imagerect.bottom<firebrick.top)):
            self.imagerect.bottom+=self.downspeed 
            self.score+=1
        if(gravity and (self.imagerect.bottom<firebrick.top)):
            self.imagerect.bottom+=self.speed
    
        
#Helper Functions
def terminate():
    pygame.quit()
    sys.exit()  #Exit from Python

def waitforkey():
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                terminate()
            if event.type==pygame.KEYDOWN:  #take any key from keyboard
                if event.key==pygame.K_ESCAPE:  #K_SPACE is escape
                    terminate()
                return
        

def flamehitsmario(playerrect,flames):  
    for f in flames:
        if playerrect.colliderect(f.imagerect):
            return True
        return False
    
def load_image(path):  #load image
    return pygame.image.load(path)

def check_level(score):
    global firebrick,cacbrick,level,addnewflamerate  #declare as global variable.
    #addnewflamerate is being reduced to increase rate of production of new flame with level up
    if score in range(0,250):  #if between 0-250
        firebrick.top=height-50  #fire_bricks.png
        cacbrick.bottom=50     #cactus_bricks.png 
        addnewflamerate=20  #delay che 20ms pachi ave
        level=1
    elif score in range(250,500):
        firebrick.top=height-100
        cacbrick.bottom=100
        addnewflamerate=18
        level=2
    elif score in range(500,750):
        firebrick.top=height-150
        cacbrick.bottom=150
        addnewflamerate=16
        level=3
    elif score in range(750,1000):
        firebrick.top=height-200
        cacbrick.bottom=200
        addnewflamerate=15
        level=4

def drawtext(text,font,x,y,surface):
    textobj=font.render(text,1,red)  #describe the text color
    textrec=textobj.get_rect()
    textrec.center=(x,y)
    surface.blit(textobj,textrec) #image is updated one image onto another

#Main Program
clock=pygame.time.Clock() 
canvas=pygame.display.set_mode((width,height)) #display screen 1200x600
pygame.display.set_caption("Maryo") #title

font=pygame.font.SysFont(None,48)  #font size
scorefont=pygame.font.SysFont(None,30) #score font
#Images loads and creating rects

endobj=load_image('ImagesSprites/end.png')
end=endobj.get_rect()
end.centery=height/2 #centee y co-ordinate
end.centerx=width/2 #centee x co-ordinate

startobj=load_image('ImagesSprites/start.png')
start=startobj.get_rect()
start.centerx=width/2
start.centery=height/2

cacbrickobj=load_image('ImagesSprites/cactus_bricks.png')
cacbrick=cacbrickobj.get_rect()

firebrickobj=load_image('ImagesSprites/fire_bricks.png')
firebrick=firebrickobj.get_rect()

#Sound
pygame.mixer.music.load("MusicSprites/mario_theme.wav")
gameover=pygame.mixer.Sound("MusicSprites/mario_dies.wav")

canvas.blit(startobj,start)
pygame.display.update()  #update only required part not the whole screen

#GamePlay

waitforkey()
topscore=0
Dragon=dragon()#Creating object of dragon class

while True:
    flame_list=[]
    player=mario()#Creating object of maryo class
    moveup=movedown=gravity=False #intially steady
    flameaddcounter=0

    gameover.stop() #intially sound off
    pygame.mixer.music.play(-1,0.0)  #loop (-1) continues start from  0.0
    while True:
        for event in pygame.event.get():  #take input continues 
            if event.type==QUIT: #if escape then quit
                terminate()

            if event.type==KEYDOWN: #continuesly pressed
                if event.key==K_UP:
                    moveup=True
                    movedown=False
                    gravity=False
                    player.update()
                if event.key==K_DOWN:
                    movedown=True
                    gravity=False
                    moveup=True
                    player.update()
                if event.key==K_ESCAPE:
                    terminate()

            if event.type==KEYUP: #pressed and release
                if event.key==K_UP:
                    gravity=True
                    moveup=False
                    player.update()
                if event.key==K_DOWN:
                    movedown=False
                    gravity=True
                    player.update()

        flameaddcounter+=1
        #print(flameaddcounter)
        check_level(player.score)
        
        if(flameaddcounter==addnewflamerate):  
            print(flameaddcounter)
            print("First")    
            flameaddcounter=0
            newflame=flames()
            flame_list.append(newflame)
            
        if(flameaddcounter>addnewflamerate): 
            #print("Second")
            flameaddcounter=0
            

        for f in flame_list:
            #print(f)    
            flames.update(f)
        

        for f in flame_list:
            #print("F::")
            #print(f)
            if f.imagerect.left<=0: 
                flame_list.remove(f)
        player.update()  #mario update
        Dragon.update()   #dragon update

        canvas.fill(black)
        canvas.blit(firebrickobj,firebrick)
        canvas.blit(cacbrickobj,cacbrick)
        canvas.blit(player.image,player.imagerect)
        canvas.blit(Dragon.image,Dragon.imagerect)


        drawtext('Score : %s | Top score : %s | Level : %s' %(player.score, topscore, level), scorefont, width/2, cacbrick.bottom + 10,canvas)
        
        for f in flame_list:
            canvas.blit(f.surface, f.imagerect)
        #Conditions to end the game
        if flamehitsmario(player.imagerect,flame_list):
            if player.score > topscore:
                topscore=player.score
            break

        if player.imagerect.top<=cacbrick.bottom or player.imagerect.bottom>=firebrick.top: #touch either bottom or up
            if player.score>topscore:
                topscore=player.score
                
            break
        pygame.display.update()
        clock.tick(fps) #set the frame per sec
    pygame.mixer.music.stop()
    gameover.play()
    canvas.blit(endobj,end)
    pygame.display.update()
    waitforkey()
            
            
                    
    



