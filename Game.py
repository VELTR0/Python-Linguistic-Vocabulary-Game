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

    
    def pick_random_words(self):
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

    # Called when the game is paused
    def on_pause(self):
        pygame.mixer.music.pause()

    # Called when the game is resumed
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

    # Blocks Player input for a number of seconds but lets animation run
    def wait_for_seconds(self, seconds, end_game_after=False):
        start_time = pygame.time.get_ticks()
        end_time = start_time + (seconds * 1000)
        clock = pygame.time.Clock()
        
        while pygame.time.get_ticks() < end_time:
            current_time = pygame.time.get_ticks()
            
            # Process events but ignore input
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.is_running = False
                    return
            
            # Continue rendering and animations
            self.update_frame(current_time)
            pygame.display.flip()
            clock.tick(60)
        
        # End game after wait if specified
        if end_game_after:
            self.is_running = False


def startGame(gamemode, screen, menu, mytheme, playerName):
    import HogansAlley
    import PraiseOrHaze
    import QuickieQuiz
    
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
        pygame.display.set_mode((800, 500))
        if game_instance is not None:
            game_instance.is_running = False
    
    pause_menu.add.button('Continue', resume_game)
    pause_menu.add.button('Back to Main Menu', quit_to_menu)
    pause_menu.add.button('Exit Game', pygame_menu.events.EXIT)
    
    clock = pygame.time.Clock()
    
    Games = [PraiseOrHaze.PraiseOrHaze]
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
        
        # Handle game state transitions
        if game_state == WAITING_FOR_OPENING:
            # Update curtain animation
            curtain.update(current_time)
            
            # Initialize the game on first frame of this state
            if not game_instance.is_running:  # Only initialize if not already running
                game_instance.initialize_game(screen)
                # Pause music immediately after initialization
                pygame.mixer.music.pause()
                music_start_time = current_time + 400  # Start music 0.2 seconds later
            
            # Render the game in the background (but without timer running)
            game_instance.update_frame(current_time)
            
            # Render curtain overlay on top
            curtain.render(screen)
            
            # Check if opening animation is complete
            if curtain.is_animation_complete():
                # Reset the bomb timer start time to NOW (not from initialization time)
                if game_instance._bomb_timer_active:
                    game_instance._bomb_timer_start_ms = pygame.time.get_ticks()
                
                # Start music if the time has come
                if music_start_time and current_time >= music_start_time:
                    pygame.mixer.music.unpause()
                    music_start_time = None  # Only play once
                
                # Signal that the game has truly started - bomb timer can now run
                game_instance.game_actually_started = True
                game_state = PLAYING
        
        elif game_state == PLAYING:
            # Check if current game ended - start closing animation
            if not game_instance.is_running:
                total_score = game_instance.score  # Keep the score
                game_instance.game_actually_started = False  # Disable bomb timer during transition
                
                # Determine if the last round was successful (score increased)
                is_success = game_instance.score > last_score
                last_score = game_instance.score
                
                # Pause the game music
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
                # Pass events to game instance for input handling
                game_instance.handle_frame_input(events, current_time)
                # Update game logic and render
                game_instance.update_frame(current_time)
        
        elif game_state == WAITING_FOR_CLOSING:
            # Update curtain closing animation
            curtain.update(current_time)
            
            # Render the game in the background (but without timer running)
            game_instance.update_frame(current_time)
            
            # Render curtain overlay on top
            curtain.render(screen)
            
            # Check if closing animation is complete
            if curtain.is_animation_complete():
                # Start a new game
                GameClass = random.choice(Games)
                game_instance = GameClass(gamemode, playerName=playerName)
                game_instance.score = total_score  # Transfer score to new instance
                game_instance.initialize_game(screen)
                game_state = WAITING_FOR_OPENING
                curtain.start_opening_animation(screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.mixer.music.stop()
    return game_running