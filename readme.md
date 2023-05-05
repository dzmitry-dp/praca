Created: 04-02-2023 19:57
Tags: #python #kivy #sqlite3

[[Структура окружения]]
___
# PracaApp

<div>
	<img src="./dev/static/Pasted image 20230416133932.png" width="400" height="840" style="margin-right: 10px; display: inline-block;">
	<img src="./dev/static/Pasted image 20230416134442.png" width="400" height="840" style="margin-right: 10px; display: inline-block;">
</div>

Программа для автоматизации бизнес-процессов: позволяет автоматизировать деловые процессы, облегчая их управление и повышая эффективность.

Приложение для обмена файлами: позволяет пользователям обмениваться файлами между собой.

# Pracodawca i pracownik

Работодатель выдает приложение на телефон своему сотруднику.

Работодатель через приложение:
- Дает ответы на самые популярные вопросы работника
- Принимает заявки на документы
- Делегирует задачи

Работник может через приложение:
- Вести учет рабочего времени
- Запросить документы
- Получить задачу

# Структура

- **/dev** - папка для разработки приложения Praca
	- **/action** - действия и логика
	- **/db** - работа с базой данных
	- **/static** - логи, доки, картинки, apk и др.
		- **/android_app** - apk на андроид
		- **/doc** - дополнительная информация
		- **/logs** - логи работы приложения
		- **/wallpapers** - картинки
	- **/view** - отображение для пользователя
- **/scripts** - вспомогательные сценарии
	- 

# Запустить проект

```bash
python ./main.py
```

# Сборка apk

	https://github.com/kivy/buildozer

```bash
pip install https://github.com/kivy/buildozer/archive/master.zip
buildozer android debug
```

Требования в файле buildozer.spec

	requirements = python3, sqlite3, kivy, kivymd, android, pyjnius

android.permissions в файле buildozer.spec

	android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, SEND_SMS

# Git

branch **master** - рабочая версия приложения

branch **dev** - ветка текущей разработки

### Клонировать ветку разработки dev

```bash
git clone -b dev https://github.com/dzmitry-dp/praca .
```
	Username for 'https://github.com': dzmitry-dp
	Password for 'https://dzmitry-dp@github.com': TOKEN

### Слияние dev ветки проекта в dev ветку
```bash
git pull dev:dev
```
### Отправить ветку dev на сервер

```bash
git push -u origin dev
```

# Code2flow
Визуализация логики проекта ./static/logic.png

```bash
pip3 install code2flow
code2flow . --language py --output ./static/logic.png 
```

```bash
python scripts/logic_to_png.py
```

___

