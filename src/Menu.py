import pygame, sys

mapas = ["mapaFase1.txt", "mapaTeste.txt"]
size = width, height = 700,700

def printOpcoes(options, screen, selected=0):

    yOffset = height/(len(options)+1)
    font = pygame.font.Font('freesansbold.ttf', 20)

    for i in range(1, len(options)+1):
        text = font.render(options[i-1], True, (0,0,0))
        textRect = text.get_rect()
        textRect.topleft = [int(width/2-textRect.width/2),int(i*yOffset+5)]
        
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(int(width/2-textRect.width/2 - 13), int(i*yOffset-3), textRect.width+26, textRect.height+16))
        pygame.draw.rect(screen, (255,0,0) if selected==i-1 else (255,150,150), pygame.Rect(int(width/2-textRect.width/2 - 10), int(i*yOffset), textRect.width+20, textRect.height+10))
        screen.blit(text, textRect)

    pygame.display.flip()



def main():
    pygame.init()
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Vector Race")
    screen.fill((255,200,200))

    clock = pygame.time.Clock()

    selected = 0
    opcoes = ["Selecionar Mapa", "Cona", "Sair"]

    while True:
        for event in pygame.event.get():
                ## Se encontrat um quit sai da janela
            if event.type == pygame.QUIT:
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                    selected = (selected+1)%len(opcoes)
            if pygame.key.get_pressed()[pygame.K_UP]:
                    selected = (selected-1 + len(opcoes))%len(opcoes)


        print(selected)
        printOpcoes(opcoes, screen, selected)
        clock.tick(30)


if __name__ == "__main__":
    main()