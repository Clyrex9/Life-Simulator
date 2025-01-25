import pygame
import pygame_gui
import sys
import random
import json
from pathlib import Path
from character_system import CharacterCreator, Character
from education_system import EducationSystem

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

class GameState:
    MAIN_MENU = "main_menu"
    CHARACTER_CREATION = "character_creation"
    GAME = "game"
    EDUCATION = "education"
    PAUSE = "pause"

class LifeSimulator:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Life Simulator")
        
        self.manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'data/themes/theme.json')
        self.clock = pygame.time.Clock()
        
        self.state = GameState.MAIN_MENU
        self.character = None
        self.character_creator = None
        self.education_system = EducationSystem(SCREEN_WIDTH, SCREEN_HEIGHT, self.manager)
        
        self.load_assets()
        self.setup_ui()
        
    def load_assets(self):
        self.background = pygame.image.load('background.jpg')
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Ses efektleri
        self.click_sound = pygame.mixer.Sound('click.wav')
        self.work_sound = pygame.mixer.Sound('work.wav')
        self.school_sound = pygame.mixer.Sound('school.wav')
        
    def setup_ui(self):
        if self.state == GameState.MAIN_MENU:
            self.setup_main_menu()
        elif self.state == GameState.CHARACTER_CREATION:
            self.setup_character_creation()
        elif self.state == GameState.GAME:
            self.setup_game_ui()

    def setup_main_menu(self):
        self.manager.clear_and_reset()
        
        # Ana menü butonları
        button_width = 200
        button_height = 50
        start_y = 250
        
        self.main_menu_buttons = {
            'new_game': pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((SCREEN_WIDTH//2 - button_width//2, start_y),
                                        (button_width, button_height)),
                text='Yeni Oyun',
                manager=self.manager),
            'load_game': pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((SCREEN_WIDTH//2 - button_width//2, start_y + 70),
                                        (button_width, button_height)),
                text='Oyun Yükle',
                manager=self.manager),
            'settings': pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((SCREEN_WIDTH//2 - button_width//2, start_y + 140),
                                        (button_width, button_height)),
                text='Ayarlar',
                manager=self.manager),
            'quit': pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((SCREEN_WIDTH//2 - button_width//2, start_y + 210),
                                        (button_width, button_height)),
                text='Çıkış',
                manager=self.manager)
        }

    def setup_character_creation(self):
        self.character_creator = CharacterCreator(SCREEN_WIDTH, SCREEN_HEIGHT, self.manager)
        self.character_creator.create_ui()

    def setup_game_ui(self):
        self.manager.clear_and_reset()
        
        # Stat paneli
        panel_width = 200
        self.game_ui = {
            'stats_panel': pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((0, 0), (panel_width, SCREEN_HEIGHT)),
                manager=self.manager
            ),
            'action_panel': pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((SCREEN_WIDTH - panel_width, 0), 
                                        (panel_width, SCREEN_HEIGHT)),
                manager=self.manager
            ),
            'event_panel': pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((panel_width, SCREEN_HEIGHT - 150), 
                                        (SCREEN_WIDTH - 2 * panel_width, 150)),
                manager=self.manager
            )
        }
        
        # Karakter bilgileri
        y_pos = 10
        stats = [
            f'İsim: {self.character.name}',
            f'Yaş: {self.character.age}',
            f'Para: {self.character.money}₺',
            f'Mutluluk: {self.character.stats["Mutluluk"]}',
            f'Sağlık: {self.character.stats["Sağlık"]}',
            f'Zeka: {self.character.stats["Zeka"]}',
            f'Enerji: {self.character.stats["Enerji"]}',
            f'Okul: {self.character.education["school"] or "Gitmiyor"}'
        ]
        
        for i, stat in enumerate(stats):
            self.game_ui[f'stat_{y_pos}'] = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, y_pos), (180, 30)),
                text=stat,
                manager=self.manager,
                container=self.game_ui['stats_panel']
            )
            y_pos += 40
            
        # Aksiyon butonları
        y_pos = 10
        actions = ['Okul', 'İş', 'İlişkiler', 'Alışveriş', 'Sağlık', 'Yaş İlerle']
        for action in actions:
            button_key = action.lower().replace(' ', '_').replace('ş', 's').replace('İ', 'i')
            self.game_ui[f'{button_key}_button'] = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((10, y_pos), (180, 40)),
                text=action,
                manager=self.manager,
                container=self.game_ui['action_panel']
            )
            y_pos += 50
        
        # Olay mesajları
        self.game_ui['event_text'] = pygame_gui.elements.UITextBox(
            html_text="Hayatına hoş geldin! Ne yapmak istersin?",
            relative_rect=pygame.Rect((10, 10), (SCREEN_WIDTH - 2 * panel_width - 20, 130)),
            manager=self.manager,
            container=self.game_ui['event_panel']
        )

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
            
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            self.click_sound.play()
            
            if self.state == GameState.MAIN_MENU:
                if event.ui_element == self.main_menu_buttons['new_game']:
                    self.state = GameState.CHARACTER_CREATION
                    self.setup_character_creation()
                elif event.ui_element == self.main_menu_buttons['quit']:
                    return False
                    
            elif self.state == GameState.CHARACTER_CREATION:
                character_data = self.character_creator.handle_event(event)
                if character_data:
                    self.character = Character(character_data)
                    self.state = GameState.GAME
                    self.setup_game_ui()
                    
            elif self.state == GameState.GAME:
                self.handle_game_buttons(event.ui_element)
                
            elif self.state == GameState.EDUCATION:
                result = self.education_system.handle_event(event, self.character)
                if result == 'back':
                    self.state = GameState.GAME
                    self.setup_game_ui()
                elif result == 'enrolled':
                    self.state = GameState.GAME
                    self.setup_game_ui()

        self.manager.process_events(event)
        return True

    def handle_game_buttons(self, button):
        if not self.character:
            return
            
        if button == self.game_ui['yas_ilerle_button']:
            events = self.character.age_up()
            
            # Eğitim durumunu kontrol et
            if self.character.education['level'] != 'Yok' and self.character.education['school']:
                self.education_system.update_grades(self.character)
                events.append(f"{self.character.education['school']}'da yeni dönem başladı!")
            
            event_text = "\n".join(events)
            self.game_ui['event_text'].html_text = event_text
            self.game_ui['event_text'].rebuild()
            self.update_stats_display()
            
        elif button == self.game_ui['okul_button']:
            self.school_sound.play()
            self.state = GameState.EDUCATION
            if self.character.education['school']:
                self.education_system.show_current_school_info(self.character)
            else:
                self.education_system.show_school_selection(self.character)
                
        elif button == self.game_ui['is_button']:
            self.work_sound.play()
            self.show_job_menu()
        elif button == self.game_ui['iliskiler_button']:
            self.show_relationships_menu()
        elif button == self.game_ui['alisveris_button']:
            self.show_shopping_menu()
        elif button == self.game_ui['saglik_button']:
            self.show_health_menu()

    def update_stats_display(self):
        if not hasattr(self, 'game_ui'):
            return
            
        stats = [
            f'İsim: {self.character.name}',
            f'Yaş: {self.character.age}',
            f'Para: {self.character.money}₺',
            f'Mutluluk: {self.character.stats["Mutluluk"]}',
            f'Sağlık: {self.character.stats["Sağlık"]}',
            f'Zeka: {self.character.stats["Zeka"]}',
            f'Enerji: {self.character.stats["Enerji"]}',
            f'Okul: {self.character.education["school"] or "Gitmiyor"}'
        ]
        
        for i, stat in enumerate(stats):
            y_pos = i * 40 + 10
            self.game_ui[f'stat_{y_pos}'].set_text(stat)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.manager.draw_ui(self.screen)
        pygame.display.update()

    def run(self):
        running = True
        while running:
            time_delta = self.clock.tick(FPS)/1000.0
            
            for event in pygame.event.get():
                running = self.handle_event(event)
                
            self.manager.update(time_delta)
            self.draw()

if __name__ == '__main__':
    game = LifeSimulator()
    game.run()