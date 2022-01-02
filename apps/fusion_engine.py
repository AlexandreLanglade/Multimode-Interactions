from ivy.ivy import IvyServer
from random import randint
import palette
import pygame
import time


class FusionInfo:
	def __init__(self) -> None:
		self.clicks = []
		self.speech = ["","","","",""]
		self.draw = ""

	def add_click(self, x, y):
		self.clicks.append((x,y))

	def add_speech(self, action, where, form, color, localisation):
		self.speech[0] = action
		self.speech[1] = where
		self.speech[2] = form
		self.speech[3] = color
		self.speech[4] = localisation

	def add_draw(self, draw):
		if draw == "cercle":
			draw = "circle"
		self.draw = draw

	def __str__(self):
		s = "----------------------------------------\n"
		s = s + str(self.clicks) + "\n" + str(self.draw) + "\n" + str(self.speech)
		s = s + "\n----------------------------------------"
		return s

class FusionEngine(IvyServer):

	list_figure = []
	fusion_info = FusionInfo()

	def __init__(self):
		IvyServer.__init__(self, "FusionEngine")
		self.start('127.255.255.255:2010')
		self.bind_msg(self.receive_vocal, '^sra5 Parsed=action=(.*) where=(.*) form=(.*) color=(.*) localisation=(.*) Confidence=(.*)')
		self.bind_msg(self.receive_click, '^CLICK ([0-9]*) ([0-9]*)')
		self.bind_msg(self.receive_gesture, '^ICAR Gesture=(.*)')

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

	def move_figure(self, x, y, new_x, new_y):
		figures_under_target = []
		for figure in self.list_figure:
			if figure.is_inside(x, y):
					figures_under_target.append(figure)
		if len(figures_under_target) == 0:
			print("Warning : no figure matching the description")
			return
		figures_under_target[0].x = new_x
		figures_under_target[0].y = new_y
		self.send_figures_to_palette()
	
	def receive_vocal(self, agent_name, action, where, form, color, localisation, confidence):
		self.fusion_info.add_speech(action, where, form, color, localisation)
		self.fusion()

	def receive_click(self, agent_name, x, y):
		self.fusion_info.add_click(int(x),int(y))

	def receive_gesture(self, agent_name, draw):
		self.fusion_info.add_draw(draw)

	def fusion(self):
		if self.fusion_info.speech[0] == "CREATE":
			if self.fusion_info.speech[2] == "undefined":
				if self.fusion_info.speech[1] == "undefined":
					self.fusion_rejected()
					return
				if self.fusion_info.draw != "":
					if len(self.fusion_info.clicks) == 0:
						coord = self.get_random_coord()
					else:
						coord = self.fusion_info.clicks[0]
					color = self.get_color_value(self.fusion_info.speech[3])
					self.add_figure(self.fusion_info.draw,coord[0],coord[1],color)
				else:
					if len(self.fusion_info.clicks) == 0:
						self.fusion_rejected()
						return
					figures_under_target = []
					for figure in self.list_figure:
						if figure.is_inside(self.fusion_info.clicks[0][0], self.fusion_info.clicks[0][1]):
							figures_under_target.append(figure)
					if len(figures_under_target) == 0:
						print("Warning : no figure pointed")
						self.fusion_rejected()
						return
					type_fig = figures_under_target[0].type_figure
					color = self.get_color_value(self.fusion_info.speech[3])
					if len(self.fusion_info.clicks)>1:
						coord = self.fusion_info.clicks[1]
					else:
						coord = self.get_random_coord()
					self.add_figure(type_fig,coord[0],coord[1],color)
			else:
				if len(self.fusion_info.clicks)==0:
					self.fusion_rejected()
					return
				color = self.get_color_value(self.fusion_info.speech[3])
				self.add_figure(self.fusion_info.speech[2].lower(),self.fusion_info.clicks[0][0],self.fusion_info.clicks[0][1],color)
		elif self.fusion_info.speech[0] == "MOVE":
			if len(self.fusion_info.clicks)<2:
				self.fusion_rejected()
				return
			old = self.fusion_info.clicks[0]
			new = self.fusion_info.clicks[1]
			self.move_figure(old[0],old[1],new[0],new[1])
		else:
			self.fusion_rejected()
			return
		print(self.fusion_info)
		self.fusion_info = FusionInfo()

	def get_color_value(self, name):
		match name:
			case "YELLOW":
				return pygame.Color(240, 222, 17)
			case "GREEN":
				return pygame.Color(17, 240, 111)
			case "BLUE":
				return pygame.Color(17, 240, 222)
			case "RED":
				return pygame.Color(240, 30, 17)
			case _:
				return pygame.Color(255, 255, 255)

	def get_random_coord(self, XMAX=700, YMAX=400):
		return (randint(0,700),randint(0,400))

	def fusion_rejected(self):
		print("[!]fusion rejected : ")
		print(self.fusion_info)
		self.fusion_info = FusionInfo()

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
			return (x-self.x)*(x-self.x)+(y-self.y)*(y-self.y) <= 22*22
		elif self.type_figure == "rectangle":
			return x >= self.x and x <= self.x + 60 and y >= self.y and y <= self.y + 30
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
	fe.add_figure("circle", 38, 80, pygame.Color(255, 255, 255))
	fe.add_figure("rectangle", 10, 20, pygame.Color(255, 255, 255))
	fe.add_figure("triangle", 38, 130, pygame.Color(255, 255, 255))