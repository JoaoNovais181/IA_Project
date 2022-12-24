import pygame, sys, os
from Problema import Problema
import Mapa


diretoriaMapas = "../mapas"
mapas = os.listdir(diretoriaMapas)
clock = pygame.time.Clock()
SIZE = 700,500
bg = pygame.image.load("../images/VectorRace.png")
bg = pygame.transform.scale(bg, SIZE)


class Popup():

    def __init__(self, text, x=0, y=0):

        font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = text
        text_image = font.render(text, True, (0,0,0))

        width, height = text_image.get_width() + 20, text_image.get_height() + 20
        self.image = pygame.Surface((width,height))
        self.image.fill((0,0,0))
        self.image.fill((255,0,0), pygame.Rect(5, 5, width - 10, height-10))

        self.rect = self.image.get_rect()
         
        text_rect = text_image.get_rect(center = self.rect.center)
        
        self.image.blit(text_image, text_rect)

        self.rect.center = (x, y)

    def draw(self, surface):

        surface.blit(self.image, self.rect)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return True
        return False


def printOpcoes(options, screen, selected : int | None = 0):

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
        if selected is not None:
            pygame.draw.rect(screen, (255,0,0) if selected==i-1 else (255,150,150), pygame.Rect(int(width/2-textRect.width/2 - 10), int(i*yOffset), textRect.width+20, textRect.height+10))
        else:
            pygame.draw.rect(screen, (255,150,150), pygame.Rect(int(width/2-textRect.width/2 - 10), int(i*yOffset), textRect.width+20, textRect.height+10))
        screen.blit(text, textRect)

    pygame.display.flip()

def getNumJog(screen, problema : Problema) -> int:
    maxJog = len(problema.inicio)

    numJogadores = 0
    numJogadoresEscolhido = False
    
    listaAvisos = []
    opcoes = [f"Defina um numero de jogadores (max = {maxJog})", str(numJogadores)]

    while not numJogadoresEscolhido:

        for event in pygame.event.get():
                ## Se encontrat um quit sai da janela
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if numJogadores <= 0:
                        listaAvisos.append(Popup("Nº Jogadores Demasiado Baixo (q para apagar mensagem)", screen.get_rect().centerx, screen.get_rect().centery))
                    elif numJogadores > maxJog:
                        listaAvisos.append(Popup("Nº Jogadores Acima do Valor Máximo (q para apagar mensagem)", screen.get_rect().centerx, screen.get_rect().centery))
                    else:
                        numJogadoresEscolhido = True
                if event.key == pygame.K_LEFT:
                    numJogadores -= 1
                    opcoes[1] = str(numJogadores)
                if event.key == pygame.K_RIGHT:
                    numJogadores += 1
                    opcoes[1] = str(numJogadores)
                if event.key == pygame.K_ESCAPE:
                    return        
            for popup in listaAvisos:
                delete = popup.handle_event(event)
                if delete:
                    listaAvisos.remove(popup)
    
        printOpcoes(opcoes, screen, None)
        screen.blit(bg, (0, 0))
        for popup in listaAvisos:
            popup.draw(screen)
        clock.tick(30)

    return numJogadores

def getJogadores(screen, numJogadores):


    competitors = {}

    for i in range(numJogadores):
        algoritmoJogador = None
        opcoes = [f"Escolha o Algoritmo de Procura do Jogador {i}","DFS - Depth First Search", "BFS - Breadth First Search", "A*", "Gulosa"]
        nOpcoes = 4
        selected = 0

        while algoritmoJogador is None:

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
                        if selected == 0:
                            algoritmoJogador = "DFS"
                        elif selected == 1:
                            algoritmoJogador = "BFS"
                        elif selected == 2:
                            algoritmoJogador = "A*"
                        elif selected == 3:
                            algoritmoJogador = "Greedy"
                    if event.key == pygame.K_ESCAPE:
                        return

            printOpcoes(opcoes, screen, selected+1)
            screen.blit(bg, (0, 0))
            clock.tick(30)
        
        competitors[i] = algoritmoJogador

    return competitors

