import pygame
from Game import Game
import Vocabulary
import time
import random
from Font import SpriteFont

pygame.init()

# Sprites (werden später geladen)
class PraiseOrHaze(Game):
    def __init__(self, gamemode=1, playerName="Player"):
        super().__init__(gamemode, playerName=playerName)
        self.sprite_font = None
        self.selector = None
        self.correct = None
        self.wrong = None
        self.Background = None
        self.selected_index = 0
        self.answered = False
        self.was_correct = False
        self.answer_time = 0
        self.screen = None
        self.w = 0
        self.h = 0
        self.question_text = ""
        self.options = []
        self.correct_index = 0
        self.load_sprites()

    def load_sprites(self):
        self.Background = pygame.image.load(r"Sprites\Backgrounds\Praise_or_Haze.png").convert_alpha()
        self.selector = pygame.image.load(r"Sprites\PraiseOrHaze\Selector.png").convert_alpha()
        self.correct = pygame.image.load(r"Sprites\PraiseOrHaze\Correcto.png").convert_alpha()
        self.wrong = pygame.image.load(r"Sprites\PraiseOrHaze\Wrong.png").convert_alpha()

    def build_question(self):
        # Get a random pair and options from base Game
        correct_urdu, correct_english, options, correct_index, word_type = self.pick_random_words()
        if word_type == "english":
            question_word = correct_english
            mapped_options = []
            for opt in options:
                urdu_match = None
                for urdu, eng in Vocabulary.lightVerbs.items():
                    if eng == opt:
                        urdu_match = urdu
                        break
                mapped_options.append(urdu_match)
            question_text = f"{question_word} means..."
        else:
            question_word = correct_urdu
            mapped_options = []
            for opt in options:
                eng_match = Vocabulary.lightVerbs.get(opt, opt)
                mapped_options.append(eng_match)
            question_text = f"{question_word} means..."

        return question_text, mapped_options, correct_index
    
    def update_frame(self, current_time):
        # If answered and 1s passed, prepare next question
        if self.answered and (time.time() - self.answer_time) > 1.0:
            self.selected_index = 0
            self.answered = False
            self.question_text, self.options, self.correct_index = self.build_question()

        self.screen.fill((248, 40, 248))

        # ---------- BACKGROUND ----------
        scaledW = int(self.w * 0.9)
        scaledH = int(self.h * 0.9)
        scaledWin = pygame.transform.scale(self.Background, (scaledW, scaledH))
        centredB = scaledWin.get_rect(center=(self.w // 2, self.h // 2))
        self.screen.blit(scaledWin, centredB)

        # ---------- QUESTION (YELLOW) ----------
        question_surface = self.sprite_font.render(self.question_text, color=(255, 255, 0))
        question_surface = pygame.transform.scale_by(question_surface, 4.5)
        qrect = question_surface.get_rect(center=(self.w // 2, int(self.h * 0.2)))
        self.screen.blit(question_surface, qrect)

        # ---------- OPTIONS (WHITE) ----------
        start_y = int(self.h * 0.45)
        spacing = int(self.h * 0.08)

        for i, opt in enumerate(self.options):
            option_surface = self.sprite_font.render(opt, color=(255, 255, 255))
            option_surface = pygame.transform.scale_by(option_surface, 3.5)

            orect = option_surface.get_rect(center=(self.w // 2, start_y + i * spacing))
            self.screen.blit(option_surface, orect)

            # Selector / Correct / Wrong bei ausgewählter Option
            if i == self.selected_index:
                if not self.answered:
                    arrow_img = pygame.transform.scale_by(self.selector, 3.75)
                else:
                    arrow_img = (
                        pygame.transform.scale_by(self.correct, 3.75)
                        if self.was_correct
                        else pygame.transform.scale_by(self.wrong, 3.75)
                    )

                arrow_rect = arrow_img.get_rect(center=(orect.left - 70, orect.centery + 10))
                self.screen.blit(arrow_img, arrow_rect)
                

    def initialize_game(self, screen):
        # Set screen and cached dimensions
        self.screen = screen
        self.w, self.h = self.screen.get_size()
        self.sprite_font = SpriteFont()
        # Prepare first question
        self.question_text, self.options, self.correct_index = self.build_question()
        self.selected_index = 0
        self.answered = False
        self.was_correct = False
        self.answer_time = 0
        self.is_running = True

        pygame.mixer.music.stop()
        #pygame.mixer.music.load(r"Sounds/JimmyRemix.ogg")
        #pygame.mixer.music.play(-1)


    def handle_frame_input(self, events, current_time):
        # Basic input: navigate options and submit answer
        for event in events:
            if event.type == pygame.KEYDOWN and not self.answered:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.answered = True
                    self.was_correct = (self.selected_index == self.correct_index)
                    self.answer_time = time.time()
                    # Play sounds and update score via base class
                    self.check_answer(self.selected_index, self.correct_index)
                    self.wait_for_seconds(1.0, True)

            
