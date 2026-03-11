import os
from PIL import Image
import shutil

# Директория, откуда начинаем поиск (текущая директория, поменять на нужную)
root_dir = 'E:\\Python\\GptEngineer\\Excursion\\output\\images'
# Ограничиваем глубину поиска только прямым дочерними папками
subdirs = next(os.walk(root_dir))[1][:20]  # Берем первые 20 директорий первого уровня
# Лимит размера файла (более 500KB)
size_limit = 500 * 1024


def process_image(file_path):
    """
    Сжимает изображение и сохраняет оригинальную большую картинку в папку large_orig
    """
    img = Image.open(file_path)
    # Создаем резервную копию оригинала
    backup_folder = os.path.join(os.path.dirname(file_path), 'large_orig')
    os.makedirs(backup_folder, exist_ok=True)
    shutil.copy(file_path, os.path.join(backup_folder, os.path.basename(file_path)))
    # Сжимаем изображение
    img.save(file_path, optimize=True, quality=85)


for dir_name in subdirs:
    dir_path = os.path.join(root_dir, dir_name)
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        if os.path.isfile(filepath) and filename.lower().endswith('.jpg'):
            if os.path.getsize(filepath) > size_limit:
                print(f'Squeezing image: {filepath}')
                process_image(filepath)

print("All images processed.")