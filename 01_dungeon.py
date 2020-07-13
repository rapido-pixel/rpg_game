# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...
import json
from decimal import Decimal
import re
import csv
from datetime import datetime

LOGS = 'dungeon.csv'
REMAINING_TIME = '123456.0987654321'
GAME_MAP = "rpg.json"


# если изначально не писать число в виде строки - теряется точность!
# field_names = ['current_location', 'current_experience', 'current_date']


class Game:

    def __init__(self, file, time, logs):
        self.file = file
        self.game_settings = None
        self.values_for_locations = []
        self.current_location = None
        self.remaining_time = Decimal(time)
        self.current_experience = Decimal("0")
        self.current_date = datetime.now()
        self.logs = logs
        self.exit = False

    def read_file(self):

        with open(self.file, "r") as json_file:
            self.game_settings = json.load(json_file)

    def parsing_locations(self):

        for keys, values in self.game_settings.items():
            self.current_location = keys
            for value in values:
                if isinstance(value, str):
                    self.values_for_locations.append(value)
                elif isinstance(value, dict):
                    for k, v in value.items():
                        self.values_for_locations.append(k)

    def action_on_location(self):

        print(f"""
        Вы находитесь в локации {self.current_location}
        У вас {self.current_experience} опыта и осталось {self.remaining_time} секунд до наводнения
        """)
        if len(self.values_for_locations) == 0:
            print("В это локации нет переходов")
            self.exit = True
        else:
            print("Вы видете: ")
            for value in self.values_for_locations:
                if "Hatch" in value:
                    print(" - Вы видете ВЫХОД!")
                elif "Location" not in value:
                    print(f"- Монстра {value}")
                else:
                    print(f"- Переход в локацию {value}")
            self.change_player()

    def change_player(self):

        print("Ваш выбор:")

        for index, value in enumerate(self.values_for_locations, 1):
            if "Hatch" in value:
                print(f"{index}. Открыть люк")
            elif "Location" not in value:
                print(f"{index}. Атаковать {value}")
            else:
                print(f"{index}. Перейти в {value}")

        user_input = input("Выберите номер действия: ")
        for index, value in enumerate(self.values_for_locations, 1):
            if user_input.isdigit() and int(user_input) == index:
                if "Hatch" in value:
                    self.current_location = value
                    self.calculation_time(value)
                elif "Location" not in value:
                    self.atack_monster(value)
                else:
                    self.current_location = value
                    self.run_to_location(value)

        self.values_for_locations = []
        self.game_leveling = {}

    def run_to_location(self, value):

        for values in self.game_settings.values():
            for val in values:
                if isinstance(val, dict):
                    if val.get(self.current_location):
                        self.game_settings = val
        self.calculation_time(value)

    def atack_monster(self, value):

        print(f"""
        Вы атаковали монстра {value}
        """)
        self.calculation_exp(value)
        self.calculation_time(value)
        self.values_for_locations.remove(value)
        self.action_on_location()

    def calculation_exp(self, value):

        exp_search = Decimal(re.search(r'exp\d+', value)[0][3:])
        self.current_experience += exp_search

    def calculation_time(self, value):

        time_search = Decimal(re.search(r'tm\d+', value)[0][2:])
        self.remaining_time -= time_search

    def write_in_csv(self):

        data_for_csv = [self.current_location, self.current_experience, self.current_date]
        with open(self.logs, 'a', newline='') as out_csv:
            writer = csv.writer(out_csv)
            writer.writerow(data_for_csv)

    def play(self):
        game.read_file()
        while True:

            self.parsing_locations()
            self.action_on_location()
            if self.remaining_time <= 0:
                print("""
                Вы проиграли.
                Вы не успели выбраться.
                Вода заполнила всю пещеру.
                """)
                break
            elif "Hatch" in self.current_location:
                if self.current_experience >= Decimal("280"):
                    print("""
                    Поздравдяем!!!
                    Вы выбрались из пещеры
                    Вы прошли игру
                    """)
                    break
                else:
                    print("""
                    Вы нашли выход, но у вас недостаточно опыта, чтобы выбраться
                    Вода заполнила пещеру.
                    Выхода нет
                    """)
                    break
            elif self.exit:
                print("Вы не видите прохода")
                break
        self.write_in_csv()

    def return_game(self):
        while True:
            print("1. Играть заново")
            print("2. Выйти из игры")
            user_input = input("Выберите дейcтвие: ")
            if user_input.isdigit() and int(user_input) == 1:
                game.play()
            elif user_input.isdigit() and int(user_input) == 2:
                break
            else:
                print("Выберите 1 или 2")

    def run(self):
        self.play()


while True:
    game = Game(GAME_MAP, REMAINING_TIME, LOGS)
    game.run()
    print("1. Играть заново")
    print("2. Выйти из игры")
    user_input = input("Выберите дейcтвие: ")
    if user_input.isdigit() and int(user_input) == 1:
        continue
    elif user_input.isdigit() and int(user_input) == 2:
        break
    else:
        print("Выберите 1 или 2")
