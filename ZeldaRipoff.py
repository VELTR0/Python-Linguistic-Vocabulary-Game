import pygame
import Vocabulary
import random
from Game import Game
from Font import SpriteFont

pygame.init()

class ZeldaRipoff(Game):

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
        char_height = screen.get_height() // 10
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
        
        # Player
        player_start_x = screen.get_width() / 2 - screen.get_width() / 30
        player_start_y = screen.get_height() / 2 - screen.get_height() / 24
        self.player_obj = self.player(player_start_x, player_start_y, screen.get_width() / 15, screen.get_height() / 12, screen)
        
        # Music
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"Sounds/PenguinShuffle.ogg")
        pygame.mixer.music.play(-1)
        
        # Scale assets
        scaled_assets = self.scale_assets(screen)
        self.background_scaled = scaled_assets['background_scaled']
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
        
        # Start first round
        self.correct_urdu, self.correct_english, self.options, self.correct_index, self.current_word_type = self.pick_random_words(self.gamemode)
        self.agentive_question = (self.current_word_type == "agentive")
        self.BombTimer(self.BOMB_TIMER_SECONDS)

    def handle_frame_input(self, events, current_time):
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
        # Update player position
        if not self.player_obj.standing:
            if self.player_obj.current_direction == 'left':
                self.player_obj.x -= self.player_obj.vel
            elif self.player_obj.current_direction == 'right':
                self.player_obj.x += self.player_obj.vel
            elif self.player_obj.current_direction == 'up':
                self.player_obj.y -= self.player_obj.vel
            elif self.player_obj.current_direction == 'down':
                self.player_obj.y += self.player_obj.vel
            self.player_obj.walkCount += 1
        
        self.screen.blit(self.background_scaled, (0, 0))
        
        # Renders the player
        if self.player_obj.standing:
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
        if self.player_obj.attack:
            attack_size = 50
            char_center_x = self.player_obj.x + self.character_scaled.get_width() / 2
            char_center_y = self.player_obj.y + self.character_scaled.get_height() / 2
            attack_rect = None
            if self.player_obj.current_direction == 'left':
                attack_rect = pygame.Rect(char_center_x - attack_size - 25, char_center_y - 25, attack_size, 50)
            elif self.player_obj.current_direction == 'right':
                attack_rect = pygame.Rect(char_center_x + 25, char_center_y - 25, attack_size, 50)
            elif self.player_obj.current_direction == 'up':
                attack_rect = pygame.Rect(char_center_x - 25, char_center_y - attack_size - 25, 50, attack_size)
            elif self.player_obj.current_direction == 'down':
                attack_rect = pygame.Rect(char_center_x - 25, char_center_y + 25, 50, attack_size)
            if attack_rect:
                pygame.draw.rect(self.screen, (255, 0, 0), attack_rect, 3)
            self.player_obj.attack = False
        
        self.bomb_logic(current_time)