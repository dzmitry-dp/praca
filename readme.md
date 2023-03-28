Created: 04-02-2023 19:57
Tags: #python #kivy #sqlite3
___
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

# Запустить dev проект

```bash
python ./main.py
```

# Сборка

	https://github.com/kivy/buildozer

Собрать Python проект можно только на Linux

```bash
buildozer android debug
```

Требования в файле buildozer.spec

	requirements = python3, sqlite3, kivy, kivymd, android, pyjnius

android.permissions в файле buildozer.spec

	android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, SEND_SMS

# Git

branch **master** - рабочая версия приложения
branch **dev** - ветка текущей разработки

### Клонировать ветку разработки

```bash
git clone https://github.com/dzmitry-dp/praca -b dev
```
	Username for 'https://github.com': dzmitry-dp
	Password for 'https://dzmitry-dp@github.com': TOKEN

### Отправить ветку master на сервер

```bash
git push -u origin master
```

# Code2flow
Визуализация логики проекта

```bash
code2flow . --language py --output ./static/logic.png 
```

___

