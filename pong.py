
import pygame, sys , random ,time
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
###################################################################classes############################################################################

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
		elif(self.x==0):
			self.vx=self.vx*-1
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
		self.hit=pygame.mixer.Sound("data/boing.wav")
		self.out=pygame.mixer.Sound("data/out.wav")
	def collision_boundary(self):
		if((self.y+self.l==HEIGHT and self.v==1) or (self.y==0 and self.v==-1)):
			self.v=0
	def collision_ball(self,ball):													#pass ball by reference 
		if(ball.x+ball.r==self.x or ball.x==self.x+self.w):
			if(ball.y+ball.r>=self.y and ball.y<=self.y+self.l):
				ball.vx=ball.vx*-1
				self.hit.play()
				return 0
			else:
				global LS,RS
				if(ball.x+ball.r==self.x):
					LS=LS+1
				else:
					RS=RS+1
				self.out.play()
				ball.BallInit()
				return 1
			return -1
	def move(self):
		#print("Entered bar moved")
		self.y += self.v

####################################################################################################################################################


####################################################################screens##########################################################################

def start_screen():
	pygame.display.set_caption("Ping Pong" )
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
	global LS,RS
	LS=0
	RS=0
	barL=Bar(0,160,80,20,0,RED)
	barR=Bar(580,160,80,20,0,GREEN)
	ball=Ball(300,200,10,0,0,WHITE)
	ball.BallInit()
	while True:
		pygame.display.set_caption("Pong Scores - Left Player = " + str(LS)+ " Right Player = " + str(RS) )
		if(LS>=10 or RS>=10):
			result_screen2()
		ball.collision_boundary()
		#print("drawing")
		window.fill(BLACK)
		pygame.draw.rect(window,ball.color,pygame.Rect((ball.x,ball.y),(ball.r,ball.r)))
		pygame.draw.rect(window,barL.color,pygame.Rect((barL.x,barL.y),(barL.w,barL.l)))
		pygame.draw.rect(window,barR.color,pygame.Rect((barR.x,barR.y),(barR.w,barR.l)))
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
					exit_screen()
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
	sm=pygame.font.SysFont("Arial",20)
	font=pygame.font.SysFont("Arial",30)
	cap=pygame.font.SysFont("Arial",50)
	med=pygame.font.SysFont("Arial",35)
	f = []
	f.append((cap.render("Controls",True,WHITE),(210,20)))
	f.append((med.render("Player 1",True,WHITE),(80,100)))
	f.append((med.render("Player 2",True,WHITE),(400,100)))
	f.append((sm.render("W - Go Up",True,WHITE),(400,150)))
	f.append((sm.render("S - Go Down",True,WHITE),(400,180)))
	f.append((sm.render("UP - Go Up",True,WHITE),(80,150)))
	f.append((sm.render("Down - Go Down",True,WHITE),(80,180)))
	f.append((font.render("First player to score 10 points win",True,WHITE),(110,280)))
	f.append((sm.render("Press Esc to go back",True,WHITE),(220,370)))
	
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
	score=0
	bar=Bar(580,160,80,20,0,GREEN)
	ball=Ball(300,200,10,0,0,WHITE)
	ball.BallInit()
	while True:
		pygame.display.set_caption("Pong Score : " + str(score) )
		ball.collision_boundary()
		#print("drawing")
		window.fill(BLACK)
		pygame.draw.rect(window,ball.color,pygame.Rect((ball.x,ball.y),(ball.r,ball.r)))
		pygame.draw.rect(window,bar.color,pygame.Rect((bar.x,bar.y),(bar.w,bar.l)))
		#checking collisions
		bar.collision_boundary()
		i=bar.collision_ball(ball)
		if i==0:
			score+=1
		elif i==1:
			result_screen1("Score : "+str(score))
		#moving objects
		ball.move()
		bar.move()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type==pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					exit_screen()
				elif event.key == pygame.K_UP:
					bar.v = -1
				elif event.key == pygame.K_DOWN:
					bar.v = 1
			elif event.type == pygame.KEYUP:
				if event.key in (pygame.K_UP, pygame.K_DOWN):
					bar.v = 0
		pygame.display.update()
		fps.tick(200)

def result_screen1(txt):
	window.fill(BLACK)
	font=pygame.font.SysFont("Arial",30)
	f = []
	f.append((font.render(txt,True,WHITE),(215,170)))
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

def result_screen2():
	global LS,RS
	window.fill(BLACK)
	font=pygame.font.SysFont("Arial",30)
	f = []
	if(LS==RS):
		f.append((font.render("Draw",True,WHITE),(240,170)))
	elif(LS>RS):
		f.append((font.render("Player1 Wins",True,WHITE),(215,170)))
	else:
		f.append((font.render("Player2 Wins",True,WHITE),(215,170)))
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

def exit_screen():
	pygame.display.set_caption("Ping Pong" )

	b1=Button("YES",(250,120))
	b2=Button("NO",(252,170))
	select = 1
	loop=True
	font=pygame.font.SysFont("Arial",30)
	while loop:
		window.fill(BLACK)
		window.blit(font.render("Are You Sure You Want To Quit",True,WHITE),(120,50))
		b1.color=WHITE
		b2.color=WHITE
		if(select==1):
			b1.color=RED
		else:
			b2.color=RED
		b1.draw(window)
		b2.draw(window)
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
					if(select<2):
						select=select + 1
				elif event.key == pygame.K_RETURN:
					if(select==1):
						start_screen()
					else:
						loop=False
		pygame.display.update()
		fps.tick(200)
######################################################################################################################################################

start_screen()