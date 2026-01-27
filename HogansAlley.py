import pygame
import pygame_menu
import random
from Font import SpriteFont
from Game import Game

pygame.init()
# TODO agentive/non agentive

class HogansAlley(Game):
    DISPLAY_TIME = 1000  
    WAIT_TIME = 1800
    ANSWER_DISPLAY_TIME = 1000  # Wait time after answer before ending game
    
    def __init__(self, gamemode=1, playerName="Player"):
        super().__init__(gamemode, playerName=playerName)
        self.GAMEMODE = gamemode
        self.font_options = SpriteFont()
        self.load_sprites()
        self.scaled_assets = None
    
    def load_sprites(self):
        self.background_image = pygame.image.load(r"Sprites\HogansAlley\Screen.png")
        self.thug1_image = pygame.image.load(r"Sprites\HogansAlley\Thug1.png")
        self.thug2_image = pygame.image.load(r"Sprites\HogansAlley\Thug2.png")
        self.thug3_image = pygame.image.load(r"Sprites\HogansAlley\Thug3.png")
        self.woman_image = pygame.image.load(r"Sprites\HogansAlley\Woman.png")
        self.policeman_image = pygame.image.load(r"Sprites\HogansAlley\Policeman.png")
        self.stick_image = pygame.image.load(r"Sprites\HogansAlley\Stick.png")
        self.unfolding_image = pygame.image.load(r"Sprites\HogansAlley\Unfolding.png")
        self.hit_image = pygame.image.load(r"Sprites\HogansAlley\Hit.png")
        self.unfolding_flash_image = pygame.image.load(r"Sprites\HogansAlley\UnfoldingFlash.png")
        self.hit_flash_image = pygame.image.load(r"Sprites\HogansAlley\HitFlash.png")
        self.crosshair_image = pygame.image.load(r"Sprites\HogansAlley\Crosshair.png")
        self.wrong_image = pygame.image.load(r"Sprites\QuickieQuiz\Wrong.png")
        self.barrel_mid_image = pygame.image.load(r"Sprites\HogansAlley\BarrelMid.png")
        self.barrel_farleft_image = pygame.image.load(r"Sprites\HogansAlley\BarrelFarLeft.png")
        self.barrel_farright_image = pygame.image.load(r"Sprites\HogansAlley\BarrelFarRight.png")
        self.monitor_image = pygame.image.load(r"Sprites\HogansAlley\Monitor.png")
    
    def scale_assets(self, screen):
        assets = {}
        assets['background_scaled'] = pygame.transform.scale(self.background_image, (screen.get_width(), screen.get_height()))
        assets['character_scale'] = ((screen.get_height() / 2.75) * 0.6, screen.get_height() / 2.75)
        
        stick_height = screen.get_height() / 2.5
        stick_width = int(stick_height * 0.1)
        assets['stick_scaled'] = pygame.transform.scale(self.stick_image, (stick_width, stick_height))
        
        unfolding_scale = (assets['character_scale'][0] * 0.3, int(assets['character_scale'][1]))
        assets['unfolding_scaled'] = pygame.transform.scale(self.unfolding_image, unfolding_scale)
        assets['unfolding_flash_scaled'] = pygame.transform.scale(self.unfolding_flash_image, unfolding_scale)
        assets['hit_scaled'] = pygame.transform.scale(self.hit_image, assets['character_scale'])
        assets['hit_flash_scaled'] = pygame.transform.scale(self.hit_flash_image, assets['character_scale'])
        
        assets['thug_sprites'] = [
            pygame.transform.scale(self.thug1_image, assets['character_scale']),
            pygame.transform.scale(self.thug2_image, assets['character_scale']),
            pygame.transform.scale(self.thug3_image, assets['character_scale'])
        ]
        assets['civilian_sprites'] = [
            pygame.transform.scale(self.woman_image, assets['character_scale']),
            pygame.transform.scale(self.policeman_image, assets['character_scale'])
        ]
        
        assets['crosshair_scaled'] = pygame.transform.scale(self.crosshair_image, (assets['character_scale'][0], assets['character_scale'][0]))
        assets['wrong_scaled'] = pygame.transform.scale(self.wrong_image, assets['character_scale'])
        
        barrel_height = screen.get_height() / 3
        barrel_width = int(barrel_height * 1.0)
        assets['barrel_mid_scaled'] = pygame.transform.scale(self.barrel_mid_image, (barrel_width, barrel_height))
        assets['barrel_farleft_scaled'] = pygame.transform.scale(self.barrel_farleft_image, (barrel_width, barrel_height))
        assets['barrel_farright_scaled'] = pygame.transform.scale(self.barrel_farright_image, (barrel_width, barrel_height))
        assets['monitor_scaled'] = pygame.transform.scale(self.monitor_image, (screen.get_width(), screen.get_height()))
        
        return assets
    
    def assign_character_sprites(self, correct_index, num_options, thug_sprites, civilian_sprites):
        sprites = []
        used_civilian_idx = -1
        
        for i in range(num_options):
            if i == correct_index:
                sprites.append(random.choice(thug_sprites))
            else:
                used_civilian_idx = (used_civilian_idx + 1) % len(civilian_sprites)
                sprites.append(civilian_sprites[used_civilian_idx])
        
        return sprites
    
    def update_animations(self, current_time, selection_made, last_frame_time, animation_frame_index, animation_frames, frame_duration):
        if selection_made and current_time - last_frame_time >= frame_duration:
            new_animation_frame_index = (animation_frame_index + 1) % len(animation_frames)
            new_last_frame_time = current_time
            return new_animation_frame_index, new_last_frame_time
        return animation_frame_index, last_frame_time
    
    def calculate_stick_animation_progress(self, current_time, round_start_time):
        elapsed_time = current_time - round_start_time
        return min(1.0, elapsed_time / self.DISPLAY_TIME)
    
    def render_game(self, screen, show_urdu_display, current_time, round_start_time,
                    options, centers, y, character_scale, stick_scaled, unfolding_scaled, character_sprites,
                    selection_made, selected_index, animation_frames, animation_frame_index,
                    show_wrong, show_correct, correct_index, crosshair_scaled, wrong_scaled,
                    display_word, barrel_farleft_scaled, barrel_farright_scaled, barrel_mid_scaled,
                    background_scaled, monitor_scaled, spacing):
        screen.blit(background_scaled, (0, 0))
        n = len(options)
        
        if n == 0:
            return

        if show_urdu_display:
            progress = self.calculate_stick_animation_progress(current_time, round_start_time)
            elapsed_time = current_time - round_start_time
            
            for i, word in enumerate(options):
                cx_final = centers[i][0]
                x_init = -character_scale[0] - spacing * (n - 1 - i)
                x_current = x_init + (cx_final - x_init) * progress
                stick_rect = stick_scaled.get_rect(center=(x_current, y))
                screen.blit(stick_scaled, stick_rect)
                
                if elapsed_time / self.WAIT_TIME >= 0.9:
                    unfolding_rect = unfolding_scaled.get_rect(center=(cx_final, y-20))
                    screen.blit(unfolding_scaled, unfolding_rect)
        else:
            for i in range(n):
                cx, cy = centers[i]
                stick_rect = stick_scaled.get_rect(center=(cx, y))
                screen.blit(stick_scaled, stick_rect)

            for i, word in enumerate(options):
                cx, cy = centers[i]
                
                if selection_made and i == selected_index:
                    current_animation_frame = animation_frames[animation_frame_index]
                    if current_animation_frame is not None:
                        anim_rect = current_animation_frame.get_rect(center=(cx, cy-20))
                        screen.blit(current_animation_frame, anim_rect)
                else:
                    char_rect = character_sprites[i].get_rect(center=(cx, cy-20))
                    screen.blit(character_sprites[i], char_rect)
                    text_surface = self.font_options.render(word, color=(255, 255, 255))
                    text_surface = pygame.transform.scale_by(text_surface, 2.5)
                    text_rect = text_surface.get_rect(center=(cx, cy))
                    screen.blit(text_surface, text_rect)
                
                if i == selected_index:
                    crosshair_rect = crosshair_scaled.get_rect(center=(cx, cy))
                    screen.blit(crosshair_scaled, crosshair_rect)
                
                if show_wrong and i != correct_index:
                    char_rect = character_sprites[i].get_rect(center=(cx, cy-20))
                    screen.blit(wrong_scaled, char_rect)
                
                if show_correct and i == correct_index:
                    crosshair_rect = crosshair_scaled.get_rect(center=(cx, cy))
                    screen.blit(crosshair_scaled, crosshair_rect)

        if show_urdu_display:
            prompt_surface = self.font_options.render(("The Thug is... " + display_word), color=(255, 255, 0))
            prompt_surface = pygame.transform.scale_by(prompt_surface, 5)
            prompt_rect = prompt_surface.get_rect(center=(screen.get_width()/2, screen.get_height()/3))
            screen.blit(prompt_surface, prompt_rect)

        screen.blit(monitor_scaled, (0, 0))
        
        if not show_urdu_display:
            if selected_index == 0:
                barrel = barrel_farleft_scaled
            elif selected_index == n - 1:
                barrel = barrel_farright_scaled
            else:
                barrel = barrel_mid_scaled
            barrel_rect = barrel.get_rect(midbottom=(screen.get_width() / 2, screen.get_height()))
            screen.blit(barrel, barrel_rect)
    
    def handle_game_logic(self, current_time, round_start_time, show_urdu_display, selection_made, last_action_time):
        new_show_urdu_display = show_urdu_display
        new_round_needed = False
        
        if show_urdu_display and current_time - round_start_time >= self.WAIT_TIME:
            new_show_urdu_display = False
        
        if selection_made and current_time - last_action_time >= self.WAIT_TIME:
            new_round_needed = True
        
        return new_show_urdu_display, new_round_needed
    
    def handle_input(self, event, selection_made, current_time, round_start_time, selected_index, n, correct_index):
        new_selected_index = selected_index
        new_selection_made = selection_made
        new_last_action_time = None
        
        if event.type == pygame.KEYDOWN and not selection_made and (current_time - round_start_time) >= self.WAIT_TIME:
            if event.key == pygame.K_LEFT:
                new_selected_index = max(0, selected_index - 1)
            elif event.key == pygame.K_RIGHT:
                new_selected_index = min(n - 1, selected_index + 1)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.check_answer(selected_index, correct_index)
                new_selection_made = True
                new_last_action_time = current_time
        
        return new_selected_index, new_selection_made, new_last_action_time
        
        # Note: Game will end after ANSWER_DISPLAY_TIME in update_frame()
    
    def initialize_game(self, screen):
        self.is_running = True
        self.screen = screen
        
        # Game state
        self.correct_urdu = ""
        self.correct_english = ""
        self.options = []
        self.correct_index = 0
        self.selected_index = 0
        self.show_correct = False
        self.show_wrong = False
        self.selection_made = False
        self.last_action_time = 0
        self.round_start_time = pygame.time.get_ticks()
        self.show_urdu_display = True
        self.current_word_type = "english"
        self.animation_frame_index = 0
        self.last_frame_time = 0

        # Music
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"Sounds/JimmyRemix.ogg")
        pygame.mixer.music.play(-1)

        # Scale assets
        scaled_assets = self.scale_assets(screen)
        self.background_scaled = scaled_assets['background_scaled']
        self.character_scale = scaled_assets['character_scale']
        self.stick_scaled = scaled_assets['stick_scaled']
        self.unfolding_scaled = scaled_assets['unfolding_scaled']
        self.thug_sprites = scaled_assets['thug_sprites']
        self.civilian_sprites = scaled_assets['civilian_sprites']
        self.crosshair_scaled = scaled_assets['crosshair_scaled']
        self.wrong_scaled = scaled_assets['wrong_scaled']
        self.barrel_farleft_scaled = scaled_assets['barrel_farleft_scaled']
        self.barrel_farright_scaled = scaled_assets['barrel_farright_scaled']
        self.barrel_mid_scaled = scaled_assets['barrel_mid_scaled']
        self.monitor_scaled = scaled_assets['monitor_scaled']

        self.animation_frames = [scaled_assets['hit_scaled'], self.unfolding_scaled, None, 
                          scaled_assets['unfolding_flash_scaled'], scaled_assets['hit_flash_scaled'], 
                          scaled_assets['unfolding_flash_scaled'], None, self.unfolding_scaled, scaled_assets['hit_scaled']]
        self.frame_duration = 150

        # Start first round
        self.correct_urdu, self.correct_english, self.options, self.correct_index, self.current_word_type = self.pick_random_words()
        self.character_sprites = self.assign_character_sprites(self.correct_index, len(self.options), self.thug_sprites, self.civilian_sprites)
    
    # Blocks Player input
    def handle_frame_input(self, events, current_time):
        n = len(self.options)
        
        for event in events:
            new_selected_index, new_selection_made, new_last_action_time = self.handle_input(
                event, self.selection_made, current_time, self.round_start_time, self.selected_index, n, self.correct_index
            )
            if new_selection_made and not self.selection_made:
                self.selection_made = True
                self.last_action_time = new_last_action_time
                self.animation_frame_index = 0
                self.last_frame_time = current_time
            self.selected_index = new_selected_index
    
    def update_frame(self, current_time):
        n = len(self.options)
        
        # Update animations
        self.animation_frame_index, self.last_frame_time = self.update_animations(
            current_time, self.selection_made, self.last_frame_time, self.animation_frame_index, self.animation_frames, self.frame_duration
        )
        
        # Update game logic
        self.show_urdu_display, new_round_needed = self.handle_game_logic(
            current_time, self.round_start_time, self.show_urdu_display, self.selection_made, self.last_action_time
        )
        
        # Check if answer was given and wait time passed - then end game
        if self.selection_made and current_time - self.last_action_time >= self.ANSWER_DISPLAY_TIME:
            self.is_running = False
            return
        
        # Start new round if needed
        if new_round_needed:
            self.correct_urdu, self.correct_english, self.options, self.correct_index, self.current_word_type = self.pick_random_words()
            self.character_sprites = self.assign_character_sprites(self.correct_index, len(self.options), self.thug_sprites, self.civilian_sprites)
            self.show_correct = False
            self.show_wrong = False
            self.selection_made = False
            self.selected_index = 0
            self.round_start_time = current_time
            self.show_urdu_display = True
            self.animation_frame_index = 0
        
        # Calculate positions
        if n == 0:
            return
        
        spacing = self.screen.get_width() / (n + 1)
        y = self.screen.get_height() / 2
        centers = [(spacing * (i + 1), y) for i in range(n)]
        
        # Display word to translate
        display_word = self.correct_urdu if self.current_word_type == "english" else self.correct_english
        
        # Rendering
        self.render_game(
            self.screen, self.show_urdu_display, current_time, self.round_start_time,
            self.options, centers, y, self.character_scale, self.stick_scaled, self.unfolding_scaled, self.character_sprites,
            self.selection_made, self.selected_index, self.animation_frames, self.animation_frame_index,
            self.show_wrong, self.show_correct, self.correct_index, self.crosshair_scaled, self.wrong_scaled,
            display_word, self.barrel_farleft_scaled, self.barrel_farright_scaled, self.barrel_mid_scaled,
            self.background_scaled, self.monitor_scaled, spacing
        )
    
    def on_pause(self):
        pygame.mixer.music.pause()
    
    def on_resume(self, paused_duration):
        # Adjust all time-based variables
        self.round_start_time += paused_duration
        self.last_action_time += paused_duration
        self.last_frame_time += paused_duration
        pygame.mixer.music.unpause()