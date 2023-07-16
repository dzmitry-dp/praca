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

Работодатель через приложение:
- Дает ответы на самые популярные вопросы работника
- Принимает заявки на документы
- Делегирует задачи

Работник может через приложение:
- Вести учет рабочего времени
- Запросить документы
- Получить задачу

# Структура разработки

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

# Сборка .apk

	https://github.com/kivy/buildozer

```bash
pip install Cython==0.29.33 https://github.com/kivy/buildozer/archive/master.zip Kivy https://github.com/kivymd/KivyMD/archive/master.zip cryptography setuptools

sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev xclip xsel libmtdev-dev

buildozer android debug
```

Требования в файле **buildozer.spec**

	requirements = python3, kivy==master, https://github.com/kivymd/KivyMD/archive/master.zip, android, pyjnius, requests, cryptography, urllib3, chardet, idna

android.permissions в файле buildozer.spec

	android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, SEND_SMS

	p4a.branch = develop

# Сборка .aab
1. Запустите эту команду для клонирования версии Buildozer, поддерживающей создание файлов .aab: 
```bash
pip install git+https://github.com/misl6/buildozer.git@feat/aab-support
```
2. После установки Buildozer с помощью того же терминала, который вы использовали в предоставленной ссылке, перейдите в корневую папку вашего проекта.
3. Если вы уже использовали Buildozer ранее и внутри папки вашего проекта есть файл `buildozer.spec`, удалите его.
4. Теперь запустите команду `buildozer init` в терминале.
5. Откройте сгенерированный файл `buildozer.spec` в любом текстовом редакторе и найдите строки:

```
# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64 
android.archs = arm64-v8a, armeabi-v7a

# (str) The format used to package the app for release mode (aab or apk). 
android.release_artifact = aab

p4a.branch = develop
```

8. Если вы ранее использовали Buildozer, удалите папку `.buildozer` внутри папки вашего проекта. Если вы не видите эту папку, убедитесь, что в вашем файловом браузере включено отображение скрытых файлов.
9. В терминале, где вы вводили информацию о вашем ключе (как указано в начале этого документа), выполните следующую команду: 
```
buildozer -v android release
```

При каждой финальной компиляции удалите файл `.buildozer` и запустите компиляцию заново. Это может занять больше времени, но гарантирует, что Buildozer не пропустит какие-либо зависимости.

# Git

branch **master** - рабочая версия приложения

branch **dev** - ветка текущей разработки

### Клонировать ветку разработки dev в текущий каталог

```bash
git clone -b dev https://github.com/dzmitry-dp/praca .
```
	Username for 'https://github.com': dzmitry-dp
	Password for 'https://dzmitry-dp@github.com': TOKEN

### Слияние удаленной dev ветки проекта в локальную dev ветку

```bash
git pull branch_1:branch_2
```

`branch1` является удаленной веткой, а ветка `branch2` является локальной веткой

### Отправить ветку dev на GitHub

```bash
git push -u origin dev
```

# Code2flow
Визуализация логики проекта ./static/logic.png

```bash
pip3 install code2flow
code2flow . --language py --output ./static/logic.png 
```
___

