import pygame
import pygame_menu
from Game import startGame

pygame.init()


current_gamemode = 1
# starting score
total_score = 10000
def set_gamemode(value, gamemode):
    global current_gamemode
    current_gamemode = gamemode
    

def start_the_game():
    global total_score
    player_name = name.get_value()
    menu.disable()
    player_name = "Player" if player_name == '' else player_name
    # startGame now returns the total total score
    returned = startGame(current_gamemode, screen, menu, mytheme, player_name, total_score)
    if isinstance(returned, int):
        total_score = returned

    menu.enable()

# Screen setup
screen = pygame.display.set_mode((1024, 768),0,32)
pygame.display.set_caption("Learning Urdu")

# Theme
mytheme = pygame_menu.themes.THEME_BLUE.copy()
mytheme.widget_font = r"Sprites\Menu\WW.ttf"
mytheme.widget_font_size = 28
mytheme.background_color = (255, 255, 255)
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
pygame_menu.widgets.Button.get_allignment = lambda self: pygame_menu.locals.ALIGN_CENTER


menu = pygame_menu.Menu('', 1024, 768, theme=mytheme)
menu.add.image(r"Sprites\Menu\Menu.png", scale=(0.75, 0.75))



score_label = menu.add.label(f'Score: {total_score}')
menu.score_label = score_label
name = menu.add.text_input('PLEASE ENTER NAME :', default='')

def start_mode(mode):
    global total_score
    if mode == 2 and total_score < 1000:
        return
    if mode == 3 and total_score < 2000:
        return

    player_name = name.get_value()
    menu.disable()
    player_name = "Player" if player_name == '' else player_name
    returned = startGame(mode, screen, menu, mytheme, player_name, total_score)   
    if isinstance(returned, int):
        total_score = returned
    menu.enable()

vocab_btn = menu.add.button('Vocabulary', lambda m=1: start_mode(m))
grammer_btn = menu.add.button('Grammar', lambda m=2: start_mode(m))
test_btn = menu.add.button('Test', lambda m=3: start_mode(m))
if total_score < 1000:
    grammer_btn.set_title('Grammer (1000 points to unlock)')
if total_score < 2000:
    test_btn.set_title('Test (2000 points to unlock)')

menu.add.button('Quit', pygame_menu.events.EXIT)



# Main loop
menu.mainloop(screen)