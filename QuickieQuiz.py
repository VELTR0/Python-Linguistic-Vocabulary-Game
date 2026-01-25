import pygame

pygame.init()

def startGame(screen):
    game_running = True
    screen.fill((0, 0, 128))
    print("2") 
    while game_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_running = False
    pygame.display.update()
    pass