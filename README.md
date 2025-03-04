# linux-byedpi-auto 

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)


Консольная утилита для автоматического тестирования стратегий обхода блокировок с использованием ByeDPI.

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/dead-meme-plug/linux-byedpi-auto.git
cd linux-byedpi-auto
```

2. Создайте виртуальное окружение и активируйте его
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Установите зависимости
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корне проекта. 
- Вам нужно указать путь до исполняемого файла ByeDPI в переменной BYEDPI_PATH
```
BYEDPI_PATH="/path/to/file/ciadpi"
```

## Использование

Запустите утилиту:
```bash
python src
```

После завершения тестирования будет создан файл `results.txt` с результатами.
![image](https://github.com/user-attachments/assets/d5a9d8eb-989e-4656-a36d-875602e90775)

## Зависимости

- [Python](https://www.python.org/downloads) 3.8+
- [ByeDPI](https://github.com/hufrea/byedpi)
