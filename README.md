# Fractel

![2024-08-24_06-02-06](https://github.com/user-attachments/assets/596c38ef-0bc5-4dcf-8030-bf34cb813d1b)

RU:

Это простая игра-скроллер, где главная задача у игрока набрать счёт равный 450 очков.
Навстречу игроку летят энергошары, очко даётся за достижение энергошара левого края экрана.
Каждые 10 энергошаров, которые засчитались как очки, дают игроку плюс одну энергию (жизнь).
Если игрок столкнётся с энергошаром, то потеряет одну энергию(жизнь). В начале игры вам даётся 3 энергии.
Игрок, нажимая SPACE, может активировать реактивный ранец и подпрыгивать в воздухе.
При столкновении с верхней границей экрана ранец отключается, игрок падает вниз с большой скоростью.
Нажатие LEFT CONTROL позволяет отключать ранец и падать быстре в произвольный момент.

Управление:

Курсор LEFT/RIGHT - движение вправо-влево

Курсор UP/DOWN - взлёт-падение

SPACE - выстрел (три выстрела за 1 энергию)

LALT - подрыв всех энергошаров на экране за 10 энергии

Дополнительно:

TAB - переход в FullScreen

ESC - возврат в оконный режим

P - пауза

Чтобы поиграть, скачайте последнюю версию https://github.com/nixodmin/Fractel/releases

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

This is a simple scrolling game, where the main task of the player is to score 450 points.
Energy balls fly towards the player, a point is given for reaching the energy ball on the left edge of the screen.
Every 10 energy balls that are counted as points give the player plus one energy (life).
If the player collides with an energy ball, he will lose one energy (life). At the beginning of the game, you are given 3 energies.
The player, by pressing SPACE, can activate the jetpack and jump in the air.
When colliding with the upper edge of the screen, the jetpack turns off, the player falls down at high speed.
Pressing LEFT CONTROL allows you to turn off the jetpack and fall faster at any time.

Controls:

Курсор LEFT/RIGHT - left-right

Курсор UP/DOWN - jump-fall

SPACE - shot (3 shots for 1 energy)

LALT - destroys all energy ball on screen for 10 energy

Дополнительно:

TAB - FullScreen

ESC - return to widowed mode

P - pause

To play download last version https://github.com/nixodmin/Fractel/releases

How to make your own build:

Be sure to add to the pyhon environment:

pip install numpy

pip install pygame

pip install matplotlib

Place the fractel.py file in a separate directory

Take media files from the release you want to build https://github.com/nixodmin/Fractel/releases

Place directory with media files in the directory with the fractel.py file


