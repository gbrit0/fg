import os
import zipfile
import subprocess
import requests
from pathlib import Path
from .fg_api import get_available_versions
from .fg_utils import generate_fg_url, get_installation_path, FG_HOME

#Instala uma versão específica do FHIR Guard.
def fg_install(version):
    if not version:
        print("Uso: fg install <versao>")
        return

    available_versions = get_available_versions()
    if version not in available_versions:
        print(f"Erro: A versão {version} não está disponível!")
        return

    fg_folder = get_installation_path(version)
    if fg_folder.exists():
        print(f"FHIR Guard {version} já está instalado.")
        return

    print(f"Baixando FHIR Guard {version}...")
    fg_url = generate_fg_url(version)
    zip_path = Path(os.getenv("TEMP")) / f"fhir-guard-{version}.zip"

    try:
        response = requests.get(fg_url, stream=True)
        response.raise_for_status()
        with open(zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.RequestException as e:
        print(f"Erro ao baixar o FHIR Guard: {e}")
        return

    fg_folder.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(FG_HOME)
        zip_path.unlink()
        print(f"Versão {version} instalada com sucesso em {fg_folder}")
    except zipfile.BadZipFile:
        print("Erro ao extrair o arquivo ZIP. O download pode estar corrompido.")

#Remove uma versão específica do aplicativo.
def fg_uninstall(version):
    fg_folder = get_installation_path(version)
    if not fg_folder.exists():
        print(f"Versão {version} não encontrada.")
        return

    confirm = input(f"Confirm uninstallation of version {version}? (y/N) ")
    if confirm.lower() != 'y':
        print("Operação cancelada.")
        return

    try:
        for item in fg_folder.rglob("*"):
            if item.is_file():
                item.unlink()
        fg_folder.rmdir()
        print(f"Version {version} uninstalled successfully.")
    except Exception as e:
        print(f"Failed to uninstall version {version}: {e}")

#Atualiza para a versão mais recente.
def fg_update():
    available_versions = get_available_versions()
    installed_versions = [folder.name for folder in FG_HOME.iterdir() if folder.is_dir()]
    latest_version = available_versions[0] if available_versions else None

    if latest_version and latest_version not in installed_versions:
        print(f"Updating to version {latest_version}...")
        fg_install(latest_version)
        print(f"Updated to version {latest_version}. This is now the default version.")
    else:
        print(f"No newer version available. You have the latest version: {latest_version}.")

#Lista todas as versões instaladas do FG.
def fg_list():
    print("Installed versions:")
    installed_versions = sorted(FG_HOME.iterdir(), key=lambda v: v.name, reverse=True)
    for folder in installed_versions:
        marker = "* " if folder == installed_versions[0] else "  "
        print(f"{marker}{folder.name}")

#Lista as versões disponíveis para instalação.
def fg_available():
    print("Fetching available versions from GitHub...")
    versions = get_available_versions()
    if versions:
        print("Available versions:")
        for version in versions:
            print(f"- {version}")
    else:
        print("No versions found!")
