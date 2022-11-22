
class Node:

	def __init__(self, pos, vel):
		self.pos = pos
		self.vel = vel
		self.id  = -1

	def __str__(self):
		return f'Node(x:{self.pos[0]}, y:{self.pos[1]}, velx:{self.vel[0]}, vely:{self.vel[1]})'

	def __repr__(self):
		return f'Node(x:{self.pos[0]}, y:{self.pos[1]}, velx:{self.vel[0]}, vely:{self.vel[1]})'

	def getPos(self):
		return self.pos

	def getVel(self):
		return self.vel

	def getID(self):
		return self.id

	def setID(self, id):
		self.id = id

	def __eq__(self,other):
		return self.pos==other.pos and self.vel==other.vel

	def __hash__(self):
		return hash(self.pos[0] + self.pos[1] + self.vel[0] + self.vel[1])
