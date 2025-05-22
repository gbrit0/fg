from interfaces.command import Command
import requests
import zipfile
import os
import shutil
from pathlib import Path


class InstallCommand(Command):
    """
    Instala uma versão específica.
    """

    def __init__(self, version):
        self.version = version

    def execute(self):
        try:
            url = f"https://github.com/gbrit0/fg/releases/download/{self.version}/fg-{self.version}.zip"
            install_dir = Path.home() / ".fg" / self.version

            if install_dir.exists():
                print(f"Versão {self.version} já está instalada.")
                return

            install_dir.mkdir(parents=True, exist_ok=True)
            zip_path = install_dir / "fg.zip"

            print(f"Baixando {url}...")
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Versão {self.version} não encontrada.")
                return

            with open(zip_path, "wb") as file:
                file.write(response.content)

            print("Extraindo arquivos...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(install_dir)

            os.remove(zip_path)

            print(f"Versão {self.version} instalada em {install_dir}")
        except Exception as e:
            print(f"Erro ao instalar a versão {self.version}: {e}")
