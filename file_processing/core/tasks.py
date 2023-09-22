import re
from celery import shared_task
from .models import File


@shared_task
def process_file(file_id: int) -> None:
    """
    Асинхронная задача для обработки файлов.
    Определяет формат файла и выполняет соответствующую операцию над ним.
    """
    try:
        file = File.objects.get(id=file_id)
        filename = file.file.name

        file_type = determine_file_type(filename)
        
        if file_type in ['img', 'jpg', 'png']:
            file.processed = True
        
        if file_type=='txt':
            process_text(file)
            file.processed = True

        file.save()
    except File.DoesNotExist:
        pass

def determine_file_type(name: str) -> str:
    """
    Определяет формат файла.
    
    Алгоритм:
        Разбиваем строку на подстроки используя split "."
        Получаем последний элемент т.к это расширение
    """
    file_type = name.split(".")[-1]

    return file_type

def process_text(file: File) -> str:
    """
    Обрабатывает текстовые файлы.
    Получает из текста номер телефона используя регулярные выражения

    Возвращает:
        Путь к измененному файлу
    """
    with open(file.file.path, 'r') as text_file:
        text_content = text_file.read()
        
        # Шаблон регулярного выражения для номера телефона. Взято из iHateRegex
        phone_number_pattern = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
        phone_numbers = re.findall(phone_number_pattern, text_content)
        
        processed_text_path = 'processed_text.txt'
        with open(processed_text_path, 'w') as processed_file:
            processed_file.write('Номер телефона: ' + ', '.join(phone_numbers))
    
    return processed_text_path