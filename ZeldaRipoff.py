import pygame
import Vocabulary
import random
import math
from Game import Game
from Font import SpriteFont

pygame.init()

class ZeldaRipoff(Game):
    DISPLAY_TIME = 1500  
    WAIT_TIME = 1000
    ANSWER_DISPLAY_TIME = 1000  # Wait time after answer before ending game
    BOMB_TIMER_SECONDS = 7

    class player(object):
        def __init__(self,x,y,width,height, screen):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = 5
            self.walkCount= 0
            self.current_direction = None
            self.standing = True
            self.hitbox = None
            self.attack = False

    class enemy(object):
        def __init__(self, x, y, width, height, screen, center_x, center_y, radius):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = 2
            self.screen = screen
            self.center_x = center_x
            self.center_y = center_y
            self.radius = radius
            self.angle = 0
            self.is_alive = True
        
        def update_position(self):
            self.angle += 0.05
            self.x = self.center_x + self.radius * math.cos(self.angle) - self.width / 2
            self.y = self.center_y + self.radius * math.sin(self.angle) - self.height / 2
        
        def get_hitbox(self):
            return pygame.Rect(self.x, self.y, self.width, self.height)

    DISPLAY_TIME = 2000
    ANSWER_DISPLAY_TIME = 1000
    BOMB_TIMER_SECONDS = 5
    
    def __init__(self, gamemode=1, playerName="Player"):
        super().__init__(gamemode, num_words=4, playerName=playerName)
        self.GAMEMODE = gamemode
        self.font_options = SpriteFont()
        self.load_sprites()
    
    def load_sprites(self):
        self.background_image = pygame.image.load(r"Sprites\ZeldaRipoff\Background.png")
        self.background_image2 = pygame.image.load(r"Sprites\ZeldaRipoff\Background2.png")
        self.card_image = pygame.image.load(r"Sprites\QuickieQuiz\Card.png")
        self.won_sound = pygame.mixer.Sound(r"Sounds\Won.wav")
        self.won_image = pygame.image.load(r"Sprites\ZeldaRipoff\Won.png")
        self.lost_sound = pygame.mixer.Sound(r"Sounds\Lost.wav")
        self.lost_image = pygame.image.load(r"Sprites\ZeldaRipoff\Lost.png")
        self.character_image_down = pygame.image.load(r"Sprites\ZeldaRipoff\Character.png")
        self.character_image_up = pygame.image.load(r"Sprites\ZeldaRipoff\Character_Up.png")
        self.character_image_left = pygame.image.load(r"Sprites\ZeldaRipoff\Character_Left.png")
        self.character_image_right = pygame.image.load(r"Sprites\ZeldaRipoff\Character_Right.png")
        self.character_left_walking = [pygame.image.load(r"Sprites\ZeldaRipoff\l1.png"),
                                       pygame.image.load(r"Sprites\ZeldaRipoff\l2.png")]
        self.character_right_walking = [pygame.image.load(r"Sprites\ZeldaRipoff\r1.png"),
                                        pygame.image.load(r"Sprites\ZeldaRipoff\r2.png")]
        self.character_up_walking = [pygame.image.load(r"Sprites\ZeldaRipoff\u1.png"),
                                     pygame.image.load(r"Sprites\ZeldaRipoff\u2.png")]
        self.character_down_walking = [pygame.image.load(r"Sprites\ZeldaRipoff\d1.png"),
                                       pygame.image.load(r"Sprites\ZeldaRipoff\d2.png")]
        self.correct_image = pygame.image.load(r"Sprites\ZeldaRipoff\Correct.png")
        self.wrong_image = pygame.image.load(r"Sprites\ZeldaRipoff\Wrong.png")
    
    def scale_assets(self, screen):
        assets = {}
        assets['background_scaled'] = pygame.transform.scale(self.background_image, (screen.get_width(), screen.get_height()))
        char_height = screen.get_height() // 12
        char_width = int(char_height * self.character_image_down.get_width() / self.character_image_down.get_height())
        assets['character_scaled'] = pygame.transform.scale(self.character_image_down, (char_width, char_height))
        assets['character_left_scaled'] = pygame.transform.scale(self.character_image_left, (char_width, char_height))
        assets['character_right_scaled'] = pygame.transform.scale(self.character_image_right, (char_width, char_height))   
        assets['character_up_scaled'] = pygame.transform.scale(self.character_image_up, (char_width, char_height))
        assets['character_left_walking_scaled'] = [pygame.transform.scale(img, (char_width, char_height)) for img in self.character_left_walking]
        assets['character_right_walking_scaled'] = [pygame.transform.scale(img, (char_width, char_height)) for img in self.character_right_walking]
        assets['character_up_walking_scaled'] = [pygame.transform.scale(img, (char_width, char_height)) for img in self.character_up_walking]
        assets['character_down_walking_scaled'] = [pygame.transform.scale(img, (char_width, char_height)) for img in self.character_down_walking]
        assets['correct_scaled'] = pygame.transform.scale(self.correct_image, (char_width, char_height))
        assets['wrong_scaled'] = pygame.transform.scale(self.wrong_image, (char_width, char_height))
        assets['card_scaled'] = pygame.transform.scale(self.card_image, (int(char_width * 3), int(char_height * 0.5)))
        assets['won_scaled'] = pygame.transform.scale(self.won_image, (char_width, char_height))
        assets['lost_scaled'] = pygame.transform.scale(self.lost_image, (char_width, char_height))
        self.hitbox = (self.player_obj.x, self.player_obj.y, char_width, char_height)
        return assets

    def initialize_game(self, screen):
        self.is_running = True
        self.screen = screen
        
        # Game state
        self.correct_urdu = ""
        self.correct_english = ""
        self.options = []
        self.correct_index = 0
        self.selection_made = False
        self.last_action_time = 0
        self.round_start_time = pygame.time.get_ticks()
        self.show_word_display = True
        self.current_word_type = None
        self.agentive_question = False
        self.word_selected = False
        self.show_question = True
        self.show_options = False
        self.selected_word_index = -1
        self.is_correct = False
        
        # Player
        player_start_x = screen.get_width() / 2 - screen.get_width() / 30
        player_start_y = screen.get_height() / 2 - screen.get_height() / 24
        self.player_obj = self.player(player_start_x, player_start_y, screen.get_width() / 15, screen.get_height() / 12, screen)
        
        # Enemy
        # char_height = screen.get_height() // 10
        # char_width = int(char_height * self.character_image_down.get_width() / self.character_image_down.get_height())
        # enemy_start_x = screen.get_width() / 2
        # enemy_start_y = screen.get_height() / 2 - 150
        # self.enemy_obj = self.enemy(enemy_start_x, enemy_start_y, char_width, char_height, screen, screen.get_width() / 2, screen.get_height() / 2, 150)
        
        # Music
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"Sounds/Overworld.mp3")
        pygame.mixer.music.play(-1)
        
        # Scale assets
        scaled_assets = self.scale_assets(screen)
        self.character_scaled = scaled_assets['character_scaled']
        self.character_left_scaled = scaled_assets['character_left_scaled']
        self.character_right_scaled = scaled_assets['character_right_scaled']
        self.character_up_scaled = scaled_assets['character_up_scaled']
        self.character_left_walking_scaled = scaled_assets['character_left_walking_scaled']
        self.character_right_walking_scaled = scaled_assets['character_right_walking_scaled']
        self.character_up_walking_scaled = scaled_assets['character_up_walking_scaled']
        self.character_down_walking_scaled = scaled_assets['character_down_walking_scaled']
        self.correct_scaled = scaled_assets['correct_scaled']
        self.wrong_scaled = scaled_assets['wrong_scaled']
        self.card_scaled = scaled_assets['card_scaled']
        self.won_scaled = scaled_assets['won_scaled']
        self.lost_scaled = scaled_assets['lost_scaled']
        
        # Start first round
        self.correct_urdu, self.correct_english, self.options, self.correct_index, self.current_word_type = self.pick_random_words(self.gamemode)
        self.agentive_question = (self.current_word_type == "agentive")
        
        if self.current_word_type == "agentive":
            self.background_scaled = pygame.transform.scale(self.background_image2, (screen.get_width(), screen.get_height()))
            self.background_pixel_map = pygame.transform.scale(self.background_image2, (screen.get_width(), screen.get_height()))
        else:
            self.background_scaled = pygame.transform.scale(self.background_image, (screen.get_width(), screen.get_height()))
            self.background_pixel_map = pygame.transform.scale(self.background_image, (screen.get_width(), screen.get_height()))
        
        self.word_positions = [self.get_word_position(i, screen, self.current_word_type) for i in range(len(self.options))]
        
        self.BombTimer(self.BOMB_TIMER_SECONDS)
    
    def is_green_pixel(self, r, g, b):
        green_pixel = g > 100 and g > r + 50 and g > b + 50
        return green_pixel
    
    def get_word_position(self, word_index, screen, word_type=None):
        width = screen.get_width()
        height = screen.get_height()
        if word_type == "agentive":
            positions = [
                (width * 0.85, height * 0.06),
                (width * 0.15, height * 0.94)
            ]
        else:
            positions = [
                (width * 0.15, height * 0.06),
                (width * 0.46, height * 0.06),
                (width * 0.85, height * 0.06), 
                (width * 0.15, height * 0.94)
            ]
        
        return positions[word_index % len(positions)]
    
    def check_collision(self, x, y, width, height):
        left = max(0, int(x))
        top = max(0, int(y))
        right = min(self.background_pixel_map.get_width(), int(x + width))
        bottom = min(self.background_pixel_map.get_height(), int(y + height))
        step = 5
        for px in range(left, right, step):
            for py in range(top, bottom, step):
                try:
                    pixel_color = self.background_pixel_map.get_at((px, py))
                    r, g, b = pixel_color[0], pixel_color[1], pixel_color[2]
                    if self.is_green_pixel(r, g, b):
                        return True
                except:
                    pass
        
        return False
    
    def get_question_text(self):
        if self.current_word_type == "agentive":
            return f"Is \"{self.correct_urdu}\" agentive?"
        elif self.current_word_type == "english":
            return f"Translate \"{self.correct_urdu}\""
        elif self.current_word_type == "urdu":
            return f"Translate \"{self.correct_english}\""
        elif self.current_word_type == "verb_pair":
            return f"What verb goes with \"{self.correct_urdu}\""
        return ""

    def handle_frame_input(self, events, current_time):
        if self.word_selected:
            return
        
        for event in events:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.player_obj.attack = True
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.player_obj.current_direction = 'down'
                self.player_obj.standing = False
            elif pygame.key.get_pressed()[pygame.K_UP]:
                self.player_obj.current_direction = 'up'
                self.player_obj.standing = False
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.player_obj.current_direction = 'left'
                self.player_obj.standing = False
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.player_obj.current_direction = 'right'
                self.player_obj.standing = False
            else:
                self.player_obj.standing = True


    def update_frame(self, current_time):
        char_width = self.character_scaled.get_width()
        char_height = self.character_scaled.get_height()
        
        if not self.player_obj.standing:
            new_x = self.player_obj.x
            new_y = self.player_obj.y
            
            if self.player_obj.current_direction == 'left':
                new_x -= self.player_obj.vel
            elif self.player_obj.current_direction == 'right':
                new_x += self.player_obj.vel
            elif self.player_obj.current_direction == 'up':
                new_y -= self.player_obj.vel
            elif self.player_obj.current_direction == 'down':
                new_y += self.player_obj.vel
            
            if not self.check_collision(new_x, new_y, char_width, char_height):
                self.player_obj.x = new_x
                self.player_obj.y = new_y
            
            self.player_obj.walkCount += 1
        
        self.screen.blit(self.background_scaled, (0, 0))
        
        if self.show_question and current_time - self.round_start_time < self.DISPLAY_TIME:
            question_text = self.get_question_text()
            question_surface = self.font_options.render(question_text, scale=3, color=(255, 255, 0))
            question_rect = question_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 3))
            self.screen.blit(question_surface, question_rect)
        elif current_time - self.round_start_time >= self.DISPLAY_TIME:
            self.show_question = False
            self.show_options = True
        
        # Renders player
        if self.word_selected:
            if self.is_correct:
                self.screen.blit(self.won_scaled, (self.player_obj.x, self.player_obj.y))
            else:
                self.screen.blit(self.lost_scaled, (self.player_obj.x, self.player_obj.y))
        elif self.player_obj.standing:
            if self.player_obj.current_direction == 'left':
                self.screen.blit(self.character_left_scaled, (self.player_obj.x, self.player_obj.y))
            elif self.player_obj.current_direction == 'right':
                self.screen.blit(self.character_right_scaled, (self.player_obj.x, self.player_obj.y))
            elif self.player_obj.current_direction == 'up':
                self.screen.blit(self.character_up_scaled, (self.player_obj.x, self.player_obj.y))
            else:
                self.screen.blit(self.character_scaled, (self.player_obj.x, self.player_obj.y))
        else:
            if self.player_obj.current_direction == 'left':
                sprite_index = (self.player_obj.walkCount // 5) % len(self.character_left_walking_scaled)
                self.screen.blit(self.character_left_walking_scaled[sprite_index], (self.player_obj.x, self.player_obj.y))
            elif self.player_obj.current_direction == 'right':
                sprite_index = (self.player_obj.walkCount // 5) % len(self.character_right_walking_scaled)
                self.screen.blit(self.character_right_walking_scaled[sprite_index], (self.player_obj.x, self.player_obj.y))
            elif self.player_obj.current_direction == 'up':
                sprite_index = (self.player_obj.walkCount // 5) % len(self.character_up_walking_scaled)
                self.screen.blit(self.character_up_walking_scaled[sprite_index], (self.player_obj.x, self.player_obj.y))
            elif self.player_obj.current_direction == 'down':
                sprite_index = (self.player_obj.walkCount // 5) % len(self.character_down_walking_scaled)
                self.screen.blit(self.character_down_walking_scaled[sprite_index], (self.player_obj.x, self.player_obj.y))
        
        # renders Attack Hitbox
        # if self.player_obj.attack:
        #     attack_size = 50
        #     char_center_x = self.player_obj.x + self.character_scaled.get_width() / 2
        #     char_center_y = self.player_obj.y + self.character_scaled.get_height() / 2
        #     attack_rect = None
        #     if self.player_obj.current_direction == 'left':
        #         attack_rect = pygame.Rect(char_center_x - attack_size - 25, char_center_y - 25, attack_size, 50)
        #     elif self.player_obj.current_direction == 'right':
        #         attack_rect = pygame.Rect(char_center_x + 25, char_center_y - 25, attack_size, 50)
        #     elif self.player_obj.current_direction == 'up':
        #         attack_rect = pygame.Rect(char_center_x - 25, char_center_y - attack_size - 25, 50, attack_size)
        #     elif self.player_obj.current_direction == 'down':
        #         attack_rect = pygame.Rect(char_center_x - 25, char_center_y + 25, 50, attack_size)
        #     if attack_rect:
        #         pygame.draw.rect(self.screen, (255, 0, 0), attack_rect, 3)
        #         # Collision Detection with Enemy
        #         if self.enemy_obj.is_alive and attack_rect.colliderect(self.enemy_obj.get_hitbox()):
        #             self.enemy_obj.is_alive = False
        #     self.player_obj.attack = False
        
        # Render Enemy
        # if self.enemy_obj.is_alive:
        #     self.enemy_obj.update_position()
        #     enemy_hitbox = self.enemy_obj.get_hitbox()
        #     pygame.draw.rect(self.screen, (0, 255, 0), enemy_hitbox, 3)
        
        # Rendering
        if self.show_options:
            player_hitbox = pygame.Rect(self.player_obj.x, self.player_obj.y, char_width, char_height)
            
            for i, word in enumerate(self.options):
                x, y = self.word_positions[i]
                
                card_rect = self.card_scaled.get_rect(center=(x, y))
                self.screen.blit(self.card_scaled, card_rect)
                
                display_text = word
                if self.current_word_type == "agentive":
                    if word == "agentive":
                        display_text = "Yes"
                    elif word == "non-agentive":
                        display_text = "No"
                
                word_surface = self.font_options.render(display_text, scale=2, color=(255, 255, 255))
                word_rect = word_surface.get_rect(center=(x, y))
                self.screen.blit(word_surface, word_rect)
                
                # Resize hitbox of options
                word_hitbox = word_rect.inflate(100, 100) 
                if player_hitbox.colliderect(word_hitbox) and not self.word_selected:
                    self.word_selected = True
                    self.selected_word_index = i
                    self.player_obj.standing = True
                    self.last_action_time = current_time  
                    if i == self.correct_index:
                        self.is_correct = True
                        self.won_sound.play()
                        self.succ() 
                    else:
                        self.is_correct = False
                        self.lost_sound.play()
                        self.fail()  #
        
        if self.word_selected and current_time - self.last_action_time >= self.WAIT_TIME:
            self.is_running = False
        
        self.bomb_logic(current_time)
        
        if self._bomb_timer_just_ended and not self.word_selected:
            self.word_selected = True
            self.is_correct = False
            self.lost_sound.play()
            self.fail()  
            self.last_action_time = current_time
            self._bomb_timer_just_ended = False