import pygame
import sys


def desenhaMapa (Map):
    print(Map)
    xpix = len(Map[0])
    ypix = len(Map)
    scalex, scaley = 30,30
    ## Tamanho para o texto ##
    # textSize = 10

    ## Iniciar o pygame ##
    pygame.init()

    ## Criar a janela ##
    screen = pygame.display.set_mode((xpix*scalex,(ypix*scaley)+textSize))
    ## Definir o nome da janela ##
    pygame.display.set_caption('Vector Race')

    ## Definicao das cores usadas ##

    green = (0, 255, 0)
    blue = (0, 0, 128)
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
            print(xpix, ypix, x, y)
            # pygame.draw.rect(screen, rideableColor if (Map[y][x] > ridealbleLimit) else notRideableColor, pygame.Rect(x*scalex, y*scaley, scalex, scaley))  # noqa: E501
            pygame.draw.rect(screen, rideableColor if (Map[y][x]==" ") else notRideableColor, pygame.Rect(x*scalex, y*scaley, scalex, scaley))  # noqa: E501
            # Desenhar a grelha ##
            pygame.draw.rect(screen, gridColor , pygame.Rect(x*scalex, y*scaley, scalex, scaley),1)  # noqa: E203, E501 E231

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