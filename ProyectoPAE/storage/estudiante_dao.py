from database.models import Estudiante

class EstudianteDAO:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def crear_estudiante(self, estudiante):
        query = """
        INSERT INTO Estudiantes (Documento, Nombres, Apellidos, Grado)
        VALUES (%s, %s, %s, %s)
        """
        params = (estudiante.documento, estudiante.nombres, estudiante.apellidos, estudiante.grado)
        return self.db_connector.execute_query(query, params) is not None

    def buscar_estudiante(self, documento):
        query = "SELECT * FROM Estudiantes WHERE Documento = %s"
        result = self.db_connector.execute_query(query, (documento,))
        if result and result[0]:
            return Estudiante(*result[0])
        return None

    def actualizar_estudiante(self, estudiante):
        query = """
        UPDATE Estudiantes
        SET Nombres = %s, Apellidos = %s, Grado = %s
        WHERE Documento = %s
        """
        params = (estudiante.nombres, estudiante.apellidos, estudiante.grado, estudiante.documento)
        return self.db_connector.execute_query(query, params) is not None

    def eliminar_estudiante(self, documento):
        query = "DELETE FROM Estudiantes WHERE Documento = %s"
        return self.db_connector.execute_query(query, (documento,)) is not None

    def ver_estudiantes(self):
        query = "SELECT * FROM Estudiantes"
        result = self.db_connector.execute_query(query)
        return [Estudiante(*row) for row in result] if result else []