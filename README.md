## Colab и датасет
Весь код обучения модели и тестирования API доступен в Colab:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1jGTugdvApstCRFS_gT0C7l4Banta9lyK)
https://colab.research.google.com/drive/1jGTugdvApstCRFS_gT0C7l4Banta9lyK
### Датасет
Датасет с изображениями доступен в Google Drive:
[Ссылка на папку с датасетом](https://drive.google.com/drive/folders/1FnsepC6eK71MwYzGTgwrR42P7JzqGcmC)

```markdown
<!--Блок информации о репозитории в бейджах-->
# Cosmetics Classification API

Сервис компьютерного зрения для автоматической классификации косметической продукции по фотографиям.

![Static Badge](https://img.shields.io/badge/FastAPI-Cosmetics_API-blue)
![GitHub top language](https://img.shields.io/github/languages/top/OkulusDev/CosmeticsAPI)
![GitHub](https://img.shields.io/github/license/OkulusDev/CosmeticsAPI)
![Version](https://img.shields.io/badge/version-1.0.0-green)

<!--Установка-->
## Установка (Windows/Linux)

У вас должны быть установлены зависимости проекта

1. Клонирование репозитория 

```git clone https://github.com/OkulusDev/CosmeticsAPI.git```

2. Переход в директорию CosmeticsAPI

```cd CosmeticsAPI```

3. Создание виртуального окружения

```python -m venv venv```

4. Активация виртуального окружения

Windows:
```venv\Scripts\activate```

Linux:
```source venv/bin/activate```

5. Установка зависимостей

```pip install -r requirements.txt```

6. Запуск сервиса

```uvicorn main:app --reload```

<!--Документация-->
## Документация

API документация доступна после запуска сервиса по ссылке http://127.0.0.1:8000/docs

<!--Описание задачи-->
## Описание задачи

Сервис автоматически определяет категорию косметического товара по загруженному изображению. Решает задачу упрощения каталогизации товаров для интернет-магазина.

Целевые классы:
- lipstick — помада и блеск для губ
- eyeshadow — тени для век
- mascara — тушь для ресниц
- foundation — тональный крем
- other — другие косметические товары

<!--Архитектура решения-->
## Архитектура решения

| Компонент | Описание |
|-----------|----------|
| Модель | ResNet18, предобученная на ImageNet, с дообучением (transfer learning) на 5 классов |
| Препроцессинг | Resize до 224x224, преобразование в тензор, нормализация |
| Сервис | FastAPI (REST API) |
| Запуск | Uvicorn |
| Формат входных данных | JPEG, PNG (до 10 МБ) |

<!--Структура проекта-->
### Структура проекта

```
cosmetics_api/
├── main.py                 # FastAPI приложение
├── requirements.txt        # Зависимости
├── model/
│   └── cosmetics_model.pt  # Обученная модель
└── README.md               # Документация
```

<!--Пример запроса и ответа-->
## Пример запроса и ответа

### GET /health

```bash
curl http://127.0.0.1:8000/health
```

```json
{
  "status": "ok"
}
```

### POST /predict

```bash
curl -X POST http://127.0.0.1:8000/predict -F "file=@image.jpg"
```

```json
{
  "class": "mascara",
  "probability": 0.9226731061935425,
  "all_classes": {
    "eyeshadow": 0.003627229481935501,
    "foundation": 0.00411420826734304,
    "lipstick": 0.050592146813869476,
    "mascara": 0.9226731061935425,
    "other": 0.01899324543774128
  }
}
```

<!--Результаты обучения модели-->
## Результаты обучения модели

| Показатель | Значение |
|------------|----------|
| Лучшая точность | 90.67% |
| Финальная точность | 88.00% |
| Количество эпох | 30 |
| Batch size | 16 |
| Learning rate | 0.0001 |
| Размер датасета | 151 изображение |

<!--Обработка ошибок-->
## Обработка ошибок

| Код | Ситуация | Ответ |
|-----|----------|-------|
| 400 | Неверный формат файла | {"detail": "Неверный формат. Поддерживаются JPEG, PNG"} |
| 400 | Файл больше 10 МБ | {"detail": "Файл больше 10 МБ"} |
| 500 | Внутренняя ошибка сервера | {"detail": "Ошибка при обработке изображения"} |

<!--Зависимости-->
## Зависимости

Проект зависит от интерпретатора Python версии 3.7 или выше и следующих библиотек:
- FastAPI
- Uvicorn
- PyTorch
- torchvision
- Pillow
