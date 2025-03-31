import os
from pathlib import Path

FG_HOME = Path.home() / "fhir-guard" / "versions"

#Gera a URL para download da versão especificada.
def generate_fg_url(version):
    return f"https://github.com/gbrit0/fg/releases/download/{version}/fhir-guard-{version}.zip" #Exemplo de url

#Retorna o caminho de instalação da versão especificada.
def get_installation_path(version):
    return FG_HOME / version