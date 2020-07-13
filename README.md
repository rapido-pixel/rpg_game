# rpg_game
Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
приключений.
Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
солдат и вас, как известного в этих краях героя, наняли для их спасения.

Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
где N - это номер локации (целое число), а T (вещественное число) - это время,
которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
то он тратит на это 30000 секунд.
По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
которое потратит игрок для уничтожения данного монстра.
Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
Гарантируется, что в начале пути будет две локации и один монстр
(то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).

На прохождение игры игроку дается 123456.0987654321 секунд.
Цель игры: за отведенное время найти выход ("Hatch")

По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
в каждую локацию можно попасть только один раз,
и выйти из нее нельзя (то есть двигаться можно только вперед).

Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
готовый к следующей попытке (игра начинается заново).

Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.

Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
- текущую локацию
- текущее количество опыта
- текущие дату и время (для этого используйте библиотеку datetime)
После успешного или неуспешного завершения игры вам необходимо записать
всю собранную информацию в csv файл dungeon.csv.
Названия столбцов для csv файла: current_location, current_experience, current_date


Пример взаимодействия с игроком:

Вы находитесь в Location_0_tm0
У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
Прошло времени: 00:00

Внутри вы видите:
— Вход в локацию: Location_1_tm1040
— Вход в локацию: Location_2_tm123456
Выберите действие:
1.Атаковать монстра
2.Перейти в другую локацию
3.Сдаться и выйти из игры

Вы выбрали переход в локацию Location_2_tm1234567890

Вы находитесь в Location_2_tm1234567890
У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
Прошло времени: 20:00

Внутри вы видите:
— Монстра Mob_exp10_tm10
— Вход в локацию: Location_3_tm55500
— Вход в локацию: Location_4_tm66600
Выберите действие:
1.Атаковать монстра
2.Перейти в другую локацию
3.Сдаться и выйти из игры

Вы выбрали сражаться с монстром

Вы находитесь в Location_2_tm0
У вас 10 опыта и осталось -9.9012345679 секунд до наводнения

Вы не успели открыть люк!!!
