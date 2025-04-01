from PIL import Image
import os

def compress_image(input_path, output_path, quality=70):
    """
    Сжимает изображение и сохраняет его.
    
    :param input_path: Путь к исходному изображению.
    :param output_path: Путь для сохранения сжатого изображения.
    :param quality: Качество сжатия (по умолчанию 85%).
    """
    # Открытие изображения
    with Image.open(input_path) as img:
        # Сжимаем изображение, поддерживая оригинальный формат
        img.save(output_path, optimize=True, quality=quality)

    print(f"Изображение сохранено как {output_path} с качеством {quality}%")

# Пример использования:
input_image_path = '/Users/loki/Desktop/web_view/src/assets/image/background_old.jpg'  # Путь к исходному изображению
output_image_path = '/Users/loki/Desktop/web_view/src/assets/image/background.jpg'  # Путь для сохранения сжатого изображения

compress_image(input_image_path, output_image_path)

