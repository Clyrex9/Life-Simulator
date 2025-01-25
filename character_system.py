import pygame
import pygame_gui
import json
import random
from pathlib import Path

class CharacterCreator:
    def __init__(self, screen_width, screen_height, manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.manager = manager
        
        self.selected_gender = 'Erkek'
        self.current_character_index = 1
        self.max_character_index = 5
        
        # Karakter resimlerini yükle
        self.character_images = {
            'Erkek': {},
            'Kadın': {}
        }
        self.load_all_character_images()
        
        # Başlangıç değerleri
        self.starting_stats = {
            'Zeka': {'min': 40, 'max': 80},
            'Karizma': {'min': 40, 'max': 80},
            'Enerji': {'min': 40, 'max': 80},
            'Sağlık': {'min': 80, 'max': 100}
        }
        
        self.stat_values = {}
        self.reroll_stats()  # İlk stats değerlerini oluştur
        self.create_ui()
        
    def load_all_character_images(self):
        for i in range(1, self.max_character_index + 1):
            # Erkek karakterleri yükle
            try:
                male_img = pygame.image.load(f'assets/characters/male{i}.png')
                male_img = pygame.transform.scale(male_img, (180, 270))  # Biraz daha küçük
                self.character_images['Erkek'][i] = male_img
            except pygame.error as e:
                print(f"Erkek karakter {i} yüklenemedi: {e}")
                # Yüklenemezse siyah kare oluştur
                self.character_images['Erkek'][i] = pygame.Surface((180, 270))
                self.character_images['Erkek'][i].fill((0, 0, 0))
                
            # Kadın karakterleri yükle
            try:
                female_img = pygame.image.load(f'assets/characters/female{i}.png')
                female_img = pygame.transform.scale(female_img, (180, 270))  # Biraz daha küçük
                self.character_images['Kadın'][i] = female_img
            except pygame.error as e:
                print(f"Kadın karakter {i} yüklenemedi: {e}")
                # Yüklenemezse siyah kare oluştur
                self.character_images['Kadın'][i] = pygame.Surface((180, 270))
                self.character_images['Kadın'][i].fill((0, 0, 0))
                
    def get_current_character_image(self):
        return self.character_images[self.selected_gender].get(self.current_character_index)
            
    def next_character(self):
        self.current_character_index = (self.current_character_index % self.max_character_index) + 1
        
    def prev_character(self):
        self.current_character_index = (self.current_character_index - 2) % self.max_character_index + 1
        
    def toggle_gender(self):
        self.selected_gender = 'Kadın' if self.selected_gender == 'Erkek' else 'Erkek'
        self.elements['gender_button'].set_text(self.selected_gender)
        self.current_character_index = 1
        
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.elements['prev_character']:
                self.prev_character()
                return None
            elif event.ui_element == self.elements['next_character']:
                self.next_character()
                return None
            elif event.ui_element == self.elements['gender_button']:
                self.toggle_gender()
                return None
            elif event.ui_element == self.elements['reroll_button']:
                self.reroll_stats()
                return None
            elif event.ui_element == self.elements['create_button']:
                return self.create_character()
        return None
        
    def reroll_stats(self):
        for stat in self.starting_stats.keys():
            value = random.randint(self.starting_stats[stat]['min'], self.starting_stats[stat]['max'])
            self.stat_values[stat] = value
            if hasattr(self, 'elements') and f'{stat}_label' in self.elements:
                self.elements[f'{stat}_label'].set_text(f'{stat}: {value}')
            
    def create_character(self):
        name = self.elements['name_entry'].get_text()
        if not name:
            return None
            
        character_data = {
            'name': name,
            'gender': self.selected_gender,
            'appearance': f'{"male" if self.selected_gender == "Erkek" else "female"}{self.current_character_index}',
            'traits': {
                'Kişilik': self.elements['personality_dropdown'].selected_option,
                'Hobiler': self.elements['hobbies_dropdown'].selected_option,
                'Yetenekler': self.elements['skills_dropdown'].selected_option
            },
            'stats': self.stat_values
        }
        
        return character_data
        
    def draw(self, screen):
        # Karakter resmini çiz
        character_image = self.get_current_character_image()
        if character_image:
            panel_rect = self.elements['character_panel'].get_relative_rect()
            image_x = panel_rect.x + (panel_rect.width - character_image.get_width()) // 2
            image_y = panel_rect.y + 20  # Biraz yukarıdan başlat
            screen.blit(character_image, (image_x, image_y))
        
    def create_ui(self):
        # Ana panel
        panel_width = 800
        panel_height = 600
        panel_x = (self.screen_width - panel_width) // 2
        panel_y = (self.screen_height - panel_height) // 2
        
        self.elements = {}
        self.elements['main_panel'] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((panel_x, panel_y), (panel_width, panel_height)),
            manager=self.manager
        )
        
        # Başlık
        self.elements['title'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 20), (panel_width, 40)),
            text='Karakter Oluşturma',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Sol Panel - Karakter Görseli
        character_panel_width = 250
        character_panel_height = 400
        self.elements['character_panel'] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((50, 80), (character_panel_width, character_panel_height)),
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Karakter değiştirme butonları
        button_width = 40
        button_height = 40
        button_y = character_panel_height // 2 - button_height // 2
        
        self.elements['prev_character'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, button_y), (button_width, button_height)),
            text='<',
            manager=self.manager,
            container=self.elements['character_panel']
        )
        
        self.elements['next_character'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((character_panel_width - button_width - 10, button_y), 
                                    (button_width, button_height)),
            text='>',
            manager=self.manager,
            container=self.elements['character_panel']
        )
        
        # Cinsiyet değiştirme butonu
        gender_button_width = 120
        gender_button_height = 40
        self.elements['gender_button'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((character_panel_width//2 - gender_button_width//2, 
                                     character_panel_height - gender_button_height - 10),
                                    (gender_button_width, gender_button_height)),
            text=self.selected_gender,
            manager=self.manager,
            container=self.elements['character_panel']
        )
        
        # Sağ Panel - Karakter Bilgileri
        right_panel_x = 350
        right_panel_width = 400
        
        # İsim girişi
        self.elements['name_label'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((right_panel_x, 100), (100, 30)),
            text='İsim:',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        self.elements['name_entry'] = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((right_panel_x + 110, 100), (250, 30)),
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Dropdown'lar için yükseklik ve boşluk ayarları
        dropdown_height = 35
        vertical_spacing = 20
        label_height = 30
        
        # Kişilik
        y_pos = 160
        self.elements['personality_label'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((right_panel_x, y_pos), (right_panel_width, label_height)),
            text='Kişilik:',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        y_pos += label_height
        self.elements['personality_dropdown'] = pygame_gui.elements.UIDropDownMenu(
            options_list=['Dışa Dönük', 'İçe Dönük', 'Yaratıcı', 'Analitik', 'Lider'],
            starting_option='Dışa Dönük',
            relative_rect=pygame.Rect((right_panel_x, y_pos), (right_panel_width, dropdown_height)),
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Hobiler
        y_pos += dropdown_height + vertical_spacing
        self.elements['hobbies_label'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((right_panel_x, y_pos), (right_panel_width, label_height)),
            text='Hobiler:',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        y_pos += label_height
        self.elements['hobbies_dropdown'] = pygame_gui.elements.UIDropDownMenu(
            options_list=['Spor', 'Sanat', 'Müzik', 'Oyun', 'Kitap'],
            starting_option='Spor',
            relative_rect=pygame.Rect((right_panel_x, y_pos), (right_panel_width, dropdown_height)),
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Yetenekler
        y_pos += dropdown_height + vertical_spacing
        self.elements['skills_label'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((right_panel_x, y_pos), (right_panel_width, label_height)),
            text='Yetenekler:',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        y_pos += label_height
        self.elements['skills_dropdown'] = pygame_gui.elements.UIDropDownMenu(
            options_list=['İletişim', 'Problem Çözme', 'Organizasyon', 'Yaratıcılık', 'Teknik'],
            starting_option='İletişim',
            relative_rect=pygame.Rect((right_panel_x, y_pos), (right_panel_width, dropdown_height)),
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Stats paneli
        stats_panel_height = 150
        self.elements['stats_panel'] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((right_panel_x, y_pos + dropdown_height + vertical_spacing), 
                                    (right_panel_width, stats_panel_height)),
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Stats değerleri
        stats_y = 10
        for stat in self.starting_stats.keys():
            self.elements[f'{stat}_label'] = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, stats_y), (right_panel_width - 20, label_height)),
                text=f'{stat}: {self.stat_values[stat]}',
                manager=self.manager,
                container=self.elements['stats_panel']
            )
            stats_y += label_height
        
        # Yeniden At butonu
        self.elements['reroll_button'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, stats_panel_height - 50), (right_panel_width - 20, 40)),
            text='Değerleri Yeniden At',
            manager=self.manager,
            container=self.elements['stats_panel']
        )
        
        # Karakteri Oluştur butonu
        self.elements['create_button'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((panel_width//2 - 100, panel_height - 60), (200, 40)),
            text='Karakteri Oluştur',
            manager=self.manager,
            container=self.elements['main_panel']
        )

class Character:
    def __init__(self, data):
        self.name = data['name']
        self.gender = data['gender']
        self.appearance = data['appearance']
        self.traits = data['traits']
        self.stats = data['stats']
        self.age = 18
        self.money = 1000
        self.education = {
            'level': 'Lise',
            'school': None,
            'grades': []
        }
        self.job = None
        self.relationships = []
        
    def age_up(self):
        self.age += 1
        events = [f"{self.age}. yaşına girdin!"]
        
        # Rastgele olaylar ve stat değişimleri
        for stat in self.stats:
            change = random.randint(-5, 5)
            self.stats[stat] = max(0, min(100, self.stats[stat] + change))
            if abs(change) > 2:
                if change > 0:
                    events.append(f"{stat} +{change} arttı!")
                else:
                    events.append(f"{stat} {change} azaldı!")
                    
        return events