def competitivo(screen, problema : Problema):

    numJogadores = getNumJog(screen, problema)
    
    if numJogadores is None:
        return

    competitors = getJogadores(screen, numJogadores)
    
    if competitors is None:
        return
   
    mensagem = Popup("Resultados vão ser calculados, aguarde..", screen.get_rect().centerx, screen.get_rect().centery)
    mensagem.draw(screen)
    pygame.display.flip()

    d = problema.Competicao(competitors)
    resultList = []
    for k in d.keys():
        resultList.append((f"{k}:{competitors[k]}",d[k][0],d[k][1]))

    Mapa.desenhaMapa(problema.mapa, resultList)

def comecaJogo(screen, ficheiroMapa):

    mapa = Mapa.carregaMapa(diretoriaMapas+"/"+ficheiroMapa)
    problema = Problema(diretoriaMapas+"/"+ficheiroMapa)
    problema.constroiGrafo()

    opcoes = ["DFS - Depth First Search", "BFS - Breadth First Search", "A*", "Gulosa", "Todos (Não Competitivo)", "Competicao", "Ver Mapa", "Voltar"]
    nOpcoes = len(opcoes)

    selected = 0

    while True:
        if screen.get_size() != SIZE:
            pygame.init()
            screen = pygame.display.set_mode(SIZE)
            pygame.transform.scale(screen, SIZE)
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
                        Mapa.desenhaMapa(mapa, [("DFS",path,custo)])
                    elif selected == 1:
                        path, custo = problema.BFS()
                        Mapa.desenhaMapa(mapa, [("BFS",path,custo)])
                    elif selected == 2:
                        path, custo = problema.AStar()
                        Mapa.desenhaMapa(mapa, [("A*",path,custo)])
                    elif selected == 3:
                        path, custo = problema.Greedy()
                        Mapa.desenhaMapa(mapa, [("Gulosa",path,custo)])
                    elif selected == 4:
                        path1, custo1 = problema.DFS()
                        path2, custo2 = problema.BFS()
                        path3, custo3 = problema.AStar()
                        path4, custo4 = problema.Greedy()
                        resultList = []
                        resultList.append(("DFS", path1, custo1))
                        resultList.append(("BFS", path2, custo2))
                        resultList.append(("A*", path3, custo3))
                        resultList.append(("Gulosa", path4, custo4))
                        Mapa.desenhaMapa(mapa, resultList)
                    elif selected == 5:
                        competitivo(screen, problema)
                    elif selected == 6:
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
    numPags = len(mapas) // (mapaPorPag + 1) + 1
    pagAtual = 0

    while True:
        if screen.get_size() != SIZE:
            screen = pygame.display.set_mode(SIZE)
            pygame.transform.scale(screen, SIZE)
        opcoes = mapas[pagAtual*mapaPorPag:pagAtual*mapaPorPag + mapaPorPag]

        while len(opcoes) < mapaPorPag:
            opcoes.append("")
        opcoes.append("Voltar")
        opcoes.append(f"Pagina {pagAtual+1} de {numPags}")

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
                        popup = Popup("A gerar Grafo, por favor aguarde...", screen.get_rect().centerx, screen.get_rect().centery)
                        popup.draw(screen)
                        pygame.display.flip()


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
    screen = pygame.display.set_mode(SIZE)

    pygame.display.set_caption("Vector Race")
    screen.fill((255,200,200))




    selected = 0
    opcoes = {"Selecionar Mapa":selecionarMapa, "Sair":sys.exit}
    opcoesPrint = ["Menu Principal", "Selecionar Mapa", "Sair"]

    while True:
        if screen.get_size() != SIZE:
            screen = pygame.display.set_mode(SIZE)
            pygame.transform.scale(screen, SIZE)
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
                    if selected == 0:
                        selecionarMapa(screen)
                    else:
                        sys.exit()
        
        screen.blit(bg, (0, 0)) 
        printOpcoes(opcoesPrint, screen, selected+1)

        clock.tick(30)


if __name__ == "__main__":
    main()
