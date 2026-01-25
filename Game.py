import pygame
import time
pygame.init()


# Settings
screen = pygame.display.set_mode((1100,500),0,32)
pygame.display.set_caption("Learning Urdu")


# Music
# music = pygame.mixer.music.load("Sounds/Music.mp3")
# pygame.mixer.music.play(-1)


# Bakcground Image
# background_image = pygame.image.load("Graphics/Background/background.png")


def redrawGameWindow():
    pygame.display.update()


clock = pygame.time.Clock()
gameRunning = True 


# Game Loop
while gameRunning:
    clock.tick(60)
    keys = pygame.key.get_pressed()     # Checks pressed keys
    redrawGameWindow()                  # Updates the display every frame   
    #pygame.time.delay(5)                # Adds a small delay to the game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
pygame.quit()









