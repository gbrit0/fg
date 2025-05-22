from interfaces.command import Command
from pathlib import Path


class ListCommand(Command):
    """
    Lista todas as versões instaladas.
    """

    def execute(self):
        base_dir = Path.home() / ".fg"
        if not base_dir.exists():
            print("Nenhuma versão instalada.")
            return

        versions = [d.name for d in base_dir.iterdir() if d.is_dir()]
        if not versions:
            print("Nenhuma versão instalada.")
        else:
            print("Versões instaladas:")
            for version in versions:
                print(f"- {version}")
