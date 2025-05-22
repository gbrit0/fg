from interfaces.command import Command
import os
import signal


class StopCommand(Command):
    """
    Para uma instância através do PID.
    """

    def __init__(self, pid):
        self.pid = pid

    def execute(self):
        try:
            os.kill(self.pid, signal.SIGTERM)
            print(f"Processo {self.pid} parado com sucesso.")
        except ProcessLookupError:
            print(f"Processo {self.pid} não encontrado.")
        except Exception as e:
            print(f"Erro ao parar processo: {e}")
