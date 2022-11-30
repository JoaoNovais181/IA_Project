from perlin_noise import PerlinNoise
import pygame, sys, os
import random

ridealbleLimit = -0.15
minPlayablePercent = 0.6

def cleanupMap (m):
    notRideable = 0
    totalNodes = 0
    for row in m:
        for col in row:
            if col <= ridealbleLimit:
                notRideable += 1
            totalNodes += 1

    rideable = totalNodes - notRideable
    reachable = 0
    reached = set()
    maxY = len(m)
    maxX = len(m[0])

    while (reachable/rideable) < 0.4:
        firstPosY = random.randint(0, maxY) - 1
        firstPosX = random.randint(0, maxX) - 1
        reached = set()
        queue = []
        queue.append((firstPosX,firstPosY))

        reachable = 0

        while len(queue) > 0:
            x,y = queue.pop(0)
            if m[y][x] <= ridealbleLimit:
                continue
            
            reachable += 1
            reached.add((x,y))

            if y > 0:
                if (x, y-1) not in reached and (x, y-1) not in queue: queue.append((x, y-1))
            if x > 0:
                if (x-1, y) not in reached and (x-1, y) not in queue: queue.append((x-1, y))
            if x < maxX-1:
                if (x+1, y) not in reached and (x+1, y) not in queue: queue.append((x+1, y))
            if y < maxY-1:
                if (x, y+1) not in reached and (x, y+1) not in queue: queue.append((x,y+1))


    ## Preencher como nao dirigiveis todas as zonas que nao tenham sido atingidas
    for y in range(0,maxY):
        for x in range(0, maxX):
            if (x,y) not in reached:
                m[y][x] = ridealbleLimit

def generateMap (seed=1, xpix=100, ypix=100, octaves = 2, multipleNoise = False):

    Map = []

    total = xpix * ypix
    playable = 0

    ## Enquanto o mapa obtido nao tiver o minimo de area dirigivel ##
    while playable/total < minPlayablePercent:

        Map = []
        playable = 0

        ## Se for para gerar com multiplos barulhos
        if multipleNoise:
            noise1 = PerlinNoise(octaves=octaves, seed=seed)
            noise2 = PerlinNoise(octaves=octaves*2, seed=seed)
            noise3 = PerlinNoise(octaves=octaves*3, seed=seed)
            noise4 = PerlinNoise(octaves=octaves*4, seed=seed)
            for i in range(ypix):
                Map.append([])
                for j in range(xpix):
                    Map[i].append(noise1([i/xpix, j/ypix])+0.5*noise2([i/xpix, j/ypix])+0.25*noise3([i/xpix, j/ypix])+0.125*noise4([i/xpix, j/ypix]))
                    if Map[i][j] > ridealbleLimit: playable += 1
        
        else:
            noise = PerlinNoise(octaves=octaves, seed=seed)
            for i in range(ypix):
                Map.append([])
                for j in range(xpix):
                    val = noise([i/xpix, j/ypix])
                    Map[i].append(val)
                    if val > ridealbleLimit: playable += 1

        seed += 1
        print(playable/total)

    ## Limpeza do mapa ##
    cleanupMap(Map)

    print(seed - 1)
    return Map,seed



def main ():
    args = sys.argv[1:]

    seed = 1

    if len(args) == 0:
        seed = os.getpid()
    else:
        try:
            seed = int(args[0])
        except:
            print("Not valid seed value!")
            return -1

    ## Variaveis de geracao para o mapa
    xpix,ypix = 25,20
    octaves = 2
    multipleNoise = True
    ## Obter mapa e seed usada no final ##
    Map,seed = generateMap(seed=seed, xpix=xpix, ypix=ypix, octaves=octaves, multipleNoise=multipleNoise)

    ## Escala para os quadrados do mapa ## 
    scalex, scaley = 30,30
    ## Tamanho para o texto ##
    textSize = 10

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
    font = pygame.font.Font('freesansbold.ttf', 10)
    text = font.render(f'{ypix}x{xpix}, seed={seed}, rideable limit={ridealbleLimit}, octaves={octaves}, multipleNoise={multipleNoise}, min Playable %={minPlayablePercent}',True, blue, green)
    textRect = text.get_rect()
    textRect.topleft = [0,scaley*ypix]
    screen.blit(text, textRect)


    for y in range(0,ypix):
        for x in range(0,xpix):
            ## Desenhar o mapa ##
            pygame.draw.rect(screen, rideableColor if (Map[y][x] > ridealbleLimit) else notRideableColor, pygame.Rect(x*scalex, y*scaley, scalex, scaley))
            ## Desenhar a grelha ##
            pygame.draw.rect(screen, gridColor , pygame.Rect(x*scalex, y*scaley, scalex, scaley),1)

    ## Objeto colock para definir os frames por segundo ##
    clock = pygame.time.Clock()

    with open("mapFile.txt", "w") as file:
        for row in Map:
            for col in row:
                if col <= ridealbleLimit:
                    file.write("#")
                else:
                    file.write("-")
            file.write("\n")

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

   

if __name__ == "__main__":
    main()
