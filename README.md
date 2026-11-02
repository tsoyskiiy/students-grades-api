# Grades API

REST API на FastAPI для управления студентами, курсами и оценками.
Данные хранятся в PostgreSQL, доступ через SQLAlchemy.

## 1. База данных

```powershell
docker start pg
docker exec pg psql -U postgres -c "CREATE DATABASE school"
Get-Content student_grades.sql | docker exec -i pg psql -U postgres -d school
```

(На Mac и Linux: `docker exec -i pg psql -U postgres -d school < student_grades.sql`.)

## 2. Настройки

Создайте файл `.env` рядом с `main.py`:

```
DATABASE_URL=postgresql+psycopg2://postgres:ВАШ_ПАРОЛЬ@localhost:5432/school
```

Файл `.env` не попадает в репозиторий (он указан в `.gitignore`).

## 3. Установка и запуск

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
fastapi dev main.py
```

Документация API: http://127.0.0.1:8000/docs

Тесты: `pytest -v`

## 4. Удаление студентов и курсов

Для настоящей школы я бы не давал возможность полное удаление студентов и курсов, у которых есть оценки. Так как если студент вернёться, данные вернуть не получиться. Вместо этого я бы выбрал помечать неактивные.