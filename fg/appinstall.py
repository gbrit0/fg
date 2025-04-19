

import platform
import requests
import tarfile
import zipfile
import os

import pathControll


FG_HOME = pathControll.home_path()

def install_jdk():
    system = platform.system()
    if system == "Windows":
        return installJdkWindows()
    elif system == "Linux":
        return installJdkLinux()
    elif system == "Darwin":
        return installJdkMac()
    else:
        return "Sistema operacional não suportado."


def installJdkMac():
    jdk_url = "https://download.java.net/java/GA/jdk24/1f9ff9062db4449d8ca828c504ffae90/36/GPL/openjdk-24_macos-x64_bin.tar.gz"

    jdk_archive_path = os.path.join(FG_HOME, "jdk.tar.gz") #arquivo compactado .zip
    jdk_install_dir = os.path.join(FG_HOME,"jdk") #path onde eu vou descompactar o jdk

    os.makedirs(FG_HOME, exist_ok= True)

    if not os.path.exists(jdk_archive_path):
        jdk = requests.get(jdk_url, allow_redirects=True)

        if(jdk.status_code != 200): 
            return f"Falha no download do JDK. Status: {jdk.status_code}"

        with open(jdk_archive_path, 'wb') as arquivo:
            arquivo.write(jdk.content)

        try: 
            #descompactando
            with tarfile.open(jdk_archive_path,"r:gz") as arquivo:
                arquivo.extractall(jdk_install_dir)


           
            jdk_contents = os.listdir(jdk_install_dir)
            if len(jdk_contents) == 1:  # Se houver apenas 1 item na pasta
                subdir = os.path.join(jdk_install_dir, jdk_contents[0])
                if os.path.isdir(subdir):  # E esse item for uma pasta
                    # Move todos os arquivos para o diretório principal
                    for item in os.listdir(subdir):
                        os.rename(
                            os.path.join(subdir, item),
                            os.path.join(jdk_install_dir, item)
                        )
                    # Remove a subpasta vazia
                    os.rmdir(subdir)

            return f"JDK descompactado em: {jdk_install_dir}"
            
        except Exception as e:
            return f"Erro ao descompactar: {str(e)}"
        
def installJdkWindows():
    jdk_url = "https://download.java.net/java/GA/jdk24/1f9ff9062db4449d8ca828c504ffae90/36/GPL/openjdk-24_windows-x64_bin.zip"

    jdk_archive_path = os.path.join(FG_HOME, "jdk.zip") #arquivo compactado .zip
    jdk_install_dir = os.path.join(FG_HOME,"jdk") #path onde eu vou descompactar o jdk

    os.makedirs(FG_HOME, exist_ok= True)
    #instalando o arquivo .zip
    if not os.path.exists(jdk_archive_path):
        jdk = requests.get(jdk_url, allow_redirects=True)
        if jdk.status_code != 200: #retorna erro se a requisição der errado
            return f"Falha no download do JDK. Status: {jdk.status_code}"

        with open(jdk_archive_path, 'wb') as arquivo:
            arquivo.write(jdk.content)
    #dencompactando o .zip
    try:
        with zipfile.ZipFile(jdk_archive_path, 'r') as zip_ref:
            zip_ref.extractall(jdk_install_dir)

        # Organizar a estrutura de diretórios (o JDK geralmente vem em uma subpasta)
        jdk_contents = os.listdir(jdk_install_dir)
        if len(jdk_contents) == 1:  # Se houver apenas 1 item na pasta
            subdir = os.path.join(jdk_install_dir, jdk_contents[0])
            if os.path.isdir(subdir):  # E esse item for uma pasta
                # Move todos os arquivos para o diretório principal
                for item in os.listdir(subdir):
                    os.rename(
                        os.path.join(subdir, item),
                        os.path.join(jdk_install_dir, item)
                    )
                # Remove a subpasta vazia
                os.rmdir(subdir)

        return f"JDK descompactado em: {jdk_install_dir}"
    
    except Exception as e:
        return f"Erro ao descompactar: {str(e)}"


def installJdkLinux():
    jdk_url = "https://download.java.net/java/GA/jdk24/1f9ff9062db4449d8ca828c504ffae90/36/GPL/openjdk-24_linux-x64_bin.tar.gz"

    jdk_archive_path = os.path.join(FG_HOME, "jdk.tar.gz")  # Arquivo compactado
    jdk_install_dir = os.path.join(FG_HOME, "jdk")          # Pasta de instalação final

    #Criar diretório se não existir
    os.makedirs(FG_HOME, exist_ok=True)

    #Baixar o JDK (se já não existir)
    if not os.path.exists(jdk_archive_path):
        jdk = requests.get(jdk_url, allow_redirects=True)
        if jdk.status_code != 200:
            return f"Falha no download do JDK. Status: {jdk.status_code}"
        
        with open(jdk_archive_path, 'wb') as arquivo: #instala o jdk no destino selecionado
            arquivo.write(jdk.content)
    #tentanr descompactar o arquivo 
    try:
        # Abre o arquivo .tar.gz como um arquivo tar
        with tarfile.open(jdk_archive_path, "r:gz") as tar:
            # Extrai tudo para o diretório de instalação
            tar.extractall(path=jdk_install_dir)
        
        #Organizar a estrutura de diretórios removendo a  subpasta jdk-24.0.1
        # O JDK geralmente é extraído em uma subpasta (ex: 'jdk-24.0.1')
        jdk_contents = os.listdir(jdk_install_dir)
        if len(jdk_contents) == 1:  # Se houver apenas 1 item na pasta
            subdir = os.path.join(jdk_install_dir, jdk_contents[0])
            if os.path.isdir(subdir):  # E esse item for uma pasta
                # Move todos os arquivos para o diretório principal
                for item in os.listdir(subdir):
                    os.rename(
                        os.path.join(subdir, item),
                        os.path.join(jdk_install_dir, item)
                    )
                # Remove a subpasta vazia
                os.rmdir(subdir)

        return f"JDK descompactado em: {jdk_install_dir}"

    except Exception as e:
        return f"Erro ao descompactar: {str(e)}"

def install():
    return_code = ""

    arquivo_validator = os.path.join(FG_HOME, "validator_cli.jar")
    os.makedirs(FG_HOME, exist_ok=True) # cria o diretorio se ele nao existir, se existir ele so ignora
    # Faz o download do arquivo
    
    validator_url = "https://github.com/hapifhir/org.hl7.fhir.core/releases/latest/download/validator_cli.jar"
    validator = requests.get(validator_url, allow_redirects=True)
    
    if validator.status_code == 200 and not os.path.exists(arquivo_validator):
        with open(arquivo_validator, 'wb') as arquivo:
            arquivo.write(validator.content)
        return_code = f"Arquivo baixado no destino {arquivo_validator}\n"
    else:
        return_code = f"Falha no download. Código de status: {validator.status_code}\n"


    return return_code + install_jdk()
    