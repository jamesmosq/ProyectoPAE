from database.models import EventoAlimenticio

class EventoDAO:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def crear_evento(self, evento):
        query = """
        INSERT INTO EventosAlimenticios (ID_evento, Documento, Fecha, Hora, Tipo_evento)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (evento.id_evento, evento.documento, evento.fecha, evento.hora, evento.tipo_evento)
        return self.db_connector.execute_query(query, params) is not None

    def buscar_evento(self, id_evento):
        query = "SELECT * FROM EventosAlimenticios WHERE ID_evento = %s"
        result = self.db_connector.execute_query(query, (id_evento,))
        if result and result[0]:
            return EventoAlimenticio(*result[0])
        return None

    def actualizar_evento(self, evento):
        query = """
        UPDATE EventosAlimenticios
        SET Documento = %s, Fecha = %s, Hora = %s, Tipo_evento = %s
        WHERE ID_evento = %s
        """
        params = (evento.documento, evento.fecha, evento.hora, evento.tipo_evento, evento.id_evento)
        return self.db_connector.execute_query(query, params) is not None

    def eliminar_evento(self, id_evento):
        query = "DELETE FROM EventosAlimenticios WHERE ID_evento = %s"
        return self.db_connector.execute_query(query, (id_evento,)) is not None

    def ver_eventos(self):
        query = "SELECT * FROM EventosAlimenticios"
        result = self.db_connector.execute_query(query)
        return [EventoAlimenticio(*row) for row in result] if result else []