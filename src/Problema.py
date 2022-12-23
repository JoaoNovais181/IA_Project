import os, pickle, subprocess
#  import pygame as pg
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
        if ficheiroGrafo in os.listdir(graphDir):
            file = graphDir + "/" + ficheiroGrafo
            if os.path.getsize(file) > 0:
                with open(graphDir + "/" + ficheiroGrafo, "rb") as graphFile:
                    obj = pickle.load(graphFile)
                    if isinstance(obj, Grafo):
                        self.grafo = obj
                        return


        subprocess.run(["/usr/bin/notify-send", "--icon=warning", "Grafo vai ser gerado, pode demorar um bocado..."])
        
        initialStates = list(map(lambda x : (x,x, [0,0]), self.inicio))
        expand = []
        expand.extend(initialStates)
        expanded = set()
        for initialState in initialStates:
            self.grafo.addNode(Node(initialState[0], initialState[2]))
        maxX = len(self.mapa[0])
        maxY = len(self.mapa)

        while len(expand) > 0:
            #  print(len(expand), len(expanded))
            currState = expand.pop(0)
            (currPos, prevPos, currVel) = currState
            expandedState = self.expandState(currState)
            expanded.add(f"{currPos},{currVel}")

            if (currPos[0] < 0 or currPos[0] >= maxX) or (currPos[1] < 0 or currPos[1] >= maxY):
                self.grafo.addHeuristic((currPos,currVel), self.mapaDistancias[prevPos[1]][prevPos[0]])
            else:
                self.grafo.addHeuristic((currPos,currVel), self.mapaDistancias[currPos[1]][currPos[0]])

            for ((pos,vel), pPos, weight) in expandedState:
                self.grafo.addEdge(Node(currPos,currVel), Node(pos,vel), weight)
                if f"{pos},{vel}" not in expanded and (pos, pPos, vel) not in expand:
                    expand.append((pos, pPos, vel))
        subprocess.run(["/usr/bin/notify-send", "--icon=warning", "Grafo Gerado!"])

        with open(graphDir + "/" + ficheiroGrafo, "wb") as fileToStore:
            pickle.dump(self.grafo, fileToStore)
    

    def expandState(self, state):

        Map = self.mapa
        pos, _, vel = state

        if pos in self.fim:
            return []

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

    def Competicao(self, competitors):

        def getCompetitorDistToEnd(competitorCurrNode):
            pos = competitorCurrNode.getPos()
            return self.mapaDistancias[pos[1]][pos[0]]

        if len(competitors) > len(self.inicio):
            return None

        functions = {"A*":self.AStar, "Greedy":self.Greedy, "BFS":self.BFS, "DFS":self.DFS}
        functions2 = {"A*":self.grafo.AStar, "Greedy":self.grafo.Greedy, "BFS":self.grafo.BFS, "DFS":self.grafo.DFS}

        paths = {}
        finalPath = {}

        for competitor in competitors.keys():
            path, cost = functions[competitors[competitor]]()
            paths[competitor] = path
            finalPath[competitor] = []

        competitorsList = [key for key in competitors.keys()]
        competitorCurrNode = {}
        for competitor in competitorsList:
            competitorCurrNode[competitor] = paths[competitor][0]
        competitorsList.sort(reverse=True, key=(lambda c : getCompetitorDistToEnd(competitorCurrNode[c])))
        #  orderedCompetitors = competitorsList.sort(key=(lambda c : self.mapaDistancias[paths[c][0].getPos()[1]][paths[c][0].getPos()[0]]))

        lastNode = {}
        ignoreIV = {}
        for competitor in competitorsList:
            lastNode[competitor] = None
            ignoreIV[competitor] = False
        occupiedPositions = []
        finished = 0
        i = 0
        while finished != len(competitorsList):
            #  print(f"Iter{i}, {occupiedPositions}")
            i+=1
            for competitor in competitorsList:
                competitorPos = competitorCurrNode[competitor].getPos()
                if competitorPos in self.fim:
                    if (competitor, competitorPos) not in occupiedPositions:
                        occupiedPositions.pop(list(map(lambda x : x[0], occupiedPositions)).index(competitor))
                        occupiedPositions.append((competitor,competitorPos))
                        
                        finalPath[competitor].append(competitorCurrNode[competitor])

                        finished += 1
                    continue

                if competitorPos in map(lambda x : x[1], occupiedPositions):
                    initialNodes = None
                    if not ignoreIV[competitor]:
                        initialNodes = list(map(lambda p : self.grafo.getNodeBySearchNode(Node(p,[0,0])), self.inicio))
                        for n in initialNodes:
                            if n.getPos() in map(lambda p : p[1],occupiedPositions):
                                initialNodes.remove(n)

                    else:
                        initialNodes = [lastNode[competitor]]
                    
    
                    for c,pos in occupiedPositions:
                        if c == competitor:
                            occupiedPositions.remove((c,pos))
                            break
                    

                    path, cost = functions2[competitors[competitor]](initialNodes, self.fim, list(map(lambda x : x[1], occupiedPositions)), ignoreIV[competitor]) 
                    if not ignoreIV[competitor] :
                        paths[competitor] = path
                        ignoreIV[competitor] = True
                    else:
                        if path is None:
                            print(f"competitor:{competitor}, alg:{competitors[competitor]}, currPos:{competitorPos}, initialNodes: {initialNodes}, occupiedPositions:{occupiedPositions}, lastNode:{lastNode}")
                        paths[competitor] = path[1::]
                    competitorCurrNode[competitor] = path[0]
                
                lastNode[competitor] = paths[competitor].pop(0)

                for c,pos in occupiedPositions:
                    if c == competitor:
                        occupiedPositions.remove((c,pos))
                        break
                #  occupiedPositions.pop(list(map(lambda x : x[0], occupiedPositions)).index(competitor))
                occupiedPositions.append((competitor,lastNode[competitor].getPos()))
                finalPath[competitor].append(lastNode[competitor])
                competitorCurrNode[competitor] = paths[competitor][0]

            competitorsList.sort(reverse=True, key=(lambda c : getCompetitorDistToEnd(competitorCurrNode[c])))

        for k in finalPath.keys():
            path = finalPath[k]
            custo = self.grafo.pathCost(path)
            #  print(custo)
            finalPath[k] = (path,custo)
        return finalPath


    def printGrafo(self):
        print(self.grafo.m_nodes)



#  competitors = {1:"Greedy", 2:"Greedy"}
#  p = Problema("../mapas/mapaComplicado.txt")
#  p.constroiGrafo()
#  d = p.Competicao(competitors)
#  
#  resultList = []
#  for k in d.keys():
    #  resultList.append((k,d[k][0],d[k][1]))
#  
#  m.desenhaMapa(p.mapa, resultList)
