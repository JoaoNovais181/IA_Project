import pygame
import sys
from Node import Node


def draw_arrow(surface: pygame.Surface,start: pygame.Vector2,end: pygame.Vector2,color: pygame.Color,body_width: int = 2,head_width: int = 4,head_height: int = 2,):
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pygame.Surface): The surface to draw on
        start (pygame.Vector2): Start position
        end (pygame.Vector2): End position
        color (pygame.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
    arrow = start - end
    angle = arrow.angle_to(pygame.Vector2(0, -1))
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pygame.Vector2(0, head_height / 2),  # Center
        pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pygame.draw.polygon(surface, color, head_verts)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pygame.Vector2(body_width / 2, body_length / 2),  # Topright
            pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        pygame.draw.polygon(surface, color, body_verts)


def desenhaMapa (Map, path=None):
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

    green = (0, 255, 0)
    blue = (0, 0, 128)
    red = (255,0,0)
    rideableColor = 190, 190,210
    notRideableColor = 120, 120, 150
    gridColor = 150,150,255


    ## Texto com as informações acerca do mapa ##
    # font = pygame.font.Font('freesansbold.ttf', 10)
    # text = font.render(f'{ypix}x{xpix}, seed={seed}, rideable limit={ridealbleLimit}, octaves={octaves}, multipleNoise={multipleNoise}, min Playable %={minPlayablePercent}',True, blue, green)
    # textRect = text.get_rect()
    # textRect.topleft = [0,scaley*ypix]
    # screen.blit(text, textRect)

    for y in range(0, ypix):
        for x in range(0, xpix):
            # Desenhar o mapa ##
            # print(xpix, ypix, x, y)
            # pygame.draw.rect(screen, rideableColor if (Map[y][x] > ridealbleLimit) else notRideableColor, pygame.Rect(x*scalex, y*scaley, scalex, scaley))  # noqa: E501
            pygame.draw.rect(screen, rideableColor if (Map[y][x]==" ") else notRideableColor, pygame.Rect(x*scalex, y*scaley, scalex, scaley))  # noqa: E501
            # Desenhar a grelha ##
            pygame.draw.rect(screen, gridColor , pygame.Rect(x*scalex, y*scaley, scalex, scaley),1)  # noqa: E203, E501 E231

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

        for node in path:
            pos = node.getPos()
            x = pos[0]*scalex + scalex*0.5
            y = pos[1]*scaley + scaley*0.5
            pygame.draw.circle(screen, red, (x,y), radius)

    ## Objeto colock para definir os frames por segundo ## #noqa: E233
    clock = pygame.time.Clock()

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

def carregaMapa (filename):
    with open(filename, "r") as mapFile:
        lines = mapFile.read().split("\n")

        Map = [[c if c not in "PFS" else " " for c in line] for line in lines]

        return Map 

if __name__ == "__main__":
    Map = carregaMapa("./mapaFase1.txt")
    desenhaMapa(Map)