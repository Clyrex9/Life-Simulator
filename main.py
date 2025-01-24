import pygame
import sys
import random
import time

# Pygame başlatma
pygame.init()

# Ekran boyutları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Life Simulator")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Fontlar
font = pygame.font.Font(None, 36)

# Metin animasyonu fonksiyonu
def draw_animated_text(screen, text, x, y, color=BLACK, delay=0.05):
    for i in range(len(text) + 1):
        screen.fill(WHITE)  # Ekranı temizle
        partial_text = text[:i]
        text_surface = font.render(partial_text, True, color)
        screen.blit(text_surface, (x, y))
        pygame.display.flip()
        time.sleep(delay)

# Buton sınıfı
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Character:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.health = 100
        self.money = 0
        self.job = "Öğrenci"
        self.education_level = "İlkokul"
        self.skills = {
            "zeka": 50,
            "fiziksel_güç": 50,
            "sosyal_beceri": 50,
            "sanat": 0,
            "spor": 0
        }
        self.relationships = {
            "arkadaşlar": [],
            "aile": [],
            "romantik": None
        }

    def display_info(self, screen):
        y_offset = 50
        info_lines = [
            f"Ad: {self.name}, Yaş: {self.age}, Cinsiyet: {self.gender}",
            f"Sağlık: {self.health}, Para: {self.money}, Meslek: {self.job}",
            f"Eğitim Seviyesi: {self.education_level}",
            f"Yetenekler: Zeka: {self.skills['zeka']}, Fiziksel Güç: {self.skills['fiziksel_güç']}, Sosyal Beceri: {self.skills['sosyal_beceri']}",
            f"Sanat: {self.skills['sanat']}, Spor: {self.skills['spor']}",
            f"İlişkiler: Arkadaşlar: {self.relationships['arkadaşlar']}, Aile: {self.relationships['aile']}, Romantik: {self.relationships['romantik']}"
        ]
        for line in info_lines:
            text = font.render(line, True, BLACK)
            screen.blit(text, (50, y_offset))
            y_offset += 40

    def age_up(self):
        self.age += 1
        self.random_event()

    def random_event(self):
        events = [
            self._get_sick,
            self._have_accident,
            self._win_lottery,
            self._find_money,
            self._nothing_happens,
            self._get_promoted,
            self._lose_job,
            self._learn_new_skill,
            self._lose_friend,
            self._family_member_gets_sick,
            self._break_up
        ]
        random.choice(events)()

    def _get_sick(self):
        self.health -= 20
        draw_animated_text(screen, f"{self.name} hastalandı! Sağlık: {self.health}", 50, 300, RED)

    def _have_accident(self):
        self.health -= 30
        self.money -= 50
        draw_animated_text(screen, f"{self.name} kaza geçirdi! Sağlık: {self.health}, Para: {self.money}", 50, 300, RED)

    def _win_lottery(self):
        lottery_money = random.randint(1000, 5000)
        self.money += lottery_money
        draw_animated_text(screen, f"{self.name} piyangodan {lottery_money} TL kazandı! Toplam para: {self.money}", 50, 300, GREEN)

    def _find_money(self):
        found_money = random.randint(10, 100)
        self.money += found_money
        draw_animated_text(screen, f"{self.name} yerde {found_money} TL buldu! Toplam para: {self.money}", 50, 300, GREEN)

    def _nothing_happens(self):
        draw_animated_text(screen, f"{self.name} için bu yıl sakin geçti. Hiçbir şey olmadı.", 50, 300, BLACK)

    def _get_promoted(self):
        if self.job != "Öğrenci":
            self.money += 500
            draw_animated_text(screen, f"{self.name} işinde terfi etti! Yeni maaş: {self.money} TL", 50, 300, GREEN)
        else:
            draw_animated_text(screen, f"{self.name} öğrenci olduğu için terfi edemez.", 50, 300, RED)

    def _lose_job(self):
        if self.job != "Öğrenci":
            self.job = "İşsiz"
            self.money -= 200
            draw_animated_text(screen, f"{self.name} işten atıldı! Yeni durum: İşsiz, Para: {self.money} TL", 50, 300, RED)
        else:
            draw_animated_text(screen, f"{self.name} öğrenci olduğu için işten atılamaz.", 50, 300, RED)

    def _learn_new_skill(self):
        skill = random.choice(["sanat", "spor"])
        self.skills[skill] += 20
        draw_animated_text(screen, f"{self.name} yeni bir yetenek öğrendi: {skill.capitalize()}!", 50, 300, BLUE)

    def _lose_friend(self):
        if self.relationships["arkadaşlar"]:
            lost_friend = random.choice(self.relationships["arkadaşlar"])
            self.relationships["arkadaşlar"].remove(lost_friend)
            draw_animated_text(screen, f"{self.name}, {lost_friend} ile arkadaşlığını kaybetti.", 50, 300, RED)
        else:
            draw_animated_text(screen, f"{self.name}'in kaybedecek arkadaşı yok.", 50, 300, BLACK)

    def _family_member_gets_sick(self):
        if self.relationships["aile"]:
            sick_member = random.choice(self.relationships["aile"])
            self.money -= 100
            draw_animated_text(screen, f"{sick_member} hastalandı! Sağlık harcamaları: 100 TL, Para: {self.money} TL", 50, 300, RED)
        else:
            draw_animated_text(screen, f"{self.name}'in ailesinde hastalanacak kimse yok.", 50, 300, BLACK)

    def _break_up(self):
        if self.relationships["romantik"]:
            partner = self.relationships["romantik"]
            self.relationships["romantik"] = None
            draw_animated_text(screen, f"{self.name}, {partner} ile ayrıldı.", 50, 300, RED)
        else:
            draw_animated_text(screen, f"{self.name}'in ayrılacak bir ilişkisi yok.", 50, 300, BLACK)

    def go_to_school(self):
        if self.education_level == "İlkokul":
            self.education_level = "Lise"
            self.skills["zeka"] += 20
            draw_animated_text(screen, f"{self.name} liseye başladı! Zeka: {self.skills['zeka']}", 50, 300, BLUE)
        elif self.education_level == "Lise":
            self.education_level = "Üniversite"
            self.skills["zeka"] += 30
            draw_animated_text(screen, f"{self.name} üniversiteye başladı! Zeka: {self.skills['zeka']}", 50, 300, BLUE)
        else:
            draw_animated_text(screen, f"{self.name} zaten en yüksek eğitim seviyesinde.", 50, 300, BLACK)

    def work(self):
        if self.job == "Öğrenci":
            draw_animated_text(screen, f"{self.name} öğrenci olduğu için çalışamıyor.", 50, 300, RED)
        else:
            earned_money = random.randint(50, 200)
            self.money += earned_money
            draw_animated_text(screen, f"{self.name} {earned_money} TL kazandı. Toplam para: {self.money} TL", 50, 300, GREEN)

    def make_friend(self):
        friend_name = f"Arkadaş {random.randint(1, 100)}"
        self.relationships["arkadaşlar"].append(friend_name)
        draw_animated_text(screen, f"{self.name}, {friend_name} ile arkadaş oldu!", 50, 300, YELLOW)

    def add_family_member(self):
        family_member = f"Aile Üyesi {random.randint(1, 100)}"
        self.relationships["aile"].append(family_member)
        draw_animated_text(screen, f"{family_member}, {self.name}'in ailesine eklendi.", 50, 300, PURPLE)

    def start_romantic_relationship(self):
        if self.relationships["romantik"]:
            draw_animated_text(screen, f"{self.name} zaten {self.relationships['romantik']} ile bir ilişki içinde.", 50, 300, RED)
        else:
            partner_name = f"Partner {random.randint(1, 100)}"
            self.relationships["romantik"] = partner_name
            draw_animated_text(screen, f"{self.name}, {partner_name} ile romantik bir ilişkiye başladı!", 50, 300, PURPLE)

