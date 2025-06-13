
Инструкция по запуску:

1.Установить Python и MySQL (если нужно).

2.Создать виртуальное окружение:
python -m venv venv  # bash
venv\Scripts\activate  # для Windows

3.Установить зависимости:
pip install -r requirements.txt  # bash

4.Восстановить базу данных:
mysql -u пользователь -p название_базы < backup.sql  # bash

5.Запустить сервер:
python manage.py runserver  # bash

PS: подставляйте свои данные (например, если у вас в MySQL пользователь teacher, а база oilmarket_temp):
mysql -u teacher -p oilmarket_temp < backup.sql  # bash

И в этом случае:
В settings.py вашего Django-проекта должно быть:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oilmarket_temp',  # <- используйте своё название!
        'USER': 'teacher',         # <- ваш пользователь MySQL
        'PASSWORD': '...',         # ваш пароль
    }
}