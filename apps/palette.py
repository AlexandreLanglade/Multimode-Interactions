from ivy.ivy import IvyServer
import pygame
import sys
from math import tan

class Palette(IvyServer):
	def __init__(self):
		IvyServer.__init__(self,"Palette")
		self.start('127.255.255.255:2010')
		# MAJ id=0 type=rectangle x=765 y=546 color=blue size=3
		self.bind_msg(self.update, '^MAJ id=([0-9]*) type=([a-z]*) x=([0-9]*) y=([0-9]*) color=([a-z]*) size=([0-9]*)')
		
	def update(self, *args):
		print(" [ ", args[1], " | ", args[2], " | ", args[3], " | ", args[4], " | ", args[5], " | ", args[6], " ] ")
		self.send_msg("ok")

WIN_SIZE_X = 700
WIN_SIZE_Y = 400

def triangle(x, y, size):
	a = (x, y-size)
	b = (x+((2*size)/tan(1.047197)), y+size)
	c = (x-((2*size)/tan(1.047197)), y+size)
	return (a,b,c)


if __name__ == "__main__":
	
	palette = Palette()
	pygame.init()
	fps_clock = pygame.time.Clock()
	screen = pygame.display.set_mode((WIN_SIZE_X,WIN_SIZE_Y))
	pygame.display.set_caption("Palette")
	while True:
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				pygame.quit()
				palette.stop()
				sys.exit()
		screen.fill("#09133A")
		r = pygame.Rect(200,200,30,30)
		pygame.draw.rect(screen,pygame.Color(255,255,255),r)
		pygame.display.update()
		fps_clock.tick(30)
