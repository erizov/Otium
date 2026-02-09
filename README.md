# Otium

Guides by themes.

---

## Excursion — московские монастыри

Каталог из 20 монастырей и подворий Москвы: адреса, стили, история,
значение, факты. Генерация HTML- и PDF-путеводителя с картами и разделом
«Вопросы и ответы». Изображения хранятся в подпапке по темам для
возможности добавлять другие PDF (например, по другим городам).

### Данные

- **data/monasteries.py** — список `MONASTERIES` (20 объектов), константа
  `IMAGES_SUBFOLDER = "moscow_monasteries"`.
- **data/qa.py** — вопросы и ответы для раздела в конце PDF.
- **data/image_urls.py** — публичные URL изображений (Wikipedia/Commons):
  свободные лицензии, узнаваемые виды.

Фотографии сохраняются в **output/images/moscow_monasteries/** — отдельная
подпапка под тему, чтобы в будущем добавлять, например,
`output/images/saint_petersburg/` для другого путеводителя.

### Сборка PDF

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
древнерусской письменности (Pochaevsk / Source Serif 4), один объект — новая
страница, карты по координатам (Яндекс). В конце — раздел «Вопросы и ответы».

### Excursion — 60 значимых храмов Москвы

Отдельный путеводитель по 60 храмам: те же шрифты, цвета и вёрстка, что и у гида
по монастырям. Изображения — в **output/images/moscow_churches/**; для каждого
храма свой файл, дубликаты по содержимому (SHA256) проверяются.

```bash
python scripts/build_pdf.py --guide churches
```

- **output/churches_guide.html**, **output/churches_guide.pdf**
- Данные: **data/churches.py** (60 храмов), **data/church_image_urls.py** (URL Commons),
  **data/qa_churches.py** (вопросы и ответы). URL изображений при необходимости
  уточняют по Commons для соответствия храму.

### Другие путеводители (тот же принцип, отдельные подпапки для изображений)

| Гиды | Команда | Мест | Подпапка изображений |
|------|---------|------|----------------------|
| Парки | `--guide parks` | 20 | moscow_parks |
| Музеи | `--guide museums` | 30 | moscow_museums |
| Усадьбы и дворцы | `--guide palaces` | 20 | moscow_palaces |
| Знаменитые здания | `--guide buildings` | 50 | moscow_buildings |
| Скульптуры и памятники | `--guide sculptures` | 60 | moscow_sculptures |
| Места (улицы, площади, районы) | `--guide places` | 50 | moscow_places |

Данные: **data/parks.py**, **data/museums.py**, **data/palaces.py**, **data/buildings.py**,
**data/sculptures.py**, **data/places.py** и соответствующие `*_image_urls.py`, `qa_*.py`.

### Структура проекта

- `data/monasteries.py`, `data/churches.py`, `data/parks.py`, `data/museums.py`,
  `data/palaces.py`, `data/buildings.py`, `data/sculptures.py`, `data/places.py` —
  каталоги объектов и `IMAGES_SUBFOLDER`
- `data/qa.py`, `data/qa_churches.py`, `data/qa_parks.py`, … — вопросы и ответы
- `data/image_urls.py`, `data/church_image_urls.py`, `data/park_image_urls.py`, … —
  URL изображений (Commons)
- `scripts/build_pdf.py` — сборка HTML/PDF (`--guide` с выбором гида)
- `scripts/download_images.py` — цикл загрузки фото в `moscow_monasteries` до успеха
- `output/images/moscow_monasteries/`, `moscow_churches/`, `moscow_parks/`,
  `moscow_museums/`, `moscow_palaces/`, `moscow_buildings/`, `moscow_sculptures/`,
  `moscow_places/`
- `requirements.txt` — playwright

### Workflow и проверка изображений (4 на объект)

**scripts/workflow_build_guides.py** — полный цикл: бэкап → загрузка изображений
по всем гидам → дедупликация по контенту между гидами → проверка «4 изображения
на объект» → сборка PDF.

Требование: у каждого объекта в гиде должно быть **ровно 4 изображения** с
разными URL в `*_image_urls.py` (без дубликатов внутри объекта). Проверка:
**scripts/validate_images_per_item.py**. Гиды, где уже 4 изображения на объект:
places (moscow_places). Остальные гиды нужно дополнить по тому же принципу:
в `data/<guide>.py` у каждого объекта список из 4 файлов (_1 … _4), в
`data/<guide>_image_urls.py` — по 4 разных URL на объект. Чтобы собрать PDF
без прохождения проверки (пока не все гиды расширены), задайте
`SKIP_IMAGE_VALIDATION=1` перед запуском workflow.

Кодировка UTF-8, стиль кода PEP 8.
