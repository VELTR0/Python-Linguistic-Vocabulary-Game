import pygame
import Vocabulary

pygame.init()

# Sprites
selector =            pygame.image.load(r"Sprites\PraiseOrHaze\Selector.png")
correct =         pygame.image.load(r"Sprites\PraiseOrHaze\Correcto.png")
wrong =           pygame.image.load(r"Sprites\PraiseOrHaze\Wrong.png")

def startGame(screen):
    game_running = True
    screen.fill((0, 0, 0))
    while game_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_running = False

        font_size = 

            
        pygame.display.update()