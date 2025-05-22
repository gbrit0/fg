from interfaces.command import Command
from pathlib import Path
import yaml


class ConfigCommand(Command):
    """
    Exibe a configuração da versão.
    """

    def __init__(self, version):
        self.version = version

    def execute(self):
        config_file = Path.home() / ".fg" / self.version / "config.yaml"

        if not config_file.exists():
            print(f"Configuração não encontrada para a versão {self.version}.")
            return

        try:
            with open(config_file, "r") as file:
                config = yaml.safe_load(file)
                print(f"Configuração para {self.version}:")
                print(yaml.dump(config, sort_keys=False))
        except Exception as e:
            print(f"Erro ao ler configuração: {e}")
