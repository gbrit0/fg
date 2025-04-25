
import os
import requests
import tarfile
import zipfile
import shutil

import pathControll

def get_file_extension(url: str) -> str:
    # Remove parâmetros da URL (tudo após '?')
    clean_url = url.split('?')[0]
    # Remove fragmentos (tudo após '#')
    clean_url = clean_url.split('#')[0]
    # Pega a última parte do caminho (nome do arquivo)
    filename = os.path.basename(clean_url)
    # Separa a extensão (pode ser .zip, .tar.gz, etc.)
    _, extension = os.path.splitext(filename)
    return extension.lower()  # Retorna em minúsculas para consistência


def install(
        version: str
):
    

    homePath = pathControll.home_path()

    pathOfDownload = os.path.join(homePath,version)

    jdkPath = os.path.join(pathOfDownload,"jdk")

        
    if os.path.exists(pathOfDownload): #se a pasta de download existir ela apaga tudo
        shutil.rmtree(pathOfDownload)
    os.makedirs(pathOfDownload, exist_ok=True)

    jdkUrl =  pathControll.getJdkUrl(version)
    ## PARA TAR.GZ
    if get_file_extension(jdkUrl) == '.gz':
        jdkCompactadoPath = os.path.join(jdkPath,"jdk.tar.gz")

        os.makedirs(jdkPath, exist_ok=True)
        jdkRequest = requests.get(jdkUrl)
        
        with open(jdkCompactadoPath, 'wb') as file:
            file.write(jdkRequest.content)
        
        with tarfile.open(jdkCompactadoPath, 'r:gz') as file:
            file.extractall(jdkPath)

    ## PARA .ZIP
    elif get_file_extension(jdkUrl) == '.zip':
        jdkCompactadoPath = os.path.join(jdkPath,"jdk.zip")

        os.makedirs(jdkPath, exist_ok=True)
        jdkRequest = requests.get(jdkUrl)
        
        with open(jdkCompactadoPath, 'wb') as file:
            file.write(jdkRequest.content)

        with zipfile.ZipFile(jdkCompactadoPath, 'r') as file:
            file.extractall(jdkPath)
    
    os.remove(jdkCompactadoPath)

    #Organizar a estrutura de diretórios removendo a  subpasta jdk-24.0.1
    # O JDK geralmente é extraído em uma subpasta (ex: 'jdk-24.0.1')
    jdk_contents = os.listdir(jdkPath)
    if len(jdk_contents) == 1:  # Se houver apenas 1 item na pasta
        subdir = os.path.join(jdkPath, jdk_contents[0])
        if os.path.isdir(subdir):  # E esse item for uma pasta
            # Move todos os arquivos para o diretório principal
            for item in os.listdir(subdir):
                os.rename(
                    os.path.join(subdir, item),
                    os.path.join(jdkPath, item)
                )
            # Remove a subpasta vazia
            os.rmdir(subdir)    




if __name__ == "__main__":
    install(
        "6.5.18"
    )
