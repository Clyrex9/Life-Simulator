import random

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

    def display_info(self):
        print(f"Ad: {self.name}, Yaş: {self.age}, Cinsiyet: {self.gender}")
        print(f"Sağlık: {self.health}, Para: {self.money}, Meslek: {self.job}")
        print(f"Eğitim Seviyesi: {self.education_level}")
        print(f"Yetenekler: Zeka: {self.skills['zeka']}, Fiziksel Güç: {self.skills['fiziksel_güç']}, Sosyal Beceri: {self.skills['sosyal_beceri']}")

    def age_up(self):
        self.age += 1
        print(f"{self.name} bir yaş büyüdü! Şimdi {self.age} yaşında.")
        self.random_event()  # Yaşlanınca rastgele bir olay tetikle

    def check_health(self):
        if self.health > 70:
            print(f"{self.name} sağlıklı görünüyor.")
        elif self.health > 30:
            print(f"{self.name} biraz hasta görünüyor.")
        else:
            print(f"{self.name} çok hasta! Acilen doktora gitmeli.")

    def work(self):
        if self.job == "Öğrenci":
            print(f"{self.name} öğrenci olduğu için çalışamıyor.")
        else:
            earned_money = random.randint(50, 200)
            self.money += earned_money
            print(f"{self.name} {earned_money} TL kazandı. Toplam para: {self.money} TL")

    def change_job(self, new_job):
        self.job = new_job
        print(f"{self.name} artık {self.job} olarak çalışıyor.")

    def random_event(self):
        events = [
            self._get_sick,
            self._have_accident,
            self._win_lottery,
            self._find_money,
            self._nothing_happens
        ]
        random.choice(events)()  # Rastgele bir olay seç ve tetikle

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

# Karakter oluşturma
player_name = input("Karakter adını girin: ")
player_age = int(input("Karakter yaşını girin: "))
player_gender = input("Karakter cinsiyetini girin (Erkek/Kadın): ")

player = Character(player_name, player_age, player_gender)
player.display_info()

# Yaşlanma ve rastgele olaylar
player.age_up()
player.display_info()

# Sağlık kontrolü
player.check_health()

# Eğitim alma
player.go_to_school()
player.display_info()

# Meslek değiştirme
player.change_job("Mühendis")
player.display_info()

# Çalışma
player.work()
player.display_info()