from ivy.ivy import IvyServer
import pygame
import sys
from math import tan

class Palette(IvyServer):
	def __init__(self):
		IvyServer.__init__(self,"Palette")
		self.start('127.255.255.255:2010')
		self.bind_msg(self.update, '^DISPLAY (.*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)')
		
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
			if(event.type == pygame.MOUSEBUTTONUP):
				position = pygame.mouse.get_pos()
				message = "CLICK " + str(position[0]) + " " + str(position[1])
				palette.send_msg(message)
		# Background
		screen.fill("#09133A")
		# Form Choice
		pygame.draw.rect(screen,pygame.Color(255,255,255),pygame.Rect(10,20,60,30))
		pygame.draw.circle(screen, pygame.Color(255,255,255),(38,80),22)
		pygame.draw.polygon(screen,pygame.Color(255,255,255),triangle(38,130,22))
		
		# Display + fps
		pygame.display.update()
		fps_clock.tick(30)
