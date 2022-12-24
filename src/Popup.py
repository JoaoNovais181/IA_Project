import pygame

class Popup():

    def __init__(self, text, x=0, y=0, centerCoords = True):

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

        if centerCoords:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x,y)

    def draw(self, surface):

        surface.blit(self.image, self.rect)

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return True
        return False
