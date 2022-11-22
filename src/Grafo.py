import networkx as nx
import math
from Node import Node
from queue import Queue

class Grafo:

	def __init__(self):
		self.nodeCounter = 0
		self.m_nodes  	 = []
		# self.m_nodeID 	 = {}
		self.m_graph  	 = {}
		self.m_heuristic = {}
		self.m_h      	 = {}

	def __str__(self):
		out = ""
		for key in self.m_graph.keys():
			out = out + f"node {str(key)} : {str(self.m_graph[key])}\n"

		return out

	def addEdge(self, node1, node2, weight):

		if node1 not in self.m_nodes:
			self.m_nodes.append(node1)
			# self.m_nodeID[node1] = self.nodeCounter
			node1.setID(self.nodeCounter)
			self.nodeCounter += 1
			# self.m_graph[self.m_nodeID[node1]] = set()
			self.m_graph[node1.getID()] = set()
		else: 
			node1 = self.getNodeBySearchNode(node1)

		if node2 not in self.m_nodes:
			self.m_nodes.append(node2)
			# self.m_nodeID[node2] = self.nodeCounter
			node2.setID(self.nodeCounter)
			self.nodeCounter += 1
			# self.m_graph[self.m_nodeID[node2]] = set()
			self.m_graph[node2.getID()] = set()
		else:
			node2 = self.getNodeBySearchNode(node2)

		# self.m_graph[self.m_nodeID[node1]].add((self.m_nodeID[node2], weight))
		self.m_graph[node1.getID()].add((node2.getID(), weight))

	def addNode(self, pos, vel):
		node = Node(pos,vel)
		if node not in self.m_nodes:
			self.m_nodes.append(node)
			node.setID(self.nodeCounter)
			self.nodeCounter += 1
			self.m_graph[node.getID()] = set()


	def getNodeBySearchNode(self, searchNode):

		for node in self.m_nodes:
			if node == searchNode:
				return node

		return None

	def getNodeByID(self, id):

		for node in self.m_nodes:
			if node.getID() == id:
				return node

		return None

	def getArcCost(self, node1ID, node2ID):

		custoT = math.inf
		listaArestas = self.m_graph[node1ID]

		for (nodeID, weight) in listaArestas:
			if nodeID == node2ID:
				custoT = weight

		return custoT

	def pathCost(self, path):
		cost = 0
		i = 0
		for i in range(0,len(path)-1):
			cost += self.getArcCost(path[i].getID(), path[i+1].getID())

		return cost

	def addHeuristic(self, state, heuristic):
		pos,vel = state
		node = Node(pos,vel)
		n = self.getNodeBySearchNode(node)
		if n is not None: self.m_heuristic[n.getID()] = heuristic

	def procura_BFS(self, start, endPos):
        # definir nodos visitados para evitar ciclos
		visited = set()
		fila = Queue()

        # adicionar o nodo inicial à fila e aos visitados
		fila.put(start.getID())
		visited.add(start.getID())

        # garantir que o start node nao tem pais...
		parent = dict()
		parent[start.getID()] = None

		end = None

		path_found = False
		while not fila.empty() and path_found == False:
			nodo_atual = self.getNodeByID(fila.get())
			# print(nodo_atual, endPos)
			if nodo_atual.getPos() == endPos:
				path_found = True
				end = nodo_atual
			else:
				for (adjacente, peso) in self.m_graph[nodo_atual.getID()]:
					if adjacente not in visited:
						fila.put(adjacente)
						parent[adjacente] = nodo_atual.getID()
						visited.add(adjacente)
        # Reconstruir o caminho
		path = []
		if path_found:
			path.append(end)
			while parent[end.getID()] is not None:
				parentNode = self.getNodeByID(parent[end.getID()])
				path.append(parentNode)
				end = parentNode
			
			path.reverse()
            # funçao calcula custo caminho
			custo = self.pathCost(path)
			return (path, custo)
		
		return None

	def procura_DFS(self, start, endPos):
        # definir nodos visitados para evitar ciclos
		visited = set()
		fila = []

        # adicionar o nodo inicial à fila e aos visitados
		fila.append(start.getID())
		visited.add(start.getID())

        # garantir que o start node nao tem pais...
		parent = dict()
		parent[start.getID()] = None

		end = None

		path_found = False
		while len(fila)>0 and end is None:
			nodo_atual = self.getNodeByID(fila.pop())
			# print(nodo_atual, endPos)
			if nodo_atual.getPos() == endPos:
				end = nodo_atual
			else:
				paraMandar = []
				for (adjacente, peso) in self.m_graph[nodo_atual.getID()]:
					if adjacente not in visited:
						paraMandar.append(adjacente)
						parent[adjacente] = nodo_atual.getID()
						visited.add(adjacente)
				paraMandar.reverse()
				fila.extend(paraMandar)

        # Reconstruir o caminho
		path = []
		if end is not None:
			path.append(end)
			while parent[end.getID()] is not None:
				parentNode = self.getNodeByID(parent[end.getID()])
				path.append(parentNode)
				end = parentNode
			
			path.reverse()
            # funçao calcula custo caminho
			custo = self.pathCost(path)
			return (path, custo)
		
		return None