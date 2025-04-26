import os
import requests
import tarfile
import zipfile
import shutil
from typing import Generator

import pathControll

def get_file_extension(url: str) -> str:
    clean_url = url.split('?')[0]
    clean_url = clean_url.split('#')[0]
    filename = os.path.basename(clean_url)
    _, extension = os.path.splitext(filename)
    return extension.lower()

def download_com_progresso(url: str, destino: str) -> Generator[str, None, None]:
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    baixado = 0
    bloco = 1024 * 32

    with open(destino, 'wb') as arquivo:
        for dado in response.iter_content(chunk_size=bloco):
            arquivo.write(dado)
            baixado += len(dado)
            porcentagem = (baixado / total) * 100 if total else 0
            yield f"\r📥 Baixando: {porcentagem:6.2f}%"
    
    yield " ✅"

def extrair_com_progresso_tar(path_compactado: str, destino: str) -> Generator[str, None, None]:
    with tarfile.open(path_compactado, 'r:gz') as tar:
        membros = tar.getmembers()
        total = len(membros)
        for i, membro in enumerate(membros, 1):
            tar.extract(membro, path=destino)
            porcentagem = (i / total) * 100
            yield f"\r📦 Extraindo .tar.gz: {porcentagem:6.2f}%"
    yield " ✅"

def extrair_com_progresso_zip(path_compactado: str, destino: str) -> Generator[str, None, None]:
    with zipfile.ZipFile(path_compactado, 'r') as zipf:
        membros = zipf.infolist()
        total = len(membros)
        for i, membro in enumerate(membros, 1):
            zipf.extract(membro, path=destino)
            porcentagem = (i / total) * 100
            yield f"\r📦 Extraindo .zip: {porcentagem:6.2f}%"
    yield " ✅"

def install(version: str) -> Generator[str, None, None]:
    try:
        yield f"🟡 Iniciando instalação da versão {version}..."

        homePath = pathControll.home_path()
        pathOfDownload = os.path.join(homePath, version)
        jdkPath = os.path.join(pathOfDownload, "jdk")

        if os.path.exists(pathOfDownload):
            yield f"🔄 Removendo diretório existente: {pathOfDownload}"
            shutil.rmtree(pathOfDownload)

        yield f"📁 Criando diretório: {pathOfDownload}"
        os.makedirs(pathOfDownload, exist_ok=True)

        jdkUrl = pathControll.getJdkUrl(version)
        ext = get_file_extension(jdkUrl)

        if ext == '.gz':
            yield f"⬇️ Baixando JDK (.tar.gz) de: {jdkUrl}"
            jdkCompactadoPath = os.path.join(jdkPath, "jdk.tar.gz")
            os.makedirs(jdkPath, exist_ok=True)
            
            for progresso in download_com_progresso(jdkUrl, jdkCompactadoPath):
                yield progresso

            yield f"📦 Extraindo arquivo: {jdkCompactadoPath}"
            for progresso in extrair_com_progresso_tar(jdkCompactadoPath, jdkPath):
                yield progresso

        elif ext == '.zip':
            yield f"⬇️ Baixando JDK (.zip) de: {jdkUrl}"
            jdkCompactadoPath = os.path.join(jdkPath, "jdk.zip")
            os.makedirs(jdkPath, exist_ok=True)
            
            for progresso in download_com_progresso(jdkUrl, jdkCompactadoPath):
                yield progresso

            yield f"📦 Extraindo arquivo: {jdkCompactadoPath}"
            for progresso in extrair_com_progresso_zip(jdkCompactadoPath, jdkPath):
                yield progresso

        yield "🧹 Removendo arquivo compactado..."
        os.remove(jdkCompactadoPath)

        jdk_contents = os.listdir(jdkPath)
        if len(jdk_contents) == 1:
            subdir = os.path.join(jdkPath, jdk_contents[0])
            if os.path.isdir(subdir):
                yield f"📂 Reorganizando estrutura: movendo arquivos de {subdir} para {jdkPath}"
                for item in os.listdir(subdir):
                    os.rename(
                        os.path.join(subdir, item),
                        os.path.join(jdkPath, item)
                    )
                os.rmdir(subdir)

        yield "⬇️ Baixando dependências..."
        dependencies = pathControll.getDependencies(version)
        for dependencie in dependencies:
            dependenciePath = os.path.join(pathOfDownload, dependencie['localName'])
            dependencieUrl = dependencie['url']
            yield f"   🔹 {dependencie['localName']} de {dependencieUrl}"
            for progresso in download_com_progresso(dependencieUrl, dependenciePath):
                yield progresso

        yield "✅ Instalação concluída com sucesso."
        return
    
    except Exception as e:
        if os.path.exists(pathOfDownload):
            yield f"🔄 Removendo diretório existente: {pathOfDownload}"
            shutil.rmtree(pathOfDownload)
        yield f"❌ Erro durante a instalação: {str(e)}"
        return

def uninstall(version: str) -> Generator[str, None, None]:
    try:
        yield f"🗑️ Iniciando desinstalação da versão {version}..."

        homePath = pathControll.home_path()
        versionPath = os.path.join(homePath, version)

        if os.path.exists(versionPath):
            yield f"🔄 Removendo diretório: {versionPath}"
            shutil.rmtree(versionPath)
            yield f"✅ Versão {version} desinstalada com sucesso."
            return
        else:
            yield f"⚠️ Versão {version} não encontrada em: {versionPath}"
            return
    
    except Exception as e:
        yield f"❌ Erro durante a desinstalação: {str(e)}"
        return

if __name__ == "__main__":
    for message in install("6.5.1"):
        if message.startswith("\r"):
            print(message, end="", flush=True)
        else:
            print(message)