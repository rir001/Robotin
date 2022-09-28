from parametros import *
from pygame.locals import Rect

class Robotin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pestaneo = 0
        self.contador = 0
    
    def update(self):
        self.contador += 1
        self.pestanear()
    
    def draw(self, screen):
        # Get mouse position
        punto = pygame.mouse.get_pos()
        x = (SCREEN_WIDTH - punto[0])/80
        y = (SCREEN_HEIGHT - punto[1])/80


        pygame.draw.ellipse(screen, (0, 0, 0),
                            Rect(SCREEN_WIDTH/2 - PASO_W*3 - x*3, SCREEN_HEIGHT/2 - PASO_H*2 + self.pestaneo - y*3,
                            OJO_ANCHO, OJO_ALTO - self.pestaneo*2))

        pygame.draw.ellipse(screen, (0, 0, 0),
                            Rect(SCREEN_WIDTH/2 + PASO_W*3 - OJO_ANCHO - x*3, SCREEN_HEIGHT/2 - PASO_H*2 + self.pestaneo - y*3,
                            OJO_ANCHO, OJO_ALTO - self.pestaneo*2))

        pygame.draw.ellipse(screen, (0, 0, 0),
                            Rect(SCREEN_WIDTH/2-90 - x, SCREEN_HEIGHT/2 - y,
                            180, 100))

        pygame.draw.ellipse(screen, COLOR_CARA,
                            Rect(SCREEN_WIDTH/2-70 - x, SCREEN_HEIGHT/2 - y,
                            140, 80))

        pygame.draw.rect(screen, COLOR_CARA,
                            Rect(SCREEN_WIDTH/2-90 - x, SCREEN_HEIGHT/2 - y,
                            180, 50))

        pygame.draw.ellipse(screen, (0, 0, 0),
                            Rect(SCREEN_WIDTH/2-90 - x, SCREEN_HEIGHT/2+40 - y,
                            22, 20))

        pygame.draw.ellipse(screen, (0, 0, 0),
                            Rect(SCREEN_WIDTH/2+90-22 - x, SCREEN_HEIGHT/2+40 - y,
                            22, 20))
    

    
    def pestanear(self):
        if self.contador > 1000:
            if self.contador < 1000 + 60:
                if self.contador % 5 == 0:
                    self.pestaneo += OJO_STEP
            elif self.contador < 1000 + 120:
                if self.contador % 5 == 0:
                    self.pestaneo -= OJO_STEP
        if self.contador > 1000 + 120:
            self.pestaneo = 0
            self.contador = 0
    
