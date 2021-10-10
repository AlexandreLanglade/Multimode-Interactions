from ivy.ivy import IvyServer
from random import randint
import pygame
import sys

class Palette(IvyServer):
	def __init__(self):
		IvyServer.__init__(self,"Palette")
		self.start('127.255.255.255:2010')
		# MAJ id=0 type=rectangle x=765 y=546 color=blue size=3
		self.bind_msg(self.update, '^MAJ id=([0-9]*) type=([a-z]*) x=([0-9]*) y=([0-9]*) color=([a-z]*) size=([0-9]*)')
		
	def update(self, *args):
		print(" [ ", args[1], " | ", args[2], " | ", args[3], " | ", args[4], " | ", args[5], " | ", args[6], " ] ")
		self.send_msg("ok")


class Figure:

	how_many = 0

	def __init__(self, type, x=-1, y=-1, color=pygame.Color(225,133,104), size=1) -> None:
		self.color = color
		self.size = size
		self.type = type # circle, rectangle or triangle
		if(x==-1):
			self.x = randint(10, WIN_SIZE_X-10)
			self.y = randint(10, WIN_SIZE_Y-10)
		else:
			self.x = x
			self.y = y	
		self.how_many += 1
		self.id = self.how_many



WIN_SIZE_X = 700
WIN_SIZE_Y = 400

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
		pygame.display.update()
		fps_clock.tick(30)
