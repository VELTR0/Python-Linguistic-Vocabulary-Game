"""
Linguistic Vocabulary Learning Game
A Python game using Pygame for learning vocabulary words
"""

import pygame
import random
import sys
from vocabulary import vocabulary


class VocabularyGame:
    """Main game class for the vocabulary learning game"""
    
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        
        # Screen settings
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Vocabulary Learning Game")
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.BLUE = (0, 100, 200)
        self.GRAY = (200, 200, 200)
        
        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.word_font = pygame.font.Font(None, 48)
        self.option_font = pygame.font.Font(None, 36)
        self.score_font = pygame.font.Font(None, 32)
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"  # menu, playing, game_over
        
        # Game variables
        self.score = 0
        self.total_questions = 0
        self.current_word = None
        self.correct_answer = None
        self.options = []
        self.feedback = ""
        self.feedback_timer = 0
        
        # Vocabulary data
        self.vocabulary = vocabulary
        self.word_list = list(vocabulary.keys())
        
    def new_question(self):
        """Generate a new vocabulary question"""
        if not self.word_list:
            self.game_state = "game_over"
            return
        
        # Select a random word
        self.current_word = random.choice(self.word_list)
        self.correct_answer = self.vocabulary[self.current_word]
        
        # Generate multiple choice options
        all_answers = list(self.vocabulary.values())
        wrong_answers = [ans for ans in all_answers if ans != self.correct_answer]
        
        # Select 3 random wrong answers
        if len(wrong_answers) >= 3:
            selected_wrong = random.sample(wrong_answers, 3)
        else:
            selected_wrong = wrong_answers
        
        # Combine with correct answer and shuffle
        self.options = selected_wrong + [self.correct_answer]
        random.shuffle(self.options)
        
    def check_answer(self, selected_answer):
        """Check if the selected answer is correct"""
        self.total_questions += 1
        
        if selected_answer == self.correct_answer:
            self.score += 1
            self.feedback = "Correct!"
            self.feedback_timer = 60  # Show feedback for 60 frames (1 second at 60 FPS)
        else:
            self.feedback = f"Wrong! Correct answer: {self.correct_answer}"
            self.feedback_timer = 120  # Show feedback for 2 seconds
            
    def draw_menu(self):
        """Draw the main menu screen"""
        self.screen.fill(self.WHITE)
        
        # Title
        title = self.title_font.render("Vocabulary Game", True, self.BLUE)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Instructions
        inst1 = self.option_font.render("Learn vocabulary words!", True, self.BLACK)
        inst1_rect = inst1.get_rect(center=(self.width // 2, 250))
        self.screen.blit(inst1, inst1_rect)
        
        inst2 = self.option_font.render("Click the correct translation", True, self.BLACK)
        inst2_rect = inst2.get_rect(center=(self.width // 2, 300))
        self.screen.blit(inst2, inst2_rect)
        
        # Start button
        button_rect = pygame.Rect(300, 400, 200, 60)
        pygame.draw.rect(self.screen, self.GREEN, button_rect)
        pygame.draw.rect(self.screen, self.BLACK, button_rect, 3)
        
        start_text = self.option_font.render("START", True, self.WHITE)
        start_rect = start_text.get_rect(center=button_rect.center)
        self.screen.blit(start_text, start_rect)
        
        return button_rect
        
    def draw_game(self):
        """Draw the game screen"""
        self.screen.fill(self.WHITE)
        
        # Score
        score_text = self.score_font.render(
            f"Score: {self.score}/{self.total_questions}", 
            True, 
            self.BLACK
        )
        self.screen.blit(score_text, (20, 20))
        
        # Current word
        if self.current_word:
            word_text = self.word_font.render(
                f"Translate: {self.current_word}", 
                True, 
                self.BLUE
            )
            word_rect = word_text.get_rect(center=(self.width // 2, 100))
            self.screen.blit(word_text, word_rect)
        
        # Options
        option_rects = []
        for i, option in enumerate(self.options):
            y_pos = 200 + i * 80
            option_rect = pygame.Rect(200, y_pos, 400, 60)
            
            # Draw button
            pygame.draw.rect(self.screen, self.GRAY, option_rect)
            pygame.draw.rect(self.screen, self.BLACK, option_rect, 2)
            
            # Draw text
            option_text = self.option_font.render(option, True, self.BLACK)
            text_rect = option_text.get_rect(center=option_rect.center)
            self.screen.blit(option_text, text_rect)
            
            option_rects.append(option_rect)
        
        # Feedback
        if self.feedback_timer > 0:
            color = self.GREEN if "Correct" in self.feedback else self.RED
            feedback_text = self.word_font.render(self.feedback, True, color)
            feedback_rect = feedback_text.get_rect(center=(self.width // 2, 520))
            self.screen.blit(feedback_text, feedback_rect)
            self.feedback_timer -= 1
            
        return option_rects
        
    def draw_game_over(self):
        """Draw the game over screen"""
        self.screen.fill(self.WHITE)
        
        # Game Over text
        title = self.title_font.render("Game Over!", True, self.BLUE)
        title_rect = title.get_rect(center=(self.width // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Final score
        score_text = self.word_font.render(
            f"Final Score: {self.score}/{self.total_questions}", 
            True, 
            self.BLACK
        )
        score_rect = score_text.get_rect(center=(self.width // 2, 250))
        self.screen.blit(score_text, score_rect)
        
        # Percentage
        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100
            percent_text = self.option_font.render(
                f"Accuracy: {percentage:.1f}%", 
                True, 
                self.BLACK
            )
            percent_rect = percent_text.get_rect(center=(self.width // 2, 320))
            self.screen.blit(percent_text, percent_rect)
        
        # Play again button
        button_rect = pygame.Rect(250, 400, 300, 60)
        pygame.draw.rect(self.screen, self.GREEN, button_rect)
        pygame.draw.rect(self.screen, self.BLACK, button_rect, 3)
        
        again_text = self.option_font.render("PLAY AGAIN", True, self.WHITE)
        again_rect = again_text.get_rect(center=button_rect.center)
        self.screen.blit(again_text, again_rect)
        
        return button_rect
        
    def handle_events(self, clickable_rects):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                
                if self.game_state == "menu":
                    if clickable_rects.collidepoint(mouse_pos):
                        self.game_state = "playing"
                        self.score = 0
                        self.total_questions = 0
                        self.new_question()
                        
                elif self.game_state == "playing":
                    # Only allow clicking if no feedback is showing
                    if self.feedback_timer == 0:
                        for i, rect in enumerate(clickable_rects):
                            if rect.collidepoint(mouse_pos):
                                self.check_answer(self.options[i])
                                pygame.time.wait(500)  # Brief pause to show feedback
                                if self.feedback_timer > 0:
                                    # Wait for feedback to be visible
                                    pygame.time.wait(1000)
                                self.new_question()
                                break
                                
                elif self.game_state == "game_over":
                    if clickable_rects.collidepoint(mouse_pos):
                        self.game_state = "menu"
                        
    def run(self):
        """Main game loop"""
        while self.running:
            clickable_rects = None
            
            if self.game_state == "menu":
                clickable_rects = self.draw_menu()
            elif self.game_state == "playing":
                clickable_rects = self.draw_game()
            elif self.game_state == "game_over":
                clickable_rects = self.draw_game_over()
                
            self.handle_events(clickable_rects)
            
            pygame.display.flip()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()


def main():
    """Main entry point"""
    game = VocabularyGame()
    game.run()


if __name__ == "__main__":
    main()
