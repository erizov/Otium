# Quickstart: гид Санкт-Петербург (SPB)

Корень дерева: **`spb/`** (отдельно от Москвы).  
Данные: **`spb/data/spb_places.json`** (список объектов; в коде — `SPB_PLACES` из `places_registry.py`).  
Тексты для PDF/HTML (адрес, стиль, годы, описание, история, значение, факты, истории): опционально **`spb/data/spb_place_details.json`** — объекты по ключу `slug` подмешиваются к записям при загрузке.  
Сейчас в v1 **64** объекта (≥ 50 по плану).  
Фото: `spb/images/...` (пути в поле `image_rel_path`).  
Whitelist URL: `spb/docs/SOURCES_WHITELIST.md`.

Все команды из **корня репозитория** (`Excursion/`).

---

## 1. Проверка ссылок на источники

```bash
python scripts/validate_spb_sources.py
```

---

## 2. Скачать только изображения

У каждого объекта в JSON уже заданы `image_source_url` (whitelist) и `image_rel_path`. При добавлении своих записей — те же поля, затем:

```bash
python scripts/download_spb_images.py
```

По умолчанию скрипт качает **превью Commons** (`/thumb/.../1280px-...`), делает **паузу ~3.5 с** между файлами и при **HTTP 429** ждёт и повторяет запрос — так реже режет rate limit Wikimedia. Оригиналы (выше риск 429):

```bash
python scripts/download_spb_images.py --full-size --delay 6
```

Полезные опции: `--delay 5`, `--thumb-width 1024`, `--pause-429 60`, `--retries-429 6`.

Перезаписать существующие файлы:

```bash
python scripts/download_spb_images.py --force
```

Другой корень дерева SPB:

```bash
python scripts/download_spb_images.py --spb-root path/to/spb
```

Отключить проверку whitelist (не рекомендуется):

```bash
python scripts/download_spb_images.py --no-whitelist-check
```

---

## 3. Собрать PDF по уже лежащим локально фото

Скрипт **не качает** ничего из сети: берутся только объекты, у которых файл по `image_rel_path` есть под `spb/` и не меньше ~500 байт.

```bash
python scripts/build_spb_pdf.py
```

Результат:

- `spb/output/spb_guide.html`
- `spb/output/spb_guide.pdf`

Другой каталог вывода:

```bash
python scripts/build_spb_pdf.py --output-dir spb/output
```

Если локальных фото ни у одного объекта нет, скрипт завершится с кодом **2** и подсказкой в stderr.

### Playwright (нужен для PDF)

```bash
pip install playwright
playwright install chromium
```

---

## 4. Типичный цикл

```bash
python scripts/validate_spb_sources.py
python scripts/download_spb_images.py
python scripts/build_spb_pdf.py
```

На Windows (PowerShell) то же самое, из каталога репозитория.
