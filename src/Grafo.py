import math
from queue import Queue
from Node import Node

class Grafo:

    def __init__(self):
        #contador de nodos, de forma a atribuir ID's aos nodos
        self.nodeCounter = 0
        #lista de nodos presentes no grafo
        self.m_nodes  	 = []
        #dicionario usado para associar o id de um nodo ao tuplo (id,peso) com os nodos a que ele está ligado
        self.m_graph  	 = {}
        #dicionario para guardar a distancia de cada nodo ao nodo final (parte da heuristica)
        self.m_heuristic = {}
#         self.m_h      	 = {}

    def __str__(self):
        out = ""
        # para cada par chave-valor no dicionario de ligacoes adicionar ao resultado final "node IDchave : (IDvalor,peso)"
        for key, val in self.m_graph:
            out = out + f"node {str(key)} : {str(val)}\n"

        return out

    def addEdge(self, node1 : Node, node2 : Node, weight):

        # usar o metodo addNode para adicionar um nodo ao grafo ou retornar o guardado se este já existir
        node1 = self.addNode(node1)

        node2 = self.addNode(node2)

        # self.m_graph[self.m_nodeID[node1]].add((self.m_nodeID[node2], weight))
        # adicionar a ligacao entre os nodos
        self.m_graph[node1.getID()].add((node2.getID(), weight))

    def addNode(self, node : Node):
        # se o nodo nao estiver no grafo, adicionamo-lo
        if node not in self.m_nodes:
            self.m_nodes.append(node)
            node.setID(self.nodeCounter)
            self.nodeCounter += 1
            self.m_graph[node.getID()] = set()
            return node
        #caso contrário retornamos o que está no grafo
        return self.getNodeBySearchNode(node)
    
    def getNodeBySearchNode(self, searchNode):
    
        for node in self.m_nodes:
            if node == searchNode:
                return node

        return None

    def getNodeByID(self, searchID: int) -> Node:

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
            #  print(path[i], path[i+1], cost)

        return cost

    def addHeuristic(self, state, heuristic):
        pos,vel = state
        node = Node(pos,vel)
        n = self.getNodeBySearchNode(node)
        if n is not None:
            self.m_heuristic[n.getID()] = heuristic

    def BFS(self, start:list[Node], endPos, prohibitedPos = [], ignoreInitialVerification = False):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()
        parent = dict()

        if not ignoreInitialVerification:
            for n in start:
                if n.getPos() in prohibitedPos:
                    start.remove(n)

        # adicionar o nodo inicial à fila e aos visitados
        for node in start:
            fila.put(node.getID())
            visited.add(node.getID())
            parent[node.getID()] = None


        end = None

        while not fila.empty() and end is None:
            nodo_atual = self.getNodeByID(fila.get())
            if nodo_atual.getPos() in endPos:
                end = nodo_atual
            else:
                for (adjacente, _) in self.m_graph[nodo_atual.getID()]:

                    if self.getNodeByID(adjacente).getPos() in prohibitedPos:
                        continue

                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual.getID()
                        visited.add(adjacente)
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

    def DFS(self, start:list[Node], endPos, prohibitedPos = [], ignoreInitialVerification = False):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = []
        parent = dict()

        if not ignoreInitialVerification:
            for n in start:
                if n.getPos() in prohibitedPos:
                    start.remove(n)

        # adicionar o nodo inicial à fila e aos visitados
        for n in start:
            fila.append(n.getID())
            visited.add(n.getID())
            parent[n.getID()] = None

        end = None

        while len(fila)>0 and end is None:
            nodo_atual = self.getNodeByID(fila.pop())

            if not ignoreInitialVerification and nodo_atual.getPos() in prohibitedPos:
                continue

            if nodo_atual.getPos() in endPos:
                end = nodo_atual
            else:
                paraMandar = []
                for (adjacente, _) in self.m_graph[nodo_atual.getID()]:

                    if self.getNodeByID(adjacente).getPos() in prohibitedPos:
                        continue

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

    def AStar(self, start:list[Node], endPos, prohibitedPos = [], ignoreInitialVerification = False):
        gScore = {}
        fScore = {}
        parent = {}

        if not ignoreInitialVerification:
            for n in start:
                if n.getPos() in prohibitedPos:
                    start.remove(n)

        for node in self.m_nodes:
            gScore[node.getID()] = fScore[node.getID()] = float('inf')

        open_list = []
        open_list.extend(list(map(lambda n : n.getID(), start)))
        for n in start:
            gScore[n.getID()] = 0
            fScore[n.getID()] = self.m_heuristic[n.getID()]
            parent[n.getID()] = None

        while len(open_list) > 0:
            current = open_list[0]
            currentNode : Node = self.getNodeByID(current)

            if currentNode.getPos() in endPos:
                path = []
                while current is not None:
                    path.append(self.getNodeByID(current))
                    current = parent[current]

                path.reverse()

                return path, self.pathCost(path)

            open_list.remove(current)
            for adj, custo in self.m_graph[current]:
                adjNode = self.getNodeByID(adj)
                
                if adjNode.getPos() in prohibitedPos:
                    continue

                tentative_gScore = gScore[current] + custo
                if tentative_gScore < gScore[adj]:
                    parentVel = currentNode.getVel()
                    currVel   = self.getNodeByID(adj).getVel()
                    normDiff = 0.5*((parentVel[0]*parentVel[0] + parentVel[1]*parentVel[1]) - (currVel[0]*currVel[0] + currVel[1]*currVel[1]))
                    parent[adj] = current
                    gScore[adj] = tentative_gScore
                    fScore[adj] = (tentative_gScore + self.m_heuristic[adj]) / (currVel[0]*currVel[0] + currVel[1]*currVel[1]+1) + normDiff

                    if adj not in open_list:
                        open_list.append(adj)
                        open_list.sort(key=(lambda el : fScore[el]))

        return None, None

    def Greedy(self, start:list[Node], endPos, prohibitedPos = [], ignoreInitialVerification = False):
        parent = {}

        if not ignoreInitialVerification:
            for n in start:
                if n.getPos() in prohibitedPos:
                    start.remove(n)

        open_list = []
        closed_list = []
        open_list.extend(list(map(lambda n : (n.getID(),0,1) , start)))
        for n in start:
            #  gScore[n.getID()] = 0
            #  fScore[n.getID()] = self.m_heuristic[n.getID()]
            parent[(n.getID(),0)] = (None, 0)

        while len(open_list) > 0:
            current, normDiff, currentNorm = None, None, None

            for nID, nD, nN in open_list:
                if current == None or (self.m_heuristic[nID]/nN) + nD < (self.m_heuristic[current]/currentNorm) + normDiff:
                    current = nID
                    normDiff = nD
                    currentNorm = nN
            
            if current == None:
                return None
            
            currentNode : Node = self.getNodeByID(current)

            if currentNode.getPos() in endPos:
                path = []
                while current is not None:
                    path.append(self.getNodeByID(current))
                    current, normDiff = parent[(current,normDiff)]

                path.reverse()

                return path, self.pathCost(path)

            for adj, _ in self.m_graph[current]:
                
                if self.getNodeByID(adj).getPos() in prohibitedPos:
                    continue

                parentVel = currentNode.getVel()
                currVel   = self.getNodeByID(adj).getVel()
                nD = 0.5*((parentVel[0]*parentVel[0] + parentVel[1]*parentVel[1]) - (currVel[0]*currVel[0] + currVel[1]*currVel[1]))
                if (adj, nD) not in open_list and (adj,nD) not in closed_list:
                    parent[(adj,nD)] = (current, normDiff)
                    norm = (currVel[0]**2 + currVel[1]**2 +1)
                    open_list.append((adj,nD,norm))
            
            open_list.remove((current,normDiff,currentNorm))
            closed_list.append((current,normDiff,currentNorm))

        return None
