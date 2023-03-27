Created: 04-02-2023 19:57
Tags: #kivy #sqlite3
___
```bash
git push -u origin master
```

# Code2flow
Визуализация логики проекта

```bash
code2flow . --language py --output ./static/logic.png 
```

# Запустить dev проект

```bash
python ./main.py
```

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

# MVP

Приложение которое устанавливается на телефон и бесполезно после увольнения сотрудника

Приложение содержит только личные данные сотрудника

Бесполезным приложение становится после того, как абонента отключают от сервисов Power Apps

# Команды

	https://github.com/kivy/buildozer

Собрать Python проект можно только на Linux

```bash
buildozer android debug
```

Требования в файле buildozer.spec

	requirements = python3, sqlite3, kivy, kivymd, android, pyjnius

android.permissions в файле buildozer.spec

	android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, SEND_SMS

___

