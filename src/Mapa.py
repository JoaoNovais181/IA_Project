import sys, os
import pygame
from Node import Node
from Popup import Popup

COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255), (255,255,255)]



def draw_arrow(surface: pygame.Surface,start: pygame.Vector2,end: pygame.Vector2,color: pygame.Color,bodyWidth: int = 2,headWidth: int = 4,headHeight: int = 2,):
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pygame.Surface): The surface to draw on
        start (pygame.Vector2): Start position
        end (pygame.Vector2): End position
        color (pygame.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        headWidth (int, optional): Defaults to 4.
        headHeight (float, optional): Defaults to 2.
    """
    arrow = start - end
    angle = arrow.angle_to(pygame.Vector2(0, -1))
    bodyLength = arrow.length() - headHeight

    # Create the triangle head around the origin
    headVerts = [
        pygame.Vector2(0, headHeight / 2),  # Center
        pygame.Vector2(headWidth / 2, -headHeight / 2),  # Bottomright
        pygame.Vector2(-headWidth / 2, -headHeight / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pygame.Vector2(0, arrow.length() - (headHeight / 2)).rotate(-angle)
    for headVert in headVerts:
        headVert.rotate_ip(-angle)
        headVert += translation
        headVert += start

    pygame.draw.polygon(surface, color, headVerts)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= headHeight:
        # Calculate the body rect, rotate and translate into place
        bodyVerts = [
            pygame.Vector2(-bodyWidth / 2, bodyLength / 2),  # Topleft
            pygame.Vector2(bodyWidth / 2, bodyLength / 2),  # Topright
            pygame.Vector2(bodyWidth / 2, -bodyLength / 2),  # Bottomright
            pygame.Vector2(-bodyWidth / 2, -bodyLength / 2),  # Bottomleft
        ]
        translation = pygame.Vector2(0, bodyLength / 2).rotate(-angle)
        for bodyVert in bodyVerts:
            bodyVert.rotate_ip(-angle)
            bodyVert += translation
            bodyVert += start

        pygame.draw.polygon(surface, color, bodyVerts)



def desenhaMapa (Map, resultList : list[tuple[str, list[Node],int]] | None = None, immediate : bool = False):
    def drawNodePath (node1 : Node, node2 : Node, color, diff=0):
        posi = node1.getPos()
        posf = node2.getPos()
        xi = posi[0]*scalex + scalex*0.5
        yi = posi[1]*scaley + scaley*0.5
        xf = posf[0]*scalex + scalex*0.5
        yf = posf[1]*scaley + scaley*0.5
        inicio = pygame.Vector2((xi,yi))
        fim = pygame.Vector2((xf,yf))
        draw_arrow(screen, inicio, fim, color, 3+diff, 10+diff, 10+diff)
        pos = node1.getPos()
        x = pos[0]*scalex + scalex*0.5
        y = pos[1]*scaley + scaley*0.5
        pygame.draw.circle(screen, color, (x,y), radius+diff)
        pos = node2.getPos()
        x = pos[0]*scalex + scalex*0.5
        y = pos[1]*scaley + scaley*0.5
        pygame.draw.circle(screen, color, (x,y), radius+diff)
        pygame.display.flip()


    xpix = len(Map[0])
    ypix = len(Map)
    scalex, scaley = 30,30
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    ## Iniciar o pygame ##
    pygame.init()

    monitorSize = pygame.display.get_desktop_sizes()[0]
    desiredSize = xpix*scalex + (0 if resultList is None else 200),ypix*scaley

    if monitorSize[0]-40 < desiredSize[0]:
        scalex = (monitorSize[0]-40-(0 if resultList is None else 200)) // xpix
        desiredSize = xpix*scalex+(0 if resultList is None else 200),desiredSize[1]
    if monitorSize[1]-40 < desiredSize[1]:
        scaley = (monitorSize[1]-40) // ypix
        desiredSize = desiredSize[0],ypix*scaley

    ## Criar a janela ##
    screen = pygame.display.set_mode(desiredSize)
    screen.fill((50,50,50))
    ## Definir o nome da janela ##
    pygame.display.set_caption('Vector Race')

    ## Definicao das cores usadas ##

    rideableColor = 190, 190,210
    notRideableColor = 120, 120, 150
    startColor = 170, 255, 170
    endColor = 255,170,170
    gridColor = 150,150,255


    for y in range(0, ypix):
        for x in range(0, xpix):
            color = rideableColor
            if Map[y][x] == "#":
                color = notRideableColor
            elif Map[y][x] == "I":
                color = startColor
            elif Map[y][x] == "F":
                color = endColor
            pygame.draw.rect(screen, color, pygame.Rect(x*scalex, y*scaley, scalex, scaley))
            # Desenhar a grelha #
            pygame.draw.rect(screen, gridColor , pygame.Rect(x*scalex, y*scaley, scalex, scaley),1)

    clock = pygame.time.Clock()


    if resultList is not None:
        resultList.sort(key=(lambda t : t[2]))
        paths = list(map(lambda p: p[1], resultList))
        nPaths = len(paths)

        radius = scalex * 0.25

        if not immediate:
            biggest = max(list(map(len, paths)))
            for i in range(biggest - 1):
                for j, path in enumerate(paths):
                    if i < len(path) - 1:
                        node1 = path[i]
                        node2 = path[i+1]
                        drawNodePath(node1,node2, COLORS[j], (nPaths-j))
                clock.tick(5)
        else:
            for i, path in enumerate(paths):
                for j in range(len(path)-1):
                    node1 = path[j]
                    node2 = path[j+1]
                    drawNodePath(node1, node2, COLORS[i], nPaths-i)

        height = 40
        fontSize = 20
        if len(resultList) > 1 and height*len(resultList) > ypix*scaley:
            height = ypix-scaley//len(resultList)
            fontSize = height/2


        for i,(name, _, cost) in enumerate(resultList):
            font = pygame.font.Font('freesansbold.ttf', fontSize)
            text = font.render(f'{name}, custo={cost}', True, (0,0,0), COLORS[i])
            textRect = text.get_rect()
            bgRect = pygame.Rect((xpix*scalex,i*height), (200,height))
            textRect.center = bgRect.center
            pygame.draw.rect(screen, COLORS[i], bgRect)
            screen.blit(text, textRect)

    voltarMensagem = Popup("Pressione ESC para voltar", 10, 10, False)
    ## Game loop ##
    while True:

        ## Detetar eventos
        for event in pygame.event.get():
                ## Se encontrat um quit sai da janela
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        ## Definir 30 fps
        clock.tick(30)

        ## Desenhar imagem
        voltarMensagem.draw(screen)
        pygame.display.flip()

def carregaMapa (filename : str) -> list[list[str]]:
    with open(filename, "r", encoding="UTF-8") as mapFile:
        lines = mapFile.read().split("\n")
        lines = list(filter(lambda x : len(x)>0, lines))

        Map = [[c for c in line.strip()] for line in lines]

        return Map

def distanceMap (Map : list[list[str]]) -> list[list[int]] | None:


    maxX, maxY = len(Map[0]), len(Map)
    firstPos = []
    for i, li in enumerate(Map):
        for j, val in enumerate(li):
            if val == "F":
                firstPos.append((j,i,0))
    if not len(firstPos) > 0:
        return None

    distMap : list[list[int]] = [[-1 if c == "#" else 999999999 for c in line] for line in Map]
    queue = []
    queue.extend(firstPos)

    while len(queue) > 0:
        x,y,dist = queue.pop(0)
        if Map[y][x] == "#":
            continue

        distMap[y][x] = dist

        if y > 0 and Map[y-1][x] == "F" and distMap[y-1][x] != 0 and (x,y-1,0) not in queue:
            queue.append((x, y-1, 0))
        elif y > 0 and distMap[y-1][x] > dist+1 and (x,y-1,dist+1) not in queue:
            queue.append((x, y-1, dist+1))
        if x > 0 and Map[y][x-1] == "F" and distMap[y][x-1] != 0 and (x-1, y, 0) not in queue:
            queue.append((x-1, y, 0))
        elif y < maxY-1 and distMap[y][x-1] > dist+1 and (x-1,y,dist+1) not in queue:
            queue.append((x-1, y, dist+1))
        if x < maxX-1 and Map[y][x+1] == "F" and distMap[y][x+1] != 0 and (x+1, y, 0) not in queue:
            queue.append((x+1, y, 0))
        elif x < maxX-1 and distMap[y][x+1] > dist+1 and (x+1, y, dist+1) not in queue:
            queue.append((x+1, y, dist+1))
        if y < maxY-1 and Map[y+1][x] == "F" and distMap[y+1][x] != 0 and (x, y+1, 0) not in queue:
            queue.append((x,y+1, 0))
        elif y < maxY-1 and distMap[y+1][x] > dist+1 and (x, y+1, dist+1) not in queue:
            queue.append((x,y+1, dist+1))

    return distMap
