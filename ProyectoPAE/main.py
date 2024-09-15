import sys
import os

# Añade el directorio raíz del proyecto al PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from database.connector import DatabaseConnector
from storage.estudiante_dao import EstudianteDAO
from storage.evento_dao import EventoDAO
from storage.action_dao import ActionDAO
from gui.main_view import MainView
from config import DB_CONFIG, APP_NAME, VERSION
from utils.helpers import log_error


def main():
    print(f"Iniciando {APP_NAME} v{VERSION}")

    try:
        # Inicializar la conexión a la base de datos
        db_connector = DatabaseConnector(**DB_CONFIG)
        db_connector.connect()

        # Inicializar DAOs
        estudiante_dao = EstudianteDAO(db_connector)
        evento_dao = EventoDAO(db_connector)
        action_dao = ActionDAO(db_connector)

        # Iniciar la interfaz principal
        app = MainView(estudiante_dao, action_dao)
        app.title(f"{APP_NAME} v{VERSION}")
        app.mainloop()

    except Exception as e:
        error_message = f"Error crítico: {str(e)}"
        print(error_message)
        log_error(error_message)
    finally:
        # Cerrar la conexión a la base de datos al cerrar la aplicación
        if 'db_connector' in locals():
            db_connector.disconnect()


if __name__ == "__main__":
    main()