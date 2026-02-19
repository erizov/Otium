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

### Excursion — Места поклонения Москвы

Путеводитель по местам поклонения: православные храмы, мечети, синагоги, буддийские храмы,
неортодоксальные христианские церкви. Те же шрифты, цвета и вёрстка, что и у гида
по монастырям. Изображения — в **output/images/moscow_places_of_worship/**; для каждого
места свой файл, дубликаты по содержимому (SHA256) проверяются.

```bash
python scripts/build_pdf.py --guide places_of_worship
```

- **output/places_of_worship_guide.html**, **output/places_of_worship_guide.pdf**
- Данные: **data/places_of_worship.py** (65 мест поклонения), **data/places_of_worship_image_urls.py** (URL Commons/Yandex Maps),
  **data/qa_places_of_worship.py** (вопросы и ответы). URL изображений при необходимости
  уточняют по Commons или Yandex Maps для соответствия месту поклонения.

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

**Рекомендуемые категории для расширения** (идеи для новых гидов):
стадионы, планетарии, галереи, усадьбы (отдельно от дворцов), фонтаны,
памятники архитектуры, сады и оранжереи, улицы и бульвары.

### Полный путеводитель по Москве (Moscow Complete Guide)

Скрипт **scripts/build_full_guide.py** собирает один сводный HTML и PDF из всех
тематических гидов: титульная страница, предисловие, главы по темам, примечания.

```bash
# Сборка по имеющимся изображениям (без загрузки)
python scripts/build_full_guide.py

# С предварительной загрузкой недостающих изображений
python scripts/build_full_guide.py --download-images
```

Результат: **output/Moscow_Complete_Guide.html**, **output/Moscow_Complete_Guide.pdf**.
При наличии старого PDF создаётся бэкап в **output/backup/** (до 3 копий).

### User workflow — редактирование и пересборка PDF

Кратко: **собрать → открыть HTML в браузере → править текст/картинки → Export HTML → сохранить файл → пересобрать PDF** (`--use-existing-html`).

| Шаг | Действие |
|-----|----------|
| 1 | Соберите полный путеводитель: `python scripts/build_full_guide.py` |
| 2 | Откройте **output/Moscow_Complete_Guide.html** в браузере |
| 3 | Редактируйте: меняйте текст в ячейках, удаляйте фото (× на изображении), добавляйте свои (кнопка «+ Add image», до 4 на объект) |
| 4 | Нажмите **Export HTML** (кнопка справа вверху), сохраните скачанный файл поверх **output/Moscow_Complete_Guide.html** |
| 5 | Пересоберите только PDF: `python scripts/build_full_guide.py --use-existing-html` |

Итог: **output/Moscow_Complete_Guide.pdf** будет содержать все ваши правки. Шрифты и вёрстка не меняются.

### Структура проекта

- `data/monasteries.py`, `data/churches.py`, `data/parks.py`, `data/museums.py`,
  `data/palaces.py`, `data/buildings.py`, `data/sculptures.py`, `data/places.py` —
  каталоги объектов и `IMAGES_SUBFOLDER`
- `data/qa.py`, `data/qa_churches.py`, `data/qa_parks.py`, … — вопросы и ответы
- `data/image_urls.py`, `data/church_image_urls.py`, `data/park_image_urls.py`, … —
  URL изображений (Commons)
- `scripts/build_pdf.py` — сборка HTML/PDF (`--guide` с выбором гида)
- `scripts/build_full_guide.py` — полный путеводитель (Moscow_Complete_Guide), редактируемый HTML
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

### Имена файлов изображений и дедупликация по имени объекта

Имя файла изображения должно соответствовать объекту: **slug** (идентификатор)
извлекается из имени файла (например, `red_square_1.jpg` → slug `red_square`).
Правила:

- В **data/\<guide>.py** у каждого объекта список имён файлов вида
  `{slug}_1.jpg`, `{slug}_2.jpg`, … (один slug на объект).
- В **data/\*_image_urls.py** ключи DOWNLOADS — те же имена файлов; один URL
  на один объект во всех гидах (скрипт **scripts/check_duplicate_images.py**).
- При кросс-гидовой дедупликации (**workflow_build_guides.py**) один и тот же
  контент перезаписывается только если у «победителя» и «проигравшего» один
  и тот же slug (один и тот же объект). Если slug разные — замена не делается,
  в лог выводится «Same content, different items — skipped replace».
- Проверка соответствия файлов объектам:  
  `python scripts/validate_images_per_item.py --check-slugs` (по каталогу
  output/images/).

### Изображения из Yandex Maps

Для автоматической генерации URL изображений из Yandex Maps используйте:

```bash
# Генерация URL для всех гидов (поиск по названию места)
python scripts/generate_yandex_image_urls.py

# Для конкретного гида
python scripts/generate_yandex_image_urls.py --guide places

# Тестовый запуск (без реального поиска)
python scripts/generate_yandex_image_urls.py --dry-run
```

Скрипт ищет каждое место в Yandex Maps по названию и извлекает URL фотографий,
затем генерирует файлы `data/*_image_urls.py` в формате, совместимом с текущей
структурой. После генерации проверьте и при необходимости отредактируйте URL
вручную, затем зафиксируйте изменения в git.

**Требования**: Playwright установлен (`playwright install chromium`).

**Тестирование поиска для одного места**:
```bash
python scripts/yandex_maps_images.py "Красная площадь" Москва
```

### Дополнительные fallback-URL из Wikimedia Commons

Если после нескольких раундов загрузки у некоторых объектов всё ещё не хватает
изображений, можно автоматически попытаться добавить fallback-URL с фотографиями
из Wikimedia Commons:

1. Сначала сформируйте список проблемных слотов (download_todo.txt) для всех
   гидов:

   ```bash
   python scripts/build_pdf.py --all-guides --download-retries 7 --download-only
   ```

2. Затем заполните fallback-URL из Commons:

   ```bash
   python scripts/fill_commons_fallbacks.py
   ```

   Скрипт читает `output/images/<guide_subdir>/download_todo.txt` и для каждого
   базового имени (basename) ищет на Wikimedia Commons фотографии соответствующего
   места (с достаточным разрешением, игнорируя svg/gif и слишком маленькие
   изображения). Найденные URL добавляются в соответствующий
   `*_IMAGE_FALLBACKS` в `data/*_image_urls.py`.

3. После этого запустите загрузку ещё раз (по нужному гиду или по всем):

   ```bash
   python scripts/build_pdf.py --all-guides --download-retries 7
   ```

Новые fallback-URL будут использоваться наравне с Yandex Maps при следующих
запусках загрузки.

### Запрещённые изображения и папка forbidden

- В **scripts/download_with_dedup.py** заданы **FORBIDDEN_BASENAMES** (файлы, которые
  не загружаются) и **FORBIDDEN_IMAGE_HASHES** (хеши изображений, которые сразу
  отбрасываются при загрузке).
- Изображения с запрещёнными именами при наличии в каталоге переносятся в
  **output/images/\<guide_subdir>/forbidden/** — их можно просмотреть и при
  необходимости вернуть. Отклонённые по хешу копии сохраняются туда же как
  `rejected_<basename>_<hash>.jpg`.
- Хеши из папки **forbidden/** подгружаются при запуске и объединяются с
  **FORBIDDEN_IMAGE_HASHES**, чтобы быстрее пропускать нежелательные изображения.

### Сборка по имеющимся изображениям и проверки

- **--build-with-available** — собрать HTML/PDF по тем изображениям, которые уже
  есть (допускается меньше 4 на объект).
- **--all-guides** — выполнить сборку для всех гидов (всегда с
  --build-with-available). Подходит для массовой генерации по имеющимся фото.
- **--download-retries N** — с **--all-guides**: N раундов загрузки недостающих
  изображений по всем гидам, затем сборка. По умолчанию 1. Используйте 5 и более,
  чтобы многократно пытаться заполнить пропуски (зависит от наличия рабочих URL
  в `data/*_image_urls.py`).
- **--verify-images** — проверить все изображения (дубликаты + формат). Без
  --download-only: только проверка, без загрузки и сборки. С --download-only:
  загрузить недостающие и проверить.
- **AI-проверка по умолчанию**: перед принятием загруженного изображения оно
  проверяется через OpenAI Vision (gpt-4o-mini), если задан **OPENAI_API_KEY**.
  Отключить: **--no-ai-identify**.
- **Переменные окружения**: ключ OpenAI загружается из файла **.env** в корне
  проекта (если установлен `python-dotenv`). Создайте `.env` с
  `OPENAI_API_KEY=sk-proj-...` для AI-проверки изображений. Дополнительные
  источники изображений: `PIXABAY_API_KEY`, `PEXELS_API_KEY` (по желанию).
  Файл `.env` в `.gitignore`, в репозиторий не попадает.

### Источники изображений (round-robin) и русскоязычные сайты

При заполнении URL (`fill_image_urls.py`) и при загрузке без готового URL
используется round-robin по источникам (один URL не сработал — пробуем следующий):

- **Commons**, **CommonsNameOnly**, **CommonsRussia**, **CommonsCityRu** — Wikimedia Commons (в т.ч. запросы с Москвой и по-русски).
- **Pixabay**, **Pexels**, **Unsplash**, **Flickr** (+ варианты *NameOnly*, *Russia*, *CityRu*) — международные бесплатные фото; *CityRu* = запрос с городом «Москва» для русскоязычных мест.
- **FlickrRussia**, **FlickrCityRu** — Flickr с запросами Russia / Москва (доп. русскоязычный контент).
- **PixabayCityRu**, **PexelsCityRu**, **UnsplashCityRu** — те же сервисы с городом «Москва» в запросе.
- **Openverse**, **OpenverseNameOnly**, **OpenverseCityRu** — Openverse (агрегатор CC).
- **YandexMaps**, **YandexImages** — Яндекс (город Москва).
- **Pastvu**, **PastvuMoscow** — [Pastvu](https://pastvu.com) (исторические фото Москвы, API api.pastvu.com).

Для мест без единого изображения (список в `output/places_without_images.txt`, строки 548–713) сначала заполните URL по всем гидам (round-robin по всем источникам, в т.ч. русскоязычным), затем загрузите:

```bash
python scripts/fill_image_urls.py
python scripts/build_pdf.py --all-guides --download-retries 5
```

В `data/*_image_urls.py` для каждого слота пишется основной URL и до 10 fallback-URL (round-robin при загрузке).

Для слотов 1–4: если файл уже есть, он не перезагружается, только проверяется
на дубликаты. Перезапись: **--force-overwrite**. Папка **forbidden/** проверяется
при каждой загрузке и при валидации; можно вручную переносить туда ненужные
изображения.

**Детальные предупреждения при загрузке**: для каждого слота, который не удалось
заполнить, выводится причина: (1) загружено — отклонено как дубликат с
*image_name*, (2) сетевая ошибка, (3) таймаут, (4) forbidden (хеш), (5) banned,
(6) перенесён в forbidden и т.д. В конце — блок «Download failures (detail)»
и запись в **download_todo.txt**.

**Сборка при 2+ изображениях**: в гид попадают только объекты, у которых есть
не менее 2 различных изображений (объекты с 0 или 1 изображением в PDF/HTML не
включаются). Список недостающих слотов сохраняется в
**output/images/\<guide_subdir>/download_todo.txt** (формат: guide, basename,
item_name, reason). При следующих запусках загрузки скрипт читает этот список
и папку **forbidden/** и выводит «Todo: N slot(s) from download_todo.txt
(forbidden/ checked)» — используйте его для последующих попыток дозагрузки.

```bash
python scripts/build_pdf.py --guide monasteries --build-with-available
python scripts/build_pdf.py --all-guides
python scripts/build_pdf.py --all-guides --download-retries 5
python scripts/build_pdf.py --guide monasteries --verify-images
python scripts/build_pdf.py --guide monasteries --no-ai-identify
```

Кодировка UTF-8, стиль кода PEP 8.

### Тесты

```bash
pytest -q
```

**E2E-тест** (`tests/test_e2e_workflow.py`): проверяет все гиды на:
- Валидность данных (обязательные поля, координаты)
- Наличие всех 4 изображений (_1.._4) и карты для каждого объекта
- Размеры изображений (минимум 400x300)
- Корректность ссылок в HTML

**Валидация данных** (`scripts/validate_images_per_item.py`):
- Проверка наличия 4 изображений на объект (--strict)
- Проверка соответствия файлов объектам (--check-slugs)

### Возобновление после сбоя

Система автоматически возобновляет загрузку после сбоя или потери сети:
- **download_failures.log** — список неудачных URL (пропускаются при повторе)
- **download_list.txt** — статус каждого слота (exists/missing)
- **download_todo.txt** — список проблемных слотов для повторной попытки
- **excluded_sources.json** — исключённые источники (1 час TTL)

При следующем запуске скрипт автоматически продолжит с места остановки.

### Структура скриптов

- **scripts/core.py** — базовые утилиты: исключения, логирование, валидация
- **scripts/build_pdf.py** — сборка HTML/PDF
- **scripts/build_full_guide.py** — полный путеводитель, редактируемый HTML, PDF по частям
- **scripts/download_with_dedup.py** — загрузка с дедупликацией
- **scripts/guide_loader.py** — загрузка данных гидов
- **scripts/helpers/** — вспомогательные скрипты (legacy)
