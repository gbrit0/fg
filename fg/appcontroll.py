
import platform
import subprocess
import os

import pathControll

FG_HOME = pathControll.home_path()


def windowsCommand(jdk_path:str):
    return linuxMacCommand(jdk_path) + ".exe"

def linuxMacCommand(jdk_path:str):
    return os.path.join(jdk_path, "bin", "java")

def osCommand(jdk_path:str):
    system = platform.system()
    if system == "Windows":
        return windowsCommand(jdk_path)
    elif system == "Linux":
        return linuxMacCommand(jdk_path)
    elif system == "Darwin":
        return linuxMacCommand(jdk_path)
    else:
        return "Sistema operacional não suportado."



def start(
        version: str,
        jar_name:str,
        fhir_file_to_validate=None
        ): #se o usuario quiser passar um arquivo pra validar por exemplo, se none so inicia o validator
    """
    Inicia o validator FHIR CLI.
    
    Args:
        fhir_file_to_validate (str, optional): Caminho para um arquivo FHIR para validação.
                                              Se None, apenas inicia o validator.
    
    Returns:
        str: Resultado da execução ou mensagem de erro.
    """
    jar_path = os.path.join(FG_HOME, "validator_cli.jar") #caminho do validator_cli.jar
    jdk_path = pathControll.jdk_path() #caminho do jdk
    java_bin = osCommand(jdk_path) #caminho do java 
    
    # Verifica se o arquivo JAR existe
    if not os.path.exists(jar_path):
        return "Erro: validator_cli.jar não encontrado. Execute fg install primeiro."
    
    #verifica se o jdk esta instalado
    if not os.path.exists(java_bin):
        return "Erro: JDK não encontrado. Execute fg install primeiro."

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
        env["PATH"] = f"{os.path.join(jdk_path, 'bin')}:{env.get('PATH', '')}" #pode ser que de erro no windows, se der trocar o : por um ;
        
        # Executa o comando
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            env=env,
            shell= False# funcionou como false no windows, como True dava erro de que o comando fg nao estava definido, algo assim
        )
        
        return result.stdout
    
    except subprocess.CalledProcessError as e:
        return f"Erro ao executar o validator: {e.stderr}"
    except Exception as e:
        return f"Erro inesperado: {str(e)}"
    
