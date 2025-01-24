import pygame
import sys
import random

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

# Fontlar
font = pygame.font.Font(None, 36)

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
            "sosyal_beceri": 50
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
            self._nothing_happens
        ]
        random.choice(events)()

    def _get_sick(self):
        self.health -= 20
        print(f"{self.name} hastalandı! Sağlık: {self.health}")

    def _have_accident(self):
        self.health -= 30
        self.money -= 50
        print(f"{self.name} kaza geçirdi! Sağlık: {self.health}, Para: {self.money}")

    def _win_lottery(self):
        lottery_money = random.randint(1000, 5000)
        self.money += lottery_money
        print(f"{self.name} piyangodan {lottery_money} TL kazandı! Toplam para: {self.money}")

    def _find_money(self):
        found_money = random.randint(10, 100)
        self.money += found_money
        print(f"{self.name} yerde {found_money} TL buldu! Toplam para: {self.money}")

    def _nothing_happens(self):
        print(f"{self.name} için bu yıl sakin geçti. Hiçbir şey olmadı.")

    def go_to_school(self):
        if self.education_level == "İlkokul":
            self.education_level = "Lise"
            self.skills["zeka"] += 20
            print(f"{self.name} liseye başladı! Zeka: {self.skills['zeka']}")
        elif self.education_level == "Lise":
            self.education_level = "Üniversite"
            self.skills["zeka"] += 30
            print(f"{self.name} üniversiteye başladı! Zeka: {self.skills['zeka']}")
        else:
            print(f"{self.name} zaten en yüksek eğitim seviyesinde.")

    def work(self):
        if self.job == "Öğrenci":
            print(f"{self.name} öğrenci olduğu için çalışamıyor.")
        else:
            earned_money = random.randint(50, 200)
            self.money += earned_money
            print(f"{self.name} {earned_money} TL kazandı. Toplam para: {self.money} TL")

# Karakter oluşturma
player = Character("Ahmet", 18, "Erkek")

# Butonlar
buttons = [
    Button(50, 400, 150, 50, "Yaşlan", GREEN),
    Button(250, 400, 150, 50, "Çalış", BLUE),
    Button(450, 400, 150, 50, "Okula Git", RED)
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