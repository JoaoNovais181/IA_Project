#  from copy  import deepcopy
#  import math
import os, pickle
from Grafo import Grafo
from Node  import Node
import Mapa as m

graphDir = "../grafos"

class Problema:

    def __init__(self, ficheiroMapa : str):
        self.ficheiroMapa : str = ficheiroMapa
        
        mapa = m.carregaMapa(ficheiroMapa)
        self.mapa = mapa
        
        self.inicio = []
        self.fim = []

        for y, linha in enumerate(mapa):
            for x, val in enumerate(linha):
                if val == "I":
                    self.inicio.append([x,y])
                elif val == "F":
                    self.fim.append([x,y])
    
        self.mapaDistancias = m.distanceMap(mapa)
        self.grafo = Grafo()

    def constroiGrafo(self):
        
        ficheiroGrafo = self.ficheiroMapa.replace("../mapas/", "")
        #  print(ficheiroGrafo, os.listdir(graphDir))
        if ficheiroGrafo in os.listdir(graphDir):
            file = graphDir + "/" + ficheiroGrafo
            if os.path.getsize(file) > 0:
                with open(graphDir + "/" + ficheiroGrafo, "rb") as graphFile:
                    obj = pickle.load(graphFile)
                    if isinstance(obj, Grafo):
                        self.grafo = obj
                        print(len(self.grafo.m_nodes))
                        return
        
        initialStates = list(map(lambda x : (x,x, [0,0]), self.inicio))
        expand = []
        expand.extend(initialStates)
        expanded = set()
        for initialState in initialStates:
            self.grafo.addNode(Node(initialState[0], initialState[2]))
        maxX = len(self.mapa[0])
        maxY = len(self.mapa)

        while len(expand) > 0:
            currState = expand.pop(0)
            (currPos, prevPos, currVel) = currState
            expandedState = self.expandState(currState)
            expanded.add(f"{currPos},{currVel}")

            print(len(expand), len(expanded))

            if (currPos[0] < 0 or currPos[0] >= maxX) or (currPos[1] < 0 or currPos[1] >= maxY):
                self.grafo.addHeuristic((currPos,currVel), self.mapaDistancias[prevPos[1]][prevPos[0]])
            else:
                self.grafo.addHeuristic((currPos,currVel), self.mapaDistancias[currPos[1]][currPos[0]])

            for ((pos,vel), pPos, weight) in expandedState:
                self.grafo.addEdge(Node(currPos,currVel), Node(pos,vel), weight)
                if f"{pos},{vel}" not in expanded and (pos, pPos, vel) not in expand:
                    expand.append((pos, pPos, vel))

        with open(graphDir + "/" + ficheiroGrafo, "wb") as fileToStore:
            pickle.dump(self.grafo, fileToStore)
    

    def expandState(self, state):

        Map = self.mapa
        pos, _, vel = state

        if pos in self.fim:
            return []

        # print(pos, vel)
        if (pos[0]<0 or pos[0]>=len(Map[0])) or (pos[1]<0 or pos[1]>=len(Map)) or self.mapa[pos[1]][pos[0]] == "#":
            x = self.jogadorFora(state)
            return [x]

        expanded = []
        expanded.append(self.acelerarXabrandarY(state,Map))
        expanded.append(self.acelerarXmanterY(state,Map))
        expanded.append(self.acelerarXacelerarY(state,Map))
        expanded.append(self.manterXabrandarY(state,Map))
        if vel != [0,0]: expanded.append(self.manterXmanterY(state,Map))
        expanded.append(self.manterXacelerarY(state,Map))
        expanded.append(self.abrandarXabrandarY(state,Map))
        expanded.append(self.abrandarXmanterY(state,Map))
        expanded.append(self.abrandarXacelerarY(state,Map))
   
        return expanded

    def jogadorFora(self, state):
        pos, prevPos, _ = state

        return ((prevPos,[0,0]), pos, 25)

    def validVector(self, pos, vel, acl, Map): 

        velx = vel[0]+acl[0]
        vely = vel[1]+acl[1]
        posxB, posxA = pos[0], pos[0]+velx
        posyB, posyA = pos[1], pos[1]+vely
        if posxA<0 or posxA>=len(Map[0]) or posyA<0 or posyA>=len(Map) or Map[posyA][posxA] == "#":
            return [posxA, posyA]

        if  velx == 0:
            yi, yf = posyB, posyA
            if posyB > posyA:
                yf, yi = posyB, posyA
            for y, val in enumerate(list(map(lambda x: x[posxA], Map))[yi:yf+1]):
                if val == "#":
                    return [posxA,y+yi]
            return [posxA, posyA]

        if  vely == 0:
            xi, xf = posxB, posxA
            if posxB > posxA:
                xf, xi = posxB, posxA
            for x, val in enumerate(Map[posyB][xi: xf+1]):
                if val == "#":
                    return [x+xi, posyB]
            return [posxA, posyA]

        if abs(posxA - posxB)==1 or abs(posyA - posyB) == 1:
            xi, xf = posxB, posxA
            yi, yf = posyB, posyA
            if (posxA < posxB):
                xi, xf = posxA, posxB
            if (posyA < posyB):
                yi, yf = posyA, posyB

            for y in range(yi, yf+1):
                for x, val in enumerate(Map[y][xi:xf+1]):
                    if val == "#" :
                        return [x+xi,y]
            return [posxA, posyA]

        declive = (posyB - posyA)/(posxB - posxA)

        b = posyB - declive*posxB

        xi, xf = posxB, posxA
        forwardX = True
        if posxB > posxA:
            xf, xi = posxB, posxA
            forwardX = False

        for x in range(xi, xf):
            y1 = declive*x + b
            y = int(y1)
            if Map[int(y1)][x] == "#":
                return [x,y]

            if forwardX:
                if x<len(Map[0])-1 and Map[y][x+1] == "#":
                    return [x+1, y]
            else:
                if x>0 and Map[y][x-1] == "#":
                    return [x-1, y]

        declive = (posxB - posxA)/(posyB - posyA)

        b = posxB - declive*posyB

        yi, yf = posyB, posyA
        downY = True
        if posyB > posyA:
            yf, yi = posyB, posyA
            downY = False

        for y in range(yi, yf):
            x1 = declive*y + b
            x = int(x1)
            if Map[y][x] == "#":
                return [x, y]
            
            if downY:
                if y<len(Map)-1 and Map[y+1][x] == "#":
                    return [x, y+1]
            else:
                if y>0 and Map[y-1][x] == "#":
                    return [x, y-1]

        return [posxA, posyA]

    def acelerarXabrandarY(self, state, Map): 
        pos, _, vel = state
        acl = [ 1,-1]
        posA = self.validVector(pos, vel, acl, Map)
        velA = [vel[0]+acl[0],vel[1]+acl[1]]
        return ((posA, velA), pos, 1)

    def acelerarXmanterY(self, state, Map):
        pos, _, vel = state
        acl = [ 1, 0]
        posA = self.validVector(pos, vel, acl, Map)
        velA = [vel[0]+acl[0],vel[1]+acl[1]]
        return ((posA, velA), pos, 1)

    def acelerarXacelerarY(self, state, Map):
        pos, _, vel = state
        acl = [ 1, 1]
        posA = self.validVector(pos, vel, acl, Map)
        velA = [vel[0]+acl[0],vel[1]+acl[1]]
        return ((posA, velA), pos, 1)

    def abrandarXabrandarY(self, state, Map):
        pos, _, vel = state
        acl = [-1,-1]
        posA = self.validVector(pos, vel, acl, Map)
        velA = [vel[0]+acl[0],vel[1]+acl[1]]
        return ((posA, velA), pos, 1)

    def abrandarXmanterY(self, state, Map):
        pos, _, vel = state
        acl = [-1, 0]
        posA = self.validVector(pos, vel, acl, Map)
        velA = [vel[0]+acl[0],vel[1]+acl[1]]
        return ((posA, velA), pos, 1)

    def abrandarXacelerarY(self, state, Map):
        pos, _, vel = state
        acl = [-1, 1]
        posA = self.validVector(pos, vel, acl, Map)
        velA = [vel[0]+acl[0],vel[1]+acl[1]]
        return ((posA, velA), pos, 1)

    def manterXabrandarY(self, state, Map):
        pos, _, vel = state
        acl = [ 0,-1]
        posA = self.validVector(pos, vel, acl, Map)
        velA = [vel[0]+acl[0],vel[1]+acl[1]]
        return ((posA, velA), pos, 1)

    def manterXmanterY(self, state, Map):
        pos, _, vel = state
        acl = [ 0, 0]
        posA = self.validVector(pos, vel, acl, Map)
        velA = [vel[0]+acl[0],vel[1]+acl[1]]
        return ((posA, velA), pos, 1)

    def manterXacelerarY(self, state, Map):
        pos, _, vel = state
        acl = [ 0, 1]
        posA = self.validVector(pos, vel, acl, Map)
        velA = [vel[0]+acl[0],vel[1]+acl[1]]
        return ((posA, velA), pos, 1)

    def BFS(self):
        return self.grafo.BFS(list(map(lambda p : self.grafo.getNodeBySearchNode(Node(p,[0,0])), self.inicio)), self.fim)

    def DFS(self):
        return self.grafo.DFS(list(map(lambda p : self.grafo.getNodeBySearchNode(Node(p,[0,0])), self.inicio)), self.fim)

    def AStar(self):
        return self.grafo.AStar(list(map(lambda p : self.grafo.getNodeBySearchNode(Node(p,[0,0])), self.inicio)), self.fim)

    def Greedy(self):
        return self.grafo.Greedy(list(map(lambda p : self.grafo.getNodeBySearchNode(Node(p,[0,0])), self.inicio)), self.fim)
    
    def printGrafo(self):
        print(self.grafo.m_nodes)

def main():
    # Map = carregaMapa("mapaTeste.txt")
    #  Map = m.carregaMapa("mapaFase1.txt")
    problema = Problema("mapaFase1.txt")
    # problema = Problema(Map, [0,1], [5,1])
    print("Antes de construir")
    problema.constroiGrafo()
    print("Depois de construir")
    caminho, custo = problema.BFS()
    # print(list(map(lambda x : x.getPos(), caminho)), custo)
    #  m.desenhaMapa(Map, caminho, custo)

if __name__ == "__main__":
    main()
