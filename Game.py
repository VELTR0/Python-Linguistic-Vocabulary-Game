import pygame

pygame.init()

def startGame(current_gamemode,screen):
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Game 1")
    
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
        pygame.display.flip()
