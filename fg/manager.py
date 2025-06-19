import os
import requests
import tarfile
import zipfile
import shutil
import tempfile

from classes import message
from typing import Generator

import pathControll

DEFAULT_FILE = "fg/dependencias/versionDefault.txt"

def get_file_extension(url: str):
    clean_url = url.split('?')[0]
    clean_url = clean_url.split('#')[0]
    filename = os.path.basename(clean_url)
    _, extension = os.path.splitext(filename)
    return extension.lower()

def download_com_progresso(url: str, destino: str, id: int = None, nome: str = None):
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    baixado = 0
    bloco = 1024 * 32

    with open(destino, 'wb') as arquivo:
        for dado in response.iter_content(chunk_size=bloco):
            arquivo.write(dado)
            baixado += len(dado)
            porcentagem = min((baixado / total) * 100, 100) if total else 0
            yield {"indice": id,"nome": nome, "porcentagem": porcentagem}
    

def extrair_com_progresso_tar(path_compactado: str, destino: str, id: int, nome: str):
    with tarfile.open(path_compactado, 'r:gz') as tar:
        membros = tar.getmembers()
        total = len(membros)
        for i, membro in enumerate(membros, 1):
            tar.extract(membro, path=destino)
            porcentagem = (i / total) * 100
            yield {"indice": id,"nome": nome, "porcentagem": porcentagem}
            

def extrair_com_progresso_zip(path_compactado: str, destino: str, id: int, nome: str):
    with zipfile.ZipFile(path_compactado, 'r') as zipf:
        membros = zipf.infolist()
        total = len(membros)
        for i, membro in enumerate(membros, 1):
            zipf.extract(membro, path=destino)
            porcentagem = (i / total) * 100
            yield {"indice": id,"nome": nome, "porcentagem": porcentagem}

def install(version: str):
    temp_dir = None
    final_install_path = os.path.join(pathControll.home_path(), version)

    try:
        id = 0
        nome = ""

        if os.path.exists(final_install_path):
            raise Exception("A versão já foi instalada")

        # Cria pasta temporária
        temp_dir = tempfile.mkdtemp(prefix="install_temp_")
        pathOfDownload = temp_dir  # Usamos o temp até terminar tudo

        jdkPath = os.path.join(pathOfDownload, "jdk")

        jdkUrl = pathControll.getJdkUrl(version)
        ext = get_file_extension(jdkUrl)

        if ext == '.gz':
            nome = "Baixando JDK (.tar.gz)"
            yield {"indice": id, "nome": nome, "porcentagem": 0}

            jdkCompactadoPath = os.path.join(jdkPath, "jdk.tar.gz")
            os.makedirs(jdkPath, exist_ok=True)

            for progresso in download_com_progresso(jdkUrl, jdkCompactadoPath, id, nome):
                yield progresso
            id += 1

            nome = "Extraindo arquivo jdk"
            yield {"indice": id, "nome": nome, "porcentagem": 0}

            for progresso in extrair_com_progresso_tar(jdkCompactadoPath, jdkPath, id, nome):
                yield progresso
            id += 1

        elif ext == '.zip':
            nome = "Baixando JDK (.zip)"
            yield {"indice": id, "nome": nome, "porcentagem": 0}

            jdkCompactadoPath = os.path.join(jdkPath, "jdk.zip")
            os.makedirs(jdkPath, exist_ok=True)

            for progresso in download_com_progresso(jdkUrl, jdkCompactadoPath, id, nome):
                yield progresso
            id += 1

            nome = "Extraindo arquivo jdk"
            yield {"indice": id, "nome": nome, "porcentagem": 0}

            for progresso in extrair_com_progresso_zip(jdkCompactadoPath, jdkPath, id, nome):
                yield progresso
            id += 1

        os.remove(jdkCompactadoPath)

        # Remove subdiretório redundante dentro do jdk se existir
        jdk_contents = os.listdir(jdkPath)
        if len(jdk_contents) == 1:
            subdir = os.path.join(jdkPath, jdk_contents[0])
            if os.path.isdir(subdir):
                for item in os.listdir(subdir):
                    shutil.move(
                        os.path.join(subdir, item),
                        os.path.join(jdkPath, item)
                    )
                shutil.rmtree(subdir)

        # Baixa apps e dependências
        apps = pathControll.getApps(version)
        for app in apps:
            pathOfApp = os.path.join(pathOfDownload, app['nome'])
            os.makedirs(pathOfApp)

            for dependencia in app['dependencias']:
                dependenciePath = os.path.join(pathOfApp, dependencia['nomeLocal'])
                dependencieUrl = dependencia['url']

                nome = f"Baixando {dependencia['nomeLocal']}"
                yield {"indice": id, "nome": nome, "porcentagem": 0}

                for progresso in download_com_progresso(dependencieUrl, dependenciePath, id, nome):
                    yield progresso

                id += 1

        # Faz o rename/move da pasta temporária para a final
        shutil.move(temp_dir, final_install_path)
        temp_dir = None  # Marca como None para não tentar deletar

        set_default_version(version)
        return

    except Exception as e:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise Exception(f"❌ Erro durante a instalação: {str(e)}")


def update():
    pathControll.procurarNovasVersoes()
    for message in install(pathControll.mostRecentVersion()):
        yield message


def uninstall(version: str):
    try:

        homePath = pathControll.home_path()
        versionPath = os.path.join(homePath, version)

        if os.path.exists(versionPath):
            shutil.rmtree(versionPath)
            return f"Versão {version} desinstalada com sucesso."
        else:
            raise Exception(f"⚠️ Versão {version} não encontrada em: {versionPath}")
            
    
    except Exception as e:
        raise Exception(f"❌ Erro durante a desinstalação: {str(e)}")
        
def set_default_version(version: str):
    """
    Define a versão padrão do FHIR Guard. Diretorio de gravação: fg/dependencias/versionDefault.txt
    """
    from pathControll import home_path
    path = os.path.join(home_path(), version)

    if not os.path.isdir(path):
        raise Exception(f"❌ Versão '{version}' não está instalada em: {path}")

    os.makedirs(os.path.dirname(DEFAULT_FILE), exist_ok=True)

    with open(DEFAULT_FILE, "w") as f:
        f.write(version)

    return f"✅ Versão padrão definida como {version}"

def clear_default_version():
    """
    Remove o arquivo que define a versão padrão.
    """
    if os.path.exists(DEFAULT_FILE):
        os.remove(DEFAULT_FILE)

def get_default_version() -> str:
    """
    Retorna a versão padrão do FHIR Guard definida no arquivo:
    fg/dependencias/versionDefault.txt
    """
    if not os.path.isfile(DEFAULT_FILE):
        raise Exception("❌ Nenhuma versão padrão foi definida.")

    with open(DEFAULT_FILE, "r") as f:
        version = f.read().strip()

    return version
    

