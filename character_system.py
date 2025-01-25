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
        
        # Karakter özellikleri
        self.traits = {
            'Kişilik': ['Dışa Dönük', 'İçe Dönük', 'Yaratıcı', 'Analitik', 'Lider'],
            'Hobiler': ['Spor', 'Sanat', 'Müzik', 'Oyun', 'Kitap'],
            'Yetenekler': ['İletişim', 'Problem Çözme', 'Organizasyon', 'Yaratıcılık', 'Teknik']
        }
        
        # Başlangıç değerleri
        self.starting_stats = {
            'Zeka': {'min': 40, 'max': 80},
            'Karizma': {'min': 40, 'max': 80},
            'Enerji': {'min': 40, 'max': 80},
            'Sağlık': {'min': 70, 'max': 100}
        }
        
        self.selected_traits = {
            'Kişilik': None,
            'Hobiler': None,
            'Yetenekler': None
        }
        
        self.appearance = {
            'Saç Stili': ['Kısa', 'Uzun', 'Dalgalı', 'Düz'],
            'Saç Rengi': ['Siyah', 'Kahverengi', 'Sarı', 'Kızıl'],
            'Göz Rengi': ['Kahverengi', 'Mavi', 'Yeşil', 'Ela'],
            'Giyim Stili': ['Spor', 'Klasik', 'Rahat', 'Şık']
        }
        
        self.selected_appearance = {k: None for k in self.appearance.keys()}
        
    def create_ui(self):
        self.elements = {}
        
        # Ana panel
        self.elements['main_panel'] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((50, 50), (self.screen_width - 100, self.screen_height - 100)),
            manager=self.manager
        )
        
        # Başlık
        self.elements['title'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 10), (self.screen_width - 100, 40)),
            text='Karakter Oluşturma',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # İsim girişi
        self.elements['name_label'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 60), (100, 30)),
            text='İsim:',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        self.elements['name_entry'] = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((130, 60), (200, 30)),
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Cinsiyet seçimi
        self.elements['gender_label'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 100), (100, 30)),
            text='Cinsiyet:',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        self.elements['gender_dropdown'] = pygame_gui.elements.UIDropDownMenu(
            options_list=['Erkek', 'Kadın'],
            starting_option='Erkek',
            relative_rect=pygame.Rect((130, 100), (200, 30)),
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Görünüş seçimleri
        y_pos = 150
        for key, options in self.appearance.items():
            self.elements[f'{key}_label'] = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((20, y_pos), (100, 30)),
                text=key + ':',
                manager=self.manager,
                container=self.elements['main_panel']
            )
            
            self.elements[f'{key}_dropdown'] = pygame_gui.elements.UIDropDownMenu(
                options_list=options,
                starting_option=options[0],
                relative_rect=pygame.Rect((130, y_pos), (200, 30)),
                manager=self.manager,
                container=self.elements['main_panel']
            )
            y_pos += 40
        
        # Karakter özellikleri
        x_offset = 400
        y_pos = 60
        for category, traits in self.traits.items():
            self.elements[f'{category}_label'] = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((x_offset, y_pos), (100, 30)),
                text=category + ':',
                manager=self.manager,
                container=self.elements['main_panel']
            )
            
            self.elements[f'{category}_dropdown'] = pygame_gui.elements.UIDropDownMenu(
                options_list=traits,
                starting_option=traits[0],
                relative_rect=pygame.Rect((x_offset + 110, y_pos), (200, 30)),
                manager=self.manager,
                container=self.elements['main_panel']
            )
            y_pos += 40
        
        # Başlangıç değerleri (rastgele)
        y_pos += 20
        self.elements['stats_title'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((x_offset, y_pos), (310, 30)),
            text='Başlangıç Değerleri:',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        y_pos += 40
        self.stat_labels = {}
        for stat, range_values in self.starting_stats.items():
            value = random.randint(range_values['min'], range_values['max'])
            self.stat_labels[stat] = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((x_offset, y_pos), (310, 30)),
                text=f'{stat}: {value}',
                manager=self.manager,
                container=self.elements['main_panel']
            )
            y_pos += 30
        
        # Karakter oluştur butonu
        self.elements['create_button'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width//2 - 150, self.screen_height - 200), (300, 50)),
            text='Karakteri Oluştur',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Yeniden atama butonu
        self.elements['reroll_button'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x_offset, y_pos + 20), (200, 40)),
            text='Değerleri Yeniden At',
            manager=self.manager,
            container=self.elements['main_panel']
        )

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.elements['create_button']:
                return self.create_character()
            elif event.ui_element == self.elements['reroll_button']:
                self.reroll_stats()
        
        return None

    def reroll_stats(self):
        for stat, range_values in self.starting_stats.items():
            value = random.randint(range_values['min'], range_values['max'])
            self.stat_labels[stat].set_text(f'{stat}: {value}')

    def create_character(self):
        character_data = {
            'name': self.elements['name_entry'].get_text(),
            'gender': self.elements['gender_dropdown'].selected_option,
            'appearance': {
                key: self.elements[f'{key}_dropdown'].selected_option
                for key in self.appearance.keys()
            },
            'traits': {
                category: self.elements[f'{category}_dropdown'].selected_option
                for category in self.traits.keys()
            },
            'stats': {
                stat: int(self.stat_labels[stat].text.split(': ')[1])
                for stat in self.starting_stats.keys()
            }
        }
        
        return character_data

