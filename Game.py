import pygame
import pygame_menu
import random
import Vocabulary
from CurtainTransition import CurtainTransition

pygame.init()

correct_sound = pygame.mixer.Sound(r"Sounds/Correct.ogg")
wrong_sound = pygame.mixer.Sound(r"Sounds/Wrong.ogg")
class Game:
    def __init__(self, gamemode=1, num_words=4, playerName="Player"):
        self.gamemode = gamemode
        self.num_words = num_words
        self.score = 0
        self.is_running = False
        self.playerName = playerName
        self.game_actually_started = False  # Flag to indicate if the curtain animation is complete
        self.t0 = None
        self.t1 = None
        self.t2 = None
        self.t3 = None
        self.t4 = None
        self.t5 = None
        self.t6 = None
        self.t7 = None
        self.t8 = None
        self._bomb_timer_active = False
        self._bomb_timer_start_ms = 0
        self._bomb_timer_total_ms = 0
        self._bomb_timer_ticks = 9
        self._bomb_timer_just_ended = False
        self._timer_sound_3 = None
        self._timer_sound_2 = None
        self._timer_sound_1 = None
        self._last_tick_played = None

    def load_bombs(self):
        self.t0 = pygame.image.load(r"Sprites\Timer\boom.png").convert_alpha()
        self.t1 = pygame.image.load(r"Sprites\Timer\1.png").convert_alpha()
        self.t2 = pygame.image.load(r"Sprites\Timer\2.png").convert_alpha()
        self.t3 = pygame.image.load(r"Sprites\Timer\3.png").convert_alpha()
        self.t4 = pygame.image.load(r"Sprites\Timer\4.png").convert_alpha()
        self.t5 = pygame.image.load(r"Sprites\Timer\5.png").convert_alpha()
        self.t6 = pygame.image.load(r"Sprites\Timer\6.png").convert_alpha()
        self.t7 = pygame.image.load(r"Sprites\Timer\7.png").convert_alpha()
        self.t8 = pygame.image.load(r"Sprites\Timer\8.png").convert_alpha()
        self._timer_sound_3 = pygame.mixer.Sound(r"Sprites\Timer\Timer3.ogg")
        self._timer_sound_2 = pygame.mixer.Sound(r"Sprites\Timer\Timer2.ogg")
        self._timer_sound_1 = pygame.mixer.Sound(r"Sprites\Timer\Timer1.ogg")

    def BombTimer(self, seconds):
        self.load_bombs()
        self._bomb_timer_active = True
        self._bomb_timer_start_ms = pygame.time.get_ticks()
        self._bomb_timer_total_ms = max(1, int(seconds * 1000))
        self._last_tick_played = None

    # bomb timer logic and rendering
    def bomb_logic(self, current_time):
        if not self._bomb_timer_active or not self.game_actually_started:
            return

        elapsed = current_time - self._bomb_timer_start_ms
        total_ms = self._bomb_timer_total_ms

        step_ms = total_ms / float(self._bomb_timer_ticks)

        step_index = int(elapsed / step_ms)
        tick_value = max(0, min(8, 8 - step_index))

        timer_pics = getattr(self, "t" + str(tick_value))
        
        # For sounds on t1,t2 and t3
        if tick_value != self._last_tick_played:
            if tick_value == 3:
                self._timer_sound_3.play()
            elif tick_value == 2:
                self._timer_sound_2.play()
            elif tick_value == 1:
                self._timer_sound_1.play()
            self._last_tick_played = tick_value
        
        # Bomb scaler
        timer_pics = pygame.transform.scale_by(timer_pics, 4.0)

        # Bomb positioning
        w, h = self.screen.get_size()
        x = 0
        y = h - timer_pics.get_height()
        self.screen.blit(timer_pics, (x, y))

        if elapsed >= total_ms:
            self._bomb_timer_active = False
            self._bomb_timer_just_ended = True

    
    def pick_random_words(self, gamemode):
        if gamemode == 1:
            # Randomly choose between existing code or lightVerbsAgentive
            if random.choice([True, False]):
                # Existing code: use lightVerbs
                wordpair = random.choice(list(Vocabulary.lightVerbs.items()))
                correct_urdu = wordpair[0]
                correct_english = wordpair[1]
                
                word_type = random.choice(["english", "urdu"])
                if word_type == "english":
                    # English is displayed, Urdu is the answer
                    pool = list(Vocabulary.lightVerbs.values())
                    if correct_english in pool:
                        pool.remove(correct_english)
                    correct_word = correct_english
                else:
                    # Urdu is displayed, English is the answer
                    pool = list(Vocabulary.lightVerbs.keys())
                    if correct_urdu in pool:
                        pool.remove(correct_urdu)
                    correct_word = correct_urdu

                # Create false options
                false_options = random.sample(pool, self.num_words - 1)
                options = [correct_word] + false_options
                random.shuffle(options)
                correct_index = options.index(correct_word)
                
                return correct_urdu, correct_english, options, correct_index, word_type
            else:
                agentive_class = {"agentive": [], "non-agentive": []}
                for word, agentive in Vocabulary.lightVerbsAgentive.items():
                    agentive_class[agentive].append(word)

                candidates = [
                    (random.choice(agentive_class["agentive"]), "agentive"),
                    (random.choice(agentive_class["non-agentive"]), "non-agentive"),
                ]

                correct_urdu, correct_classification = random.choice(candidates)

                options = ["agentive", "non-agentive"]
                random.shuffle(options)
                correct_index = options.index(correct_classification)

                return correct_urdu, correct_classification, options, correct_index, "agentive"

                        
        elif gamemode == 2:
            # Creates 1 correct and some incorrect verb pair combinations based on these 2 rules:
            # - If first word is from agentive_verbs: second can be from agentive_verbs OR non_agentive_verbs
            # - If first word is from non_agentive_verbs: second can be from non_agentive_verbs OR ambiguous_verbs

            first_verb_pool = list(Vocabulary.agentive_verbs.keys()) + list(Vocabulary.non_agentive_verbs.keys())
            correct_first_word = random.choice(first_verb_pool)
            first_verb_type = None
            valid_second_pool = []
            invalid_second_pool = []
            
            if correct_first_word in Vocabulary.agentive_verbs:
                first_verb_type = "agentive"
                valid_second_pool = list(Vocabulary.agentive_verbs.keys()) + list(Vocabulary.non_agentive_verbs.keys())
            elif correct_first_word in Vocabulary.non_agentive_verbs:
                first_verb_type = "non-agentive"
                valid_second_pool = list(Vocabulary.non_agentive_verbs.keys()) + list(Vocabulary.ambiguous_verbs.keys())
            
            correct_second_word = random.choice(valid_second_pool)
            if first_verb_type == "agentive":
                invalid_second_pool = list(Vocabulary.ambiguous_verbs.keys())
            elif first_verb_type == "non-agentive":
                invalid_second_pool = list(Vocabulary.agentive_verbs.keys())
            
            false_options = random.sample(invalid_second_pool, min(self.num_words - 1, len(invalid_second_pool)))
            
            # Sometmes we don't have enough wrong options - so in this case we fill up
            if len(false_options) < self.num_words - 1:
                all_verbs = list(Vocabulary.agentive_verbs.keys()) + list(Vocabulary.non_agentive_verbs.keys()) + list(Vocabulary.ambiguous_verbs.keys())
                for verb in false_options + [correct_second_word]:
                    if verb in all_verbs:
                        all_verbs.remove(verb)
                additional = random.sample(all_verbs, self.num_words - 1 - len(false_options))
                false_options.extend(additional)
            
            options = [correct_second_word] + false_options[:self.num_words - 1]
            random.shuffle(options)
            correct_index = options.index(correct_second_word)
            
            return correct_first_word, correct_second_word, options, correct_index, "verb_pair"
        
        elif gamemode == 3:
            chosen_mode = random.choice([1, 2])
            return self.pick_random_words(chosen_mode)
    
    def succ(self):
        self.score += 100
        print("Score:", self.score)
    
    def fail(self):
        self.score -= 100
        print("Score:", self.score)

    def load_sprites(self):
        pass
    
    # Blocks or enables Player input as long as a bool is True
    def handle_frame_input(self, events, input_blocked):
        pass
        # if input_blocked:
        #     return
        # input

    # Renders game
    def update_frame(self, current_time):
        pass
    
    # Initializes the game with the given screen
    def initialize_game(self, screen):
        pass

    def on_pause(self):
        pygame.mixer.music.pause()

    def on_resume(self, paused_duration):
        if self._bomb_timer_active:
            self._bomb_timer_start_ms += paused_duration
        pygame.mixer.music.unpause()

    def check_answer(self, selected_index, correct_index):
        if selected_index == correct_index:
            correct_sound.play()
            self.succ()
        else:
            wrong_sound.play()
            self.fail()

    # Blocks Player input but lets animation run
    def wait_for_seconds(self, seconds, end_game_after=False):
        start_time = pygame.time.get_ticks()
        end_time = start_time + (seconds * 1000)
        clock = pygame.time.Clock()
        
        while pygame.time.get_ticks() < end_time:
            current_time = pygame.time.get_ticks()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.is_running = False
                    return
            # Continue rendering and animations
            self.update_frame(current_time)
            pygame.display.flip()
            clock.tick(60)
        if end_game_after:
            self.is_running = False


