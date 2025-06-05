import typer
from typing import List
from classes import message

import pathControll
import controller
import manager
import monitor
from fg_gui import fgGui

app = typer.Typer(no_args_is_help=True) #SE DER ERRO AO MOSTRAR O HELP SEM ARGUMENTOS É POR CONTA DO CLICK 8.2.1, FIZ O DOWNGRADE PRO CLICK 8.1.8 E FUNCIONOU SEM ERROS

# Definição dos argumentos e seus comentários
versionHelp = typer.Argument(help="Versão do FHIR Guard.")
appNameHelp = typer.Argument(help="The name of the aplication")
pidHelp = typer.Argument(help="PID can be obtained from the 'fg status' command.")
tailHelp = typer.Option(None, "--tail", "-t", help="Shows the last n lines of the logs. If not specified, shows all logs.")
followHelp = typer.Option(False, "--follow", "-f", help="Follows the log output in real-time.")

# Opções globais
@app.callback()
def global_options(
    #log_level: str = typer.Option(None, "--log-level", "-l", help="Sets the log level for the fg CLI (debug, info, warn, error)."),
    working_directory: str = typer.Option(None, "--dir", "-d", help="Specifies the working directory."),
):
    #if log_level:
    #    typer.echo("Modo detalhado ativado!")
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
            typer.echo(f"{resultado['versao']}      {resultado['data']}  {resultado['jdkVersao']}")

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
        
        sucesso = f"Versão {version} instalada com sucesso."
        typer.echo(typer.style(sucesso, fg=typer.colors.GREEN, bold=True))

    except Exception as e:
        typer.echo()

        erro = f"Falha ao instalar versão {version}: {e}"
        typer.echo(typer.style(erro, fg=typer.colors.RED, bold=True))

@app.command()
def update():
    """If a newer version exists, downloads, installs it and sets it as the current default."""
    try:
        id = 0
        for msg in manager.update():
            if(msg["indice"] != id ):
                id = msg["indice"]
                typer.echo()
            else:
                typer.echo(f"\r{msg['nome']}: {msg['porcentagem']:.2f}%", nl=False)

    except Exception as e:
        typer.echo()
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

@app.command()
def uninstall(version: str = versionHelp):
    """Removes a specific version of the application."""
    if input(f"Confirm uninstallation of version {version}? (y/N)") == 'y':
        try:
            msg = manager.uninstall(version)    
            typer.echo(msg)
        
        except Exception as e:
            typer.echo()
            typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

    else:
        typer.echo("Desinstalação cancelada!")

@app.command()
def set_default(version: str = versionHelp):
    """Define a versão padrão do FHIR GUARD."""
    try:
        msg = manager.set_default_version(version)
        typer.echo(typer.style(msg, fg=typer.colors.GREEN, bold=True))
    except Exception as e:
        typer.echo(typer.style(str(e), fg=typer.colors.RED, bold=True))

@app.command()
def list():
    """Shows all installed versions of the application."""

    try:
        versoes = pathControll.list()
        typer.echo("Installed versions:")
        
        for versao in versoes:
            if(versao["default"]):
                typer.echo(f"* {versao['nome']} (padrão - mais recente)")
            else:
                typer.echo(f"  {versao['nome']}")

    except Exception as e:
            typer.echo()
            typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))
        


# Controle da aplicação
@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def start(
    version: str = versionHelp,
    app_name: str = appNameHelp,
    #args: List[str] = typer.Argument(None, help="Additional arguments for the application")
):
    """Starts a specific version of the application (must be installed first)."""
    try:
        typer.echo(f"Aplicação iniciada com sucesso. PID: {controller.start(version, app_name)}")
    except Exception as e:
        typer.echo()
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

@app.command()
def stop(pid: int = pidHelp):
    """Stops a running instance of the application."""
    try:
        controller.stop(pid)
        typer.echo(f"Instância da aplicação (PID: {pid}) parada com sucesso")
    except Exception as e:
        typer.echo()
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

    

# Monitoramento e diagnóstico
@app.command()
def status():
    """Shows the current status of all running instances of the application."""

    try:
        processos = monitor.status()
        typer.echo("PID      Version   Port   Uptime   Memory       CPU       Tasks")
        for processo in processos:
            typer.echo(f"{processo['PID']}    {processo['Version']}    {processo['Port']}   {processo['Uptime']}       {processo['Memory']}    {processo['CPU']}    {processo['Tasks']}")
    except Exception as e:
        typer.echo()
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

@app.command()
def logs(version: str = versionHelp, app_name: str = appNameHelp, tail: int = tailHelp, follow: bool = followHelp):
    """Displays the logs for a specific running instance."""
    
    try:
        for linha in monitor.logs(app_name, version, tail, follow):
            typer.echo(linha)
    except Exception as e:
        typer.echo()
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

if __name__ == "__main__":
    app()
