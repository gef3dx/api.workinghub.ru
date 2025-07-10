
### Описание структуры

**📁 app/** - Основной пакет приложения
  - `__init__.py` - Инициализация пакета
  - `main.py` - Точка входа в приложение
- **📁 config/** - Конфигурационные файлы
  - `settings.py` - Настройки приложения

- **📁 core/** - Основные компоненты
  - `database.py` - Работа с базой данных
  - `dependencies.py` - Зависимости

- **📁 models/** - Модели данных
  - `entities.py` - Сущности БД
  - `schemas.py` - Схемы данных

- **📁 repositories/** - Репозитории данных
  - `protocols.py` - Интерфейсы репозиториев
  - `user_repository.py` - Репозиторий пользователей

- **📁 services/** - Бизнес-логика
  - `protocols.py` - Интерфейсы сервисов
  - `user_service.py` - Сервис пользователей

- **📁 controllers/** - Контроллеры API
  - `user_controller.py` - Контроллер пользователей

**Файлы проекта**
  - `.python-version` - Версия Python
  - `pyproject.toml` - Зависимости Python
  - `database.db` - Файл базы данных SQLite
  - `README.md` - Документация проекта