class Character:
    def __init__(self, data):
        self.name = data['name']
        self.gender = data['gender']
        self.appearance = data['appearance']
        self.traits = data['traits']
        
        # Temel özellikler ve stats'i data'dan alıyoruz
        self.stats = {
            'Mutluluk': 100,
            'Sağlık': data['stats']['Sağlık'],
            'Zeka': data['stats']['Zeka'],
            'Enerji': data['stats']['Enerji'],
            'Karizma': data['stats']['Karizma']
        }
        
        self.age = 0
        self.money = 1000
        self.education = {"level": "Yok", "school": ""}
        self.job = {"title": "Yok", "salary": 0}
        self.relationships = []
        self.inventory = []
        
        # Yetenekler ve deneyimler
        self.skills = {
            'İletişim': 0,
            'Problem Çözme': 0,
            'Organizasyon': 0,
            'Yaratıcılık': 0,
            'Teknik': 0
        }
        
        # Başlangıç yeteneği bonusu
        self.apply_trait_bonuses()
    
    def apply_trait_bonuses(self):
        # Kişilik bonusları
        personality_bonuses = {
            'Dışa Dönük': {'İletişim': 10},
            'İçe Dönük': {'Problem Çözme': 10},
            'Yaratıcı': {'Yaratıcılık': 10},
            'Analitik': {'Teknik': 10},
            'Lider': {'Organizasyon': 10}
        }
        
        if self.traits['Kişilik'] in personality_bonuses:
            for skill, bonus in personality_bonuses[self.traits['Kişilik']].items():
                self.skills[skill] += bonus
    
    def age_up(self):
        self.age += 1
        self.apply_age_effects()
        return self.generate_age_events()
    
    def apply_age_effects(self):
        # Yaşa bağlı değişimler
        if self.age < 18:
            self.stats['Enerji'] = min(100, self.stats['Enerji'] + 2)
        elif self.age > 50:
            self.stats['Enerji'] = max(0, self.stats['Enerji'] - 1)
    
    def generate_age_events(self):
        events = []
        
        # Yaşa özel olaylar
        if self.age == 6:
            events.append("İlkokula başlama zamanı!")
            self.education['level'] = 'İlkokul'
        elif self.age == 15:
            events.append("Lise çağına geldin!")
            self.education['level'] = 'Lise'
        elif self.age == 18:
            events.append("Reşit oldun! Artık kendi kararlarını verebilirsin.")
        
        # Random olaylar
        if random.random() < 0.3:  # %30 şans
            possible_events = [
                "Yeni bir hobi keşfettin!",
                "Bir yarışmaya katıldın.",
                "Yeni arkadaşlar edindin.",
                "Bir kitap okudun ve yeni şeyler öğrendin."
            ]
            events.append(random.choice(possible_events))
        
        return events
