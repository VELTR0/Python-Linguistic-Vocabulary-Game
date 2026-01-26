import pygame
import random
from Game import Game

pygame.init()


class HogansAlley(Game):
    #DIFFICULTY = "hard"
    DISPLAY_TIME = 1000  
    WAIT_TIME = 1800
    
    def __init__(self, difficulty="hard", num_words=4):
        super().__init__(difficulty, num_words)
        self.DIFFICULTY = difficulty
        self.font_options = pygame.font.Font(None, 50)
        self.font_urdu_large = pygame.font.Font(None, 150)
        self.load_sprites()
        self.correct_sound = pygame.mixer.Sound(r"Sounds/Correct.ogg")
        self.wrong_sound = pygame.mixer.Sound(r"Sounds/Wrong.ogg")
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
                    text_surface = self.font_options.render(word, True, (0, 0, 0))
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
            prompt_surface = self.font_urdu_large.render(f"Translate: {display_word}", True, (0, 0, 0))
            prompt_rect = prompt_surface.get_rect(center=(screen.get_width()/2, screen.get_height()/4))
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
        new_show_correct = False
        new_show_wrong = False
        new_last_action_time = None
        
        if event.type == pygame.KEYDOWN and not selection_made and (current_time - round_start_time) >= self.WAIT_TIME:
            if event.key == pygame.K_LEFT:
                new_selected_index = max(0, selected_index - 1)
            elif event.key == pygame.K_RIGHT:
                new_selected_index = min(n - 1, selected_index + 1)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                new_show_correct, new_show_wrong = self.check_answer(selected_index, correct_index)
                new_selection_made = True
                new_last_action_time = current_time
        
        return new_selected_index, new_selection_made, new_show_correct, new_show_wrong, new_last_action_time
    
    def check_answer(self, selected_index, correct_index):
        if selected_index == correct_index:
            self.correct_sound.play()
            self.record_correct_answer()
            return True, False
        else:
            self.wrong_sound.play()
            self.record_incorrect_answer()
            return False, True
    
    def start_game(self, screen):
        self.is_running = True

        correct_urdu = ""
        correct_english = ""
        options = []
        correct_index = 0
        selected_index = 0
        show_correct = False
        show_wrong = False
        selection_made = False
        last_action_time = 0
        round_start_time = pygame.time.get_ticks()
        show_urdu_display = True
        current_word_type = "english"
        animation_frame_index = 0
        last_frame_time = 0

        # Music
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"Sounds/JimmyRemix.ogg")
        pygame.mixer.music.play(-1)

        # Scale assets
        scaled_assets = self.scale_assets(screen)
        background_scaled = scaled_assets['background_scaled']
        character_scale = scaled_assets['character_scale']
        stick_scaled = scaled_assets['stick_scaled']
        unfolding_scaled = scaled_assets['unfolding_scaled']
        thug_sprites = scaled_assets['thug_sprites']
        civilian_sprites = scaled_assets['civilian_sprites']
        crosshair_scaled = scaled_assets['crosshair_scaled']
        wrong_scaled = scaled_assets['wrong_scaled']
        barrel_farleft_scaled = scaled_assets['barrel_farleft_scaled']
        barrel_farright_scaled = scaled_assets['barrel_farright_scaled']
        barrel_mid_scaled = scaled_assets['barrel_mid_scaled']
        monitor_scaled = scaled_assets['monitor_scaled']

        animation_frames = [scaled_assets['hit_scaled'], unfolding_scaled, None, 
                          scaled_assets['unfolding_flash_scaled'], scaled_assets['hit_flash_scaled'], 
                          scaled_assets['unfolding_flash_scaled'], None, unfolding_scaled, scaled_assets['hit_scaled']]
        frame_duration = 150

        # Start first round
        correct_urdu, correct_english, options, correct_index, current_word_type = self.pick_random_words()
        character_sprites = self.assign_character_sprites(correct_index, len(options), thug_sprites, civilian_sprites)

        while self.is_running:
            current_time = pygame.time.get_ticks()
            
            # Update animations
            animation_frame_index, last_frame_time = self.update_animations(
                current_time, selection_made, last_frame_time, animation_frame_index, 
                animation_frames, frame_duration
            )
            
            # Handle game logic
            show_urdu_display, new_round_needed = self.handle_game_logic(
                current_time, round_start_time, show_urdu_display, 
                selection_made, last_action_time
            )
            
            # Start new round if needed
            if new_round_needed:
                correct_urdu, correct_english, options, correct_index, current_word_type = self.pick_random_words()
                character_sprites = self.assign_character_sprites(correct_index, len(options), thug_sprites, civilian_sprites)
                show_correct = False
                show_wrong = False
                selection_made = False
                selected_index = 0
                round_start_time = current_time
                show_urdu_display = True
                animation_frame_index = 0
            
            # Calculate positions
            n = len(options)
            if n == 0:
                pygame.display.update()
                continue
            spacing = screen.get_width() / (n + 1)
            y = screen.get_height() / 2
            centers = [(spacing * (i + 1), y) for i in range(n)]
            
            # DIsplay word to translate
            display_word = correct_urdu if current_word_type == "english" else correct_english
            
            # Rendering
            self.render_game(
                screen, show_urdu_display, current_time, round_start_time,
                options, centers, y, character_scale, stick_scaled, unfolding_scaled, character_sprites,
                selection_made, selected_index, animation_frames, animation_frame_index,
                show_wrong, show_correct, correct_index, crosshair_scaled, wrong_scaled,
                display_word, barrel_farleft_scaled, barrel_farright_scaled, barrel_mid_scaled,
                background_scaled, monitor_scaled, spacing
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    self.is_running = False
                else:
                    new_selected_index, new_selection_made, new_show_correct, new_show_wrong, new_last_action_time = self.handle_input(
                        event, selection_made, current_time, round_start_time, 
                        selected_index, n, correct_index
                    )
                    
                    if new_selection_made and not selection_made:
                        selection_made = True
                        show_correct = new_show_correct
                        show_wrong = new_show_wrong
                        last_action_time = new_last_action_time
                        animation_frame_index = 0
                        last_frame_time = current_time
                    
                    selected_index = new_selected_index
            
            pygame.display.update()
        
        return True