# Karakter oluşturma
player = Character("Ahmet", 18, "Erkek")

# Butonlar
buttons = [
    Button(50, 400, 150, 50, "Yaşlan", GREEN),
    Button(250, 400, 150, 50, "Çalış", BLUE),
    Button(450, 400, 150, 50, "Okula Git", RED),
    Button(50, 500, 150, 50, "Arkadaş Edin", YELLOW),
    Button(250, 500, 150, 50, "Aile Ekle", PURPLE),
    Button(450, 500, 150, 50, "Romantik İlişki", RED)
]

# Oyun döngüsü
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.is_clicked(pos):
                    if button.text == "Yaşlan":
                        player.age_up()
                    elif button.text == "Çalış":
                        player.work()
                    elif button.text == "Okula Git":
                        player.go_to_school()
                    elif button.text == "Arkadaş Edin":
                        player.make_friend()
                    elif button.text == "Aile Ekle":
                        player.add_family_member()
                    elif button.text == "Romantik İlişki":
                        player.start_romantic_relationship()

    # Ekranı temizle
    screen.fill(WHITE)

    # Karakter bilgilerini göster
    player.display_info(screen)

    # Butonları çiz
    for button in buttons:
        button.draw(screen)

    # Ekranı güncelle
    pygame.display.flip()

    # FPS ayarı
    clock.tick(30)

# Pygame'i kapat
pygame.quit()
sys.exit()