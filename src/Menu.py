import pygame, sys, os
from Problema import Problema
import Mapa
from Node import Node


class Button:

    position = {'x':0, 'y':0}
    size = {'width':0, 'height':0}

    def __init__ (self, x, y, width, height, text):
        self.position['x']  = x
        self.position['y']  = y
        self.size['width']  = width
        self.size['height'] = height
        self.surface = pygame.display.set_mode((400, 300))
        self.text = text
        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def draw (self, mouse_pos):
        text = self.font.render(self.text, True, (0,0,0))
        textRect = text.get_rect()
        textRect.topleft = [int(self.size['width']/2-textRect.width/2),int(self.position['y']+5)]
        color = (255, 0, 0)
        if mouse_pos['x'] >= self.position['x'] and mouse_pos['x'] <= self.position['x'] + self.size['width'] and mouse_pos['y'] >= self.position['y'] and mouse_pos['y'] <= self.position['y'] + self.size['height']:
            color = (255, 100, 100)
        pygame.draw.rect(self.surface, (0,0,0), pygame.Rect(self.position['x'], self.position['y'], self.size['width'], self.size['height']))
        pygame.draw.rect(self.surface, color, pygame.Rect(self.position['x']+int(self.size['width']/2)-int(0.9*self.size['width']/2), self.position['y']+int(self.size['height']/2)-int(0.9*self.size['height']/2), int(self.size['width']*0.9), int(self.size['height']*0.9)))



diretoriaMapas = "../mapas"
mapas = os.listdir(diretoriaMapas)
clock = pygame.time.Clock()



def printOpcoes(options, screen, selected=0):

    width, height = screen.get_size()
    yOffset = height/(len(options)+1)
    font = pygame.font.Font('freesansbold.ttf', 20)

    for i in range(1, len(options)+1):
        if len(options[i-1]) == 0:
            continue
        text = font.render(options[i-1], True, (0,0,0))
        textRect = text.get_rect()
        textRect.topleft = [int(width/2-textRect.width/2),int(i*yOffset+5)]
        
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(int(width/2-textRect.width/2 - 13), int(i*yOffset-3), textRect.width+26, textRect.height+16))
        pygame.draw.rect(screen, (255,0,0) if selected==i-1 else (255,150,150), pygame.Rect(int(width/2-textRect.width/2 - 10), int(i*yOffset), textRect.width+20, textRect.height+10))
        screen.blit(text, textRect)

    pygame.display.flip()

def comecaJogo(screen, ficheiroMapa):
    bg = pygame.image.load("../images/VectorRace.png")
    size = bg.get_size()

    mapa = Mapa.carregaMapa(diretoriaMapas+"/"+ficheiroMapa)
    problema = Problema(diretoriaMapas+"/"+ficheiroMapa)
    problema.constroiGrafo()

    opcoes = ["DFS - Depth First Search", "BFS - Breadth First Search", "A*", "Greedy", "Todos", "Ver Mapa", "Voltar"]
    nOpcoes = len(opcoes)

    selected = 0

    while True:
        if screen.get_size() != size:
            screen = pygame.display.set_mode(size)
            pygame.transform.scale(screen, size)
            bg = pygame.image.load("../images/VectorRace.png")
        for event in pygame.event.get():
                ## Se encontrat um quit sai da janela
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected+1)%nOpcoes
                if event.key == pygame.K_UP:
                    selected = (selected-1 + nOpcoes)%nOpcoes
                if event.key == pygame.K_RETURN:
                    if opcoes[selected] == "Voltar":
                        return 1
                    if selected == 0:
                        path, custo = problema.DFS()
                        Mapa.desenhaMapa(mapa, [path], [custo])
                    elif selected == 1:
                        path, custo = problema.BFS()
                        Mapa.desenhaMapa(mapa, [path], [custo])
                    elif selected == 2:
                        path, custo = problema.AStar()
                        Mapa.desenhaMapa(mapa, [path], [custo])
                    elif selected == 3:
                        path, custo = problema.Greedy()
                        Mapa.desenhaMapa(mapa, [path], [custo])
                    elif selected == 4:
                        path1, custo1 = problema.DFS()
                        path2, custo2 = problema.BFS()
                        path3, custo3 = problema.AStar()
                        paths : list[list[Node]] = []
                        paths.append(path1)
                        paths.append(path2)
                        paths.append(path3)
                        costs  : list[list[int]]= []
                        costs.append(custo1)
                        costs.append(custo2)
                        costs.append(custo3)
                        Mapa.desenhaMapa(mapa, paths, costs)
                    elif selected == 5:
                        Mapa.desenhaMapa(mapa)
                if event.key == pygame.K_ESCAPE:
                    return
       
        printOpcoes(opcoes, screen, selected)
        screen.blit(bg, (0, 0))
        clock.tick(30)

    return 1

def selecionarMapa(screen):

    selected = 0
    mapaPorPag = 3
    numPags = len(mapas) // mapaPorPag + 1
    pagAtual = 0
    bg = pygame.image.load("../images/VectorRace.png")
    size = bg.get_size()
    while True:
        if screen.get_size() != size:
            screen = pygame.display.set_mode(size)
            pygame.transform.scale(screen, size)
            bg = pygame.image.load("../images/VectorRace.png")
        opcoes = mapas[pagAtual*mapaPorPag:pagAtual*mapaPorPag + mapaPorPag]

        while len(opcoes) < mapaPorPag:
            opcoes.append("")
        opcoes.append("Voltar")

        for event in pygame.event.get():
                ## Se encontrat um quit sai da janela
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    while True:
                        selected = (selected+1)%(mapaPorPag+1)

                        if len(opcoes[selected]) > 0:
                            break
                if event.key == pygame.K_UP:
                    while True:
                        selected = (selected-1 + (mapaPorPag+1))%(mapaPorPag+1)

                        if len(opcoes[selected]) > 0:
                            break

                if event.key == pygame.K_RETURN:    
                    if opcoes[selected] == "Voltar":
                        return
                    else:
                        res = comecaJogo(screen, opcoes[selected])               
                        if res == 0:
                            return
                
                if event.key == pygame.K_RIGHT:
                    pagAtual = (pagAtual+1)%numPags

                if event.key == pygame.K_LEFT:
                    pagAtual = (pagAtual+numPags-1)%numPags
            

                if event.key == pygame.K_ESCAPE:
                    return

        

        screen.blit(bg, (0, 0)) 
        printOpcoes(opcoes, screen, selected)
        clock.tick(30)

def main():
    pygame.init()
    bg = pygame.image.load("../images/VectorRace.png")
    size = bg.get_size()
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Vector Race")
    screen.fill((255,200,200))




    selected = 0
    opcoes = {"Selecionar Mapa":selecionarMapa, "Sair":sys.exit}

    while True:
        if screen.get_size() != size:
            screen = pygame.display.set_mode(size)
            pygame.transform.scale(screen, size)
            bg = pygame.image.load("../images/VectorRace.png")
        #  screen = pygame.display.set
        for event in pygame.event.get():
                ## Se encontrat um quit sai da janela
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected+1)%len(opcoes)
                if event.key == pygame.K_UP:
                    selected = (selected-1 + len(opcoes))%len(opcoes)
                if event.key == pygame.K_RETURN:    
                    #  acao = opcoes[list(opcoes.keys())[selected]]
                    if selected == 0:
                        selecionarMapa(screen)
                    else:
                        sys.exit()
        

        screen.blit(bg, (0, 0)) 
        printOpcoes(list(opcoes.keys()), screen, selected)

        clock.tick(30)


if __name__ == "__main__":
    main()
