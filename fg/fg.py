import typer
from typing import List
from classes import message

import pathControll
import controller
import manager
import monitor
from fg_gui import fgGui

app = typer.Typer(no_args_is_help=True)

# Definição dos argumentos e seus comentários
versionHelp = typer.Argument(help="Versão do FHIR Guard.")
jar_nameHelp = typer.Argument(help="The name of the jar file")
pidHelp = typer.Argument(help="PID can be obtained from the 'fg status' command.")
tailHelp = typer.Option(None, "--tail", "-t", help="Shows the last n lines of the logs. If not specified, shows all logs.")
followHelp = typer.Option(False, "--follow", "-f", help="Follows the log output in real-time.")

# Opções globais
@app.callback()
def global_options(
    log_level: str = typer.Option(None, "--log-level", "-l", help="Sets the log level for the fg CLI (debug, info, warn, error)."),
    working_directory: str = typer.Option(None, "--dir", "-d", help="Specifies the working directory."),
):
    if log_level:
        typer.echo("Modo detalhado ativado!")
    if working_directory:
        pathControll.set_home_path(working_directory)
        typer.echo(f"Using work directiry as {working_directory}")

# Comandos básicos
@app.command()
def available():
    """Lists all available FHIR Guard versions, regardless of what is installed in the working directory."""

    try:
        resultados = pathControll.available()
        typer.echo("Versão      Data        JDK")
        typer.echo("------      ----------  ---")
        for resultado in resultados:
            typer.echo(f"{resultado["versao"]}      {resultado["data"]}  {resultado["jdkVersao"]}")

    except Exception as e:
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

@app.command()
def gui():
    """Launches the graphical user interface."""
    fgGui.main()

# Gerenciamento de instalação
@app.command()
def install(version: str = versionHelp):
    """Installs a specific version of the FHIR Guard application."""
    try:
        id = 0
        for msg in manager.install(version):
            if(msg["indice"] != id ):
                id = msg["indice"]
                typer.echo()
            else:
                typer.echo(f"\r{msg['nome']}: {msg['porcentagem']:.2f}%", nl=False)

    except Exception as e:
        typer.echo()
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

@app.command()
def update():
    """If a newer version exists, downloads, installs it and sets it as the current default."""
    for msg in manager.update():
        if msg.startswith("\r"):
            typer.echo(msg, nl=False)
        else:
            typer.echo(msg)

@app.command()
def uninstall(version: str = versionHelp):
    """Removes a specific version of the application."""
    if input(f"Confirm uninstallation of version {version}? (y/N)") == 'y':
        for msg in manager.uninstall(version):
            if msg.startswith("\r"):
                typer.echo(msg, nl=False)
            else:
                typer.echo(msg)
    else:
        typer.echo("Desinstalação cancelada!")

@app.command()
def list():
    """Shows all installed versions of the application."""
    typer.echo("Installed versions:")
    for msg in pathControll.list():
        typer.echo(msg)

@app.command()
def config(version: str = versionHelp):
    """Displays (read-only) the detailed configuration for a specific version."""
    typer.echo(
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

# Controle da aplicação
@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def start(
    version: str = versionHelp,
    jar_name: str = jar_nameHelp,
    args: List[str] = typer.Argument(None, help="Additional arguments for the application")
):
    """Starts a specific version of the application (must be installed first)."""
    typer.echo(controller.start(version, jar_name, args))

@app.command()
def stop(pid: int = pidHelp):
    """Stops a running instance of the application."""
    typer.echo(controller.stop(pid))

# Monitoramento e diagnóstico
@app.command()
def status():
    """Shows the current status of all running instances of the application."""
    typer.echo("PID      Version   Port   Uptime   Memory       CPU       Tasks")
    for msg in monitor.status():
        typer.echo(msg)

@app.command()
def logs(pid: int = pidHelp, tail: int = tailHelp, follow: bool = followHelp):
    """Displays the logs for a specific running instance."""
    typer.echo(f"Mostrando os logs do processo: {pid}")
    if follow:
        typer.echo("Mostrando Logs dinamicamente.")
    typer.echo(f"Mostrando {'todos os logs' if tail is None else f'os últimos {tail} logs'}.")

if __name__ == "__main__":
    app()
