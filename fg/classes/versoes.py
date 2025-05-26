from dataclasses import dataclass
from datetime import date

@dataclass
class Registro:
    versao: str
    data: date
    valor: int