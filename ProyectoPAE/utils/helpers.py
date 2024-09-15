import re
from datetime import datetime

def validate_document(document):
    """
    Valida que el documento sea un número entero positivo.
    """
    try:
        doc = int(document)
        return doc > 0
    except ValueError:
        return False

def format_date(date):
    """
    Formatea una fecha en el formato dd/mm/yyyy.
    """
    if isinstance(date, datetime):
        return date.strftime("%d/%m/%Y")
    elif isinstance(date, str):
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            return date_obj.strftime("%d/%m/%Y")
        except ValueError:
            return "Fecha inválida"
    else:
        return "Formato de fecha no soportado"

def get_current_time_type():
    """
    Determina el tipo de evento basado en la hora actual.
    """
    now = datetime.now().time()
    if datetime.strptime("08:00", "%H:%M").time() <= now <= datetime.strptime("10:00", "%H:%M").time():
        return "REFRIGERIO"
    elif datetime.strptime("12:00", "%H:%M").time() <= now <= datetime.strptime("13:40", "%H:%M").time():
        return "ALMUERZO"
    else:
        return "FUERA DE HORARIO"

def validate_name(name):
    """
    Valida que el nombre contenga solo letras, espacios y algunos caracteres especiales.
    """
    return bool(re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\'-]+$', name))

def validate_grade(grade):
    """
    Valida que el grado sea un número del 1 al 11.
    """
    try:
        grade_num = int(grade)
        return 1 <= grade_num <= 11
    except ValueError:
        return False

def log_error(error_message):
    """
    Registra un mensaje de error en un archivo de log.
    """
    with open('error_log.txt', 'a') as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - ERROR: {error_message}\n")

def sanitize_input(input_string):
    """
    Limpia una cadena de entrada para prevenir inyección SQL.
    """
    return re.sub(r'[\'";]', '', input_string)