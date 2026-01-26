import pygame
import pygame_menu
import random
import PraiseOrHaze
import QuickieQuiz


pygame.init()

def startGame(current_gamemode, screen, menu, mytheme):
    # pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Game 1")


    pause_menu = pygame_menu.Menu('Pause', 600, 400, theme=mytheme)
    pause_menu.set_relative_position(50, 50)
    
    game_running = True
    paused = False
    InGame = False
    
    def resume_game():
        nonlocal paused
        paused = False
        pause_menu.disable()
    
    def quit_to_menu():
        nonlocal game_running
        nonlocal paused
        game_running = False
        paused = False
        pause_menu.disable()
        menu.enable()
        nonlocal InGame
        InGame = False
        pygame.display.set_mode((1024, 768))
    
    pause_menu.add.button('Continue', resume_game)
    pause_menu.add.button('Back to Main Menu', quit_to_menu)
    pause_menu.add.button('Exit Game', pygame_menu.events.EXIT)
    
    clock = pygame.time.Clock()
    
    while game_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        pause_menu.enable()
        
        if paused:
            pause_menu.enable() 
            pause_menu.mainloop(screen, disable_loop=True)
        else:
            screen.fill((0, 0, 0))
            
            
            # TODO: 
            Games = [PraiseOrHaze]

            
            if InGame == False:
                ChosenGame = random.choice(Games)
                ChosenGame.startGame(screen)
                InGame = True
            else:
                pass
        
        pygame.display.flip()
        clock.tick(60)
    
    return game_running
