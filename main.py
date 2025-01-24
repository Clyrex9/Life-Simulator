import random

class Character:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.health = 100
        self.money = 0
        self.job = "Öğrenci"

    def display_info(self):
        print(f"Ad: {self.name}, Yaş: {self.age}, Cinsiyet: {self.gender}")
        print(f"Sağlık: {self.health}, Para: {self.money}, Meslek: {self.job}")

    def age_up(self):
        self.age += 1
        print(f"{self.name} bir yaş büyüdü! Şimdi {self.age} yaşında.")

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

# Karakter oluşturma
player_name = input("Karakter adını girin: ")
player_age = int(input("Karakter yaşını girin: "))
player_gender = input("Karakter cinsiyetini girin (Erkek/Kadın): ")

player = Character(player_name, player_age, player_gender)
player.display_info()

# Yaşlanma
player.age_up()
player.display_info()

# Sağlık kontrolü
player.check_health()

# Meslek değiştirme
player.change_job("Mühendis")
player.display_info()

# Çalışma
player.work()
player.display_info()