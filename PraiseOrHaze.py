import pygame
from Game import Game
import Vocabulary
import time
import random
from Font import SpriteFont

pygame.init()

class PraiseOrHaze(Game):
    ANSWER_DISPLAY_TIME = 1500   # Time to show answer result before next question (ms)

    def __init__(self, gamemode=1, playerName="Player"):
        super().__init__(gamemode=gamemode, num_words=4, playerName=playerName)
        self.sprite_font = None
        self.selector = None
        self.correct = None
        self.wrong = None
        self.Background = None
        self.selected_index = 0
        self.answered = False
        self.was_correct = False
        self.answer_time = 0
        self.round_start_time = 0
        self.screen = None
        self.w = 0
        self.h = 0
        self.question_text = ""
        self.options = []
        self.correct_index = 0
        self.load_sprites()
        self.example_text = ""
        self.exampleSentences = {
            "le": "She will \"{w}\" a photo.",
            "de": "Please \"{w}\" me the book.",
            "a":  "They will \"{w}\" home late.",
            "ja": "We will \"{w}\" to school now.",
            "bEt.h": "He will \"{w}\" on the chair.",
            "ut.h": "The sun will \"{w}\" soon."
        }


    def load_sprites(self):
        self.Background = pygame.image.load(r"Sprites\Backgrounds\Praise_or_Haze.png").convert_alpha()
        self.selector = pygame.image.load(r"Sprites\PraiseOrHaze\Selector.png").convert_alpha()
        self.correct = pygame.image.load(r"Sprites\PraiseOrHaze\Correcto.png").convert_alpha()
        self.wrong = pygame.image.load(r"Sprites\PraiseOrHaze\Wrong.png").convert_alpha()

    def build_question(self):
        # Gamemode 2: Task 2 (verb-combination rules)
        if self.gamemode == 2:
            return self.build_questiontask2()
            

        # Gamemode 1: Task 1 (vocab meaning)
        correct_urdu, correct_english, options, correct_index, word_type = self.pick_random_words(self.gamemode)

        mapped_options = []
        example_text = ""
        if word_type == "agentive" and correct_english in ("agentive", "non-agentive"):
            question_text = f"{correct_urdu} is..."
            # show the English translation
            eng = Vocabulary.lightVerbs.get(correct_urdu, "")
            example_text = f"{correct_urdu} means {eng}" if eng else ""
        else:
            question_text = f"{correct_urdu} means..."
        for opt in options:
            if opt in Vocabulary.lightVerbs:
                mapped_options.append(Vocabulary.lightVerbs[opt])
            else:
                mapped_options.append(opt)

        if self.gamemode == 3:
            example_text = ""            

        self.BombTimer(5)

        # If example_text hasn"t been set above (normal vocab case), build it
        if not hasattr(self, "example_text") or not example_text:
            example_text = self.build_example_sentence(correct_urdu)



        return question_text, example_text, mapped_options, correct_index

    def draw_centered_multiline(self, text, y_center, color, scale, line_gap_px):
        lines = text.split("\n")

        line_surfaces = []
        max_h = 0
        for line in lines:
            surf = self.sprite_font.render(line, color=color)
            surf = pygame.transform.scale_by(surf, scale)
            line_surfaces.append(surf)
            max_h = max(max_h, surf.get_height())

        total_h = len(line_surfaces) * max_h + (len(line_surfaces) - 1) * line_gap_px
        start_y = y_center - total_h // 2

        for i, surf in enumerate(line_surfaces):
            rect = surf.get_rect(
                center=(self.w // 2, start_y + i * (max_h + line_gap_px) + surf.get_height() // 2)
            )
            self.screen.blit(surf, rect)



    # Gamemode 2
    def task2_allowed_seconds(self, first_verb: str):
        agentive = set(Vocabulary.agentive_verbs.keys())
        non_agentive = set(Vocabulary.non_agentive_verbs.keys())
        ambiguous = set(getattr(Vocabulary, "ambiguous_verbs", {}).keys())

        # combine rules
        if first_verb in agentive:
            return (agentive | non_agentive) - {"ja"}

        if first_verb in non_agentive:
            allowed = set(non_agentive)
            if "ja" in ambiguous or "ja" in Vocabulary.lightVerbs:
                allowed.add("ja")
            return allowed

        # treat ambiguous verbs like non-agentives
        allowed = set(non_agentive)
        if "ja" in ambiguous or "ja" in Vocabulary.lightVerbs:
            allowed.add("ja")
        return allowed


    def task2_make_option(self, first_verb: str, second_verb: str) -> str:
        return f"{first_verb} + {second_verb}"


    def build_questiontask2(self):
        agentive = list(Vocabulary.agentive_verbs.keys())
        non_agentive = list(Vocabulary.non_agentive_verbs.keys())
        ambiguous = list(getattr(Vocabulary, "ambiguous_verbs", {}).keys())
        all_verbs = set(agentive) | set(non_agentive) | set(ambiguous)

        ask_for_valid = (random.random() < 0.5)

        if ask_for_valid:
            # possible awnsers
            first = random.choice(non_agentive) if non_agentive else random.choice(agentive)
            allowed = self.task2_allowed_seconds(first)
            wrong_pool = list(all_verbs - allowed)

            correct_second = random.choice(list(allowed))
            wrong_seconds = random.sample(wrong_pool, k=3)

            option_pairs = [self.task2_make_option(first, correct_second)]
            option_pairs += [self.task2_make_option(first, w) for w in wrong_seconds]
            random.shuffle(option_pairs)
            correct_index = option_pairs.index(self.task2_make_option(first, correct_second))

            question_text = f"{first} is combinable\n"\
                            f"with ..."
            helper = "Non-agentive combine only \n"\
            "with non-agentive."

        else:
            # not possible answers
            first = random.choice(agentive) if agentive else random.choice(non_agentive)
            allowed = self.task2_allowed_seconds(first)

            invalid_second = "ja" if "ja" in all_verbs else random.choice(list(all_verbs - allowed))

            valid_seconds_pool = list(allowed)
            if invalid_second in valid_seconds_pool:
                valid_seconds_pool.remove(invalid_second)

            valid_seconds = random.sample(valid_seconds_pool, k=3)

            option_pairs = [self.task2_make_option(first, s) for s in valid_seconds]
            option_pairs.append(self.task2_make_option(first, invalid_second))
            random.shuffle(option_pairs)
            correct_index = option_pairs.index(self.task2_make_option(first, invalid_second))

            question_text = f"{first} is not combinable\n"\
                            f"with..."
            helper = "Agentive verbs combine\n" \
            "with all verbs - except \"ja\"."

        self.BombTimer(5)
        if self.gamemode == 2:
            self.BombTimer(6)
        return question_text, helper, option_pairs, correct_index




    def build_example_sentence(self, urdu_word: str) -> str:
        template = self.exampleSentences.get(urdu_word)

        if self.gamemode == 3:
            return ""

        if template:
                return template.format(w=urdu_word)
        return



    def update_frame(self, current_time):
        # Check if timer ran out
        if not self.answered and self._bomb_timer_just_ended:
            self.check_answer(-1, self.correct_index)
            self.answered = True
            self.was_correct = False
            self.answer_time = current_time
            self._bomb_timer_just_ended = False

        if self.answered and (current_time - self.answer_time) >= self.ANSWER_DISPLAY_TIME:
            self.is_running = False
            return

        q_scale = 4.5
        ex_scale = 3.5
        op_scale = 4

        if self.gamemode == 2:
            q_scale = 3.5
            ex_scale = 2.5
            op_scale = 3

        self.screen.fill((248, 40, 248))

        # background
        scaledW = int(self.w * 0.9)
        scaledH = int(self.h * 0.9)
        scaledWin = pygame.transform.scale(self.Background, (scaledW, scaledH))
        centredB = scaledWin.get_rect(center=(self.w // 2, self.h // 2))
        self.screen.blit(scaledWin, centredB)

        # question
        self.draw_centered_multiline(
            self.question_text,
            y_center=int(self.h * 0.2),
            color=(255, 255, 0),
            scale=q_scale,
            line_gap_px=int(self.h * 0.02)
                    
        )

        # example sentence
        self.draw_centered_multiline(
            self.example_text,
            y_center=int(self.h * 0.4),
            color=(255, 255, 255),
            scale=ex_scale,
            line_gap_px=int(self.h * 0.02)
        )

        # choosable options
        start_y = int(self.h * 0.52)
        spacing = int(self.h * 0.08)

        if self.gamemode == 2:
            start_y = int(self.h * 0.6)
            spacing = int(self.h * 0.08)

        for i, opt in enumerate(self.options):
            option_surface = self.sprite_font.render(opt, color=(176, 216, 160))
            option_surface = pygame.transform.scale_by(option_surface, op_scale)

            orect = option_surface.get_rect(center=(self.w // 2, start_y + i * spacing))
            self.screen.blit(option_surface, orect)

            # Selector
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

        self.bomb_logic(current_time)




    def initialize_game(self, screen):
        self.screen = screen
        self.w, self.h = self.screen.get_size()
        self.sprite_font = SpriteFont()
        self.question_text, self.example_text, self.options, self.correct_index = self.build_question()
        self.selected_index = 0
        self.answered = False
        self.was_correct = False
        self.answer_time = 0
        self.round_start_time = pygame.time.get_ticks()
        self.is_running = True

        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"Sounds/PraizeOrHaize.ogg")
        pygame.mixer.music.play(-1)


    def handle_frame_input(self, events, current_time):
        for event in events:
            if event.type == pygame.KEYDOWN and not self.answered:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.answered = True
                    self.was_correct = (self.selected_index == self.correct_index)
                    self.answer_time = pygame.time.get_ticks()
                    self.check_answer(self.selected_index, self.correct_index)
                    self._bomb_timer_active = False

    def on_pause(self):
        pygame.mixer.music.pause()

    def on_resume(self, paused_duration):
        super().on_resume(paused_duration)
