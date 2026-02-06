import pygame
import os

pygame.init()


class CurtainTransition:
    def __init__(self):
        self.closed_frames = []
        self.open_frames = []
        self.won_frames = []
        self.loose_frames = []
        self.transition_sound = None
        self.success_sound = None
        self.failure_sound = None
        self.current_frame = 0
        self.frame_timer = 0
        self.is_animating = False
        self.animation_type = None  # "opening" or "closing"
        self.animation_start_time = 0
        self.screen = None
        self.closing_result = None  # "won" or "lost" for closing animation
        
        self.load_sprites()
    
    def load_sprites(self):
        # Load closed frames (1-3)
        for i in range(1, 4):
            path = rf"Sprites\Übergang\Closed_{i}.png"
            if os.path.exists(path):
                self.closed_frames.append(pygame.image.load(path).convert_alpha())
        
        # Load won frames (1-3)
        for i in range(1, 4):
            path = rf"Sprites\Übergang\Won_{i}.png"
            if os.path.exists(path):
                self.won_frames.append(pygame.image.load(path).convert_alpha())
        
        # Load loose frames (1-3)
        for i in range(1, 4):
            path = rf"Sprites\Übergang\Loose_{i}.png"
            if os.path.exists(path):
                self.loose_frames.append(pygame.image.load(path).convert_alpha())
        
        # Load open frames (1-10)
        for i in range(1, 11):
            path = rf"Sprites\Übergang\Open_{i}.png"
            if os.path.exists(path):
                self.open_frames.append(pygame.image.load(path).convert_alpha())
        
        # Load transition sound
        sound_path = r"Sprites\Übergang\transition.ogg"
        if os.path.exists(sound_path):
            self.transition_sound = pygame.mixer.Sound(sound_path)
        
        # Load success/failure sounds
        success_path = r"Sprites\Übergang\Success.ogg"
        if os.path.exists(success_path):
            self.success_sound = pygame.mixer.Sound(success_path)
        
        failure_path = r"Sprites\Übergang\Failure.ogg"
        if os.path.exists(failure_path):
            self.failure_sound = pygame.mixer.Sound(failure_path)
    
    def start_opening_animation(self, screen, duration_ms=1000):        
        self.screen = screen
        self.is_animating = True
        self.animation_type = "opening"
        self.animation_start_time = pygame.time.get_ticks()
        self.current_frame = 0
        if self.transition_sound:
            self.transition_sound.play()
    
    def start_closing_animation(self, screen, duration_ms=1000, is_success=False):
        self.screen = screen
        self.is_animating = True
        self.animation_type = "closing"
        self.animation_start_time = pygame.time.get_ticks()
        self.current_frame = len(self.open_frames) - 1
        self.closing_result = "won" if is_success else "lost"
        
        # Play success or failure sound
        if is_success and self.success_sound:
            self.success_sound.play()
        elif not is_success and self.failure_sound:
            self.failure_sound.play()
        # No transition sound for closing animation
    
    def update(self, current_time):
        if not self.is_animating:
            return False
        
        elapsed = current_time - self.animation_start_time
        
        # Animation duration is 1.667 seconds (1s closed + 0.667s open for opening, or vice versa for closing)
        if elapsed >= 1750:
            self.is_animating = False
            return False
        
        return True
    
    def render(self, screen):
        frame = None
        
        if self.animation_type == "opening":
            # During opening animation
            if self.is_animating:
                # Show closed frames first, then open frames
                elapsed = pygame.time.get_ticks() - self.animation_start_time
                if elapsed < 1000:
                    # Show closed frames in loop - fast looping (3x faster)
                    frame_idx = int((elapsed / 333) * len(self.closed_frames)) % len(self.closed_frames)
                    frame = self.closed_frames[frame_idx]
                else:
                    # Show open frames progressing (1.5x faster)
                    elapsed_open = elapsed - 1000
                    frame_idx = min(int((elapsed_open / 550) * len(self.open_frames)), len(self.open_frames) - 1)
                    frame = self.open_frames[frame_idx]
            else:
                # Animation complete - show fully open
                if len(self.open_frames) > 0:
                    frame = self.open_frames[-1]
        
        elif self.animation_type == "closing":
            # During closing animation
            if self.is_animating:
                elapsed = pygame.time.get_ticks() - self.animation_start_time
                if elapsed < 550:
                    # Show open frames in reverse (1.5x faster)
                    progress = elapsed / 550.0
                    frame_idx = len(self.open_frames) - 1 - int(progress * len(self.open_frames))
                    frame_idx = max(0, frame_idx)
                    frame = self.open_frames[frame_idx]
                else:
                    # Show won/lost/closed frames - fast looping (3x faster)
                    elapsed_closed = elapsed - 550
                    
                    # Choose the appropriate frame set based on result
                    if self.closing_result == "won" and len(self.won_frames) > 0:
                        frames_to_use = self.won_frames
                    elif self.closing_result == "lost" and len(self.loose_frames) > 0:
                        frames_to_use = self.loose_frames
                    else:
                        frames_to_use = self.closed_frames
                    
                    frame_idx = int((elapsed_closed / 333) * len(frames_to_use)) % len(frames_to_use)
                    frame = frames_to_use[frame_idx]
            else:
                # Animation complete - show final frame
                if self.closing_result == "won" and len(self.won_frames) > 0:
                    frame = self.won_frames[0]
                elif self.closing_result == "lost" and len(self.loose_frames) > 0:
                    frame = self.loose_frames[0]
                elif len(self.closed_frames) > 0:
                    frame = self.closed_frames[0]
        
        if frame is None:
            return
        
        # Scale frame to screen size and render
        scaled_frame = pygame.transform.scale(frame, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_frame, (0, 0))
    
    def is_animation_complete(self):
        return not self.is_animating
