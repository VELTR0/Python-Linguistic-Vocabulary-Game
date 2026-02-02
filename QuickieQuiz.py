import pygame
import Vocabulary
import random
from Game import Game
from Font import SpriteFont

pygame.init()


class QuickieQuiz(Game):
    DISPLAY_TIME = 3000
    ANSWER_DISPLAY_TIME = 1000
    
    def __init__(self, gamemode=1, playerName="Player"):
        super().__init__(gamemode, playerName=playerName)
        self.font_options = SpriteFont()
        self.load_sprites()
    
    def load_sprites(self):
        self.background_image = pygame.image.load(r"Sprites\QuickieQuiz\Background.png")
        self.dpad_image = pygame.image.load(r"Sprites\QuickieQuiz\D-Pad.png")
        self.up_image = pygame.image.load(r"Sprites\QuickieQuiz\Up.png")
        self.down_image = pygame.image.load(r"Sprites\QuickieQuiz\Down.png")
        self.left_image = pygame.image.load(r"Sprites\QuickieQuiz\Left.png")
        self.right_image = pygame.image.load(r"Sprites\QuickieQuiz\Right.png")
        self.card_image = pygame.image.load(r"Sprites\QuickieQuiz\Card.png")
        self.correct_image = pygame.image.load(r"Sprites\QuickieQuiz\Correct.png")
        self.wrong_image = pygame.image.load(r"Sprites\QuickieQuiz\Wrong.png")
    
    def scale_assets(self, screen):
        assets = {}
        assets['background_scaled'] = pygame.transform.scale(self.background_image, (screen.get_width(), screen.get_height()))
        
        dpad_size = screen.get_height() // 6
        assets['dpad_scaled'] = pygame.transform.scale(self.dpad_image, (dpad_size, dpad_size))
        
        assets['direction_sprites'] = {
            "top": pygame.transform.scale(self.up_image, (dpad_size, dpad_size)),
            "bottom": pygame.transform.scale(self.down_image, (dpad_size, dpad_size)),
            "left": pygame.transform.scale(self.left_image, (dpad_size, dpad_size)),
            "right": pygame.transform.scale(self.right_image, (dpad_size, dpad_size))
        }
        
        card_height = screen.get_height() // 5
        card_width = int(card_height * self.card_image.get_width() / self.card_image.get_height())
        assets['card_scaled'] = pygame.transform.scale(self.card_image, (card_width, card_height))
        assets['correct_scaled'] = pygame.transform.scale(self.correct_image, (card_width, card_height))
        assets['wrong_scaled'] = pygame.transform.scale(self.wrong_image, (card_width, card_height))
        
        return assets

    def pick_random_words_quickiequiz(self):
        correct_urdu, correct_english, options_list, correct_index, word_type = \
            self.pick_random_words(self.gamemode)

        self.agentive_question = len(options_list) == 2

        if self.agentive_question:
            positions = ["left", "right"]
        else:
            positions = ["top", "bottom", "left", "right"]

        random.shuffle(positions)

        # Map positions to options - dicts can be quite nice
        options = dict(zip(positions, options_list))

        correct_word = options_list[correct_index]
        correct_position = None
        for pos, word in options.items():
            if word == correct_word:
                correct_position = pos
                break


        self.BombTimer(4)
        return correct_urdu, correct_english, correct_position, options, word_type

    
    def initialize_game(self, screen):
        self.is_running = True
        self.screen = screen
        
        # Game state
        self.correct_urdu = ""
        self.correct_english = ""
        self.correct_position = ""
        self.options = {}
        self.show_correct = False
        self.show_wrong = False
        self.selection_made = False
        self.correct_display_position = None
        self.last_action_time = 0
        self.selected_direction = None
        self.round_start_time = pygame.time.get_ticks()
        self.show_urdu_display = True
        self.current_word_type = "english"
        self.agentive_question = False

        # Music
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"Sounds/PenguinShuffle.ogg")
        pygame.mixer.music.play(-1)
        
        # Scale assets
        scaled_assets = self.scale_assets(screen)
        self.background_scaled = scaled_assets['background_scaled']
        self.dpad_scaled = scaled_assets['dpad_scaled']
        self.direction_sprites = scaled_assets['direction_sprites']
        self.card_scaled = scaled_assets['card_scaled']
        self.correct_scaled = scaled_assets['correct_scaled']
        self.wrong_scaled = scaled_assets['wrong_scaled']
        
        # Positions
        self.position_coords = {
            "top": (screen.get_width()//2, 100),
            "bottom": (screen.get_width()//2, screen.get_height()-100),
            "left": (100, screen.get_height()//2),
            "right": (screen.get_width()-100, screen.get_height()//2)
        }
        
        # Start first round
        self.correct_urdu, self.correct_english, self.correct_position, self.options, self.current_word_type = self.pick_random_words_quickiequiz()
    
    def handle_frame_input(self, events, current_time):
        for event in events:
            if event.type == pygame.KEYDOWN and not self.selection_made:
                key_to_position = {pygame.K_UP: "top", pygame.K_DOWN: "bottom", pygame.K_LEFT: "left", pygame.K_RIGHT: "right"}
                pressed_position = key_to_position.get(event.key)
                
                if pressed_position and pressed_position in self.options:
                    is_correct = self.check_answer(pressed_position, self.correct_position)
                    self.selected_direction = pressed_position
                    self.selection_made = True
                    self.last_action_time = current_time

                    # For the wrong/right sprites
                    if is_correct:
                        self.show_correct = True
                    else:
                        self.show_wrong = True
    
    def update_frame(self, current_time):
        # Check if timer ran out (and not already answered)
        if not self.selection_made and self._bomb_timer_just_ended:
            self.check_answer(-1, self.correct_position)
            self.show_wrong = True
            self.selection_made = True
            self.last_action_time = current_time
            self._bomb_timer_just_ended = False
        
        # Check if answer was given and wait time passed - then end game
        if self.selection_made and current_time - self.last_action_time >= self.ANSWER_DISPLAY_TIME:
            self.is_running = False
            return
        
        # Timer logic
        if self.show_urdu_display and current_time - self.round_start_time >= self.DISPLAY_TIME:
            self.show_urdu_display = False
        
        if self.selection_made and current_time - self.last_action_time >= self.DISPLAY_TIME:
            self.correct_urdu, self.correct_english, self.correct_position, self.options, self.current_word_type = self.pick_random_words_quickiequiz()
            self.show_correct = False
            self.show_wrong = False
            self.selection_made = False
            self.selected_direction = None
            self.round_start_time = current_time
            self.show_urdu_display = True
        
        # Rendering
        self.screen.blit(self.background_scaled, (0, 0))
        
        # Center sprite
        dpad_center = (self.screen.get_width()//2, self.screen.get_height()//2)
        if self.selected_direction:
            self.screen.blit(self.direction_sprites[self.selected_direction], self.direction_sprites[self.selected_direction].get_rect(center=dpad_center))
        else:
            self.screen.blit(self.dpad_scaled, self.dpad_scaled.get_rect(center=dpad_center))
        
        # Render option cards
        for position, word in self.options.items():
            x, y = self.position_coords[position]
            
            # Card
            card_rect = self.card_scaled.get_rect(center=(x, y))
            self.screen.blit(self.card_scaled, card_rect)
            
            # Text on the Cards
            display_option = word
            if self.agentive_question:
                if display_option == "agentive":
                    display_option = "Yes"
                else:
                    display_option = "No"
                #display_option = "Yes" if word == "agentive" else "No"
            text_surface = self.font_options.render(display_option, color =(255, 255, 255))
            text_surface = pygame.transform.scale_by(text_surface, 3.0)
            text_rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, text_rect)

            # Render the wrong words after user input
            if self.selection_made:
                if self.show_wrong and position != self.correct_position:
                    self.screen.blit(self.wrong_scaled, card_rect)
            
        # Correct Word Display
        if self.show_urdu_display:
            if self.agentive_question and self.current_word_type == "agentive":
                display_word = self.correct_urdu
            else:
                display_word = self.correct_urdu if self.current_word_type == "english" else self.correct_english
            
            suffix = ""
            if self.agentive_question:
                suffix = " is agentive?" if self.current_word_type == "agentive" else " means..."
            large_surface = self.font_options.render((display_word + suffix), color=(255, 255, 0))
            large_surface = pygame.transform.scale_by(large_surface, 5)
            large_rect = large_surface.get_rect(center=(dpad_center[0], dpad_center[1] - 120))
            self.screen.blit(large_surface, large_rect)
        
        # Draw timer on top of everything
        self.bomb_logic(current_time)
    
    def on_pause(self):
        pygame.mixer.music.pause()
    
    def on_resume(self, paused_duration):
        super().on_resume(paused_duration)