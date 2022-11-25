from copy  import deepcopy
import math
from Grafo import Grafo
from Node  import Node
import Mapa as m

class Problema:

    def __init__(self, mapa):
        self.mapa = mapa
        
        for y, linha in enumerate(mapa):
            for x, val in enumerate(linha):
                if val == "I":
                    self.inicio = [x,y]
                elif val == "F":
                    self.fim = [x,y]
    
        self.mapaDistancias = m.distanceMap(mapa)
        self.grafo = Grafo()

    def constroiGrafo(self):

        initialState = (self.inicio, [0,0])
        expand = []
        expand.append((initialState, 0))
        expanded = set()
        self.grafo.addNode(Node(*initialState))

        while len(expand) > 0:
            currState, normDiff = expand[0]
            del expand[0]
            (currPos, currVel) = currState
            expandedState = self.expandState(currState)
            expanded.add(f"{currPos},{currVel}")

            if (currPos[0] < 0 or currPos[0] >= len(self.mapa[0])) or (currPos[1] < 0 or currPos[1] >= len(self.mapa)):
                self.grafo.addHeuristic(currState, self.mapaDistancias[currPos[1]-currVel[1]][currPos[0]-currVel[0]] + normDiff)
            else:
                self.grafo.addHeuristic(currState, self.mapaDistancias[currPos[1]][currPos[0]] + normDiff)

            for ((pos,vel),weight, nD) in expandedState:
                self.grafo.addEdge(Node(currPos,currVel), Node(pos,vel), weight)
                if f"{pos},{vel}" not in expanded and ((pos,vel), nD) not in expand:
                    # expand.put((pos,vel))
                    expand.append(((pos,vel),nD))
    def expandState(self, state):

        Map = self.mapa
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

        return ((pos,[0,0]), 1, 25)

    def validVector(self, pos, vel, acl, Map): 

        velx,vely = vel[0]+acl[0], vel[1]+acl[1]
        posxB, posxA = pos[0], pos[0]+velx
        posyB, posyA = pos[1], pos[1]+vely
        # print(posxB, posxA, posyB, posyA)
        if ((posxA<0 or posxA>=len(Map[0])) or (posyA<0 or posyA>=len(Map))):
            return True


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
        normOld = (vel[0]*vel[0] + vel[1]*vel[1])
        if self.validVector(pos,vel,acl,Map):
            vel[0] += acl[0]
            vel[1] += acl[1]
            pos[0] += vel[0]
            pos[1] += vel[1]

            normNew = (vel[0]*vel[0] + vel[1]*vel[1])
            
            return ((pos,vel), 1, 0.5*(normOld - normNew))
        return None

    def acelerarXmanterY(self, state, Map):
        pos, vel = state
        acl = [ 1, 0]
        normOld = (vel[0]*vel[0] + vel[1]*vel[1])
        if self.validVector(pos,vel,acl,Map):
            vel[0] += acl[0]
            vel[1] += acl[1]
            pos[0] += vel[0]
            pos[1] += vel[1]

            normNew = (vel[0]*vel[0] + vel[1]*vel[1])

            return ((pos,vel), 1, 0.5*(normOld - normNew))
        return None

    def acelerarXacelerarY(self, state, Map):
        pos, vel = state
        acl = [ 1, 1]
        normOld = (vel[0]*vel[0] + vel[1]*vel[1])
        if self.validVector(pos,vel,acl,Map):
            vel[0] += acl[0]
            vel[1] += acl[1]
            pos[0] += vel[0]
            pos[1] += vel[1]

            normNew = (vel[0]*vel[0] + vel[1]*vel[1])
            
            return ((pos,vel), 1, 0.5*(normOld - normNew))
        return None

    def abrandarXabrandarY(self, state, Map):
        pos, vel = state
        acl = [-1,-1]
        normOld = (vel[0]*vel[0] + vel[1]*vel[1])
        if self.validVector(pos,vel,acl,Map):
            vel[0] += acl[0]
            vel[1] += acl[1]
            pos[0] += vel[0]
            pos[1] += vel[1]

            normNew = (vel[0]*vel[0] + vel[1]*vel[1])
            
            return ((pos,vel), 1, 0.5*(normOld - normNew))
        return None

    def abrandarXmanterY(self, state, Map):
        pos, vel = state
        acl = [-1, 0]
        normOld = (vel[0]*vel[0] + vel[1]*vel[1])
        if self.validVector(pos,vel,acl,Map):
            vel[0] += acl[0]
            vel[1] += acl[1]
            pos[0] += vel[0]
            pos[1] += vel[1]

            normNew = (vel[0]*vel[0] + vel[1]*vel[1])
            
            return ((pos,vel), 1, 0.5*(normOld - normNew))
        return None

    def abrandarXacelerarY(self, state, Map):
        pos, vel = state
        acl = [-1, 1]
        normOld = (vel[0]*vel[0] + vel[1]*vel[1])
        if self.validVector(pos,vel,acl,Map):
            vel[0] += acl[0]
            vel[1] += acl[1]
            pos[0] += vel[0]
            pos[1] += vel[1]

            normNew = (vel[0]*vel[0] + vel[1]*vel[1])
            
            return ((pos,vel), 1, 0.5*(normOld - normNew))
        return None

    def manterXabrandarY(self, state, Map):
        pos, vel = state
        acl = [ 0,-1]
        normOld = (vel[0]*vel[0] + vel[1]*vel[1])
        if self.validVector(pos,vel,acl,Map):
            vel[0] += acl[0]
            vel[1] += acl[1]
            pos[0] += vel[0]
            pos[1] += vel[1]

            normNew = (vel[0]*vel[0] + vel[1]*vel[1])
            
            return ((pos,vel), 1, 0.5*(normOld - normNew))
        return None

    def manterXmanterY(self, state, Map):
        pos, vel = state
        acl = [ 0, 0]
        normOld = (vel[0]*vel[0] + vel[1]*vel[1])
        if self.validVector(pos,vel,acl,Map):
            vel[0] += acl[0]
            vel[1] += acl[1]
            pos[0] += vel[0]
            pos[1] += vel[1]

            normNew = (vel[0]*vel[0] + vel[1]*vel[1])
            
            return ((pos,vel), 1, 0.5*(normOld - normNew))
        return None

    def manterXacelerarY(self, state, Map):
        pos, vel = state
        acl = [ 0, 1]
        normOld = (vel[0]*vel[0] + vel[1]*vel[1])
        if self.validVector(pos,vel,acl,Map):
            vel[0] += acl[0]
            vel[1] += acl[1]
            pos[0] += vel[0]
            pos[1] += vel[1]

            normNew = (vel[0]*vel[0] + vel[1]*vel[1])
            
            return ((pos,vel), 1, 0.5*(normOld - normNew))
        return None

    def BFS(self):
        return self.grafo.BFS(self.grafo.getNodeBySearchNode(Node(self.inicio, [0,0])), self.fim)

    def DFS(self):
        return self.grafo.DFS(self.grafo.getNodeBySearchNode(Node(self.inicio,[0,0])), self.fim)

    def AStar(self):
        return self.grafo.AStar(self.grafo.getNodeBySearchNode(Node(self.inicio,[0,0])), self.fim)

    def printGrafo(self):
        print(self.grafo.m_nodes)

def main():
    # Map = carregaMapa("mapaTeste.txt")
    Map = m.carregaMapa("mapaFase1.txt")
    problema = Problema(Map, [3,0], [7,14])
    # problema = Problema(Map, [0,1], [5,1])
    print("Antes de construir")
    problema.constroiGrafo()
    print("Depois de construir")
    caminho, custo = problema.BFS()
    # print(list(map(lambda x : x.getPos(), caminho)), custo)
    m.desenhaMapa(Map, caminho, custo)

if __name__ == "__main__":
    main()
