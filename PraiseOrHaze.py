import pygame
import Vocabulary
from Font import SpriteFont

pygame.init()

# Sprites (werden später geladen)
selector = None
correct = None
wrong = None

def load_sprites():
    global selector, correct, wrong
    selector = pygame.image.load(r"Sprites\PraiseOrHaze\Selector.png").convert_alpha()
    correct = pygame.image.load(r"Sprites\PraiseOrHaze\Correcto.png").convert_alpha()
    wrong = pygame.image.load(r"Sprites\PraiseOrHaze\Wrong.png").convert_alpha()

def startGame(screen):
    load_sprites()
    game_running = True
    screen.fill((255, 255, 255))
    while game_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_running = False

        font = SpriteFont()

        question = font.render("Hello, du alter schuh, was denkst du kommt als nächste? das nächste wort ich penis!?=", color=((255, 255, 255), (0, 255, 0)))
        question = pygame.transform.scale_by(question, 2)

        text_pos = question.get_rect(center=(640, 360))
        screen.blit(question, text_pos)

            
        pygame.display.update()