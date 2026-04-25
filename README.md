## Colab и датасет

Весь код обучения модели и тестирования API доступен в Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1jGTugdvApstCRFS_gT0C7l4Banta9lyK)

https://colab.research.google.com/drive/1jGTugdvApstCRFS_gT0C7l4Banta9lyK

### Датасет

Датасет с изображениями доступен в Google Drive:

[Ссылка на папку с датасетом](https://drive.google.com/drive/folders/1FnsepC6eK71MwYzGTgwrR42P7JzqGcmC)

<!--Установка-->
## Установка (Windows/Linux)

Должны быть установлены зависимости проекта

1. Клонирование репозитория 

```git clone https://github.com/KateRastorgueva/cosmetics-classification-api.git```

2. Переход в директорию

```cd cosmetics-classification-api```

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
cosmetics_api/

├── main.py

├── requirements.txt

├── model/

│ └── cosmetics_model.pt

└── README.md

<!--Пример запроса и ответа-->
## Пример запроса и ответа

### GET /health

```
curl http://127.0.0.1:8000/health
{
  "status": "ok"
}
POST /predict
curl -X POST http://127.0.0.1:8000/predict -F "file=@image.jpg"

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

<!--Результаты обучения модели-->
Результаты обучения модели
Показатель	Значение
Лучшая точность	90.67%
Финальная точность	88.00%
Количество эпох	30
Batch size	16
Learning rate	0.0001
Размер датасета	151 изображение
<!--Обработка ошибок-->
Обработка ошибок
Код	Ситуация	Ответ
400	Неверный формат файла	{"detail": "Неверный формат. Поддерживаются JPEG, PNG"}
400	Файл больше 10 МБ	{"detail": "Файл больше 10 МБ"}
500	Внутренняя ошибка сервера	{"detail": "Ошибка при обработке изображения"}
