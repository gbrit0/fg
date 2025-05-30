import os
import requests
import tarfile
import zipfile
import shutil
from classes import message
from typing import Generator

import pathControll

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
            porcentagem = (baixado / total) * 100 if total else 0
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
    try: 
        id = 0
        nome = ""
        homePath = pathControll.home_path()
        pathOfDownload = os.path.join(homePath, version)
        jdkPath = os.path.join(pathOfDownload, "jdk")

        if os.path.exists(pathOfDownload):
            raise Exception("A versão já foi instalada")
        
        os.makedirs(pathOfDownload, exist_ok=True)

        jdkUrl = pathControll.getJdkUrl(version)
        ext = get_file_extension(jdkUrl)

        if ext == '.gz': 
            nome = "Baixando JDK (.tar.gz)"
            yield {"indice": id,"nome": nome, "porcentagem": 0}

            jdkCompactadoPath = os.path.join(jdkPath, "jdk.tar.gz")
            os.makedirs(jdkPath, exist_ok=True)
            
            for progresso in download_com_progresso(jdkUrl, jdkCompactadoPath, id, nome):
                yield progresso
            id += 1

            nome = "Extraindo arquivo jdk"
            yield {"indice": id,"nome": nome, "porcentagem": 0}
            
            for progresso in extrair_com_progresso_tar(jdkCompactadoPath, jdkPath, id, nome):
                yield progresso
            id += 1

        elif ext == '.zip':

            nome = "Baixando JDK (.zip)"
            yield {"indice": id,"nome": nome, "porcentagem": 0}

            jdkCompactadoPath = os.path.join(jdkPath, "jdk.zip")
            os.makedirs(jdkPath, exist_ok=True)
            
            for progresso in download_com_progresso(jdkUrl, jdkCompactadoPath,id,nome):
                yield progresso
            id += 1

            nome = "Extraindo arquivo jdk"
            yield {"indice": id,"nome": nome, "porcentagem": 0}
            for progresso in extrair_com_progresso_zip(jdkCompactadoPath, jdkPath,id,nome):
                yield progresso
            id += 1

        os.remove(jdkCompactadoPath)

        jdk_contents = os.listdir(jdkPath)
        if len(jdk_contents) == 1:
            subdir = os.path.join(jdkPath, jdk_contents[0])
            if os.path.isdir(subdir):
                for item in os.listdir(subdir):
                    os.rename(
                        os.path.join(subdir, item),
                        os.path.join(jdkPath, item)
                    )
                shutil.rmtree(subdir)

        
        
        dependencies = pathControll.getDependencies(version)
        for dependencie in dependencies:
            dependenciePath = os.path.join(pathOfDownload, dependencie['nomeLocal'])
            dependencieUrl = dependencie['url']

            nome = f"Baixando {dependencie['nomeLocal']}"
            yield {"indice": id,"nome": nome, "porcentagem": 0}

            for progresso in download_com_progresso(dependencieUrl, dependenciePath,id,nome):
                yield progresso

            id +=1
        return
    
    except Exception as e:
        if os.path.exists(pathOfDownload):
            shutil.rmtree(pathOfDownload)
        raise Exception(f"❌ Erro durante a instalação: {str(e)}")
    


def update():
    for message in install(pathControll.mostRecentVersion()):
        yield message


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


def toRed(s:str):
    return "\033[91m" + s + "\033[0m"

if __name__ == "__main__":
    for msg in install("6.5.1"):
        if isinstance(msg, message.Message):
            if msg.mensagem.startswith("\r"):
                print(msg.mensagem, end="", flush=True)
            else:
                if msg.status == message.Status.ERRO:
                    print(toRed(msg.mensagem))
                else:
                    print(msg.mensagem)
        else:
            print(msg)