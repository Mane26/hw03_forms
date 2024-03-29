# hw03_forms - Сообщества создание записей, спринта 4 в Яндекс.Практикум
## Спринт 4 - Сообщества создание записей

### hw03_forms - Сообщества создание записей Яндекс.Практикум.

Добавлены следующие возможности:
- регистрация пользователя, 
- вход/выход пользователя,
- восстановления пароля,
- создания записей сообщества,
- подробная информация, редактирование только своей записи,
- отображение постов пользователя,
- пагинация, раздел Об авторе, Технологии, отображения профиля пользователя.

### Настройка и запуск на ПК

Клонируем проект:

```bash
git clone https://github.com/Mane26/hw03_forms.git
```

или

```bash
git clone git@github.com:Mane26/hw03_forms.git
```

Переходим в папку с проектом:

```bash
cd hw03_forms
```

Устанавливаем виртуальное окружение:

```bash
python -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/Scripts/activate
```

> Для деактивации виртуального окружения выполним (после работы):
> ```bash
> deactivate
> ```

Устанавливаем зависимости:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Применяем миграции:

```bash
python yatube/manage.py makemigrations
```
```bash
python yatube/manage.py migrate
```

Создаем супер пользователя:

```bash
python yatube/manage.py createsuperuser
```

При желании делаем коллекцию статики:

```bash
python yatube/manage.py collectstatic
```

Предварительно сняв комментарий с:
```bash
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

И закомментировав: 
```bash
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

Иначе получим ошибку: You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.

В папку с проектом, где файл settings.py добавляем файл .env куда прописываем наши параметры:

```bash
SECRET_KEY='Ваш секретный ключ'
ALLOWED_HOSTS='127.0.0.1, localhost'
DEBUG=True
```

Не забываем добавить в .gitingore файлы:

```bash
.env
.venv
```

Для запуска тестов выполним:

```bash
pytest
```
