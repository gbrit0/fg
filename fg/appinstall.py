
import subprocess
import platform
import requests
import tarfile
import zipfile
import os


FG_HOME = "fg/validator"

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
    
    

def start_validator(fhir_file_to_validate=None): #se o usuario quiser passar um arquivo pra validar por exemplo, se none so inicia o validator
    """
    Inicia o validator FHIR CLI.
    
    Args:
        fhir_file_to_validate (str, optional): Caminho para um arquivo FHIR para validação.
                                              Se None, apenas inicia o validator.
    
    Returns:
        str: Resultado da execução ou mensagem de erro.
    """
    jar_path = os.path.join(FG_HOME, "validator_cli.jar") #caminho do validator_cli.jar
    jdk_path = os.path.join(FG_HOME, "jdk") #caminho do jdk
    java_bin = os.path.join(jdk_path, "bin", "java") #caminho do java 
    
    # Verifica se o arquivo JAR existe
    if not os.path.exists(jar_path):
        return "Erro: validator_cli.jar não encontrado. Execute install() primeiro."
    
    #verifica se o jdk esta instalado
    if not os.path.exists(java_bin):
        return "Erro: JDK não encontrado. Execute install() primeiro."

    try:
        # Comando base para executar o JAR
        cmd = [java_bin, '-jar', jar_path]
        
        # Se um arquivo FHIR foi especificado, adiciona ao comando
        if fhir_file_to_validate:
            if not os.path.exists(fhir_file_to_validate):
                return f"Erro: Arquivo FHIR não encontrado: {fhir_file_to_validate}"
            cmd.append(fhir_file_to_validate)

        # Configura o ambiente para incluir o JDK instalado
        env = os.environ.copy()
        env["JAVA_HOME"] = jdk_path
        env["PATH"] = f"{os.path.join(jdk_path, 'bin')}:{env.get('PATH', '')}"
        
        # Executa o comando
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            env=env
        )
        
        return result.stdout
    
    except subprocess.CalledProcessError as e:
        return f"Erro ao executar o validator: {e.stderr}"
    except Exception as e:
        return f"Erro inesperado: {str(e)}"