from ivy.ivy import IvyServer

class Palette(IvyServer):
	def __init__(self):
		IvyServer.__init__(self,"Palette")
		self.start('127.255.255.255:2010')
		self.bind_msg(self.response, '^test1.*')
        
	def response(self, agname, mess):
		print("heure Well : ", agname, " : ", mess)
		self.send_msg("FusionEngine ok")
     

if __name__ == "__main__":
    palette = Palette()