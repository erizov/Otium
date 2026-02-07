# Excursion — московские монастыри

Каталог из 20 монастырей и подворий Москвы: адреса, стили, история,
значение, факты. Генерация HTML- и PDF-путеводителя с картами и разделом
«Вопросы и ответы». Изображения хранятся в подпапке по темам для
возможности добавлять другие PDF (например, по другим городам).

## Данные

- **data/monasteries.py** — список `MONASTERIES` (20 объектов), константа
  `IMAGES_SUBFOLDER = "moscow_monasteries"`.
- **data/qa.py** — вопросы и ответы для раздела в конце PDF.
- **data/image_urls.py** — публичные URL изображений (Wikipedia/Commons):
  свободные лицензии, узнаваемые виды.

Фотографии сохраняются в **output/images/moscow_monasteries/** — отдельная
подпапка под тему, чтобы в будущем добавлять, например,
`output/images/saint_petersburg/` для другого путеводителя.

## Один скрипт: PDF, загрузка фото, проверка дубликатов

**scripts/build_pdf.py** делает всё по шагам:

1. Создаёт подкаталог **output/images/moscow_monasteries/** при отсутствии.
2. Скачивает недостающие изображения (Wikipedia/Commons) в этот каталог.
3. Проверяет дубликаты по содержимому (SHA256) и выводит группы одинаковых файлов.
4. Собирает HTML и генерирует PDF.

```bash
pip install -r requirements.txt
playwright install chromium
python scripts/build_pdf.py
```

Опционально: **scripts/download_images.py** — цикл загрузки каждые 3 минуты
до успеха (если часть фото не загрузилась из‑за лимитов).

- **output/monasteries_guide.html** — всегда создаётся.
- **output/monasteries_guide.pdf** — при установленном Playwright и Chromium.

В путеводителе: нумерация 1–20, заголовки объектов оформлены шрифтом в духе
древнерусской письменности (Neucha), один объект — не более одной страницы,
карты по координатам (Яндекс). В конце — раздел «Вопросы и ответы».

## Структура проекта

- `data/monasteries.py` — каталог (20 объектов), `IMAGES_SUBFOLDER`
- `data/qa.py`, `data/image_urls.py`
- `scripts/build_pdf.py` — сборка HTML/PDF, однократная попытка загрузки фото
- `scripts/download_images.py` — цикл загрузки фото в `moscow_monasteries` до успеха
- `output/images/moscow_monasteries/` — фото для путеводителя по Москве
- `requirements.txt` — playwright

Кодировка UTF-8, стиль кода PEP 8.
