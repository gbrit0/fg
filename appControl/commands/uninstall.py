from interfaces.command import Command
import shutil
from pathlib import Path


class UninstallCommand(Command):
    """
    Desinstala uma versão específica.
    """

    def __init__(self, version):
        self.version = version

    def execute(self):
        install_dir = Path.home() / ".fg" / self.version

        if not install_dir.exists():
            print(f"A versão {self.version} não está instalada.")
            return

        shutil.rmtree(install_dir)
        print(f"A versão {self.version} foi desinstalada com sucesso.")
