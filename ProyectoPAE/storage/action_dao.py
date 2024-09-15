from database.models import EstudianteAction
from datetime import datetime


class ActionDAO:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def registrar_accion(self, documento):
        # Primero, obtenemos los datos del estudiante
        query_estudiante = "SELECT * FROM Estudiantes WHERE Documento = %s"
        estudiante_data = self.db_connector.execute_query(query_estudiante, (documento,))

        if not estudiante_data:
            return None

        # Determinamos el tipo de acción basado en la hora actual
        now = datetime.now()
        if now.time() >= datetime.strptime("08:00", "%H:%M").time() and now.time() <= datetime.strptime("10:00",
                                                                                                        "%H:%M").time():
            action_type = "REFRIGERIO"
        elif now.time() >= datetime.strptime("12:00", "%H:%M").time() and now.time() <= datetime.strptime("13:40",
                                                                                                          "%H:%M").time():
            action_type = "ALMUERZO"
        else:
            action_type = "FUERA DE HORARIO"

        # Insertamos la acción en la tabla EstudiantesActions
        query_insert = """
        INSERT INTO EstudiantesActions (Documento, Nombres, Apellidos, Grado, ActionTime, ConsultDate, Action)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
        documento, estudiante_data[0][1], estudiante_data[0][2], estudiante_data[0][3], now, now.date(), action_type)

        if self.db_connector.execute_query(query_insert, params) is not None:
            # Si la inserción fue exitosa, devolvemos un objeto EstudianteAction
            return EstudianteAction(None, documento, estudiante_data[0][1], estudiante_data[0][2],
                                    estudiante_data[0][3], now, action_type, now.date())
        return None

    def ver_acciones(self, documento=None):
        if documento:
            query = "SELECT * FROM EstudiantesActions WHERE Documento = %s ORDER BY ActionTime DESC"
            result = self.db_connector.execute_query(query, (documento,))
        else:
            query = "SELECT * FROM EstudiantesActions ORDER BY ActionTime DESC"
            result = self.db_connector.execute_query(query)

        return [EstudianteAction(*row) for row in result] if result else []