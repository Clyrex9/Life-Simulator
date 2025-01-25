import pygame
import pygame_gui
import random

class School:
    def __init__(self, name, level, quality, tuition):
        self.name = name
        self.level = level  # İlkokul, Ortaokul, Lise, Üniversite
        self.quality = quality  # 1-10 arası
        self.tuition = tuition  # Yıllık ücret
        self.courses = self.generate_courses()
    
    def generate_courses(self):
        base_courses = {
            'İlkokul': ['Matematik', 'Türkçe', 'Hayat Bilgisi', 'Resim', 'Müzik', 'Beden Eğitimi'],
            'Ortaokul': ['Matematik', 'Türkçe', 'Fen Bilgisi', 'Sosyal Bilgiler', 'İngilizce', 'Resim', 'Müzik', 'Beden Eğitimi'],
            'Lise': ['Matematik', 'Türkçe', 'Fizik', 'Kimya', 'Biyoloji', 'Tarih', 'Coğrafya', 'İngilizce'],
            'Üniversite': {
                'Mühendislik': ['Matematik', 'Fizik', 'Programlama', 'Elektronik', 'Veri Yapıları'],
                'Tıp': ['Anatomi', 'Biyoloji', 'Kimya', 'Fizyoloji', 'Patoloji'],
                'İşletme': ['Ekonomi', 'Muhasebe', 'Pazarlama', 'Yönetim', 'Finans'],
                'Hukuk': ['Medeni Hukuk', 'Ceza Hukuku', 'Anayasa Hukuku', 'Borçlar Hukuku', 'İdare Hukuku'],
                'Psikoloji': ['Gelişim Psikolojisi', 'Sosyal Psikoloji', 'Klinik Psikoloji', 'Deneysel Psikoloji', 'Nöropsikoloji']
            }
        }
        
        return base_courses[self.level]

