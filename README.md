## Проект Charity_fund
### Описание проекта:
Администратор может учередить какой-то благотворительный фонд для того чтобы собрать деньги на какие-то нужды для кошек, еду, жилье, передержки и так далее. Обычный пользователь может внести какую-то сумму при этом он не выбирает куда конкретно будет направлена сумма, деньги распределяются по принципу, какой первый проект был создан, туда и будут направленны деньги и пока проект не закроется деньги будут напрвляться в данный проект, если только его не закроют.

### Технологии создания проекта:
- Python 3.9 его можно скачать по ссылке https://www.python.org/ заходите выбирается нужную версию и скачиваете.
- FastAPI 0.78.0 https://fastapi.tiangolo.com/
- SQLAlchemy 1.4.36 https://www.sqlalchemy.org/
- pydantic 1.9.1 https://docs.pydantic.dev/
- uvicorn 0.17.6 https://www.uvicorn.org/
- alembic 1.7.7 https://alembic.sqlalchemy.org/en/latest/

### Запуск проекта
- Скачиваете проект с удаленного репозитория себе на локальную машину.
- Устанавливаете виртуальное окруженение командой `py -3.9 venv venv` в корне проекта появится папка venv
- Устанавливаете все зависимости из файла requirements.txt перед этим не забыв активировать виртуальное окружнение командой `source venv/Scripts/activate` - если у вас Windows и `source venv/bin/activate` - если не Windows, обновите pip командой `python -m pip install --upgrade pip`
команда для установки зависимостей `pip install -r requirements.txt`
- Из корневой директории запустите приложение `uvicorn app.main:app --reload` проект должен запуститься.

Всю документацию можно посмотреть по адресу http://localhost:8000/docs или http://127.0.0.1:8000/redoc <br>
Также при запуске проекта автоматически создается superuser

### .env файл<br>

APP_TITLE = Сюда пишется название вашего проекта<br>
APP_DESCRIPTION = Описание вашего проекта<br>
DATABASE_URL= адрес вашей базы данных<br>
SECRET = секретный ключ <br>
FIRST_SUPERUSER_EMAIL = email вашего суперпользователя<br>
FIRST_SUPERUSER_PASSWORD = пароль вашего суперпользователя<br>

### Примеры запросов и ответы на них:<br>
При GET запросе по этому адресу http://127.0.0.1:8000/charity_project/ вернеться список созданных проектов<br>
