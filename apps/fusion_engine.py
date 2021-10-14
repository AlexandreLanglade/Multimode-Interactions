from ivy.ivy import IvyServer
from random import randint
import palette
import pygame
import time

class FusionEngine(IvyServer):

	list_figure = []
	fusion = []

	def __init__(self):
		IvyServer.__init__(self, "FusionEngine")
		self.start('127.255.255.255:2010')
		#self.bind_msg(self.response, '^CLICK (.*)')
		#self.bind_msg(self.response, 'parole')
		#self.bind_msg(self.response, 'geste')

	def send_figures_to_palette(self):
		message = "DISPLAY "
		for figure in self.list_figure:
			word = figure.type_figure
			word = word + "," + str(figure.x) + "," + str(figure.y)
			word = word + "," + str(figure.color.r) + "," + \
				str(figure.color.g) + "," + str(figure.color.b)
			word = word + "," + str(figure.size)
			message = message + word + " "
		self.send_msg(message)

	def add_figure(self, type_figure, x=-1, y=-1, color=pygame.Color(225, 255, 255), size=20):
		new_figure = Figure(type_figure, x, y, color, size)
		self.list_figure.append(new_figure)
		self.send_figures_to_palette()

	def move_figure(self, type_figure, x, y, new_x, new_y, color=None):
		figures_under_target = []
		for figure in self.list_figure:
			if figure.is_inside(x, y) and type_figure == figure.type_figure:
				if color != None and color == figure.color:
					figures_under_target.append(figure)
				elif color == None:
					figures_under_target.append(figure)
		if len(figures_under_target) == 0:
			print("Warning : no figure matching the description")
			return
		figures_under_target[0].x = new_x
		figures_under_target[0].y = new_y
		self.send_figures_to_palette()

	def reset(self):
		self.fusion = []


class Figure:

	def __init__(self, type_figure, x, y, color, size) -> None:
		self.color = color
		self.size = size
		self.type_figure = type_figure  # circle, rectangle or triangle
		if(x == -1):
			self.x = randint(10, palette.WIN_SIZE_X-10)
			self.y = randint(10, palette.WIN_SIZE_Y-10)
		else:
			self.x = x
			self.y = y

	def is_inside(self, x, y):
		if self.type_figure == "circle":
			return (x-self.x)*(x-self.x)+(y-self.y)*(y-self.y) <= self.size*self.size
		elif self.type_figure == "rectangle":
			return x >= self.x - self.size and x <= self.x + self.size and y >= self.y - self.size/2 and y <= self.y + self.size/2
		elif self.type_figure == "triangle":
			triangle = palette.triangle(self.x, self.y, self.size)
			a = self.scalar_product2D(self.vector_product2D(self.vector(triangle[0], triangle[1]), self.vector(
				triangle[0], (x, y))), self.vector_product2D(self.vector(triangle[0], (x, y)), self.vector(triangle[0], triangle[2])))
			b = self.scalar_product2D(self.vector_product2D(self.vector(triangle[1], triangle[0]), self.vector(
				triangle[1], (x, y))), self.vector_product2D(self.vector(triangle[1], (x, y)), self.vector(triangle[1], triangle[2])))
			c = self.scalar_product2D(self.vector_product2D(self.vector(triangle[2], triangle[0]), self.vector(
				triangle[2], (x, y))), self.vector_product2D(self.vector(triangle[2], (x, y)), self.vector(triangle[2], triangle[1])))
			return a >= 0 and b >= 0 and c >= 0

	def vector(self, a, b):
		return (b[0]-a[0], b[1]-a[1])

	def vector_product2D(self, a, b):
		return (0, 0, a[0]*b[1]-a[1]*b[0])

	def scalar_product2D(self, a, b):
		return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]


if __name__ == "__main__":
	fe = FusionEngine()
	time.sleep(1)
	fe.add_figure("circle", 234, 232, pygame.Color(23, 66, 76), 54)
