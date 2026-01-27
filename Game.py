import pygame
import pygame_menu
import random
import Vocabulary

pygame.init()

correct_sound = pygame.mixer.Sound(r"Sounds/Correct.ogg")
wrong_sound = pygame.mixer.Sound(r"Sounds/Wrong.ogg")

# TODO Übergang zwischen Gamse animieren
class Game:
    def __init__(self, gamemode=1, num_words=4, playerName="Player"):
        self.gamemode = gamemode
        self.num_words = num_words
        self.score = 0
        self.is_running = False
        self.playerName = playerName
    
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

    # Renders game (Take care of Render order)
    def update_frame(self, current_time):
        pass
    
    # Initializes the game with the given screen (Set variables per game)
    def initialize_game(self, screen):
        pass

    # Called when the game is paused
    def on_pause(self):
        pygame.mixer.music.pause()

    # Called when the game is resumed (Adjust this)
    def on_resume(self, paused_duration):
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
    InGame = False
    game_instance = None
    
    def resume_game():
        nonlocal paused
        paused = False
        pause_menu.disable()
    
    def quit_to_menu():
        nonlocal game_running, paused, game_instance, InGame
        game_running = False
        paused = False
        pause_menu.disable()
        menu.enable()
        InGame = False
        pygame.display.set_mode((800, 500))
        if game_instance is not None:
            game_instance.is_running = False
    
    pause_menu.add.button('Continue', resume_game)
    pause_menu.add.button('Back to Main Menu', quit_to_menu)
    pause_menu.add.button('Exit Game', pygame_menu.events.EXIT)
    
    clock = pygame.time.Clock()
    
    Games = [HogansAlley.HogansAlley, PraiseOrHaze.PraiseOrHaze, QuickieQuiz.QuickieQuiz]
    GameClass = random.choice(Games)
    game_instance = GameClass(gamemode, playerName=playerName)
    game_instance.initialize_game(screen)
    
    paused = False
    pause_start_time = 0
    
    while game_running:
        current_time = pygame.time.get_ticks()
        
        #ANIMATION HERE
        events = pygame.event.get()
        
        # Check if current game ended - start a new one
        if not game_instance.is_running:
            GameClass = random.choice(Games)
            # Starts the game with selected gamemode
            game_instance = GameClass(gamemode)
            game_instance.initialize_game(screen)
        
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
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.mixer.music.stop()
    return game_running