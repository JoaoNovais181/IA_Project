import pygame, sys, os
from Problema import Problema
import Mapa
from Node import Node

diretoriaMapas = "../mapas"
mapas = os.listdir(diretoriaMapas)

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

    mapa = Mapa.carregaMapa(diretoriaMapas+"/"+ficheiroMapa)
    problema = Problema(diretoriaMapas+"/"+ficheiroMapa)
    problema.constroiGrafo()

    opcoes = ["DFS - Depth First Search", "BFS - Breadth First Search", "A*", "Todos", "Ver Mapa", "Voltar"]
    nOpcoes = len(opcoes)

    selected = 0

    while True:
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
                    elif selected == 4:
                        Mapa.desenhaMapa(mapa)
                    return 0
                if event.key == pygame.K_ESCAPE:
                    return
       
        printOpcoes(opcoes, screen, selected)
        screen.blit(bg, (0, 0))

    return 1

def selecionarMapa(screen):

    selected = 0
    mapaPorPag = 3
    numPags = len(mapas) // mapaPorPag
    pagAtual = 0
    bg = pygame.image.load("../images/VectorRace.png")
    while True:
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

                if event.key == pygame.K_ESCAPE:
                    return

        

        screen.blit(bg, (0, 0)) 
        printOpcoes(opcoes, screen, selected)

def main():
    pygame.init()
    bg = pygame.image.load("../images/VectorRace.png")
    size = bg.get_size()
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Vector Race")
    screen.fill((255,200,200))



    clock = pygame.time.Clock()

    selected = 0
    opcoes = {"Selecionar Mapa":selecionarMapa, "Sair":sys.exit}

    while True:
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