class EducationSystem:
    def __init__(self, screen_width, screen_height, manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.manager = manager
        self.schools = self.generate_schools()
        self.active_school = None
        self.current_menu = None
        self.elements = {}
        
    def generate_schools(self):
        schools = {
            'İlkokul': [
                School('Atatürk İlkokulu', 'İlkokul', 7, 5000),
                School('Cumhuriyet İlkokulu', 'İlkokul', 8, 7000),
                School('Özel Gelişim İlkokulu', 'İlkokul', 9, 15000)
            ],
            'Ortaokul': [
                School('Fatih Ortaokulu', 'Ortaokul', 7, 6000),
                School('Bilge Ortaokulu', 'Ortaokul', 8, 8000),
                School('Özel Başarı Ortaokulu', 'Ortaokul', 9, 18000)
            ],
            'Lise': [
                School('Anadolu Lisesi', 'Lise', 7, 8000),
                School('Fen Lisesi', 'Lise', 9, 10000),
                School('Özel Kariyer Lisesi', 'Lise', 8, 25000)
            ],
            'Üniversite': [
                School('Devlet Üniversitesi', 'Üniversite', 7, 2000),
                School('Teknik Üniversite', 'Üniversite', 9, 3000),
                School('Özel Üniversite', 'Üniversite', 8, 50000)
            ]
        }
        return schools
    
    def show_school_selection(self, character):
        self.current_menu = 'school_selection'
        self.clear_ui()
        
        # Mevcut eğitim durumuna göre uygun okulları göster
        available_level = self.get_next_education_level(character)
        if not available_level:
            self.show_message("Şu anda kayıt olabileceğin bir okul yok.")
            return
        
        # Ana panel
        panel_width = 600
        panel_height = 500
        self.elements['main_panel'] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.screen_width//2 - panel_width//2, 
                                     self.screen_height//2 - panel_height//2),
                                    (panel_width, panel_height)),
            manager=self.manager
        )
        
        # Başlık
        self.elements['title'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 10), (panel_width, 40)),
            text=f'Okul Seçimi - {available_level}',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Okul listesi
        y_pos = 60
        for school in self.schools[available_level]:
            # Okul container'ı
            container_height = 100
            school_container = pygame_gui.elements.UIPanel(
                relative_rect=pygame.Rect((10, y_pos), (panel_width-20, container_height)),
                manager=self.manager,
                container=self.elements['main_panel']
            )
            
            # Okul bilgileri
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, 5), (400, 25)),
                text=f'{school.name}',
                manager=self.manager,
                container=school_container
            )
            
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, 30), (400, 25)),
                text=f'Kalite: {school.quality}/10 | Yıllık Ücret: {school.tuition}₺',
                manager=self.manager,
                container=school_container
            )
            
            # Kayıt ol butonu
            self.elements[f'enroll_{school.name}'] = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((panel_width-140, 60), (100, 30)),
                text='Kayıt Ol',
                manager=self.manager,
                container=school_container
            )
            
            y_pos += container_height + 10
        
        # Geri dön butonu
        self.elements['back'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, panel_height-40), (100, 30)),
            text='Geri Dön',
            manager=self.manager,
            container=self.elements['main_panel']
        )
    
    def show_current_school_info(self, character):
        self.current_menu = 'school_info'
        self.clear_ui()
        
        if not character.education['school']:
            self.show_message("Şu anda okula gitmiyorsun.")
            return
        
        # Ana panel
        panel_width = 600
        panel_height = 500
        self.elements['main_panel'] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.screen_width//2 - panel_width//2, 
                                     self.screen_height//2 - panel_height//2),
                                    (panel_width, panel_height)),
            manager=self.manager
        )
        
        # Başlık
        self.elements['title'] = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 10), (panel_width, 40)),
            text=f'Okul Bilgileri - {character.education["school"]}',
            manager=self.manager,
            container=self.elements['main_panel']
        )
        
        # Ders listesi ve notlar
        y_pos = 60
        if 'grades' in character.education:
            for course, grade in character.education['grades'].items():
                pygame_gui.elements.UILabel(
                    relative_rect=pygame.Rect((10, y_pos), (panel_width-20, 30)),
                    text=f'{course}: {grade}',
                    manager=self.manager,
                    container=self.elements['main_panel']
                )
                y_pos += 35
        
        # Geri dön butonu
        self.elements['back'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, panel_height-40), (100, 30)),
            text='Geri Dön',
            manager=self.manager,
            container=self.elements['main_panel']
        )
    
    def show_message(self, message):
        # Mesaj kutusu
        panel_width = 400
        panel_height = 200
        self.elements['message_panel'] = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.screen_width//2 - panel_width//2, 
                                     self.screen_height//2 - panel_height//2),
                                    (panel_width, panel_height)),
            manager=self.manager
        )
        
        self.elements['message'] = pygame_gui.elements.UITextBox(
            html_text=message,
            relative_rect=pygame.Rect((10, 10), (panel_width-20, panel_height-60)),
            manager=self.manager,
            container=self.elements['message_panel']
        )
        
        self.elements['ok_button'] = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((panel_width//2 - 50, panel_height-40), (100, 30)),
            text='Tamam',
            manager=self.manager,
            container=self.elements['message_panel']
        )
    
    def get_next_education_level(self, character):
        education_path = ['İlkokul', 'Ortaokul', 'Lise', 'Üniversite']
        current_level = character.education['level']
        
        if character.age < 6:
            return 'İlkokul'
        elif current_level == 'Yok' and character.age >= 6:
            return 'İlkokul'
        elif current_level == 'İlkokul' and character.age >= 11:
            return 'Ortaokul'
        elif current_level == 'Ortaokul' and character.age >= 15:
            return 'Lise'
        elif current_level == 'Lise' and character.age >= 18:
            return 'Üniversite'
        
        return None
    
    def clear_ui(self):
        for element in self.elements.values():
            element.kill()
        self.elements.clear()
    
    def handle_event(self, event, character):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.elements.get('back'):
                self.clear_ui()
                return 'back'
            
            elif event.ui_element == self.elements.get('ok_button'):
                self.clear_ui()
                return 'back'
            
            # Okul kayıt butonları
            for school_level in self.schools:
                for school in self.schools[school_level]:
                    if event.ui_element == self.elements.get(f'enroll_{school.name}'):
                        if character.money >= school.tuition:
                            character.money -= school.tuition
                            character.education['level'] = school_level
                            character.education['school'] = school.name
                            character.education['grades'] = {course: '-' for course in school.courses}
                            self.show_message(f"{school.name}'a başarıyla kayıt oldun!")
                            return 'enrolled'
                        else:
                            self.show_message("Yeterli paran yok!")
                            return None
        
        return None
    
    def update_grades(self, character):
        if not character.education['school'] or 'grades' not in character.education:
            return
        
        # Her dersi güncelle
        for course in character.education['grades'].keys():
            # Zeka ve çalışma faktörüne göre not hesapla
            base_grade = random.randint(50, 85)
            intelligence_bonus = (character.stats['Zeka'] - 50) // 5  # Her 5 zeka puanı için +1
            grade = min(100, max(0, base_grade + intelligence_bonus))
            
            # Harf notuna çevir
            if grade >= 90:
                character.education['grades'][course] = 'AA'
            elif grade >= 85:
                character.education['grades'][course] = 'BA'
            elif grade >= 80:
                character.education['grades'][course] = 'BB'
            elif grade >= 75:
                character.education['grades'][course] = 'CB'
            elif grade >= 70:
                character.education['grades'][course] = 'CC'
            elif grade >= 65:
                character.education['grades'][course] = 'DC'
            elif grade >= 60:
                character.education['grades'][course] = 'DD'
            else:
                character.education['grades'][course] = 'FF'
            
            # Ders başarısına göre zeka artışı
            if grade >= 80:
                character.stats['Zeka'] = min(100, character.stats['Zeka'] + 1)