import tkinter as tk
import random
import numpy as np

class Poli(object):
	def __init__(self, *coefs):
		self.coefs = np.array(coefs)
		self.roots = np.array([])
	def solve(self, x):
		y = 0
		for i in range(len(self.coefs)):
			y += self.coefs[i]*(x**i)
		return y
	def linha(self):
		ncoefs = list(map(lambda x: x[0]*x[1], enumerate(self.coefs)))
		ncoefs.pop(0)
		return(Poli(*ncoefs))
	def __repr__(self):
		return(str(self.coefs))
	def check_root(self, new_root):
		for i, root in enumerate(self.roots):
			if abs(new_root-root) < 0.001:
				return i
		np.insert(self.roots, 0, new_root)
		return len(self.roots)-1

def newton_raphson(pol, x, error):
	for i in range(1000):
		nx = x-pol.solve(x)/pol.linha().solve(x)
		if abs(nx - x) < error:
			return nx, i
		x = nx
	return False, i

class Bacia(tk.Tk):
	"""docstring for Bacia"""
	colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255), (74, 35, 90), (244, 208, 63), (31, 97, 141), (220, 118, 51)]
	def __init__(self, *limits):
		super(Bacia, self).__init__()
		self.limits = limits
		self.geometry("800x600")
		self.canvas = tk.Canvas(self, width=800, height=800, bg = 'gray')
		self.canvas.pack()
	def pos(self,*coords):
		dx = 800/(self.limits[1]-self.limits[0])
		x = dx*(coords[0] - self.limits[0])
		dy = 600/(self.limits[2]-self.limits[3])
		y = dy*(coords[1] - self.limits[3])
		return x, y
	def paint(self, *coords, color, time):
		x = coords[0]
		y = coords[1]
		for i in range(3):
			color[i] = color[i] - int(time**4/50) + 100
			if color[i] < 0:
				color[i] = 0
			if color[i] > 255:
				color[i] = 255
		hexcolor = '#%02x%02x%02x' % tuple(color)
		self.canvas.create_rectangle((x-1,y-1,x+1,y+1), fill = hexcolor, width = 0)

bacia = Bacia(-4, 4,-4, 4)
f = Poli(48,8,4,-10,2,-3,1)

i = 0
while True:
	re = random.randint(-40000, 40000)/10000
	im = random.randint(-40000, 40000)/10000
	x0 = complex(re, im)
	root, time = newton_raphson(f, x0, 0.00001)
	root_num = f.check_root(root)
	x, y = (bacia.pos(re, im))
	bacia.paint(x, y, color=list(Bacia.colors[root_num]), time=time)
	bacia.update()
	i += 1

bacia.mainloop()