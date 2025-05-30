from enum import Enum
from dataclasses import dataclass
from typing import Any

# Enum para o status da mensagem
class Status(Enum):
    OK = "OK"
    ERRO = "ERRO"

# Classe reutilizável de mensagem
@dataclass
class Message:
    status: Status
    mensagem: str
    dado: Any = None  # Pode ser qualquer coisa: lista, número, dict, etc.


if __name__ == "__main__":
    # Exemplos de uso:
    msg1 = Message(status=Status.OK, mensagem="Operação realizada com sucesso", dado=[1, 2, 3])
    msg2 = Message(status=Status.ERRO, mensagem="Falha ao conectar no servidor", dado=None)
    msg3 = Message(status=Status.OK, mensagem="Total de registros", dado=42)

    # Exibindo
    print(msg1)
    print(msg2)
    print(msg3)