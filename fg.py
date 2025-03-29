import typer

#INTRUÇOES DE TESTE
#INSTALAR A BIBLIOTECA typer
#USAR O COMANDO pyhton fg.py --help PARA LISTAR OS COMANDOS POSSÍVEIS
#USAR O COMANDO python fg.py [command] PARA EXECURAR UM COMANDO LISTADO EX: python fg.py start
#USAR O COMANDO python fg.py [command] --help PARA MOSTRAR A LISTA DE ARGUMENTOS E OPÇÕES EX: python fg.py start --help

app = typer.Typer()

versionHelp = typer.Option("last","-v","--version", help= "Versão do FHIR Guard.")
pidHelp = typer.Argument(help = "PID can be obtained from the 'fg status' command.")
tailHelp = typer.Option(None, "--tail", "-t", help="Shows the last n lines of the logs. If not specified, shows all logs.")
followHelp = typer.Option(False, "--follow", "-f", help="Follows the log output in real-time.")

#COMANDOS 

#Basic commands

@app.command()
def available():
    """Lists all available FHIR Guard versions, regardless of what is installed in the working directory."""

    print(
"""Version     Release Date
--------    ------------
2.0.0       2024-04-05
1.2.0       2024-03-10
1.1.0       2024-02-22
1.0.0       2024-01-15"""
)

@app.command()
def gui():
    """Launches the graphical user interface."""
    print("Graphical interface started successfully.")

#Installation management
@app.command()
def install(version: str = versionHelp):
    """Installs a specific version of the FHIR Guard application."""
    print(f"Instalando a versão {version}")

@app.command()
def update():
    """If a newer version exists, downloads, installs it and sets it as the current default."""
    print("Updated to version [new version]. This is now the default version.")

@app.command()
def uninstall(version: str = versionHelp):
    """Removes a specific version of the application."""
    
    if input("Confirm uninstallation of version [version]? (y/N)") == 'y':
        print(f"Version {version} uninstalled successfully")


@app.command()
def list():
    """Shows all installed versions of the application."""
    print(
"""Installed versions:
* 1.1.0 (default - most recent)
  1.0.0
  0.9.0"""
  )
    
@app.command()
def config(version: str = versionHelp):
    """Displays (read-only) the detailed configuration for a specific version."""
    print(
        f"""Configuration for version {version}:
Source file: /home/user/.fg/versions/{version}/config.yaml

Current settings (read-only):
Server:
  - Host: 0.0.0.0
  - Port: 8080
  - Read Timeout: 30s
  - Write Timeout: 30s

Security:
  - TLS: enabled
  - Auth: enabled
  - JWT Expiry: 24h

Resources:
  - Max Memory: 1024MB
  - Max CPU: 2
  - Workers: 10

[...]

To modify these settings, edit the YAML file directly.
See Configuration Reference for all available options."""
    )

#Application control

@app.command()
def start(version: str = versionHelp):
    """Starts a specific version of the application (must be installed first)."""
    print("Application started successfully. PID: 1234")

@app.command()
def stop(pid:int = pidHelp):
    """Stops a running instance of the application."""
    print(f"Application instance (PID: {pid}) stopped successfully")


#Monitoring and diagnostics

@app.command()
def status():
    """Shows the current status of all running instances of the application."""
    print(
"""PID     Version  Port   Uptime   Memory   CPU   Tasks
1234    1.1.0    8080   2h       256MB    2%    10
5678    1.0.0    8081   30m      128MB    1%    5"""
        )
    

@app.command()
def logs(pid:int = pidHelp, tail:int = tailHelp, follow = followHelp):
    """Displays the logs for a specific running instance."""
    print(f"Mostrando os logs do processo: {pid}")
    if follow:
        print("Mostrando Logs dinamicamente.")

    print(f"Mostrando {'todos os logs' if tail is None else f'os últimos {tail} logs'}.")



if __name__ == "__main__":
    app()