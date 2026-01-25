import pygame
import pygame_menu
pygame.init()


# Settings


def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    pass

# Screen setup
screen = pygame.display.set_mode((1100,500),0,32)
pygame.display.set_caption("Learning Urdu")

# Theme
font = pygame_menu.font.FONT_8BIT
mytheme = pygame_menu.Theme(
                background_color=(0, 0, 0, 0), # transparent background
                title_background_color=(4, 47, 126),
                title_font_shadow=True,
                widget_padding=25,
                widget_font = font
                
                )

# Menu Setup
menu = pygame_menu.Menu('Welcome', 400, 300, theme=mytheme)

menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)



# Main loop
menu.mainloop(screen)









