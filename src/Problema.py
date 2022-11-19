from queue import Queue
from Grafo import Grafo
from Node  import Node
from Mapa  import carregaMapa
from copy  import deepcopy

"""
Definição da classe problemas
"""
class Problema:

	def __init__(self, mapa, inicio, fim):
		self.mapa = mapa
		self.inicio = inicio
		self.fim = fim
		self.grafo = Grafo()

	def constroiGrafo(self):
		
		initialState = (self.inicio, [0,0])
		expand = Queue()
		expand.put(initialState)
		expanded = set()

		while not expand.empty():
			currState = expand.get()
			currPos, currVel = currState
			expandedState = self.expandState(currState)
			expanded.add(f"{currPos},{currVel}")
			if  len(expandedState) == 0:
				self.grafo.addHeuristic(currState, 0)
				continue
			else:
				# adicionar heuristica do atual
				self.grafo.addHeuristic(currState, 99)

			for ((pos,vel),weight) in expandedState:
				self.grafo.addEdge(Node(currPos,currVel), Node(pos,vel), weight)
				if f"{pos},{vel}" not in expanded:
					expand.put((pos,vel))

	def expandState(self, state):

		pos, vel = state

		if pos == self.fim:
			return []

		if self.mapa[pos[1]][pos[0]] == "#":
			return [self.jogadorFora(deepcopy(state))]
		
		expanded = []
		expanded.append(self.acelerarXabrandarY(deepcopy(state)))
		expanded.append(self.acelerarXmanterY(deepcopy(state)))
		expanded.append(self.acelerarXacelerarY(deepcopy(state)))
		expanded.append(self.manterXabrandarY(deepcopy(state)))
		if vel != [0,0]: expanded.append(self.manterXmanterY(deepcopy(state)))
		expanded.append(self.manterXacelerarY(deepcopy(state)))
		expanded.append(self.abrandarXabrandarY(deepcopy(state)))
		expanded.append(self.abrandarXmanterY(deepcopy(state)))
		expanded.append(self.abrandarXacelerarY(deepcopy(state)))

		return expanded

	def jogadorFora(self, state):
		pos, vel = state
		pos[0] -= vel[0]
		pos[1] -= vel[1]

		return ((pos,[0,0]), 20)

	def acelerarXabrandarY(self, state): 
		pos, vel = state
		acl = [ 1,-1]
		vel[0] += acl[0]
		vel[1] += acl[1]
		pos[0] += vel[0]
		pos[1] += vel[1]

		return ((pos,vel), 1)

	def acelerarXmanterY(self, state):
		pos, vel = state
		acl = [ 1, 0]
		vel[0] += acl[0]
		vel[1] += acl[1]
		pos[0] += vel[0]
		pos[1] += vel[1]

		return ((pos,vel), 1)

	def acelerarXacelerarY(self, state):
		pos, vel = state
		acl = [ 1, 1]
		vel[0] += acl[0]
		vel[1] += acl[1]
		pos[0] += vel[0]
		pos[1] += vel[1]

		return ((pos,vel), 1)

	def abrandarXabrandarY(self, state):
		pos, vel = state
		acl = [-1,-1]
		vel[0] += acl[0]
		vel[1] += acl[1]
		pos[0] += vel[0]
		pos[1] += vel[1]

		return ((pos,vel), 1)
		
	def abrandarXmanterY(self, state):
		pos, vel = state
		acl = [-1, 0]
		vel[0] += acl[0]
		vel[1] += acl[1]
		pos[0] += vel[0]
		pos[1] += vel[1]

		return ((pos,vel), 1)
		
	def abrandarXacelerarY(self, state):
		pos, vel = state
		acl = [-1, 1]
		vel[0] += acl[0]
		vel[1] += acl[1]
		pos[0] += vel[0]
		pos[1] += vel[1]

		return ((pos,vel), 1)
		
	def manterXabrandarY(self, state):
		pos, vel = state
		acl = [ 0,-1]
		vel[0] += acl[0]
		vel[1] += acl[1]
		pos[0] += vel[0]
		pos[1] += vel[1]

		return ((pos,vel), 1)
		
	def manterXmanterY(self, state):
		pos, vel = state
		acl = [ 0, 0]
		vel[0] += acl[0]
		vel[1] += acl[1]
		pos[0] += vel[0]
		pos[1] += vel[1]

		return ((pos,vel), 1)
		
	def manterXacelerarY(self, state):
		pos, vel = state
		acl = [ 0, 1]
		vel[0] += acl[0]
		vel[1] += acl[1]
		pos[0] += vel[0]
		pos[1] += vel[1]

		return ((pos,vel), 1)
		
	def printGrafo(self):
		print(self.grafo.m_nodes)


Map = carregaMapa("mapaFase1.txt")
problema = Problema(Map, [3,0], [7,14])
problema.constroiGrafo()
problema.printGrafo()