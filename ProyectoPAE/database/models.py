from dataclasses import dataclass
from datetime import date, time, datetime

@dataclass
class Estudiante:
    documento: int
    nombres: str
    apellidos: str
    grado: str

    def __str__(self):
        return f"{self.nombres} {self.apellidos} (Documento: {self.documento}, Grado: {self.grado})"

@dataclass
class EventoAlimenticio:
    id_evento: int
    documento: int
    fecha: date
    hora: time
    tipo_evento: str

    def __str__(self):
        return f"Evento {self.id_evento}: {self.tipo_evento} - Estudiante {self.documento} el {self.fecha} a las {self.hora}"

@dataclass
class EstudianteAction:
    action_id: int
    documento: int
    nombres: str
    apellidos: str
    grado: str
    action_time: datetime
    action: str
    consult_date: date

    def __str__(self):
        return f"Acción {self.action_id}: {self.action} - Estudiante {self.nombres} {self.apellidos} el {self.consult_date}"