import pygame
import os

class Animation:
    def __init__(self, prefix, frame_count, speed=100):
        self.frames = []
        self.current_frame = 0
        self.frame_count = frame_count
        self.speed = speed
        self.last_update = pygame.time.get_ticks()
        self.finished = False
        
        # Load animation frames
        for i in range(1, frame_count + 1):
            frame = pygame.image.load(os.path.join('assets', 'animations', f'{prefix}{i}.png')).convert_alpha()
            self.frames.append(frame)
            
    def update(self, current_time):
        if current_time - self.last_update > self.speed:
            self.last_update = current_time
            self.current_frame += 1
            if self.current_frame >= self.frame_count:
                self.finished = True
                self.current_frame = 0
                
    def draw(self, surface, x, y):
        if not self.finished and self.frames:
            frame = self.frames[self.current_frame]
            surface.blit(frame, (x, y))
            
    def reset(self):
        self.current_frame = 0
        self.finished = False
        self.last_update = pygame.time.get_ticks()

class StatBar:
    def __init__(self, x, y, width, height, max_value=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.current_value = max_value
        self.target_value = max_value
        self.animation_speed = 2
        
        # Colors
        self.background_color = (60, 63, 65)
        self.border_color = (100, 100, 100)
        self.bar_color = (46, 204, 113)
        self.decrease_color = (231, 76, 60)
        self.increase_color = (46, 204, 113)
        
    def update(self):
        if self.current_value != self.target_value:
            diff = self.target_value - self.current_value
            if abs(diff) < self.animation_speed:
                self.current_value = self.target_value
            else:
                self.current_value += self.animation_speed if diff > 0 else -self.animation_speed
                
    def set_value(self, value):
        self.target_value = max(0, min(value, self.max_value))
        
    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, self.background_color, self.rect)
        
        # Draw the bar
        if self.current_value > 0:
            bar_width = int(self.rect.width * (self.current_value / self.max_value))
            bar_rect = pygame.Rect(self.rect.x, self.rect.y, bar_width, self.rect.height)
            
            # Choose color based on whether value is increasing or decreasing
            if self.current_value < self.target_value:
                color = self.increase_color
            elif self.current_value > self.target_value:
                color = self.decrease_color
            else:
                color = self.bar_color
                
            pygame.draw.rect(surface, color, bar_rect)
            
        # Draw border
        pygame.draw.rect(surface, self.border_color, self.rect, 1)
