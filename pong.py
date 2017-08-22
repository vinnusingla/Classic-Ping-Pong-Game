
import pygame, sys , random
#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
#globals
WIDTH = 600
HEIGHT = 400   
LS = 0
RS = 0
#initialization
pygame.init()
fps = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))
###############################################################################classes################################################################
#Buttons Class
class Button(object):
	def __init__ (self,txt,location,color=WHITE,fontName="Arial",fontSize=30):
		self.txt=txt
		self.font=pygame.font.SysFont(fontName,fontSize)
		self.loc=location
	def draw(self,canvas):
		surface=self.font.render(self.txt,True,self.color)
		canvas.blit(surface,self.loc)
#Ball class
class Ball(object):
	def __init__(self,x,y,r,vx,vy,color):
		self.x=x
		self.y=y
		self.r=r
		self.vx=vx
		self.vy=vy
		self.color=color
	def BallInit(self):
		self.x=WIDTH/2
		self.y=HEIGHT/2
		if(random.randint(0,1)==1):
			self.vx=1
		else:
			self.vx=-1
		if(random.randint(0,1)==1):
			self.vy=1
		else:
			self.vy=-1
	def collision_boundary(self):
		if(self.y+self.r==HEIGHT or self.y-self.r==0):
			self.vy=self.vy*-1
			#elif(ball.x+r==self.x)
	def move(self):
		#print("Entered ball moved")
		self.x += self.vx
		self.y += self.vy
#Bar class
class Bar(object):
	def __init__(self,x,y,l,w,v,color):
		self.x=x
		self.y=y
		self.l=l
		self.w=w
		self.v=v
		self.color=color
	def collision_boundary(self):
		if((self.y+self.l==HEIGHT and self.v==1) or (self.y==0 and self.v==-1)):
			self.v=0
	def collision_ball(self,ball):													#pass ball by reference 
		if(ball.x+ball.r==self.x or ball.x==self.x+self.w):
			if(ball.y>=self.y and ball.y<=self.y+self.l):
				ball.vx=ball.vx*-1
			else:
				global LS,RS
				if(ball.x+ball.r==self.x):
					LS=LS+1
				else:
					RS=RS+1
				ball.BallInit()
	def move(self):
		#print("Entered bar moved")
		self.y += self.v

#######################################################################################################################################################


####################################################################screens##########################################################################

def start_screen():
	b1=Button("1 Player",(250,100))
	b2=Button("2 Player",(250,170))
	b3=Button("Controls",(250,240))
	select = 1;
	while True:
		window.fill(BLACK)
		b1.color=WHITE
		b2.color=WHITE
		b3.color=WHITE
		if(select==1):
			b1.color=RED
		elif(select==2):
			b2.color=RED
		else:
			b3.color=RED
		b1.draw(window)
		b2.draw(window)
		b3.draw(window)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type==pygame.KEYDOWN:
				#print ("kd left bar = " + str(barL.y) + " right bar = "+str(barR.y))
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_UP:
					if(select>1):
						select=select - 1
				elif event.key == pygame.K_DOWN:
					if(select<3):
						select=select + 1
				elif event.key == pygame.K_RETURN:
					if(select==1):
						single_player()
					elif(select==2):
						play_screen()
					else:
						control_screen()
		pygame.display.update()
		fps.tick(200)

def play_screen():
	LS=0
	RS=0
	barL=Bar(0,160,80,20,0,RED)
	barR=Bar(580,160,80,20,0,GREEN)
	ball=Ball(300,200,10,0,0,WHITE)
	ball.BallInit()
	while True:
		pygame.display.set_caption("Pong Scores - Left Player = " + str(LS)+ " Right Player = " + str(RS) )
		#print("drawing")
		window.fill(BLACK)
		pygame.draw.rect(window,ball.color,pygame.Rect((ball.x,ball.y),(ball.r,ball.r)))
		pygame.draw.rect(window,barL.color,pygame.Rect((barL.x,barL.y),(barL.w,barL.l)))
		pygame.draw.rect(window,barR.color,pygame.Rect((barR.x,barR.y),(barR.w,barR.l)))
		ball.collision_boundary()
		#checking collisions
		barR.collision_boundary()
		barL.collision_boundary()
		barL.collision_ball(ball)
		barR.collision_ball(ball)
		#moving objects
		ball.move()
		barL.move()
		barR.move()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type==pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					start_screen()
				if event.key == pygame.K_UP:
					barR.v = -1
				elif event.key == pygame.K_DOWN:
					barR.v = 1
				elif event.key == pygame.K_w:
					barL.v = -1
				elif event.key == pygame.K_s:
					barL.v = 1
			elif event.type == pygame.KEYUP:
				if event.key in (pygame.K_w, pygame.K_s):
					barL.v = 0
				elif event.key in (pygame.K_UP, pygame.K_DOWN):
					barR.v = 0
		pygame.display.update()
		fps.tick(200)

def control_screen():
	window.fill(BLACK)
	font=pygame.font.SysFont("Arial",30)
	cap=pygame.font.SysFont("Arial",50)
	med=pygame.font.SysFont("Arial",35)
	f = []
	f.append((cap.render("Controls",True,WHITE),(220,20)))
	f.append((med.render("Player 1",True,WHITE),(80,100)))
	f.append((med.render("Player 2",True,WHITE),(400,100)))
	f.append((font.render("W - Go Up",True,WHITE),(400,170)))
	f.append((font.render("S - Go Down",True,WHITE),(400,220)))
	f.append((font.render("UP - Go Up",True,WHITE),(80,170)))
	f.append((font.render("Down - Go Down",True,WHITE),(80,220)))
	f.append((font.render("Press Esc to go back",True,WHITE),(180,350)))
	
	for a in f:
		window.blit(a[0],a[1]) 
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type==pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					start_screen()
		pygame.display.update()

def single_player():
	window.fill(BLACK)
	font=pygame.font.SysFont("Arial",30)
	f = []
	f.append((font.render("InProgress",True,WHITE),(230,150)))
	f.append((font.render("Press Esc to go back",True,WHITE),(180,350)))
	for a in f:
		window.blit(a[0],a[1])
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type==pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					start_screen()
		pygame.display.update()
###########################################################################################################################################################

start_screen()