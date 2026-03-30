# Whitelist источников (Смоленск)

Как в проекте SPB: новые объекты и картинки — с перечисленных доменов
или с явной ссылкой на одну из них. Дополнительно **разрешены** любые
`https://upload.wikimedia.org/...` и `https://commons.wikimedia.org/...`
(см. `smolensk/whitelist.py`).

---

## A. Город и регион

| URL | Назначение |
|-----|------------|
| https://www.smoladmin.ru/ | Официальный портал администрации |
| https://www.smolensk.ru/ | Информационный ресурс (при наличии) |
| https://culture.ru/ | Объекты культурного наследия |
| https://www.culture.ru/ | Портал Культура.РФ (страницы учреждений) |
| https://cdn.culture.ru/ | CDN изображений Культура.РФ |

---

## B. Энциклопедии и Commons

| URL | Назначение |
|-----|------------|
| https://ru.wikipedia.org/wiki/ | Статьи (только путь `/wiki/...`) |
| https://upload.wikimedia.org/wikipedia/commons/ | Файлы Commons |

---

## C. Федеральные музейные сети (при ссылках на объекты в Смоленске)

| URL | Назначение |
|-----|------------|
| https://www.museum.ru/ | Каталог музеев |

---

## D. Vuzopedia (логотипы «Региональные вузы»)

| URL | Назначение |
|-----|------------|
| https://i.vuzopedia.ru/ | CDN логотипов вузов (resize) |

Добавляйте новые префиксы `https://...` в эту таблицу перед использованием
в `image_source_url` вне Commons и ru.wikipedia.
