import pygame
import pygame_gui
import sys
import random
import json
from pathlib import Path
from character_system import CharacterCreator, Character
from education_system import EducationSystem
from animation_system import Animation, StatBar

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
    SETTINGS = "settings"

class LifeSimulator:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        # Ekran ayarları
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Life Simulator")
        
        # UI yöneticisi
        self.manager = pygame_gui.UIManager((self.width, self.height), 'data/themes/theme.json')
        
        # FPS ve clock
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Oyun durumu
        self.state = GameState.MAIN_MENU
        self.character = None
        self.character_creator = None
        
        # Müzik sistemi
        self.current_music = None
        self.music_volume = 0.5
        self.sound_volume = 0.3
        pygame.mixer.music.set_volume(self.music_volume)
        
        # Animasyonlar
        self.level_up_animation = None
        self.money_gain_animation = None
        self.money_loss_animation = None
        self.active_animations = []
        
        # Asset'leri yükle
        self.load_assets()
        
        # Ana menüyü kur
        self.setup_menu()
        
        # Müziği başlat
        self.play_menu_music()
        
    def load_assets(self):
        # Arkaplan resmi
        try:
            self.background_image = pygame.image.load('assets/backgrounds/background.jpg')
            self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        except pygame.error as e:
            print(f"Arkaplan resmi yüklenemedi: {e}")
            # Arkaplan resmi yüklenemezse siyah arkaplan kullan
            self.background_image = pygame.Surface((self.width, self.height))
            self.background_image.fill((0, 0, 0))
            
        # Müzikler ve ses efektleri
        self.sounds = {}
        try:
            # Ses efektleri
            sound_files = {
                'click': 'assets/sounds/effects/click.wav',
                'success': 'assets/sounds/effects/succes.wav',
                'fail': 'assets/sounds/effects/fail.wav'
            }
            
            for sound_name, sound_path in sound_files.items():
                try:
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(self.sound_volume)
                    self.sounds[sound_name] = sound
                except pygame.error as e:
                    print(f"{sound_name} sesi yüklenemedi: {e}")
                    # Ses yüklenemezse boş ses oluştur
                    empty_buffer = pygame.mixer.Sound(buffer=b'\x00' * 44100)  # 1 saniyelik boş ses
                    empty_buffer.set_volume(self.sound_volume)
                    self.sounds[sound_name] = empty_buffer
                    
        except Exception as e:
            print(f"Ses dosyaları yüklenirken hata: {e}")
            # Hiç ses yüklenemezse boş ses sözlüğü oluştur
            empty_buffer = pygame.mixer.Sound(buffer=b'\x00' * 44100)
            empty_buffer.set_volume(self.sound_volume)
            self.sounds = {
                'click': empty_buffer,
                'success': empty_buffer,
                'fail': empty_buffer
            }
            
    def play_menu_music(self):
        if self.current_music != 'menu':
            try:
                pygame.mixer.music.load('assets/sounds/music/menu_music.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(self.music_volume)
                self.current_music = 'menu'
            except pygame.error as e:
                print(f"Menü müziği yüklenemedi: {e}")
                
    def play_game_music(self):
        if self.current_music != 'game':
            try:
                pygame.mixer.music.load('assets/sounds/music/game_music.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(self.music_volume)
                self.current_music = 'game'
            except pygame.error as e:
                print(f"Oyun müziği yüklenemedi: {e}")
                
    def play_sound(self, sound_name):
        try:
            if sound_name in self.sounds:
                self.sounds[sound_name].play()
        except Exception as e:
            print(f"Ses çalınamadı: {e}")
            # Ses çalınamazsa sessizce devam et
            
    def setup_menu(self):
        self.state = GameState.MAIN_MENU
        self.manager.clear_and_reset()
        
        # Ana menü butonları
        button_width = 200
        button_height = 50
        start_y = self.height // 2 - 100
        
        self.main_menu_buttons = {}
        
        buttons = [
            ('new_game', 'Yeni Oyun'),
            ('settings', 'Ayarlar'),
            ('quit', 'Çıkış')
        ]
        
        for i, (key, text) in enumerate(buttons):
            self.main_menu_buttons[key] = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(
                    (self.width//2 - button_width//2, 
                     start_y + i * (button_height + 20)),
                    (button_width, button_height)
                ),
                text=text,
                manager=self.manager
            )
            
    def setup_settings(self):
        self.state = GameState.SETTINGS
        self.manager.clear_and_reset()
        
        panel_width = 600
        panel_height = 400
        
        # Ana panel
        self.settings_ui = {}
        self.settings_ui['panel'] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (self.width//2 - panel_width//2, 
                 self.height//2 - panel_height//2),
                (panel_width, panel_height)
            ),
            manager=self.manager
        )
        
        # Başlık
        self.settings_ui['title'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 20), (panel_width, 40)),
            text='Ayarlar',
            manager=self.manager,
            container=self.settings_ui['panel']
        )
        
        # Müzik ses seviyesi
        self.settings_ui['music_label'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 100), (150, 30)),
            text='Müzik Sesi:',
            manager=self.manager,
            container=self.settings_ui['panel']
        )
        
        self.settings_ui['music_slider'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((220, 100), (300, 30)),
            start_value=50,
            value_range=(0, 100),
            manager=self.manager,
            container=self.settings_ui['panel']
        )
        
        # Efekt ses seviyesi
        self.settings_ui['sound_label'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((50, 150), (150, 30)),
            text='Efekt Sesi:',
            manager=self.manager,
            container=self.settings_ui['panel']
        )
        
        self.settings_ui['sound_slider'] = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((220, 150), (300, 30)),
            start_value=30,
            value_range=(0, 100),
            manager=self.manager,
            container=self.settings_ui['panel']
        )
        
        # Geri dön butonu
        self.settings_ui['back_button'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((panel_width//2 - 100, panel_height - 60), 
                                    (200, 40)),
            text='Geri Dön',
            manager=self.manager,
            container=self.settings_ui['panel']
        )
        
    def setup_character_creation(self):
        self.state = GameState.CHARACTER_CREATION
        self.manager.clear_and_reset()
        
        # Character creator'ı oluştur
        self.character_creator = CharacterCreator(self.width, self.height, self.manager)
        
        # Müziği değiştir
        self.play_menu_music()
        
    def handle_character_creation_event(self, event):
        if not hasattr(self, 'character_creator') or self.character_creator is None:
            self.character_creator = CharacterCreator(self.width, self.height, self.manager)
            return
            
        character = self.character_creator.handle_event(event)
        if character:
            self.character = character
            self.setup_game()  # Karakter oluşturulduğunda oyuna geç
            
    def setup_game_ui(self):
        self.manager.clear_and_reset()
        
        # Ana panel
        panel_width = SCREEN_WIDTH - 40
        panel_height = SCREEN_HEIGHT - 40
        
        self.game_ui = {
            'main_panel': pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((20, 20), (panel_width, panel_height)),
                manager=self.manager
            ),
        }
        
        # Karakter bilgileri paneli
        info_panel_width = 300
        self.game_ui['info_panel'] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((10, 10), (info_panel_width, panel_height - 20)),
            manager=self.manager,
            container=self.game_ui['main_panel']
        )
        
        # Karakter görseli
        # character_image = self.character_images[self.player['gender']][self.player['appearance']['character_index']]
        # character_rect = character_image.get_rect()
        # character_x = info_panel_width//2 - character_rect.width//2
        # self.game_ui['character_image_rect'] = pygame.Rect(
        #     (character_x, 20), character_rect.size
        # )
        
        # Karakter bilgileri
        y_pos = 20
        stats = [
            ('Para', self.character.money),
            ('Mutluluk', self.character.stats["Mutluluk"]),
            ('Sağlık', self.character.stats["Sağlık"]),
            ('Zeka', self.character.stats["Zeka"]),
            ('Enerji', self.character.stats["Enerji"])
        ]
        
        for stat_name, stat_value in stats:
            self.game_ui[f'{stat_name}_label'] = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((20, y_pos), (info_panel_width - 40, 30)),
                text=f'{stat_name}: {stat_value}',
                manager=self.manager,
                container=self.game_ui['info_panel']
            )
            y_pos += 40
            
        # Eylem butonları paneli
        action_panel_width = panel_width - info_panel_width - 30
        self.game_ui['action_panel'] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((info_panel_width + 20, 10), 
                                    (action_panel_width, panel_height - 20)),
            manager=self.manager,
            container=self.game_ui['main_panel']
        )
        
        # Eylem butonları
        button_width = 200
        button_height = 40
        button_margin = 20
        buttons_per_row = 3
        current_row = 0
        current_col = 0
        
        actions = ['Okula Git', 'İşe Git', 'Spor Yap', 'Kitap Oku', 'Arkadaşlarla Takıl', 'Oyun Oyna']
        
        for action in actions:
            x_pos = button_margin + (button_width + button_margin) * current_col
            y_pos = button_margin + (button_height + button_margin) * current_row
            
            button_key = action.lower().replace(' ', '_') + '_button'
            self.game_ui[button_key] = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((x_pos, y_pos), (button_width, button_height)),
                text=action,
                manager=self.manager,
                container=self.game_ui['action_panel']
            )
            
            current_col += 1
            if current_col >= buttons_per_row:
                current_col = 0
                current_row += 1
        
        # Yaş ilerle butonu
        self.game_ui['yas_ilerle_button'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((action_panel_width - button_width - button_margin, 
                                     panel_height - button_height - 40),
                                    (button_width, button_height)),
            text='Yaş İlerle',
            manager=self.manager,
            container=self.game_ui['action_panel']
        )

    def setup_game(self):
        self.state = GameState.GAME
        self.setup_game_ui()
        self.play_game_music()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Tıklama sesi çal
            self.play_sound('click')
            
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if self.state == GameState.MAIN_MENU:
                if event.ui_element == self.main_menu_buttons.get('new_game'):
                    self.setup_character_creation()
                    self.play_sound('click')
                elif event.ui_element == self.main_menu_buttons.get('settings'):
                    self.setup_settings()
                    self.play_sound('click')
                elif event.ui_element == self.main_menu_buttons.get('quit'):
                    self.play_sound('click')
                    return False
                    
            elif self.state == GameState.CHARACTER_CREATION:
                self.handle_character_creation_event(event)
                self.play_sound('click')
                
            elif self.state == GameState.GAME:
                self.handle_game_buttons(event.ui_element)
                self.play_sound('click')
                
            elif self.state == GameState.SETTINGS:
                if event.ui_element == self.settings_ui.get('back_button'):
                    self.setup_menu()
                    self.play_sound('click')
                    
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if self.state == GameState.SETTINGS:
                if event.ui_element == self.settings_ui.get('music_slider'):
                    self.music_volume = event.value / 100
                    pygame.mixer.music.set_volume(self.music_volume)
                elif event.ui_element == self.settings_ui.get('sound_slider'):
                    self.sound_volume = event.value / 100
                    for sound in self.sounds.values():
                        sound.set_volume(self.sound_volume)
                    
        self.manager.process_events(event)
        return True
        
    def handle_game_buttons(self, button):
        if not self.character:
            return
            
        if button == self.game_ui.get('yas_ilerle_button'):
            # Yaş ilerleme mantığı
            pass
        elif button == self.game_ui.get('okula_git_button'):
            # Okul mantığı
            pass
        elif button == self.game_ui.get('ise_git_button'):
            # İş mantığı
            pass
        elif button == self.game_ui.get('spor_yap_button'):
            # Spor mantığı
            pass
        elif button == self.game_ui.get('kitap_oku_button'):
            # Kitap okuma mantığı
            pass
        elif button == self.game_ui.get('arkadaslarla_takil_button'):
            # Arkadaş mantığı
            pass
        elif button == self.game_ui.get('oyun_oyna_button'):
            # Oyun oynama mantığı
            pass

    def update_stats_display(self):
        if self.character and self.state == GameState.GAME:
            stats = [
                ('Para', self.character.money),
                ('Mutluluk', self.character.stats["Mutluluk"]),
                ('Sağlık', self.character.stats["Sağlık"]),
                ('Zeka', self.character.stats["Zeka"]),
                ('Enerji', self.character.stats["Enerji"])
            ]
            
            for stat_name, stat_value in stats:
                if stat_name in self.stat_bars:
                    self.stat_bars[stat_name].set_value(stat_value)
                    self.game_ui[f'{stat_name}_label'].set_text(f'{stat_name}: {stat_value}')
            
            self.game_ui['age_label'].set_text(f'Yaş: {self.character.age}')
            self.game_ui['school_label'].set_text(f'Okul: {self.character.education["school"] or "Gitmiyor"}')

    def play_money_animation(self, is_gain):
        animation = self.money_gain_animation if is_gain else self.money_loss_animation
        animation.reset()
        self.active_animations.append(animation)

    def play_level_up_animation(self):
        self.level_up_animation.reset()
        self.active_animations.append(self.level_up_animation)

    def draw(self):
        self.screen.fill((0, 0, 0))  # Siyah arkaplan
        
        # Arkaplan resmini çiz
        if hasattr(self, 'background_image'):
            self.screen.blit(self.background_image, (0, 0))
        
        # Aktif animasyonları çiz
        for animation in self.active_animations[:]:
            animation.update()
            animation.draw(self.screen)
            if animation.is_finished():
                self.active_animations.remove(animation)
        
        # Duruma göre çizim yap
        if self.state == GameState.CHARACTER_CREATION:
            if not hasattr(self, 'character_creator') or self.character_creator is None:
                self.character_creator = CharacterCreator(self.width, self.height, self.manager)
            self.character_creator.draw(self.screen)
        elif self.state == GameState.GAME:
            # Oyun içi UI'ı çiz
            pass
        
        # UI'ı çiz
        self.manager.draw_ui(self.screen)
        
        # Ekranı güncelle
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            time_delta = self.clock.tick(self.fps)/1000.0
            
            for event in pygame.event.get():
                running = self.handle_event(event)
                if not running:
                    break
                    
            self.manager.update(time_delta)
            self.draw()

if __name__ == '__main__':
    game = LifeSimulator()
    game.run()