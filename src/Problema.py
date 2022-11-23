from queue import Queue
from Grafo import Grafo
from Node  import Node
from copy  import deepcopy
import Mapa as m

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
		# expand = Queue()
		# expand.put(initialState)
		expand = []
		expand.append(initialState)
		expanded = set()

		while len(expand) > 0:
		# while not expand.empty():
			# currState = expand.get()
			currState = expand[0]
			del expand[0]
			currPos, currVel = currState
			expandedState = self.expandState(currState)
			# print(expandedState)
			expanded.add(f"{currPos},{currVel}")
			if  len(expandedState) == 0:
				self.grafo.addHeuristic(currState, 0)
				continue
			else:
				# adicionar heuristica do atual
				self.grafo.addHeuristic(currState, 99)

			for ((pos,vel),weight) in expandedState:
				self.grafo.addEdge(Node(currPos,currVel), Node(pos,vel), weight)
				if f"{pos},{vel}" not in expanded and (pos,vel) not in expand:
					# expand.put((pos,vel))
					expand.append((pos,vel))
	def expandState(self, state):

		Map = deepcopy(self.mapa)
		pos, vel = state

		if pos == self.fim:
			return []
        
		# print(pos, vel)
		if (pos[0]<0 or pos[0]>=len(Map[0])) or (pos[1]<0 or pos[1]>=len(Map)) or self.mapa[pos[1]][pos[0]] == "#":
			return [self.jogadorFora(deepcopy(state))]
		
		expanded = []
		expanded.append(self.acelerarXabrandarY(deepcopy(state),Map))
		expanded.append(self.acelerarXmanterY(deepcopy(state),Map))
		expanded.append(self.acelerarXacelerarY(deepcopy(state),Map))
		expanded.append(self.manterXabrandarY(deepcopy(state),Map))
		if vel != [0,0]: expanded.append(self.manterXmanterY(deepcopy(state),Map))
		expanded.append(self.manterXacelerarY(deepcopy(state),Map))
		expanded.append(self.abrandarXabrandarY(deepcopy(state),Map))
		expanded.append(self.abrandarXmanterY(deepcopy(state),Map))
		expanded.append(self.abrandarXacelerarY(deepcopy(state),Map))

		return list(filter(lambda x : x is not None, expanded))

	def jogadorFora(self, state):
		pos, vel = state
		pos[0] -= vel[0]
		pos[1] -= vel[1]

		return ((pos,[0,0]), 20)

	def validVector(self, pos, vel, acl, Map): 

		velx,vely = vel[0]+acl[0], vel[1]+acl[1]
		posxB, posxA = pos[0], pos[0]+velx
		posyB, posyA = pos[1], pos[1]+vely
		# print(posxB, posxA, posyB, posyA)
		if ((posxA<0 or posxA>=len(Map[0])) or (posyA<0 or posyA>=len(Map))):
			return True

		# if posxB > posxA: 
		# 	posxB, posxA = posxA, posxB
		# if posyB > posyA: 
		# 	posyB, posyA = posyA, posyB


		# if ("#" not in Map[posyB][posxB:posxA+1] and "#" not in list(map(lambda l : l[posxA], Map))[posyB:posyA+1]):#Map[posyB : posyA][posxA]):
		# 	return True
		
		# if ("#" not in list(map(lambda l : l[posxB], Map))[posyB:posyA+1] and "#" not in Map[posyA][posxB:posxA+1]):
		# 	return True

		if  posxB - posxA == 0:
			if posyB > posyA:
				posyA, posyB = posyB, posyA
			if "#" not in list(map(lambda x: x[posxB], Map))[posyB: posyA+1]:
				return True
			return False

		declive = (posyB - posyA)/(posxB - posxA)

		b = posyB - declive*posxB

		step = 1
		if posxB > posxA:
			step = -1

		for x in range(posxB+step, posxA-step, step):
			y = declive*x + b
			if Map[int(y)][x] == "#":
				return False

		if  posyB - posyA == 0:
			if posxB > posxA:
				posxA, posxB = posxB, posxA
			if "#" not in Map[posyB][posxB: posxA+1]:
				return True
			return False

		declive = (posxB - posxA)/(posyB - posyA)

		b = posxB - declive*posyB

		step = 1
		if posyB > posyA:
			step = -1

		for y in range(posyB+step, posyA-step, step):
			x = declive*y + b
			if Map[int(y)][int(x)] == "#":
				return False

		return True

	def acelerarXabrandarY(self, state, Map): 
		pos, vel = state
		acl = [ 1,-1]
		if self.validVector(pos,vel,acl,Map):
			vel[0] += acl[0]
			vel[1] += acl[1]
			pos[0] += vel[0]
			pos[1] += vel[1]

			return ((pos,vel), 1)
		return None

	def acelerarXmanterY(self, state, Map):
		pos, vel = state
		acl = [ 1, 0]
		if self.validVector(pos,vel,acl,Map):
			vel[0] += acl[0]
			vel[1] += acl[1]
			pos[0] += vel[0]
			pos[1] += vel[1]

			return ((pos,vel), 1)
		return None

	def acelerarXacelerarY(self, state, Map):
		pos, vel = state
		acl = [ 1, 1]
		if self.validVector(pos,vel,acl,Map):
			vel[0] += acl[0]
			vel[1] += acl[1]
			pos[0] += vel[0]
			pos[1] += vel[1]

			return ((pos,vel), 1)
		return None

	def abrandarXabrandarY(self, state, Map):
		pos, vel = state
		acl = [-1,-1]
		if self.validVector(pos,vel,acl,Map):
			vel[0] += acl[0]
			vel[1] += acl[1]
			pos[0] += vel[0]
			pos[1] += vel[1]

			return ((pos,vel), 1)
		return None
		
	def abrandarXmanterY(self, state, Map):
		pos, vel = state
		acl = [-1, 0]
		if self.validVector(pos,vel,acl,Map):
			vel[0] += acl[0]
			vel[1] += acl[1]
			pos[0] += vel[0]
			pos[1] += vel[1]

			return ((pos,vel), 1)
		return None
		
	def abrandarXacelerarY(self, state, Map):
		pos, vel = state
		acl = [-1, 1]
		if self.validVector(pos,vel,acl,Map):
			vel[0] += acl[0]
			vel[1] += acl[1]
			pos[0] += vel[0]
			pos[1] += vel[1]

			return ((pos,vel), 1)
		return None
		
	def manterXabrandarY(self, state, Map):
		pos, vel = state
		acl = [ 0,-1]
		if self.validVector(pos,vel,acl,Map):
			vel[0] += acl[0]
			vel[1] += acl[1]
			pos[0] += vel[0]
			pos[1] += vel[1]

			return ((pos,vel), 1)
		return None
		
	def manterXmanterY(self, state, Map):
		pos, vel = state
		acl = [ 0, 0]
		if self.validVector(pos,vel,acl,Map):
			vel[0] += acl[0]
			vel[1] += acl[1]
			pos[0] += vel[0]
			pos[1] += vel[1]

			return ((pos,vel), 1)
		return None
		
	def manterXacelerarY(self, state, Map):
		pos, vel = state
		acl = [ 0, 1]
		if self.validVector(pos,vel,acl,Map):
			vel[0] += acl[0]
			vel[1] += acl[1]
			pos[0] += vel[0]
			pos[1] += vel[1]

			return ((pos,vel), 1)
		return None

	def BFS(self):
		return self.grafo.procura_BFS(self.grafo.getNodeBySearchNode(Node(self.inicio, [0,0])), self.fim)

	def DFS(self):
		return self.grafo.procura_DFS(self.grafo.getNodeBySearchNode(Node(self.inicio,[0,0])), self.fim)
	# def BFSandBuildGraph(self):
	# 	queue = Queue()
	# 	state = (self.inicio, [0,0])
	# 	queue.put(state)
	# 	parent = {}

	# 	while not queue.empty():
	# 		curr = queue.get()

	# 		expandedState = self.expandState(curr)
	# 		expanded.add(curr)
	# 		if len(expandedState) == 0:
	# 			# reconstruir caminho
	# 			path = []

	# 			return self.grafo.pathCost(path)

	# 		for ((pos, vel), weight) in expandedState:
	# 			node = self.grafo.getNodeBySearchNode(Node(pos, vel))
	# 			if node is None:



	def printGrafo(self):
		print(self.grafo.m_nodes)

if __name__ == "__main__":
	# Map = carregaMapa("mapaTeste.txt")
	Map = m.carregaMapa("mapaFase1.txt")
	problema = Problema(Map, [3,0], [7,14])
	# l = [1,2,3,4,5,6,7]
	# problema = Problema(Map, [0,1], [5,1])
	problema.constroiGrafo()
	# problema.printGrafo()
	caminho, custo = problema.DFS()
	# print(list(map(lambda x : x.getPos(), caminho)), custo)
	m.desenhaMapa(Map, caminho, custo)
