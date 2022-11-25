import math
from queue import Queue
from Node import Node

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

    def addEdge(self, node1 : Node, node2 : Node, weight):

        node1 = self.addNode(node1)

        node2 = self.addNode(node2)

        # self.m_graph[self.m_nodeID[node1]].add((self.m_nodeID[node2], weight))
        self.m_graph[node1.getID()].add((node2.getID(), weight))

    def addNode(self, node : Node):
        if node not in self.m_nodes:
            self.m_nodes.append(node)
            node.setID(self.nodeCounter)
            self.nodeCounter += 1
            self.m_graph[node.getID()] = set()
            return node
        return self.getNodeBySearchNode(node)

    def getNodeBySearchNode(self, searchNode):

        for node in self.m_nodes:
            if node == searchNode:
                return node

        return None

    def getNodeByID(self, searchID):

        for node in self.m_nodes:
            if node.getID() == searchID:
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

    def BFS(self, start:Node, endPos):
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

    def DFS(self, start:Node, endPos):
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

    def AStar(self, start:Node, endPos):
        gScore = {}
        fScore = {}
        parent = {}

        for node in self.m_nodes:
            gScore[node.getID()] = fScore[node.getID()] = float('inf')

        open_list = [start.getID()]
        gScore[start.getID()] = 0
        fScore[start.getID()] = self.m_heuristic[start.getID()]
        parent[start.getID()] = None

        while len(open_list) > 0:
            current = open_list[0]
            currentNode : Node = self.getNodeByID(current)

            if currentNode.getPos() == endPos:
                path = []
                while current is not None:
                    path.append(self.getNodeByID(current))
                    current = parent[current]

                path.reverse()

                return path, self.pathCost(path)

            open_list.remove(current)
            for adj, custo in self.m_graph[current]:
                tentative_gScore = gScore[current] + custo
                if tentative_gScore < gScore[adj]:
                    parent[adj] = current
                    gScore[adj] = tentative_gScore
                    fScore[adj] = tentative_gScore + self.m_heuristic[adj]

                    if adj not in open_list:
                        open_list.append(adj)
                        open_list.sort(key=(lambda el : fScore[el]))

        return None