def startGame(gamemode, screen, menu, mytheme, playerName):
    import HogansAlley
    import PraiseOrHaze
    import QuickieQuiz
    import ZeldaRipoff
    import Boss
    
    pygame.display.set_mode((1024, 768))

    pause_menu = pygame_menu.Menu('Pause', 600, 400, theme=mytheme)
    pause_menu.set_relative_position(50, 50)
    
    game_running = True
    paused = False
    pause_start_time = 0
    game_instance = None
    curtain = CurtainTransition()
    
    # Game states
    WAITING_FOR_OPENING = 0
    PLAYING = 1
    WAITING_FOR_CLOSING = 2
    
    game_state = WAITING_FOR_OPENING
    transition_start_time = 0
    
    def resume_game():
        nonlocal paused
        paused = False
        pause_menu.disable()
    
    def quit_to_menu():
        nonlocal game_running, paused, game_instance
        game_running = False
        paused = False
        pause_menu.disable()
        menu.enable()
        pygame.display.set_mode((1024, 768))
        if game_instance is not None:
            game_instance.is_running = False
    
    pause_menu.add.button('Continue', resume_game)
    pause_menu.add.button('Back to Main Menu', quit_to_menu)
    pause_menu.add.button('Exit Game', pygame_menu.events.EXIT)
    
    clock = pygame.time.Clock()
    
    if gamemode == 3:
        Games = [Boss.Boss]
    else: Games = [ZeldaRipoff.ZeldaRipoff]
    GameClass = random.choice(Games)
    game_instance = GameClass(gamemode, playerName=playerName)
    # DO NOT initialize game yet - wait until curtain animation is complete
    
    total_score = 0
    last_score = 0
    music_start_time = None  # Track when to start music (0.2s after animation complete)
    
    # Start the opening curtain animation
    curtain.start_opening_animation(screen)
    
    while game_running:
        current_time = pygame.time.get_ticks()
        
        events = pygame.event.get()
        
        if game_state == WAITING_FOR_OPENING:
            curtain.update(current_time)
            
            if not game_instance.is_running: 
                game_instance.initialize_game(screen)
                pygame.mixer.music.pause()
                music_start_time = current_time + 400
            
            game_instance.update_frame(current_time)
            curtain.render(screen)
            
            if curtain.is_animation_complete():
                if game_instance._bomb_timer_active:
                    game_instance._bomb_timer_start_ms = pygame.time.get_ticks()
                if music_start_time and current_time >= music_start_time:
                    pygame.mixer.music.unpause()
                    music_start_time = None
                
                game_instance.game_actually_started = True
                game_state = PLAYING
        
        elif game_state == PLAYING:
            if not game_instance.is_running:
                total_score = game_instance.score
                game_instance.game_actually_started = False  # Disables bomb timer during transition
                is_success = game_instance.score > last_score
                last_score = game_instance.score
                pygame.mixer.music.pause()
                game_state = WAITING_FOR_CLOSING
                curtain.start_closing_animation(screen, is_success=is_success)
                continue
            
            for event in events:
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = True
                    pause_start_time = pygame.time.get_ticks()
                    game_instance.on_pause()
            
            if paused:
                pause_menu.enable()
                pause_menu.mainloop(screen, disable_loop=False)
                pause_menu.disable()
                paused_duration = pygame.time.get_ticks() - pause_start_time
                game_instance.on_resume(paused_duration)
                paused = False
            else:
                game_instance.handle_frame_input(events, current_time)
                game_instance.update_frame(current_time)
        
        elif game_state == WAITING_FOR_CLOSING:
            curtain.update(current_time)
            game_instance.update_frame(current_time)
            curtain.render(screen)
            
            # Starts a new game
            if curtain.is_animation_complete():
                GameClass = random.choice(Games)
                game_instance = GameClass(gamemode, playerName=playerName)
                game_instance.score = total_score
                game_instance.initialize_game(screen)
                game_state = WAITING_FOR_OPENING
                curtain.start_opening_animation(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.mixer.music.stop()
    return game_running