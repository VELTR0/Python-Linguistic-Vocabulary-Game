import pygame
import pygame_menu
import random
import Vocabulary
from abc import ABC, abstractmethod

DIFFICULTY = "easy"

pygame.init()


class Game(ABC):
    def __init__(self, difficulty="easy", num_words=4):
        self.difficulty = difficulty
        self.num_words = num_words
        self.correct_count = 0
        self.incorrect_count = 0
        self.is_running = False
    
    def select_correct_pair(self):
        wordpair = random.choice(list(Vocabulary.lightVerbs.items()))
        correct_urdu = wordpair[0]
        correct_english = wordpair[1]
        return correct_urdu, correct_english
    
    def build_options(self, correct_urdu, correct_english):
        word_type = random.choice(["english", "urdu"])

        if word_type == "english":
            pool = list(Vocabulary.lightVerbs.values())
            if correct_english in pool:
                pool.remove(correct_english)
            correct_word = correct_english
        else:
            pool = list(Vocabulary.lightVerbs.keys())
            if correct_urdu in pool:
                pool.remove(correct_urdu)
            correct_word = correct_urdu

        false_options = random.sample(pool, self.num_words - 1)
        options = [correct_word] + false_options
        random.shuffle(options)
        correct_index = options.index(correct_word)
        return options, correct_index, word_type
    
    def pick_random_words(self):
        correct_urdu, correct_english = self.select_correct_pair()
        options, correct_index, word_type = self.build_options(correct_urdu, correct_english)
        return correct_urdu, correct_english, options, correct_index, word_type
    
    def record_correct_answer(self):
        self.correct_count += 1
    
    def record_incorrect_answer(self):
        self.incorrect_count += 1
    
    def get_stats(self):
        return {
            "correct": self.correct_count,
            "incorrect": self.incorrect_count,
            "total": self.correct_count + self.incorrect_count
        }
    
    @abstractmethod
    def start_game(self, screen):
        pass
    
    def end_game(self):
        self.is_running = False


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
    
    def resume_game():
        nonlocal paused
        paused = False
        pause_menu.disable()
    
    def quit_to_menu():
        nonlocal game_running
        nonlocal paused
        game_running = False
        paused = False
        pause_menu.disable()
        menu.enable()
        nonlocal InGame
        InGame = False
        pygame.display.set_mode((800, 500))
    
    pause_menu.add.button('Continue', resume_game)
    pause_menu.add.button('Back to Main Menu', quit_to_menu)
    pause_menu.add.button('Exit Game', pygame_menu.events.EXIT)
    
    clock = pygame.time.Clock()
    
    while game_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if paused:
                        pause_menu.enable()
        
        if paused:
            pause_menu.enable() 
            pause_menu.mainloop(screen, disable_loop=True)
        else:
            screen.fill((0, 0, 0))
            
            
            # TODO: add more game classes here
            Games = [HogansAlley.HogansAlley]

            if InGame == False:
                GameClass = random.choice(Games)
                pygame.display.set_caption(GameClass.__name__)
                game_instance = GameClass(difficulty=DIFFICULTY, num_words=4)
                game_instance.start_game(screen)
                InGame = True
            else:
                pass
        
        pygame.display.flip()
        clock.tick(60)
    
    return game_running