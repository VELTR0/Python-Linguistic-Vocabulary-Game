import pygame
import random
import Game

pygame.init()


class HogansAlleySimple(Game):
    """Hogan's Alley Spiel - Vereinfachte Version für Anfänger."""
    
    DISPLAY_TIME = 1000  # Zeit für Stick-Animation (ms)
    WAIT_TIME = 1800     # Zeit zum Anzeigen des Wortes (ms)
    
    def __init__(self, difficulty="hard", num_words=4):
        """Initialisiere das Spiel."""
        super().__init__(difficulty, num_words)
        
        # Fonts
        self.font_options = pygame.font.Font(None, 50)
        self.font_urdu_large = pygame.font.Font(None, 150)
        
        # Lade Bilder und Sounds
        self.load_sprites()
        self.correct_sound = pygame.mixer.Sound(r"Sounds/Correct.ogg")
        self.wrong_sound = pygame.mixer.Sound(r"Sounds/Wrong.ogg")
        
        # Spielzustand - diese Variablen speichern den aktuellen Stand
        self.correct_urdu = ""
        self.correct_english = ""
        self.options = []
        self.correct_index = 0
        self.selected_index = 0
        self.current_word_type = "english"
        
        # Animation und Anzeige
        self.show_correct = False
        self.show_wrong = False
        self.selection_made = False
        self.show_urdu_display = True
        self.animation_frame_index = 0
        
        # Timing
        self.last_action_time = 0
        self.round_start_time = 0
        self.last_frame_time = 0
    
    def load_sprites(self):
        """Lade alle Bilder."""
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
        """Skaliere alle Bilder für die Bildschirmgröße."""
        # Berechne Größen
        char_height = int(screen.get_height() / 2.75)
        char_width = int(char_height * 0.6)
        stick_height = int(screen.get_height() / 2.5)
        stick_width = int(stick_height * 0.1)
        
        # Skaliere Hintergrund
        self.background_scaled = pygame.transform.scale(
            self.background_image, 
            (screen.get_width(), screen.get_height())
        )
        
        # Skaliere Stick
        self.stick_scaled = pygame.transform.scale(
            self.stick_image, 
            (stick_width, stick_height)
        )
        
        # Skaliere Unfolding
        self.unfolding_scaled = pygame.transform.scale(
            self.unfolding_image, 
            (int(char_width * 0.3), char_height)
        )
        
        # Skaliere Charaktere
        self.thug_sprites = [
            pygame.transform.scale(self.thug1_image, (char_width, char_height)),
            pygame.transform.scale(self.thug2_image, (char_width, char_height)),
            pygame.transform.scale(self.thug3_image, (char_width, char_height))
        ]
        
        self.civilian_sprites = [
            pygame.transform.scale(self.woman_image, (char_width, char_height)),
            pygame.transform.scale(self.policeman_image, (char_width, char_height))
        ]
        
        # Skaliere andere Sprites
        self.crosshair_scaled = pygame.transform.scale(self.crosshair_image, (char_width, char_width))
        self.wrong_scaled = pygame.transform.scale(self.wrong_image, (char_width, char_height))
        self.monitor_scaled = pygame.transform.scale(self.monitor_image, (screen.get_width(), screen.get_height()))
        
        # Skaliere Fässer
        barrel_size = (int(screen.get_height() / 3), int(screen.get_height() / 3))
        self.barrel_farleft_scaled = pygame.transform.scale(self.barrel_farleft_image, barrel_size)
        self.barrel_farright_scaled = pygame.transform.scale(self.barrel_farright_image, barrel_size)
        self.barrel_mid_scaled = pygame.transform.scale(self.barrel_mid_image, barrel_size)
        
        # Animations-Frames
        hit_scaled = pygame.transform.scale(self.hit_image, (char_width, char_height))
        hit_flash_scaled = pygame.transform.scale(self.hit_flash_image, (char_width, char_height))
        unfolding_flash_scaled = pygame.transform.scale(self.unfolding_flash_image, (int(char_width * 0.3), char_height))
        
        self.animation_frames = [
            hit_scaled, self.unfolding_scaled, None, 
            unfolding_flash_scaled, hit_flash_scaled, unfolding_flash_scaled, 
            None, self.unfolding_scaled, hit_scaled
        ]
        
        self.character_width = char_width
    
    def assign_character_sprites(self):
        """Weise jedem Wort einen Charakter zu."""
        self.character_sprites = []
        civilian_idx = 0
        
        for i in range(len(self.options)):
            if i == self.correct_index:
                # Richtige Antwort = Schurke
                self.character_sprites.append(random.choice(self.thug_sprites))
            else:
                # Falsche Antwort = Zivilist
                self.character_sprites.append(self.civilian_sprites[civilian_idx % 2])
                civilian_idx += 1
    
    def start_new_round(self):
        """Starte eine neue Spielrunde."""
        # Hole neue Wörter
        result = self.pick_random_words()
        self.correct_urdu = result[0]
        self.correct_english = result[1]
        self.options = result[2]
        self.correct_index = result[3]
        self.current_word_type = result[4]
        
        # Weise Charaktere zu
        self.assign_character_sprites()
        
        # Reset Zustand
        self.show_correct = False
        self.show_wrong = False
        self.selection_made = False
        self.selected_index = 0
        self.round_start_time = pygame.time.get_ticks()
        self.show_urdu_display = True
        self.animation_frame_index = 0
    
    def render_game(self, screen):
        """Zeichne das gesamte Spiel."""
        # Hintergrund
        screen.blit(self.background_scaled, (0, 0))
        
        # Berechne Positionen
        n = len(self.options)
        spacing = screen.get_width() / (n + 1)
        y = screen.get_height() / 2
        centers = [(spacing * (i + 1), y) for i in range(n)]
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.round_start_time
        
        # Zeige Wort am Anfang
        if self.show_urdu_display:
            display_word = self.correct_urdu if self.current_word_type == "english" else self.correct_english
            text = self.font_urdu_large.render(f"Translate: {display_word}", True, (0, 0, 0))
            rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/4))
            screen.blit(text, rect)
            
            # Animiere Sticks
            progress = min(1.0, elapsed / self.DISPLAY_TIME)
            for i in range(n):
                cx_final = centers[i][0]
                x_start = -self.character_width - spacing * (n - 1 - i)
                x_current = x_start + (cx_final - x_start) * progress
                stick_rect = self.stick_scaled.get_rect(center=(x_current, y))
                screen.blit(self.stick_scaled, stick_rect)
                
                # Zeige Unfolding am Ende
                if elapsed / self.WAIT_TIME >= 0.9:
                    unf_rect = self.unfolding_scaled.get_rect(center=(cx_final, y-20))
                    screen.blit(self.unfolding_scaled, unf_rect)
        
        # Zeige Charaktere
        else:
            # Sticks
            for i in range(n):
                stick_rect = self.stick_scaled.get_rect(center=centers[i])
                screen.blit(self.stick_scaled, stick_rect)
            
            # Charaktere und Wörter
            for i, word in enumerate(self.options):
                cx, cy = centers[i]
                
                # Animation bei Auswahl
                if self.selection_made and i == self.selected_index:
                    frame = self.animation_frames[self.animation_frame_index]
                    if frame:
                        rect = frame.get_rect(center=(cx, cy-20))
                        screen.blit(frame, rect)
                else:
                    # Normaler Charakter
                    char_rect = self.character_sprites[i].get_rect(center=(cx, cy-20))
                    screen.blit(self.character_sprites[i], char_rect)
                    
                    # Wort
                    text = self.font_options.render(word, True, (0, 0, 0))
                    text_rect = text.get_rect(center=(cx, cy))
                    screen.blit(text, text_rect)
                
                # Fadenkreuz
                if i == self.selected_index:
                    cross_rect = self.crosshair_scaled.get_rect(center=(cx, cy))
                    screen.blit(self.crosshair_scaled, cross_rect)
                
                # Wrong X
                if self.show_wrong and i != self.correct_index:
                    wrong_rect = self.wrong_scaled.get_rect(center=(cx, cy-20))
                    screen.blit(self.wrong_scaled, wrong_rect)
                
                # Correct Crosshair
                if self.show_correct and i == self.correct_index:
                    cross_rect = self.crosshair_scaled.get_rect(center=(cx, cy))
                    screen.blit(self.crosshair_scaled, cross_rect)
        
        # Monitor Overlay
        screen.blit(self.monitor_scaled, (0, 0))
        
        # Fass
        if not self.show_urdu_display:
            if self.selected_index == 0:
                barrel = self.barrel_farleft_scaled
            elif self.selected_index == n - 1:
                barrel = self.barrel_farright_scaled
            else:
                barrel = self.barrel_mid_scaled
            barrel_rect = barrel.get_rect(midbottom=(screen.get_width()/2, screen.get_height()))
            screen.blit(barrel, barrel_rect)
    
    def update_animations(self):
        """Update die Animationen."""
        if self.selection_made:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= 150:
                self.animation_frame_index = (self.animation_frame_index + 1) % len(self.animation_frames)
                self.last_frame_time = current_time
    
    def update_game_logic(self):
        """Update die Spiellogik."""
        current_time = pygame.time.get_ticks()
        
        # Verstecke Wort
        if self.show_urdu_display and current_time - self.round_start_time >= self.WAIT_TIME:
            self.show_urdu_display = False
        
        # Neue Runde
        if self.selection_made and current_time - self.last_action_time >= self.WAIT_TIME:
            self.start_new_round()
    
    def handle_input(self, event):
        """Verarbeite Tastatur-Eingaben."""
        if event.type != pygame.KEYDOWN:
            return
        
        # Warte bis Urdu-Display vorbei ist
        current_time = pygame.time.get_ticks()
        if self.selection_made or (current_time - self.round_start_time) < self.WAIT_TIME:
            return
        
        n = len(self.options)
        
        # Links
        if event.key == pygame.K_LEFT:
            self.selected_index = max(0, self.selected_index - 1)
        
        # Rechts
        elif event.key == pygame.K_RIGHT:
            self.selected_index = min(n - 1, self.selected_index + 1)
        
        # Schießen
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.check_answer()
            self.selection_made = True
            self.last_action_time = current_time
            self.animation_frame_index = 0
            self.last_frame_time = current_time
    
    def check_answer(self):
        """Prüfe die Antwort."""
        if self.selected_index == self.correct_index:
            self.correct_sound.play()
            self.record_correct_answer()
            self.show_correct = True
        else:
            self.wrong_sound.play()
            self.record_incorrect_answer()
            self.show_wrong = True
    
    def start_game(self, screen):
        """Hauptfunktion - starte das Spiel."""
        self.is_running = True
        
        # Musik
        pygame.mixer.music.stop()
        pygame.mixer.music.load(r"Sounds/JimmyRemix.ogg")
        pygame.mixer.music.play(-1)
        
        # Skaliere alle Bilder
        self.scale_assets(screen)
        
        # Erste Runde
        self.start_new_round()
        
        # Game Loop
        while self.is_running:
            # Update
            self.update_animations()
            self.update_game_logic()
            
            # Render
            self.render_game(screen)
            
            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    self.is_running = False
                else:
                    self.handle_input(event)
            
            pygame.display.update()
        
        return True
