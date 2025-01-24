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
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Fontlar
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)

# Buton sınıfı
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        if self.is_hovered:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

# Ana menü butonları
buttons = [
    Button(300, 200, 200, 50, "Oyna", GREEN, (0, 200, 0)),
    Button(300, 300, 200, 50, "Yükle", BLUE, (0, 0, 200)),
    Button(300, 400, 200, 50, "Ayarlar", RED, (200, 0, 0)),
    Button(300, 500, 200, 50, "Çıkış", BLACK, (50, 50, 50))
]

# Ana menü döngüsü
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(pos):
                        if button.text == "Oyna":
                            return "play"
                        elif button.text == "Çıkış":
                            pygame.quit()
                            sys.exit()

        # Ekranı temizle
        screen.fill(WHITE)

        # Butonları çiz
        for button in buttons:
            button.draw(screen)

        # Ekranı güncelle
        pygame.display.flip()

# Karakter oluşturma
def character_creation():
    name = input("Karakter adını girin: ")
    gender = input("Cinsiyet seçin (Erkek/Kadın): ")
    appearance = input("Görünüş seçin (1: Sporcu, 2: Şık, 3: Rahat): ")
    print(f"{name} adlı {gender} karakter oluşturuldu! Görünüş: {appearance}")
    return name, gender, appearance

# Yaşam simülasyonu sınıfı
class LifeSimulator:
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.age = 0
        self.health = 100
        self.money = 0
        self.education = "Yok"
        self.job = "Yok"
        self.relationships = []

    def display_status(self):
        print(f"Ad: {self.name}, Yaş: {self.age}, Cinsiyet: {self.gender}")
        print(f"Sağlık: {self.health}, Para: {self.money}")
        print(f"Eğitim: {self.education}, Meslek: {self.job}")
        print(f"İlişkiler: {self.relationships}")

    def age_up(self):
        self.age += 1
        print(f"{self.name} bir yaş büyüdü! Şimdi {self.age} yaşında.")

    def random_event(self):
        events = [
            self._get_sick,
            self._find_money,
            self._make_friend,
            self._lose_friend
        ]
        random.choice(events)()

    def _get_sick(self):
        self.health -= 10
        print(f"{self.name} hastalandı! Sağlık: {self.health}")

    def _find_money(self):
        found_money = random.randint(10, 100)
        self.money += found_money
        print(f"{self.name} yerde {found_money} TL buldu! Toplam para: {self.money}")

    def _make_friend(self):
        friend_name = f"Arkadaş {random.randint(1, 100)}"
        self.relationships.append(friend_name)
        print(f"{self.name}, {friend_name} ile arkadaş oldu!")

    def _lose_friend(self):
        if self.relationships:
            lost_friend = random.choice(self.relationships)
            self.relationships.remove(lost_friend)
            print(f"{self.name}, {lost_friend} ile arkadaşlığını kaybetti.")
        else:
            print(f"{self.name}'in kaybedecek arkadaşı yok.")

# Hikaye akışı
def story_flow(player):
    print(f"{player.name} adlı karakterin yaşamı başlıyor...")
    for year in range(player.age, 100):
        print(f"\n--- {year} Yaşında ---")
        player.age_up()
        player.random_event()
        player.display_status()
        if year == 6:
            print("İlkokula başladın!")
            player.education = "İlkokul"
        elif year == 15:
            print("Liseye başladın!")
            player.education = "Lise"
        elif year == 18:
            print("Üniversiteye başladın!")
            player.education = "Üniversite"

# Oyunu başlat
if main_menu() == "play":
    name, gender, appearance = character_creation()
    player = LifeSimulator(name, gender)
    player.display_status()
    story_flow(player)