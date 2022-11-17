import networkx as nx
import math

class Grafo:

	def __init__(self):
		self.nodeCounter = 0
		self.m_nodes  	 = []
		# self.m_nodeID 	 = {}
		self.m_graph  	 = {}
		self.m_h      	 = {}

	def __str__(self):
		out = ""
		for key in self.m_graph.keys():
			out = out + f"node {str(key)} : {str(self.m_graph[key])}\n"

		return out

	def addEdge(self, node1, node2, weight):

		if node1 not in self.m_nodes:
			self.m_nodes.append(node1)
			self.m_nodeID[node1] = self.nodeCounter
			self.nodeCounter += 1
			slef.m_graph[self.m_nodeID[node1]] = set()
		else 
			node1 = self.getNodeBySearchNode(node1)

		if node2 not in self.m_nodes:
			self.m_nodes.append(node2)
			self.m_nodeID[node2] = self.nodeCounter
			self.nodeCounter += 1
			slef.m_graph[self.m_nodeID[node2]] = set()
		else 
			node2 = self.getNodeBySearchNode(node2)

		self.m_graph[this.m_nodeID[node1]].add((self.m_nodeID[node2], weight))

	def getNodeBySearchNode(self, searchNode):

		for node in self.m_nodes:
			if node == searchNode:
				return node

		return None

	def getNodeByID(self, id):

		for node in self.m_nodes:
			if node.getID() == id:
				return key

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
		for i in range(0,len(path)-1)
			cost += self.getArcCost(path[i].getID(), path[i+1].getID())

		return cost

	