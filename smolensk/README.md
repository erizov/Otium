# Путеводитель OTIUM · Смоленск

Компактный гид на **48 объектов** (как стартовый набор; список можно
сужать или менять в `data/smolensk_places.json`). Структура повторяет
проект `spb/`, отличия:

- **Одна папка для всех фото:** `smolensk/images/` без подкаталогов.
  В JSON у каждого объекта путь вида `images/<slug>.jpg`.
- Тексты карточек (адрес, описание, история…) подмешиваются из
  `data/smolensk_place_details.json` и при необходимости
  `data/smolensk_place_details_more.json` — по полю `slug`, как в SPB.

## Зависимости

- Python 3.10+
- Для PDF: `pip install playwright pypdf` и `playwright install chromium`

## Загрузка изображений

Из корня репозитория `Excursion`:

```text
python scripts/download_smolensk_images.py
```

По умолчанию качаются превью Commons (~1280 px) с паузой между файлами,
чтобы реже ловить HTTP 429. Полезные флаги:

- `--force` — перезаписать уже существующие файлы.
- `--smolensk-root путь` — корень дерева (по умолчанию `smolensk/`).
- `--full-size` — оригиналы с Commons (выше риск 429).
- `--no-whitelist-check` — только для отладки.

URL берутся из поля `image_source_url` в `data/smolensk_places.json`;
домены должны проходить проверку `docs/SOURCES_WHITELIST.md` и правила
в `smolensk/whitelist.py` (Commons и ru.wikipedia разрешены по тем же
принципам, что у SPB).

## Проверка URL

```text
python scripts/validate_smolensk_sources.py
```

## Сборка HTML и PDF

```text
python scripts/build_smolensk_pdf.py
```

Результат: `smolensk/output/smolensk_guide.html` и
`smolensk/output/smolensk_guide.pdf`. В PDF попадают только объекты,
у которых локальный файл картинки не меньше 500 байт (как у SPB).

Опции:

- `--smolensk-root`, `--output-dir`
- `--image-wait-ms` — ожидание прогрузки картинок в Chromium (большие
  отчёты можно увеличить, например до 60000).

## Редактирование данных

1. **Список объектов:** `smolensk/data/smolensk_places.json`  
   Поля: `slug`, `category`, `name_ru`, `subtitle_en`, `image_source_url`,
   `image_rel_path` (обязательно `images/<slug>.jpg`), `license_note`,
   `attribution`. Опционально **`additional_images`**: массив объектов
   с теми же полями `image_rel_path` и `image_source_url` для второй
   и следующих фотографий (всё в том же каталоге `images/`).
2. **Тексты:** `smolensk/data/smolensk_place_details.json` — объект
   верхнего уровня, ключи = `slug`, значения как в SPB: `address`,
   `year_built`, `architecture_style`, `description`, `history`,
   `significance`, `facts`, `stories`. Пустые поля можно не указывать —
   в PDF они не показываются (год и стиль только если есть текст).

В PDF **нет заголовков разделов** («Мосты», «Музеи» и т.д.): идёт
непрерывный список карточек, по умолчанию **по алфавиту русского
названия**. Поле `category` в JSON остаётся для учёта и возможных
будущих сценариев.

Дополнительные идеи без добавления в JSON: `docs/CANDIDATES_20.md`
(20 кандидатов на согласование).

## Примечание о стартовом списке

Часть пунктов тематически близка (несколько видов крепости/Успенского
собора) — так задано для быстрого старта с рабочими ссылками на Commons.
Имеет смысл со временем объединить или заменить дубликаты на другие
популярные места города.

В PDF **нет заголовков разделов** («Мосты Смоленска» и т.п.): только
обложка, заголовок гида и карточки объектов. Если в старом
`smolensk_guide.html` они ещё видны — пересоберите:
`python scripts/build_smolensk_pdf.py`.
