import subprocess
import os

def start(
    args: list[str]
):
    jar_path = r"C:\Users\genov\OneDrive\Documentos\Tarefas Moisés\Constrção\fg\fg\validator\validator_cli.jar"
    jdk_path = r"C:\Users\genov\OneDrive\Documentos\Tarefas Moisés\Constrção\fg\fg\validator\jdk"
    java_bin = os.path.join(jdk_path, "bin", "java")

    cmd = [java_bin, "-jar", jar_path]
    
    if args != None:
        cmd += args

     # Define o ambiente com JAVA_HOME e PATH usando o JDK fornecido
    env = os.environ.copy()
    env["JAVA_HOME"] = jdk_path
    env["PATH"] = os.path.join(jdk_path, "bin") + os.pathsep + env["PATH"]

    # Executa o comando
    subprocess.run(cmd, env=env)
    