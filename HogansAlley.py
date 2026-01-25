import pygame
import Vocabulary
import random

pygame.init()

DIFFICULTY = "hard"
DISPLAY_TIME = 1000  # ms: prompt display and post-selection delay
WAIT_TIME = 1800  # ms: block input for first 2 seconds of each round

font_options = pygame.font.Font(None, 50)
font_urdu_large = pygame.font.Font(None, 150)

# Sprites
background_image = pygame.image.load(r"Sprites\HogansAlley\Screen.png")
thug1_image =      pygame.image.load(r"Sprites\HogansAlley\Thug1.png")
thug2_image =      pygame.image.load(r"Sprites\HogansAlley\Thug2.png")
thug3_image =      pygame.image.load(r"Sprites\HogansAlley\Thug3.png")
woman_image =      pygame.image.load(r"Sprites\HogansAlley\Woman.png")
policeman_image =  pygame.image.load(r"Sprites\HogansAlley\Policeman.png")
stick_image =      pygame.image.load(r"Sprites\HogansAlley\Stick.png")
unfolding_image =  pygame.image.load(r"Sprites\HogansAlley\Unfolding.png")
hit_image =        pygame.image.load(r"Sprites\HogansAlley\Hit.png")
unfolding_flash_image = pygame.image.load(r"Sprites\HogansAlley\UnfoldingFlash.png")
hit_flash_image =  pygame.image.load(r"Sprites\HogansAlley\HitFlash.png")
crosshair_image =  pygame.image.load(r"Sprites\HogansAlley\Crosshair.png")
wrong_image =      pygame.image.load(r"Sprites\QuickieQuiz\Wrong.png")
barrel_mid_image =       pygame.image.load(r"Sprites\HogansAlley\BarrelMid.png")
barrel_farleft_image =   pygame.image.load(r"Sprites\HogansAlley\BarrelFarLeft.png")
barrel_farright_image =  pygame.image.load(r"Sprites\HogansAlley\BarrelFarRight.png")
monitor_image =    pygame.image.load(r"Sprites\HogansAlley\Monitor.png")

# Sounds
correct_sound = pygame.mixer.Sound(r"Sounds/Correct.ogg")
wrong_sound =   pygame.mixer.Sound(r"Sounds/Wrong.ogg")

