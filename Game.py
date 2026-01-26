import pygame
import pygame_menu
import random
import Vocabulary

DIFFICULTY = "hard"

pygame.init()


class Game:
    def __init__(self, difficulty="easy", num_words=4):
        self.difficulty = difficulty
        self.num_words = num_words
        self.correct_count = 0
        self.incorrect_count = 0
        self.is_running = False
    
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
    
    def add_correct(self):
        self.correct_count += 1
        print("Correct answers:", self.correct_count)
    
    def add_incorrect(self):
        self.incorrect_count += 1
        print("Incorrect answers:", self.incorrect_count)
    
    def get_stats(self):
        return {
            "correct": self.correct_count,
            "incorrect": self.incorrect_count,
            "total": self.correct_count + self.incorrect_count
        }
    
    def start_minigame(self, screen):
        pass

    def on_pause(self):
        pass


def startGame(current_gamemode, screen, menu, mytheme):
    import HogansAlley
    import PraiseOrHaze
    import QuickieQuiz
    
    pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Game 1")

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
    
    Games = [HogansAlley.HogansAlley, QuickieQuiz.QuickieQuiz]
    GameClass = random.choice(Games)
    game_instance = GameClass(difficulty=DIFFICULTY)
    game_instance.initialize_game(screen)
    
    paused = False
    pause_start_time = 0
    
    while game_running:
        current_time = pygame.time.get_ticks()
        events = pygame.event.get()
        
        # Check if current game ended - start a new one
        if not game_instance.is_running:
            # Save statistics from previous game
            old_correct = game_instance.correct_count
            old_incorrect = game_instance.incorrect_count
            
            GameClass = random.choice(Games)
            game_instance = GameClass(difficulty=DIFFICULTY)
            
            # Restore statistics
            game_instance.correct_count = old_correct
            game_instance.incorrect_count = old_incorrect
            
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