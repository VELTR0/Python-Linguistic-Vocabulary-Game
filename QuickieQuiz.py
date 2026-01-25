import pygame
import Vocabulary
import random

pygame.init()

DIFFICULTY = "hard" 
WORD_TYPE = "english"
DISPLAY_TIME = 1000

font_options = pygame.font.Font(None, 50)
font_urdu_large = pygame.font.Font(None, 150)

# Sprites
background_image =      pygame.image.load(r"Sprites\QuickieQuiz\Background.png")
dpad_image =            pygame.image.load(r"Sprites\QuickieQuiz\D-Pad.png")
up_image =              pygame.image.load(r"Sprites\QuickieQuiz\Up.png")
down_image =            pygame.image.load(r"Sprites\QuickieQuiz\Down.png")
left_image =            pygame.image.load(r"Sprites\QuickieQuiz\Left.png")
right_image =           pygame.image.load(r"Sprites\QuickieQuiz\Right.png")
card_image =            pygame.image.load(r"Sprites\QuickieQuiz\Card.png")
correct_image =         pygame.image.load(r"Sprites\QuickieQuiz\Correct.png")
wrong_image =           pygame.image.load(r"Sprites\QuickieQuiz\Wrong.png")

# Sounds
correct_sound =     pygame.mixer.Sound(r"Sounds/Correct.ogg")
wrong_sound =       pygame.mixer.Sound(r"Sounds/Wrong.ogg")

def startGame(screen):
    game_running = True
    correct_urdu = ""
    correct_english = ""
    correct_position = ""
    options = {}
    show_correct = False
    show_wrong = False
    selection_made = False
    correct_display_position = None
    last_action_time = 0
    selected_direction = None
    round_start_time = pygame.time.get_ticks()
    show_urdu_display = True
    current_word_type = "english"
    
    # Scaling of all sprites
    background_scaled = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
    
    dpad_size = screen.get_height() // 6
    dpad_scaled = pygame.transform.scale(dpad_image, (dpad_size, dpad_size))
    
    direction_sprites = {
        "top": pygame.transform.scale(up_image, (dpad_size, dpad_size)),
        "bottom": pygame.transform.scale(down_image, (dpad_size, dpad_size)),
        "left": pygame.transform.scale(left_image, (dpad_size, dpad_size)),
        "right": pygame.transform.scale(right_image, (dpad_size, dpad_size))
    }
    
    card_height = screen.get_height() // 5
    card_width = int(card_height * card_image.get_width() / card_image.get_height())
    card_scaled = pygame.transform.scale(card_image, (card_width, card_height))
    correct_scaled = pygame.transform.scale(correct_image, (card_width, card_height))
    wrong_scaled = pygame.transform.scale(wrong_image, (card_width, card_height))
    
    # Positions
    position_coords = {
        "top": (screen.get_width()//2, 100),
        "bottom": (screen.get_width()//2, screen.get_height()-100),
        "left": (100, screen.get_height()//2),
        "right": (screen.get_width()-100, screen.get_height()//2)
    }
    
    # Start first round
    correct_urdu, correct_english, correct_position, options, current_word_type = pickRandomWords()
    
    while game_running:
        # Timer logic
        current_time = pygame.time.get_ticks()
        if show_urdu_display and current_time - round_start_time >= DISPLAY_TIME:
            show_urdu_display = False
        
        if selection_made and current_time - last_action_time >= DISPLAY_TIME:
            correct_urdu, correct_english, correct_position, options, current_word_type = pickRandomWords()
            show_correct = False
            show_wrong = False
            selection_made = False
            selected_direction = None
            round_start_time = current_time
            show_urdu_display = True
        
        # Rendering
        screen.blit(background_scaled, (0, 0))
        
        # Center sprite
        dpad_center = (screen.get_width()//2, screen.get_height()//2)
        if selected_direction:
            screen.blit(direction_sprites[selected_direction], direction_sprites[selected_direction].get_rect(center=dpad_center))
        else:
            screen.blit(dpad_scaled, dpad_scaled.get_rect(center=dpad_center))
        
        # Render option cards
        for position, word in options.items():
            x, y = position_coords[position]
            
            # Card
            card_rect = card_scaled.get_rect(center=(x, y))
            screen.blit(card_scaled, card_rect)
            
            # Text
            text_surface = font_options.render(word, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x, y))
            screen.blit(text_surface, text_rect)
            
            # Correct sprite
            if show_correct and correct_display_position == position:
                screen.blit(correct_scaled, card_rect)
            
            # Wrong sprite
            if show_wrong and correct_position != position:
                screen.blit(wrong_scaled, card_rect)
        
        # Correct Word Display
        if show_urdu_display:
            display_word = correct_urdu if current_word_type == "english" else correct_english
            text = f" {display_word}" # Add String here to display 
            large_surface = font_urdu_large.render(text, True, (0, 0, 0))
            large_rect = large_surface.get_rect(center=(dpad_center[0], dpad_center[1] - 120))
            screen.blit(large_surface, large_rect)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN and not selection_made:
                key_to_position = {pygame.K_UP: "top", pygame.K_DOWN: "bottom", pygame.K_LEFT: "left", pygame.K_RIGHT: "right"}
                pressed_position = key_to_position.get(event.key)
                
                if pressed_position and pressed_position in options:
                    show_correct, correct_display_position, show_wrong = checkAnswer(pressed_position, correct_position)
                    selected_direction = pressed_position
                    selection_made = True
                    last_action_time = current_time
        
        pygame.display.update()


# This function starts a new round
def pickRandomWords():
    wordpair = random.choice(list(Vocabulary.lightVerbs.items()))
    correct_urdu = wordpair[0]
    correct_english = wordpair[1]
    
    # Difficulty settings
    if DIFFICULTY == "easy":
        available_positions = ["top", "bottom"]
        num_false_options = 1
    else:
        available_positions = ["top", "bottom", "left", "right"]
        num_false_options = 3
    
    # English or Urdu
    word_type = random.choice(["english", "urdu"])
    if word_type == "english":
        false_options_list = list(Vocabulary.lightVerbs.values())
        false_options_list.remove(correct_english)
        false_options = random.sample(false_options_list, num_false_options)
        correct_word = correct_english
    else: 
        false_options_list = list(Vocabulary.lightVerbs.keys())
        false_options_list.remove(correct_urdu)
        false_options = random.sample(false_options_list, num_false_options)
        correct_word = correct_urdu
    
    # Placing of the words 
    correct_position = random.choice(available_positions)
    options = {}
    all_options = [correct_word] + false_options
    random.shuffle(all_options)
    for i, position in enumerate(available_positions):
        if position == correct_position:
            options[position] = correct_word
        else:
            false_option = next(opt for opt in all_options if opt != correct_word and opt not in options.values())
            options[position] = false_option

    return correct_urdu, correct_english, correct_position, options, word_type


def checkAnswer(pressed_position, correct_position):
    if pressed_position == correct_position:
        show_correct, correct_display_position = corectAnswerSelected(pressed_position)
        return show_correct, correct_display_position, False
    else:
        show_wrong = wrongAnswerSelected()
        return False, None, show_wrong


def corectAnswerSelected(position):
    correct_sound.play()
    return True, position


def wrongAnswerSelected():
    wrong_sound.play()
    return True