def startGame(screen):
    game_running = True
    correct_urdu = ""
    correct_english = ""
    options = []
    correct_index = 0
    selected_index = 0
    show_correct = False
    show_wrong = False
    selection_made = False
    last_action_time = 0
    round_start_time = pygame.time.get_ticks()
    show_urdu_display = True
    current_word_type = "english"
    animation_frame_index = 0
    last_frame_time = 0

    # Scaling of sprites
    background_scaled = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
    character_scale = ((screen.get_height() // 2.75)* 0.6, ((screen.get_height() // 2.75) ))
    #character_height = screen.get_height() // 2.75
    #character_width = int(character_height * 0.6)  # Approx aspect ratio for standing figure
    
    # Pre-scale character sprites
    thug_sprites = [
        pygame.transform.scale(thug1_image, character_scale),
        pygame.transform.scale(thug2_image, character_scale),
        pygame.transform.scale(thug3_image, character_scale)
    ]
    civilian_sprites = [
        pygame.transform.scale(woman_image, character_scale),
        pygame.transform.scale(policeman_image, character_scale)
    ]
    stick_height = screen.get_height() // 2.5
    stick_width = int(stick_height * 0.1)
    stick_scaled = pygame.transform.scale(stick_image, (stick_width, stick_height))
    unfolding_scale = (character_scale[0]* 0.3, int(character_scale[1] ))
    #unfolding_height = character_height
    #unfolding_width = int(unfolding_height * 0.3)
    unfolding_scaled = pygame.transform.scale(unfolding_image, unfolding_scale)
    unfolding_flash_scaled = pygame.transform.scale(unfolding_flash_image, unfolding_scale)

    hit_scaled = pygame.transform.scale(hit_image, character_scale)
    hit_flash_scaled = pygame.transform.scale(hit_flash_image, character_scale)
    
    # Animation sequence: Hit, Unfolding, None, UnfoldingFlash, HitFlash, UnfoldingFlash, None, Unfolding, Hit...
    animation_frames = [hit_scaled, unfolding_scaled, None, unfolding_flash_scaled, hit_flash_scaled, unfolding_flash_scaled, None, unfolding_scaled, hit_scaled]
    frame_duration = 150  # ms per frame
    
    crosshair_scaled = pygame.transform.scale(crosshair_image, (character_scale[0], character_scale[0]))
    wrong_scaled = pygame.transform.scale(wrong_image, character_scale)
    barrel_height = screen.get_height() // 3
    barrel_width = int(barrel_height * 1.0)
    barrel_mid_scaled = pygame.transform.scale(barrel_mid_image, (barrel_width, barrel_height))
    barrel_farleft_scaled = pygame.transform.scale(barrel_farleft_image, (barrel_width, barrel_height))
    barrel_farright_scaled = pygame.transform.scale(barrel_farright_image, (barrel_width, barrel_height))
    monitor_scaled = pygame.transform.scale(monitor_image, (screen.get_width(), screen.get_height()))

    # Start first round
    correct_urdu, correct_english, options, correct_index, current_word_type = pickRandomWords()
    character_sprites = assignCharacterSprites(correct_index, len(options), thug_sprites, civilian_sprites)

    while game_running:
        current_time = pygame.time.get_ticks()
        if show_urdu_display and current_time - round_start_time >= WAIT_TIME:
            show_urdu_display = False

        # Update animation frame if selection is made
        if selection_made and current_time - last_frame_time >= frame_duration:
            animation_frame_index = (animation_frame_index + 1) % len(animation_frames)
            last_frame_time = current_time
        
        if selection_made and current_time - last_action_time >= WAIT_TIME:
            correct_urdu, correct_english, options, correct_index, current_word_type = pickRandomWords()
            character_sprites = assignCharacterSprites(correct_index, len(options), thug_sprites, civilian_sprites)
            show_correct = False
            show_wrong = False
            selection_made = False
            selected_index = 0
            round_start_time = current_time
            show_urdu_display = True
            animation_frame_index = 0

        # Render background
        screen.blit(background_scaled, (0, 0))

        # Compute horizontal positions
        n = len(options)
        if n == 0:
            pygame.display.update()
            continue
        spacing = screen.get_width() // (n + 1)
        y = screen.get_height() // 2
        centers = [(spacing * (i + 1), y) for i in range(n)]

        # Render option characters and texts, or animated sticks during first second
        if show_urdu_display:
            # Animate sticks sliding in from the left
            elapsed_time = current_time - round_start_time
            progress = min(1.0, elapsed_time / DISPLAY_TIME)  # Clamp to [0, 1]
            
            # Calculate animation: all sticks start with equal spacing and slide at same speed
            for i, word in enumerate(options):
                cx_final = centers[i][0]
                # Initial x positions: sticks start to the left with proper spacing
                x_init = -character_scale[0] - spacing * (n - 1 - i)
                # Interpolate current position
                x_current = x_init + (cx_final - x_init) * progress
                
                stick_rect = stick_scaled.get_rect(center=(x_current, y))
                screen.blit(stick_scaled, stick_rect)
                
                # Show unfolding sprite during last 30% of animation (from 70% progress onwards)
                if elapsed_time / WAIT_TIME >= 0.9:
                    unfolding_rect = unfolding_scaled.get_rect(center=(cx_final, y-20))
                    screen.blit(unfolding_scaled, unfolding_rect)
        else:
            # Keep sticks rendered underneath characters
            for i in range(n):
                cx, cy = centers[i]
                stick_rect = stick_scaled.get_rect(center=(cx, y))
                screen.blit(stick_scaled, stick_rect)

            # Render characters and words on top after the stick animation
            for i, word in enumerate(options):
                cx, cy = centers[i]
                
                # If selection is made and this is the selected word, show animation instead of character
                if selection_made and i == selected_index:
                    current_animation_frame = animation_frames[animation_frame_index]
                    if current_animation_frame is not None:
                        anim_rect = current_animation_frame.get_rect(center=(cx, cy-20))
                        screen.blit(current_animation_frame, anim_rect)
                else:
                    # Normal rendering: character and text
                    char_rect = character_sprites[i].get_rect(center=(cx, cy-20))
                    screen.blit(character_sprites[i], char_rect)
                    text_surface = font_options.render(word, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(cx, cy))
                    screen.blit(text_surface, text_rect)

                # Selection indicator
                if i == selected_index:
                    crosshair_rect = crosshair_scaled.get_rect(center=(cx, cy))
                    screen.blit(crosshair_scaled, crosshair_rect)

                # Show wrong overlay after confirmation
                if show_wrong and i != correct_index:
                    screen.blit(wrong_scaled, char_rect)

                # Show correct overlay after confirmation
                if show_correct and i == correct_index:
                    crosshair_rect = crosshair_scaled.get_rect(center=(cx, cy))
                    screen.blit(crosshair_scaled, crosshair_rect)

        # Prompt word at top for a moment
        if show_urdu_display:
            display_word = correct_urdu if current_word_type == "english" else correct_english
            prompt_surface = font_urdu_large.render(f"Translate: {display_word}", True, (0, 0, 0))
            prompt_rect = prompt_surface.get_rect(center=(screen.get_width()//2, screen.get_height()//4))
            screen.blit(prompt_surface, prompt_rect)

        # Render monitor overlay over everything except the barrel
        screen.blit(monitor_scaled, (0, 0))

        # Render barrel at bottom center over everything (only when not showing prompt)
        if not show_urdu_display:
            # Determine which barrel to show based on selected_index
            if selected_index == 0:
                barrel = barrel_farleft_scaled
            elif selected_index == n - 1:
                barrel = barrel_farright_scaled
            else:
                barrel = barrel_mid_scaled
            
            barrel_rect = barrel.get_rect(midbottom=(screen.get_width() // 2, screen.get_height()))
            screen.blit(barrel, barrel_rect)

        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN and not selection_made and (current_time - round_start_time) >= WAIT_TIME:
                if event.key == pygame.K_LEFT:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_RIGHT:
                    selected_index = min(n - 1, selected_index + 1)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    show_correct, show_wrong = checkAnswer(selected_index, correct_index)
                    selection_made = True
                    last_action_time = current_time
                    animation_frame_index = 0
                    last_frame_time = current_time

        pygame.display.update()


def assignCharacterSprites(correct_index, num_options, thug_sprites, civilian_sprites):
    """Assign random character sprites to each option.
    Correct answer gets a random Thug, wrong answers get random Civilians."""
    sprites = []
    used_civilian_idx = -1
    
    for i in range(num_options):
        if i == correct_index:
            # Correct answer: random Thug
            sprites.append(random.choice(thug_sprites))
        else:
            # Wrong answer: alternate between Woman and Policeman
            used_civilian_idx = (used_civilian_idx + 1) % len(civilian_sprites)
            sprites.append(civilian_sprites[used_civilian_idx])
    
    return sprites


# This function starts a new round
def pickRandomWords():
    wordpair = random.choice(list(Vocabulary.lightVerbs.items()))
    correct_urdu = wordpair[0]
    correct_english = wordpair[1]

    # Difficulty settings: number of options
    num_options = 2 if DIFFICULTY == "easy" else 4

    # Randomly choose language type
    word_type = random.choice(["english", "urdu"])
    if word_type == "english":
        pool = list(Vocabulary.lightVerbs.values())
        pool.remove(correct_english)
        correct_word = correct_english
    else:
        pool = list(Vocabulary.lightVerbs.keys())
        pool.remove(correct_urdu)
        correct_word = correct_urdu

    # Build options list
    false_options = random.sample(pool, num_options - 1)
    options = [correct_word] + false_options
    random.shuffle(options)
    correct_index = options.index(correct_word)

    return correct_urdu, correct_english, options, correct_index, word_type


def checkAnswer(selected_index, correct_index):
    if selected_index == correct_index:
        corectAnswerSelected()
        return True, False
    else:
        wrongAnswerSelected()
        return False, True


def corectAnswerSelected():
    correct_sound.play()


def wrongAnswerSelected():
    wrong_sound.play()