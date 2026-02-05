import pygame
import random
from Game import Game
import HogansAlley
Games = [HogansAlley.HogansAlley]
from Boss_Font import BossFont
from Vocabulary import agentive_verbs, non_agentive_verbs, ambiguous_verbs
from CurtainTransition import CurtainTransition

pygame.init()

class Boss(Game):
    ANIMATION_SPEED = 150
    TEXT_TYPING_DURATION = 400
    ANSWER_TYPING_DURATION = 600
    BOSS_HIT_DURATION = 1000
    BOSS_HIT_BLINK_SPEED = 100
    LOSE_DURATION = 500
    BOSS_SLIDE_DOWN_DURATION = 1000
    UI_FADE_OUT_DURATION = 500
    BACKGROUND_ANIM_DURATION = 1000
    BOSS_JUMP_HEIGHT = 80
    BOSS_JUMP_DURATION = 300
    SHAKE_INTENSITY = 20

    def __init__(self, gamemode=3, playerName="Player"):
        super().__init__(gamemode=gamemode, num_words=4, playerName=playerName)
        self.background = None
        self.boss_frames = []
        self.boss_sprites = []
        self.boss_hit_sprites = []
        self.selected_boss = None
        self.selected_boss_hit = None
        self.boss_index = 0
        self.current_frame = 0
        self.last_frame_time = 0
        self.screen = None
        self.w = 0
        self.h = 0
        self.intro_start_time = 0
        self.intro_playing = False
        self.intro_finished = False
        self.animation_frozen_frame = 0
        self.boss_y_pos = -500
        self.boss_target_y = 0 
        self.boss_fly_in_complete = False
        self.stats_image = None
        self.stats_original_image = None
        self.stats_loose_image = None
        self.stats_current_width = 0
        self.stats_target_width = 0
        self.stats_animation_complete = False
        self.text_image = None
        self.text_original_image = None
        self.text_loose_image = None
        self.text_current_width = 0
        self.text_target_width = 0
        self.text_animation_complete = False
        self.boss_jump_active = False
        self.boss_jump_start_time = 0
        self.boss_jump_offset_y = 0
        
        self.boss_font = None
        self.boss_names = ["Ganon", "Wario", "Sauron", "Bowser", "Vader", "Thanos", "Sidious", "Minotaur", "Medusa", "Zanto", "Pirate"]
        self.boss_name = "Ganon"
        
        self.dialog_raw_texts = []
        self.dialog_screens = []
        
        self.current_screen_index = 0
        self.text_display_active = False
        self.current_text_lines = []
        self.waiting_for_input = False
        
        self.text_typing_active = False
        self.text_typing_start_time = 0
        self.text_display_progress = 0.0
        self.texting_sound = None
        self.texting_sound_playing = False
        
        self.current_question_index = 0
        self.questions = []
        self.current_question = None
        self.current_answers = []
        self.selected_answer_index = 0
        self.selector_image = None
        self.selector_original_image = None
        self.answer_text_lines = []
        self.answer_display_progress = 0.0
        self.answer_typing_active = False
        self.answer_typing_start_time = 0
        self.question_waiting = False
        
        self.boss_level = 1
        self.boss_hp = 30
        self.boss_hit_active = False
        self.boss_hit_start_time = 0

        self.pending_hit_messages = []
        self.post_hit_action = None
        self.hit_message_mode = False
        
        self.lose_active = False
        self.lose_start_time = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        self.lose_waiting_for_input = False
        
        self.win_active = False
        self.win_start_time = 0
        self.boss_slide_down_active = False
        self.boss_slide_down_start_time = 0
        self.boss_slide_offset_y = 0
        self.ui_fade_out_active = False
        self.ui_fade_out_start_time = 0
        self.ui_fade_progress = 1.0
        self.background_anim_active = False
        self.background_anim_start_time = 0
        
        self.curtain = CurtainTransition()
        self.curtain_closing = False
        self.curtain_opening = False

        self.block_input_until_reset = False
        
        self.load_sprites()
        # Minigame encounter
        self.minigame_chance = 0.2
        self.minigame_triggered = False

    def load_sprites(self):
        self.background = pygame.image.load(r"Sprites\Boss\Background.png").convert()
        
        # Background animation
        for i in range(1, 5):
            frame = pygame.image.load(rf"Sprites\Boss\{i}.png").convert_alpha()
            self.boss_frames.append(frame)
        
        # Boss sprites
        for i in range(1, 4):
            boss = pygame.image.load(rf"Sprites\Boss\Boss{i}.png").convert_alpha()
            self.boss_sprites.append(boss)
            boss_hit = pygame.image.load(rf"Sprites\Boss\Boss{i}_hit.png").convert_alpha()
            self.boss_hit_sprites.append(boss_hit)
        
        # save originals for scaling
        self.boss_sprites_original = self.boss_sprites.copy()
        self.boss_hit_sprites_original = self.boss_hit_sprites.copy()
        self.stats_image = pygame.image.load(r"Sprites\Boss\Stats.png").convert_alpha()
        self.stats_original_image = self.stats_image.copy()
        self.stats_loose_image = pygame.image.load(r"Sprites\Boss\Stats_loose.png").convert_alpha()
        self.text_image = pygame.image.load(r"Sprites\Boss\Text.png").convert_alpha()
        self.text_original_image = self.text_image.copy()
        self.text_loose_image = pygame.image.load(r"Sprites\Boss\Text_loose.png").convert_alpha()
        self.selector_image = pygame.image.load(r"Sprites\Boss\Selector.png").convert_alpha()
        self.selector_original_image = self.selector_image.copy()
        self.boss_font = BossFont()

        self.texting_sound = pygame.mixer.Sound(r"Sprites\Boss\texting.ogg")
        self.hit_sound = pygame.mixer.Sound(r"Sprites\Boss\hit.ogg")

    def _get_minigame_chance(self):
        chance = float(getattr(self, "minigame_chance", 0))
        return chance / 100.0 if chance > 1.0 else chance

    def _start_text_typing(self, lines, play_sound=True):
        self.current_text_lines = lines
        self.text_display_active = True
        self.text_typing_active = True
        self.text_typing_start_time = pygame.time.get_ticks()
        self.text_display_progress = 0.0
        self.waiting_for_input = False
        if play_sound and self.texting_sound:
            try:
                self.texting_sound.play(-1)
                self.texting_sound_playing = True
            except Exception:
                self.texting_sound_playing = False

    def _show_static_text(self, lines):
        self.current_text_lines = lines
        self.text_display_active = True
        self.waiting_for_input = True
        self.text_typing_active = False
        self.text_display_progress = 1.0

    def _stop_texting_sound(self):
        if self.texting_sound_playing:
            try:
                self.texting_sound.stop()
            except Exception:
                pass
            self.texting_sound_playing = False

    def initialize_game(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.is_running = True
        self.last_frame_time = pygame.time.get_ticks()
        self.intro_start_time = pygame.time.get_ticks()
        self.intro_playing = False
        self.intro_finished = False
        
        # Scaling
        self.background = pygame.transform.scale(self.background, (self.w, self.h))
        scaled_frames = []
        for frame in self.boss_frames:
            scaled_frame = pygame.transform.scale(frame, (self.w, self.h))
            scaled_frames.append(scaled_frame)
        self.boss_frames = scaled_frames
        
        # Scale boss sprites
        self.boss_sprites = []
        self.boss_hit_sprites = []
        for i in range(len(self.boss_sprites_original)):
            boss = self.boss_sprites_original[i]
            boss_hit = self.boss_hit_sprites_original[i]
            scaled_size = (boss.get_width() * 5, boss.get_height() * 5)
            self.boss_sprites.append(pygame.transform.scale(boss, scaled_size))
            self.boss_hit_sprites.append(pygame.transform.scale(boss_hit, scaled_size))
        self.boss_index = random.randint(0, len(self.boss_sprites) - 1)
        self.selected_boss = self.boss_sprites[self.boss_index]
        self.selected_boss_hit = self.boss_hit_sprites[self.boss_index]
        
        # Boss name + dialog content
        self.boss_name = random.choice(self.boss_names)
        self.dialog_raw_texts = [
            f"AAgh! It is {self.boss_name}!",
            f"To defeat {self.boss_name}, you need to know Urdu!"
        ]
        self.dialog_screens = []
        for text in self.dialog_raw_texts:
            screens = self.split_text_into_screens(text, max_chars=25, max_lines=2)
            self.dialog_screens.extend(screens)
        self.current_screen_index = 0
        self.current_text_lines = []
        self.text_display_active = False
        self.waiting_for_input = False
        
        self.setup_questions()
        
        # Boss
        self.boss_target_y = self.h // 2 + 100
        self.boss_y_pos = -self.selected_boss.get_height()
        self.boss_fly_in_complete = False
        
        # Stats screen
        stats_scale = 4.5
        original_stats_size = self.stats_original_image.get_size()
        scaled_stats_size = (int(original_stats_size[0] * stats_scale), int(original_stats_size[1] * stats_scale))
        self.stats_image = pygame.transform.scale(self.stats_original_image, scaled_stats_size)
        self.stats_loose_image = pygame.transform.scale(self.stats_loose_image, scaled_stats_size)
        
        # Stats animation
        self.stats_target_width = scaled_stats_size[0]
        self.stats_current_width = 0
        self.stats_animation_complete = False
        
        # Text screen
        text_scale = 4.5
        original_text_size = self.text_original_image.get_size()
        scaled_text_size = (int(original_text_size[0] * text_scale), int(original_text_size[1] * text_scale))
        self.text_image = pygame.transform.scale(self.text_original_image, scaled_text_size)
        self.text_loose_image = pygame.transform.scale(self.text_loose_image, scaled_text_size)
        
        # Text animation
        self.text_target_width = scaled_text_size[0]
        self.text_current_width = 0
        self.text_animation_complete = False
        self.text_display_active = False
        
        self.texting_sound = pygame.mixer.Sound(r"Sprites\Boss\texting.ogg")

    # Text splitting
    def split_text_into_screens(self, text, max_chars=20, max_lines=2):
        import re
        sentence_parts = re.split(r"([.!?])", text)
        sentences = []
        i = 0
        while i < len(sentence_parts):
            if i + 1 < len(sentence_parts) and sentence_parts[i + 1] in ",.!?":
                sentence = sentence_parts[i].strip() + sentence_parts[i + 1]
                if sentence.strip():
                    sentences.append(sentence)
                i += 2
            elif sentence_parts[i].strip():
                sentences.append(sentence_parts[i].strip())
                i += 1
            else:
                i += 1
        
        screens = []
        current_screen = []
        
        for sentence in sentences:
            words = sentence.split()
            sentence_lines = []
            current_line = ""
            
            for word in words:
                if len(current_line) + len(word) + 1 <= max_chars:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
                else:
                    if current_line:
                        sentence_lines.append(current_line)
                    current_line = word
            if current_line:
                sentence_lines.append(current_line)
            if len(current_screen) + len(sentence_lines) <= max_lines:
                current_screen.extend(sentence_lines)
            else:
                if current_screen:
                    screens.append(current_screen)
                current_screen = sentence_lines
        if current_screen:
            screens.append(current_screen)
        
        return screens

    # dialog only continues if player presses anything
    def wrap_text(self, text, max_chars=20, max_lines=2):
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
                
                if len(lines) >= max_lines:
                    if current_line:
                        lines.append(current_line)
                    return lines
        
        if current_line:
            lines.append(current_line)
        
        return lines[:max_lines]

    def setup_questions(self):
        self.questions = []
        
        all_verbs = {**agentive_verbs, **non_agentive_verbs, **ambiguous_verbs}
        urdu_words = list(all_verbs.keys())
        all_english = list(all_verbs.values())
        
        # Urdu to English
        for urdu_word in urdu_words:
            correct_answer = all_verbs[urdu_word]
            wrong_answers = [w for w in all_english if w != correct_answer]
            if len(wrong_answers) >= 3:
                wrong_answers = random.sample(wrong_answers, 3)
            else:
                wrong_answers = random.sample(wrong_answers, min(3, len(wrong_answers)))
            
            all_answers = [correct_answer] + wrong_answers
            random.shuffle(all_answers)
            correct_index = all_answers.index(correct_answer)
            
            self.questions.append({
                "question": f"In english {urdu_word} means...",
                "type": "translate",
                "answers": all_answers,
                "correct": correct_index
            })
        
        # Agentive or Non-Agentive
        for urdu_word in urdu_words:
            if urdu_word in agentive_verbs:
                answers = ["Non-Agentive", "Agentive"]
                correct_index = 1
            elif urdu_word in non_agentive_verbs:
                answers = ["Non-Agentive", "Agentive"]
                correct_index = 0
            else:
                answers = ["Agentive", "Ambiguous"]
                correct_index = 1
            
            self.questions.append({
                "question": f"{urdu_word} is ...?",
                "type": "agentive",
                "answers": answers,
                "correct": correct_index
            })
        
        # English to Urdu
        unique_english = list(set(all_english))
        for english_word in unique_english:
            correct_urdu = [k for k, v in all_verbs.items() if v == english_word][0]
            wrong_urdu = [k for k, v in all_verbs.items() if v != english_word]
            if len(wrong_urdu) >= 3:
                wrong_urdu = random.sample(wrong_urdu, 3)
            else:
                wrong_urdu = random.sample(wrong_urdu, min(3, len(wrong_urdu)))
            
            all_answers = [correct_urdu] + wrong_urdu
            random.shuffle(all_answers)
            correct_index = all_answers.index(correct_urdu)
            
            self.questions.append({
                "question": f"In Urdu {english_word} means...",
                "type": "translate",
                "answers": all_answers,
                "correct": correct_index
            })
        
        # combinable questions 
        additional = []
        total_verbs = list(all_verbs.keys())
        sample_size = min(6, max(1, len(total_verbs)//4))

        for _ in range(sample_size):
            try:
                first, second, options, correct_index, mode = self.pick_random_words(gamemode=2)
            except Exception:
                continue
            if mode == "verb_pair":
                additional.append({
                    "question": f"{first} can be combined with...",
                    "type": "combinable_options",
                    "answers": options,
                    "correct": correct_index
                })

        for _ in range(sample_size):
            try:
                first, valid_second, options, correct_index, mode = self.pick_random_words(gamemode=2)
            except Exception:
                continue


            make_valid = random.choice([True, False])
            if make_valid:
                q = f"Is {first} combinable with {valid_second}?"
                correct = 0
            else:
                if first in agentive_verbs:
                    invalid_pool = list(ambiguous_verbs.keys())
                else:
                    invalid_pool = list(agentive_verbs.keys())
                if not invalid_pool:
                    invalid_second = valid_second
                else:
                    invalid_second = random.choice(invalid_pool)
                q = f"Is {first} combinable with {invalid_second}?"
                correct = 1

            additional.append({
                "question": q,
                "type": "is_combinable",
                "answers": ["Yes", "No"],
                "correct": correct
            })

        # Question shuffle, that several questions can appear in one boss fight
        random.shuffle(additional)
        base = self.questions.copy()
        mixed = []
        while additional or base:
            if additional:
                mixed.append(additional.pop(0))
            if base:
                mixed.append(base.pop(0))

        self.questions = mixed
        self.current_question_index = 0

    def show_question(self):
        if self.current_question_index < len(self.questions):
            # Question animation
            self.current_question = self.questions[self.current_question_index]
            self.current_answers = self.current_question["answers"]
            self.selected_answer_index = 0
            qtext = self.current_question.get("question", "")
            self._start_text_typing(self.wrap_text(qtext, max_chars=25, max_lines=2))
            self.question_waiting = False
        else:
            return

    def questions_or_minigame(self):
        if random.random() < self._get_minigame_chance():
            self.minigame_triggered = True
            self._start_text_typing(["BeAt Me!"])
        else:
            self.show_question()

    def update_frame(self, current_time):
        if not self.intro_playing and not self.intro_finished:
            if current_time - self.intro_start_time >= 1300:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(r"Sprites\Boss\Intro.ogg")
                pygame.mixer.music.play(0)
                self.intro_playing = True
        
        if self.intro_playing and not self.intro_finished:
            if not pygame.mixer.music.get_busy():
                self.animation_frozen_frame = self.current_frame
                pygame.mixer.music.load(r"Sprites\Boss\Boss.ogg")
                pygame.mixer.music.play(-1)
                self.intro_finished = True
        
        if not self.intro_finished:
            if current_time - self.last_frame_time >= self.ANIMATION_SPEED:
                self.last_frame_time = current_time
                self.current_frame = (self.current_frame + 1) % len(self.boss_frames)
        
        # loosing Background animation
        if self.lose_active:
            elapsed_time = current_time - self.lose_start_time
            if elapsed_time < Boss.LOSE_DURATION:
                progress = (elapsed_time % 50) / 50.0
                self.shake_offset_x = int(Boss.SHAKE_INTENSITY * progress)
                self.shake_offset_y = int(Boss.SHAKE_INTENSITY * progress)
            else:
                # restart only if player clicks something
                if not self.lose_waiting_for_input:
                    self.lose_waiting_for_input = True
                    self.shake_offset_x = 0
                    self.shake_offset_y = 0
                    try:
                        pygame.mixer.music.stop()
                    except Exception:
                        pass
        
        # Curtain animations and logic
        if self.curtain_closing:
            still_animating = self.curtain.update(current_time)
            if not still_animating:
                self.curtain_closing = False
                self.curtain_opening = True
                
                # Reset game state if lost
                self.boss_level = 1
                self.boss_hp = 30
                
                # Reset animation states
                self.intro_finished = False
                self.intro_playing = False
                self.animation_frozen_frame = None
                self.boss_fly_in_complete = False
                self.boss_jump_active = False
                self.boss_hit_active = False
                self.stats_animation_complete = False
                self.text_animation_complete = False
                self.text_display_active = False
                self.question_waiting = False
                self.selected_answer_index = 0
                
                # Reset for new boss
                self.current_question_index = 0
                self.initialize_game(self.screen)
                
                self.curtain.start_opening_animation(self.screen)
        
        if self.curtain_opening:
            still_animating = self.curtain.update(current_time)
            if not still_animating:
                self.curtain_opening = False
        
        if self.win_active:
            elapsed_time = current_time - self.win_start_time

            # remove Boss (slide down)
            if not self.boss_slide_down_active:
                self.boss_slide_down_active = True
                self.boss_slide_down_start_time = current_time
                

            if self.boss_slide_down_active:
                slide_elapsed = current_time - self.boss_slide_down_start_time
                if slide_elapsed < Boss.BOSS_SLIDE_DOWN_DURATION:
                    progress = slide_elapsed / Boss.BOSS_SLIDE_DOWN_DURATION
                    self.boss_slide_offset_y = int(progress * (self.h + 200))
                else:
                        # Ui fade out
                    if not self.ui_fade_out_active:
                        self.ui_fade_out_active = True
                        self.ui_fade_out_start_time = current_time
                        self.text_display_active = False
                        
                    
                    fade_elapsed = current_time - self.ui_fade_out_start_time
                    if fade_elapsed < Boss.UI_FADE_OUT_DURATION:
                        # Reverse animation (disappearing animation)
                        progress = fade_elapsed / Boss.UI_FADE_OUT_DURATION
                        self.stats_current_width = int(self.stats_target_width * (1.0 - progress))
                        self.text_current_width = int(self.text_target_width * (1.0 - progress))
                    else:
                        # Background moving forward
                        if not self.background_anim_active:
                            self.background_anim_active = True
                            self.background_anim_start_time = current_time
                            self.animation_frozen_frame = None
                        
                        bg_anim_elapsed = current_time - self.background_anim_start_time
                        if bg_anim_elapsed < Boss.BACKGROUND_ANIM_DURATION:
                            if current_time - self.last_frame_time >= self.ANIMATION_SPEED:
                                self.last_frame_time = current_time
                                self.current_frame = (self.current_frame + 1) % len(self.boss_frames)
                        else:
                            # Loosing stats reset
                            if not self.background_anim_active:
                                self.background_anim_active = True
                                self.background_anim_start_time = current_time
                                
                            bg_anim_elapsed = current_time - self.background_anim_start_time
                            if bg_anim_elapsed < Boss.BACKGROUND_ANIM_DURATION:
                                if current_time - self.last_frame_time >= self.ANIMATION_SPEED:
                                    self.last_frame_time = current_time
                                    self.current_frame = (self.current_frame + 1) % len(self.boss_frames)
                            else:
                                # finish and reset
                                
                                self.win_active = False
                                self.boss_slide_down_active = False
                                self.ui_fade_out_active = False
                                self.background_anim_active = False
                                self.boss_slide_offset_y = 0
                                self.ui_fade_progress = 1.0

                                # Increase level and HP
                                self.boss_level += 1
                                self.boss_hp = self.boss_hp + (self.boss_level - 1) * 30

                                # Reset animation states
                                self.intro_finished = False
                                self.intro_playing = False
                                self.animation_frozen_frame = None
                                self.boss_fly_in_complete = False
                                self.boss_jump_active = False
                                self.boss_hit_active = False
                                self.stats_animation_complete = False
                                self.text_animation_complete = False
                                self.text_display_active = False
                                self.question_waiting = False
                            self.selected_answer_index = 0
                            self.lose_active = False
                            self.shake_offset_x = 0
                            self.shake_offset_y = 0
                            
                            # Reset boss
                            self.current_question_index = 0
                            # re-enable input
                            self.block_input_until_reset = False
                            self.initialize_game(self.screen)
                            return
        
        # Background
        self.screen.blit(self.background, (self.shake_offset_x, self.boss_jump_offset_y + self.shake_offset_y))
        if self.animation_frozen_frame is not None and self.intro_finished:
            frame_to_draw = self.animation_frozen_frame
        else:
            frame_to_draw = self.current_frame
        self.screen.blit(self.boss_frames[frame_to_draw], (self.shake_offset_x, self.boss_jump_offset_y + self.shake_offset_y))
        
        # Boss spwan
        if self.intro_finished and self.selected_boss:
            if not self.boss_fly_in_complete:
                self.boss_y_pos += 30
                if self.boss_y_pos >= self.boss_target_y:
                    self.boss_y_pos = self.boss_target_y
                    self.boss_fly_in_complete = True
                    self.boss_jump_active = True
                    self.boss_jump_start_time = current_time
        
            if self.boss_jump_active:
                elapsed_time = current_time - self.boss_jump_start_time
                if elapsed_time < Boss.BOSS_JUMP_DURATION:
                    progress = elapsed_time / Boss.BOSS_JUMP_DURATION
                    jump_y = -Boss.BOSS_JUMP_HEIGHT * abs(((progress * 2 - 1) ** 2) - 1)
                    self.boss_jump_offset_y = int(jump_y)
                else:
                    self.boss_jump_active = False
                    self.boss_jump_offset_y = 0
            
            # Update hit animation
            if self.boss_hit_active:
                elapsed_time = current_time - self.boss_hit_start_time
                if elapsed_time < Boss.BOSS_HIT_DURATION:
                    # Blink between normal and hit sprite
                    blink_cycle = (elapsed_time // Boss.BOSS_HIT_BLINK_SPEED) % 2
                    if blink_cycle == 0:
                        boss_to_draw = self.selected_boss_hit
                    else:
                        boss_to_draw = self.selected_boss
                else:
                    self.boss_hit_active = False
                    boss_to_draw = self.selected_boss
            else:
                boss_to_draw = self.selected_boss
            
            boss_y = self.boss_y_pos + self.boss_slide_offset_y
            boss_rect = boss_to_draw.get_rect(center=(self.w // 2, boss_y))
            self.screen.blit(boss_to_draw, boss_rect)
        
        # Wait for Boss spawn to complete to make stats and text
        if self.boss_fly_in_complete and self.stats_image:
            if not self.stats_animation_complete:
                self.stats_current_width += 60
                if self.stats_current_width >= self.stats_target_width:
                    self.stats_current_width = self.stats_target_width
                    self.stats_animation_complete = True

            current_height = self.stats_image.get_height()
            if self.stats_current_width > 0 and not self.ui_fade_out_active:
                # Use loose image if loose is active
                stats_to_draw = self.stats_loose_image if self.lose_active else self.stats_image
                scaled_stats = pygame.transform.scale(stats_to_draw, (int(self.stats_current_width), current_height))
                stats_rect = scaled_stats.get_rect(midtop=(self.w // 2, 0))
                self.screen.blit(scaled_stats, stats_rect)
                
                if self.stats_animation_complete and self.boss_font:
                    stats_x = stats_rect.left
                    stats_y = stats_rect.top
                    
                    # Boss Stats
                    name_text = self.boss_font.render(self.boss_name, color=(255, 255, 255), scale=4.5)
                    lv_text = self.boss_font.render(str(self.boss_level).zfill(3), color=(255, 255, 255), scale=4.5)
                    hp_text = self.boss_font.render(str(self.boss_hp).zfill(3), color=(255, 255, 255), scale=4.5)
                    mp_text = self.boss_font.render("150", color=(255, 255, 255), scale=4.5)
                    
                    text_y = stats_y + 80
                    self.screen.blit(name_text, (stats_x + 97, text_y))
                    self.screen.blit(lv_text, (stats_x + 345, text_y))
                    self.screen.blit(hp_text, (stats_x + 522, text_y))
                    self.screen.blit(mp_text, (stats_x + 705, text_y))
        
        if self.boss_fly_in_complete and self.text_image:
            if not self.text_animation_complete:
                self.text_current_width += 60
                if self.text_current_width >= self.text_target_width:
                    self.text_current_width = self.text_target_width
                    self.text_animation_complete = True
                    if not self.text_display_active:
                        self.text_display_active = True
                        self.next_text()
            
            text_height = self.text_image.get_height()
            # Use loose png versions
            if self.text_current_width > 0 and not self.ui_fade_out_active:
                text_to_draw = self.text_loose_image if self.lose_active else self.text_image
                scaled_text = pygame.transform.scale(text_to_draw, (int(self.text_current_width), text_height))
                text_rect = scaled_text.get_rect(midbottom=(self.w // 2, self.h))
                self.screen.blit(scaled_text, text_rect)
                
                # Win/Lose Messages
                if self.win_active:
                    box_x = text_rect.left
                    box_y = text_rect.top
                    win_text = self.boss_font.render(f"You beat {self.boss_name}!", color=(255, 255, 255), scale=4.5)
                    self.screen.blit(win_text, (box_x + 50, box_y + 35))
                elif self.lose_active:
                    box_x = text_rect.left
                    box_y = text_rect.top
                    lose_text = self.boss_font.render("YoU aRe ToO wEaK!", color=(255, 255, 255), scale=4.5)
                    self.screen.blit(lose_text, (box_x + 50, box_y + 35))
                elif self.text_display_active and self.current_text_lines and not self.win_active:
                    box_x = text_rect.left
                    box_y = text_rect.top
                    
                    # dialog texting
                    if self.text_typing_active:
                        elapsed_time = pygame.time.get_ticks() - self.text_typing_start_time
                        self.text_display_progress = min(elapsed_time / Boss.TEXT_TYPING_DURATION, 1.0)
                        
                        if self.text_display_progress >= 1.0:
                            self.text_typing_active = False
                            self.waiting_for_input = True
                            if self.texting_sound_playing:
                                self.texting_sound.stop()
                                self.texting_sound_playing = False
                    
                    # Text lenght
                    all_text = "".join(self.current_text_lines)
                    total_chars = len(all_text)
                    chars_to_show = int(total_chars * self.text_display_progress)
                    displayed_lines = []
                    chars_shown = 0
                    for line in self.current_text_lines:
                        if chars_shown >= chars_to_show:
                            break
                        
                        if chars_shown + len(line) <= chars_to_show:
                            displayed_lines.append(line)
                            chars_shown += len(line)
                        else:
                            partial_line = line[:chars_to_show - chars_shown]
                            displayed_lines.append(partial_line)
                            chars_shown = chars_to_show
                            break

                    dialog_line_spacing = 75
                    for i, line in enumerate(displayed_lines):
                        if line:
                            line_text = self.boss_font.render(line, color=(255, 255, 255), scale=4.5)
                            self.screen.blit(line_text, (box_x + 50, box_y + 35 + i * dialog_line_spacing))
                            
                if getattr(self, "lose_waiting_for_input", False):
                    prompt = self.boss_font.render("Press any Key to continue", color=(255, 255, 255), scale=3.0)
                    self.screen.blit(prompt, (box_x + 50, box_y + 150))
        
        # question and answers
        if self.current_question and self.text_image and not self.win_active and not self.lose_active:
            if self.question_waiting:
                text_height = self.text_image.get_height()
                if self.text_current_width > 0:
                    scaled_text = pygame.transform.scale(self.text_image, (int(self.text_current_width), text_height))
                    text_rect = scaled_text.get_rect(midbottom=(self.w // 2, self.h))
                    self.screen.blit(scaled_text, text_rect)

                    # Creates 2x2 grid for awnsers
                    box_x = text_rect.left
                    box_y = text_rect.top

                    answer_start_left = 100
                    answer_y = box_y + 35
                    answer_spacing = 80
                    answer_x = 500

                    positions = [
                        (box_x + answer_start_left, answer_y),
                        (box_x + answer_start_left + answer_x, answer_y),
                        (box_x + answer_start_left, answer_y + answer_spacing),
                        (box_x + answer_start_left + answer_x, answer_y + answer_spacing)
                    ]

                    for i, answer in enumerate(self.current_answers):
                        if i >= len(positions):
                            break

                        answer_x, answer_y = positions[i]

                        # Selector
                        if i == self.selected_answer_index:
                            scaled_selector = pygame.transform.scale(self.selector_original_image, (35, 50))
                            self.screen.blit(scaled_selector, (answer_x - 60, answer_y + 10))

                        # Answer text
                        answer_text = self.boss_font.render(answer, color=(255, 255, 255), scale=4.5)
                        self.screen.blit(answer_text, (answer_x, answer_y))
        
        if self.curtain_closing or self.curtain_opening:
            self.curtain.render(self.screen)

    #minigame start logic
    def next_text(self):
        if self.current_screen_index < len(self.dialog_screens):
            self._start_text_typing(self.dialog_screens[self.current_screen_index])
        else:
            if random.random() < self._get_minigame_chance():
                self.minigame_triggered = True
                self._start_text_typing(["BeAt Me!"])
            else:

                self._show_static_text([""])

    def handle_frame_input(self, events, current_time):
        # If input is blocked, ignore events
        if getattr(self, "block_input_until_reset", False):
            return
        # Block input during animations
        if not self.intro_finished or self.boss_jump_active:
            return
        
        for event in events:
            # after a loss, accept any key to proceed to curtain
            if getattr(self, "lose_waiting_for_input", False) and event.type == pygame.KEYDOWN:
                self.lose_waiting_for_input = False
                self.lose_active = False
                self.shake_offset_x = 0
                self.shake_offset_y = 0
                self.curtain_closing = True
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
                self.curtain.start_closing_animation(self.screen, is_success=False)
                return
            if event.type == pygame.KEYDOWN:
                if self.current_question:
                    if not self.question_waiting:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            self.question_waiting = True
                    else:
                        # Player input
                        if event.key == pygame.K_UP:
                            if self.selected_answer_index in [2, 3]:
                                self.selected_answer_index -= 2
                        elif event.key == pygame.K_DOWN:
                            if self.selected_answer_index in [0, 1]:
                                self.selected_answer_index += 2
                        elif event.key == pygame.K_LEFT:
                            if self.selected_answer_index in [1, 3]:
                                self.selected_answer_index -= 1
                        elif event.key == pygame.K_RIGHT:
                            if self.selected_answer_index in [0, 2]:
                                self.selected_answer_index += 1
                        elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            # Check answer
                            is_correct = self.selected_answer_index == self.current_question["correct"]
                            if is_correct:
                                self.lose_active = False
                                self.shake_offset_x = 0
                                self.shake_offset_y = 0
                                
                                self.boss_hit_active = True
                                self.boss_hit_start_time = pygame.time.get_ticks()
                                dmg = 10
                                # Prevent answering the same question multiple times
                                self.current_question = None
                                self.question_waiting = False
                                self.boss_hp = max(0, self.boss_hp - dmg)
                                self.hit_sound.play()
                                # Queue hit messages; resume with win or next question
                                if self.boss_hp <= 0:
                                    self.queue_hit_messages(dmg, resume_action="win")
                                else:
                                    self.queue_hit_messages(dmg, resume_action="question")
                                continue
                            else:
                                self.lose_active = True
                                self.lose_start_time = pygame.time.get_ticks()
                                self.hit_sound.play()
                                continue
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if self.text_typing_active:
                        self.text_display_progress = 1.0
                        self.text_typing_active = False
                        self.waiting_for_input = True
                        self._stop_texting_sound()
                    elif self.text_display_active and self.waiting_for_input:
                        if getattr(self, "hit_message_mode", False):
                            if self.pending_hit_messages:
                                self.show_next_hit_message()
                                return
                            else:
                                self.hit_message_mode = False
                                action = self.post_hit_action
                                self.post_hit_action = None
                                if action == "question":
                                    self.current_question_index += 1
                                    if self.current_question_index < len(self.questions):
                                        self.questions_or_minigame()
                                    else:
                                        self.game_state = "game_over"
                                        self.is_running = False
                                elif action == "win":
                                    self.post_hit_action = None
                                    self.hit_message_mode = False
                                    self.pending_hit_messages = []
                                    self.text_display_active = False
                                    self.animation_frozen_frame = None
                                    self.boss_slide_down_active = False
                                    self.ui_fade_out_active = False
                                    self.background_anim_active = False
                                    self.win_active = True
                                    self.win_start_time = pygame.time.get_ticks()
                                    self.block_input_until_reset = True
                                return

                        # dialog animation
                        self.current_screen_index += 1
                        if self.current_screen_index < len(self.dialog_screens):
                            self.next_text()
                        else:
                            if getattr(self, "post_hit_action", None) and not self.pending_hit_messages:
                                action = self.post_hit_action
                                self.post_hit_action = None
                                if action == "question":
                                    self.current_question_index += 1
                                    if self.current_question_index < len(self.questions):
                                        self.questions_or_minigame()
                                    else:
                                        self.game_state = "game_over"
                                        self.is_running = False
                                elif action == "win":
                                    self.win_active = True
                                    self.win_start_time = pygame.time.get_ticks()
                                    self.block_input_until_reset = True
                            elif getattr(self, "minigame_triggered", False):
                                self.text_display_active = False
                                self.minigame_triggered = False
                                try:
                                    won = self.run_minigames()
                                except Exception:
                                    won = False

                                if won:
                                    dmg = 20
                                    self.boss_hit_active = True
                                    self.boss_hit_start_time = pygame.time.get_ticks()
                                    # clear active question
                                    self.current_question = None
                                    self.question_waiting = False
                                    self.boss_hp = max(0, self.boss_hp - dmg)
                                    self.hit_sound.play()
                                    if self.boss_hp <= 0:
                                        self.queue_hit_messages(dmg, resume_action="win")
                                    else:
                                        self.queue_hit_messages(dmg, resume_action="question")
                                else:
                                    self.lose_active = True
                                    self.lose_start_time = pygame.time.get_ticks()
                                    self.hit_sound.play()
                            else:
                                    self.questions_or_minigame()
                    else:
                        self.is_running = False

    def on_pause(self):
        pygame.mixer.music.pause()

    def on_resume(self, paused_duration):
        super().on_resume(paused_duration)

    def run_minigames(self):
        if not Games:
            return False

        GameClass = random.choice(Games)
        clock = pygame.time.Clock()
        game_instance = GameClass(gamemode=3, playerName=self.playerName)
        game_instance.initialize_game(self.screen)
        game_instance.game_actually_started = True
        start_score = getattr(game_instance, "score", 0)

        while game_instance.is_running:
            current_time = pygame.time.get_ticks()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    game_instance.is_running = False
                    self.is_running = False
                    return False

            try:
                game_instance.handle_frame_input(events, current_time)
            except TypeError:
                try:
                    game_instance.handle_frame_input(events)
                except Exception:
                    pass

            game_instance.update_frame(current_time)
            pygame.display.flip()
            clock.tick(60)

        final_score = getattr(game_instance, "score", 0)
        won = final_score > start_score

        # stop minigame music
        try:
            if won:
                pygame.mixer.music.fadeout(500)
            else:
                pygame.mixer.music.stop()
        except Exception:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass

        return won

    def queue_hit_messages(self, dmg, resume_action="question"):
        if getattr(self, "hit_message_mode", False):
            return

        messages = ["You hit him!", "That hurt a bit.", "Good Job!"]
        msg = random.choice(messages)
        self.pending_hit_messages = [msg]
        self.post_hit_action = resume_action
        self.lose_active = False
        self.lose_waiting_for_input = False
        self.curtain_closing = False
        self.hit_message_mode = True
        self.show_next_hit_message()

    def show_next_hit_message(self):
        if not self.pending_hit_messages:
            return
        next_msg = self.pending_hit_messages.pop(0)
        self._start_text_typing([next_msg])