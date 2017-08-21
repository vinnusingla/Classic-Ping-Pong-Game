
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

pygame.init()
fps = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))

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
		ball.x=WIDTH/2
		ball.y=HEIGHT/2
		if(random.randint(0,1)==1):
			ball.vx=1
		else:
			ball.vx=-1
		if(random.randint(0,1)==1):
			ball.vy=1
		else:
			ball.vy=-1
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

barL=Bar(0,160,80,20,0,RED)
barR=Bar(580,160,80,20,0,GREEN)
ball=Ball(300,200,10,0,0,WHITE)

def draw(canvas):
	#print("drawing")
	canvas.fill(BLACK)
	pygame.draw.rect(canvas,ball.color,pygame.Rect((ball.x,ball.y),(ball.r,ball.r)))
	pygame.draw.rect(canvas,barL.color,pygame.Rect((barL.x,barL.y),(barL.w,barL.l)))
	pygame.draw.rect(canvas,barR.color,pygame.Rect((barR.x,barR.y),(barR.w,barR.l)))

ball.BallInit()
while True:
	pygame.display.set_caption("Pong Scores - Left Player = " + str(LS)+ " Right Player = " + str(RS) )
	draw(window)
	ball.collision_boundary()
	barR.collision_boundary()
	barL.collision_boundary()
	barL.collision_ball(ball)
	barR.collision_ball(ball)
	ball.move()
	barL.move()
	barR.move()
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