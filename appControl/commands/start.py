from interfaces.command import Command
from pathlib import Path
import subprocess


class StartCommand(Command):
    """
    Inicia uma versão específica.
    """

    def __init__(self, version):
        self.version = version

    def execute(self):
        install_dir = Path.home() / ".fg" / self.version
        binary = install_dir / "fg"

        if not binary.exists():
            print(f"Versão {self.version} não está instalada.")
            return

        try:
            process = subprocess.Popen(
                [str(binary)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"Versão {self.version} iniciada com PID {process.pid}")
        except Exception as e:
            print(f"Erro ao iniciar: {e}")
