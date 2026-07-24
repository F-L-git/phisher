phisher/
├── .devcontainer/                 # (уже есть) настройки dev-контейнера
├── .github/                       # (уже есть) CI/CD, dependabot и т.д.
├── .venv/                         # виртуальное окружение (не в репозитории)
├── src/                           # основной исходный код
│   └── phisher/                   # корневой пакет проекта
│       ├── __init__.py
│       ├── __main__.py            # точка входа (использует пайплайн)
│       ├── config/                # конфигурация
│       │   ├── __init__.py
│       │   ├── loader.py          # загрузка конфига из YAML + env
│       │   └── config.yaml        # основной файл конфигурации
│       ├── core/                  # ядро: интерфейсы и пайплайн
│       │   ├── __init__.py
│       │   ├── interfaces.py      # абстрактные классы (SearchEngine, WhoisProvider, MutationGenerator)
│       │   └── pipeline.py        # класс Pipeline для последовательного выполнения шагов
│       ├── adapters/              # реализации интерфейсов для внешних сервисов
│       │   ├── __init__.py
│       │   ├── netlas_adapter.py  # адаптер для Netlas (SearchEngine + WhoisProvider)
│       │   └── dnstwist_adapter.py # адаптер для dnstwist (MutationGenerator)
│       ├── steps/                 # отдельные шаги пайплайна (бывшие модули)
│       │   ├── __init__.py
│       │   ├── domain_mutations.py
│       │   ├── subdomains.py
│       │   ├── whoisreg.py
│       │   └── double_check.py    # можно выделить отдельно, но пока внутри whoisreg
│       ├── utils/                 # вспомогательные утилиты
│       │   ├── __init__.py
│       │   ├── cout.py            # вывод в консоль (rich)
│       │   ├── inparse.py         # парсинг входного JSON (можно переименовать, но оставим)
│       │   ├── keywords.py        # поиск ключевых слов
│       │   ├── links_check.py     # поиск ссылок на изображения
│       │   └── logging_setup.py   # настройка логирования
│       ├── models/                # модели данных (pydantic)
│       │   ├── __init__.py
│       │   └── perimeter.py       # валидация входного JSON (Pydantic-схема)
│       ├── tests/                 # тесты (рядом с кодом, но можно вынести в корень)
│       │   ├── __init__.py
│       │   ├── unit/              # модульные тесты
│       │   │   ├── test_domain_mutations.py
│       │   │   ├── test_whoisreg.py
│       │   │   └── ...
│       │   └── integration/       # интеграционные тесты
│       │       └── test_pipeline.py
│       └── examples/              # примеры входных файлов
│           └── perimeter_example.json
├── docs/                          # дополнительная документация (опционально)
├── requirements.txt               # зависимости
├── pyproject.toml                 # настройки линтеров, mypy, и т.д.
├── setup.py (или pyproject.toml с poetry) # для установки пакета
├── .gitignore
└── README.md
