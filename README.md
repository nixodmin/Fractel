# Fractel

![screen](https://github.com/user-attachments/assets/79bad538-e187-4df7-be7e-87c6c69d105b)

RU:

Это простая игра-скроллер, где главная задача у игрока набрать счёт равный 450 и победить босса.
Навстречу игроку летят энергошары, очко даётся за достижение энергошара левого края экрана.
Каждые 10 энергошаров, которые засчитались как очки, дают игроку плюс одну энергию (жизнь).
Если игрок столкнётся с энергошаром, то потеряет одну энергию(жизнь). В начале игры вам даётся 3 энергии.
Игрок, нажимая SPACE, может активировать реактивный ранец и подпрыгивать в воздухе.
При столкновении с верхней границей экрана ранец отключается, игрок падает вниз с большой скоростью.
Нажатие LEFT CONTROL позволяет отключать ранец и падать быстре в произвольный момент.

В новом релизе появились баффы на оружие и щит!

Бафф на щит (пассивка) даёт восполняемый каждые 20 секунд щит, который выдерживает 1 столкновение.

Бафф на выстрел [SPACE] увеличивает область поражения и наносит больший урон боссам.

Бафф на ракетный удар [X] добавляет +2 ракеты (итого пять за вызов ракетного удара)

Бафф на подрыв энергошаров [LALT] теперь все взорванные энергошары засчитывает в очки и соотвественно за каждые 10 очков прибавляет 1 энергию, плюс наносит усиленный урон по боссам.

Управление:

Курсор LEFT/RIGHT - движение вправо-влево

Курсор UP/DOWN - взлёт-падение

SPACE - выстрел (три выстрела за 1 энергию)

LALT - подрыв всех энергошаров на экране за 10 энергии

X - ракетный удар

Дополнительно:

TAB - переход в FullScreen

ESC - возврат в оконный режим

P - пауза

L - переключение языка RU / ENG

Минус - отключить фоновую музыку

Чтобы поиграть, скачайте последнюю версию: https://github.com/nixodmin/Fractel/releases

Если хотите сделать свой билд:

Обязательно добавьте в окружение pyhon:

pip install numpy

pip install pygame

pip install matplotlib


Разместите файл fractel.py в отдельную директорию

Возьмите медиафайлы из соответствующего релиза https://github.com/nixodmin/Fractel/releases

Директорию с медиафайлами поместите в директорию с файлом  fractel.py

---------------------------------------

EN:

This is a simple scrolling game, where the main task of the player is to score 450 points and destroy level boss.
Energy balls fly towards the player, a point is given for reaching the energy ball on the left edge of the screen.
Every 10 energy balls that are counted as points give the player plus one energy (life).
If the player collides with an energy ball, he will lose one energy (life). At the beginning of the game, you are given 3 energies.
The player, by pressing SPACE, can activate the jetpack and jump in the air.
When colliding with the upper edge of the screen, the jetpack turns off, the player falls down at high speed.
Pressing LEFT CONTROL allows you to turn off the jetpack and fall faster at any time.

The new release features weapon and shield buffs!

Shield buff (passive) gives a shield that replenishes every 20 seconds and can withstand 1 collision.

Shot buff [SPACE] increases the area of ​​effect and deals more damage to bosses.

Rocket strike buff [X] adds +2 rockets (total of five for calling a rocket strike)

Energy ball detonation buff [LALT] now counts all detonated energy balls as points and accordingly adds 1 energy for every 10 points, plus deals increased damage to bosses.

Controls:

LEFT/RIGHT - left-right

UP/DOWN - jump-fall

SPACE - shot (3 shots for 1 energy)

LALT - destroys all energy ball on screen for 10 energy

X - rocket strike

Others:

TAB - FullScreen

ESC - return to widowed mode

P - pause

L - switch language RU / ENG

Download last version to play: https://github.com/nixodmin/Fractel/releases

How to make your own build:

Be sure to add to the pyhon environment:

pip install numpy

pip install pygame

pip install matplotlib

Place the fractel.py file in a separate directory

Take media files from the release you want to build https://github.com/nixodmin/Fractel/releases

Place directory with media files in the directory with the fractel.py file


