import sys
import pygame


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


def desenhaMapa (Map, path=None, custo=0):
    # print(Map)
    xpix = len(Map[0])
    ypix = len(Map)
    scalex, scaley = 30,30
    ## Tamanho para o texto ##
    # textSize = 10

    ## Iniciar o pygame ##
    pygame.init()

    ## Criar a janela ##
    screen = pygame.display.set_mode((xpix*scalex,(ypix*scaley)))
    ## Definir o nome da janela ##
    pygame.display.set_caption('Vector Race')

    ## Definicao das cores usadas ##

    #  green = (0, 255, 0)
    #  blue = (0, 0, 128)
    red = (255,0,0)
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

    if path is not None:
        radius = scalex * 0.25
        for i in range(len(path)-1):
            node1 = path[i]
            node2 = path[i+1]
            posi = node1.getPos()
            posf = node2.getPos()
            xi = posi[0]*scalex + scalex*0.5
            yi = posi[1]*scaley + scaley*0.5
            xf = posf[0]*scalex + scalex*0.5
            yf = posf[1]*scaley + scaley*0.5
            inicio = pygame.Vector2((xi,yi))
            fim = pygame.Vector2((xf,yf))
            # pygame.draw.line(screen, (0,0,0), (xi,yi), (xf,yf), width = int(scalex*0.1))
            draw_arrow(screen, inicio, fim, (0,0,0), 3, 10, 10)
            pos = node1.getPos()
            x = pos[0]*scalex + scalex*0.5
            y = pos[1]*scaley + scaley*0.5
            pygame.draw.circle(screen, red, (x,y), radius)
            pos = node2.getPos()
            x = pos[0]*scalex + scalex*0.5
            y = pos[1]*scaley + scaley*0.5
            pygame.draw.circle(screen, red, (x,y), radius)
            pygame.display.flip()

            clock.tick(10)


        # for node in path:
        #     pos = node.getPos()
        #     x = pos[0]*scalex + scalex*0.5
        #     y = pos[1]*scaley + scaley*0.5
        #     pygame.draw.circle(screen, red, (x,y), radius)

    ## Objeto colock para definir os frames por segundo ## #noqa: E233

    font = pygame.font.Font('freesansbold.ttf', 20)
    msg = f'Custo do caminho = {custo}'
    text = font.render(msg,True, (0,0,0), (255,200,200))
    textRect = text.get_rect()
    textRect.topleft = [(xpix-1)*scalex-textRect.width,(ypix-1)*scaley]
    screen.blit(text, textRect)

    ## Game loop ##
    while True:

        ## Detetar eventos
        for event in pygame.event.get():
            ## Se encontrat um quit sai da janela
            if event.type == pygame.QUIT:
                sys.exit()

        ## Definir 30 fps
        clock.tick(30)

        ## Desenhar imagem
        pygame.display.flip()

def carregaMapa (filename : str) -> list[list[str]]:
    with open(filename, "r", encoding="UTF-8") as mapFile:
        lines = mapFile.read().split("\n")

        Map = [[c for c in line.strip()] for line in lines]

        return Map

def distanceMap (Map : list[list[str]]) -> list[list[int]] | None:

    maxX, maxY = len(Map[0]), len(Map)
    firstPosX, firstPosY = -1, -1
    for i, li in enumerate(Map):
        for j, val in enumerate(li):
            if val == "F":
                firstPosX = j
                firstPosY = i
                break
    if firstPosX == -1 or firstPosY == -1:
        return None

    distMap : list[list[int]] = [[-1 if c == "#" else 999999999 for c in line] for line in Map]
    queue = []
    queue.append((firstPosX,firstPosY,0))

    while len(queue) > 0:
        x,y,dist = queue.pop(0)
        if Map[y][x] == "#":
            continue

        distMap[y][x] = dist

        if y > 0 and Map[y-1][x] != "F" and distMap[y-1][x] > dist+1:
            queue.append((x, y-1, dist+1))
        if x > 0 and Map[y][x-1] != "F" and distMap[y][x-1] > dist+1:
            queue.append((x-1, y, dist+1))
        if x < maxX-1 and Map[y][x+1] != "F" and distMap[y][x+1] > dist+1:
            queue.append((x+1, y, dist+1))
        if y < maxY-1 and Map[y+1][x] != "F" and distMap[y+1][x] > dist+1:
            queue.append((x,y+1, dist+1))


    return distMap

def main():
    Map = carregaMapa("./mapaFase1.txt")
    for line in distanceMap(Map):
        for val in line:
            print(f'{val:4d}', end='')
        print()

if __name__ == "__main__":
    main()
