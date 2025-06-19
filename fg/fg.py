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
versionOptionHelp = typer.Option(manager.get_default_version, "--version", "-v", help="Versão do FHIR Guard (se não for especificada, usa a versão padrão).")
appNameHelp = typer.Argument(help="Nome da aplicação.")
pidHelp = typer.Argument(help="PID pode ser obtido com o comando 'fg status'.")
tailHelp = typer.Option(None, "--tail", "-t", help="Mostra as últimas N linhas dos logs. Se não for especificado, mostra todo o log.")
followHelp = typer.Option(False, "--follow", "-f", help="Acompanha a saída dos logs em tempo real.")

# Opções globais
@app.callback()
def global_options(
    #log_level: str = typer.Option(None, "--log-level", "-l", help="Sets the log level for the fg CLI (debug, info, warn, error)."),
    working_directory: str = typer.Option(None, "--dir", "-d", help="Especifica o diretório de trabalho."),
):
    #if log_level:
    #    typer.echo("Modo detalhado ativado!")
    if working_directory:
        pathControll.set_home_path(working_directory)
        typer.echo(f"Usando o diretório de trabalho como {working_directory}")

# Comandos básicos
@app.command()
def available():
    """Lista todas as versões disponíveis do FHIR Guard, independentemente do que estiver instalado no diretório de trabalho."""

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
    """Inicia a interface gráfica do usuário."""
    fgGui.main()

# Gerenciamento de instalação
@app.command()
def install(version: str = versionHelp):
    """Instala uma versão específica do aplicativo FHIR Guard."""
    try:
        id = 0
        for msg in manager.install(version):
            if(msg["indice"] != id ):
                id = msg["indice"]
                typer.echo()
            else:
                typer.echo(f"\r{msg['nome']}: {msg['porcentagem']:.2f}%", nl=False)
        
        sucesso = f"\nVersão {version} instalada com sucesso."
        typer.echo(typer.style(sucesso, fg=typer.colors.GREEN, bold=True))

    except Exception as e:
        typer.echo()

        erro = f"Falha ao instalar versão {version}: {e}"
        typer.echo(typer.style(erro, fg=typer.colors.RED, bold=True))

@app.command()
def update():
    """Se houver uma versão mais nova, baixa e instala-a e define-a como a versão padrão atual."""
    try:
        versaoAtual = pathControll.mostRecentInstalledVersion()
        if pathControll.mostRecentVersion() == versaoAtual:
            id = 0
            for msg in manager.update():
                if(msg["indice"] != id ):
                    id = msg["indice"]
                    typer.echo()
                else:
                    typer.echo(f"\r{msg['nome']}: {msg['porcentagem']:.2f}%", nl=False)

            sucesso = f"\nAtualizado para versão {pathControll.mostRecentVersion()}. Esta é agora a versão padrão."
            typer.echo(typer.style(sucesso, fg=typer.colors.GREEN, bold=True))
        else:
            typer.echo(f"Nenhuma versão mais recente disponível. Você tem disponível a versão mais recente: {versaoAtual}.")

    except Exception as e:
        typer.echo()
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

@app.command()
def uninstall(version: str = versionHelp):
    """Remove uma versão específica do aplicativo."""
    if input(f"Confirma a remoção da versão {version}? (s/N)") == 's':
        try:
            msg = manager.uninstall(version)    
            typer.echo(typer.style(msg, fg=typer.colors.GREEN, bold=True))
        
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
    """Exibe todas as versões instaladas do aplicativo."""

    try:
        versoes = pathControll.list()
        typer.echo("Versões instaladas:")
        
        for versao in versoes:
            if(versao["default"]):
                typer.echo(f"* {versao['nome']} (padrão)")
            else:
                typer.echo(f"  {versao['nome']}")

    except Exception as e:
            typer.echo()
            typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))
        


# Controle da aplicação
#@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
@app.command()
def start(
    version: str = versionOptionHelp,
    app_name: str = appNameHelp,
    #args: List[str] = typer.Argument(None, help="Additional arguments for the application")
):
    """Inicia uma versão específica do aplicativo (deve ser instalada primeiro)."""
    try:
        msg = f"Aplicação iniciada com sucesso. PID: {controller.start(version, app_name)}"
        typer.echo(typer.style(msg, fg=typer.colors.GREEN, bold=True))
    except Exception as e:
        typer.echo()
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

@app.command()
def stop(pid: int = pidHelp):
    """Para uma instância em execução do aplicativo."""
    try:
        controller.stop(pid)
        msg = f"Instância da aplicação (PID: {pid}) parada com sucesso"
        typer.echo(typer.style(msg, fg=typer.colors.GREEN, bold=True))
    except Exception as e:
        typer.echo()
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

    

# Monitoramento e diagnóstico
@app.command()
def status():
    """Exibe o status atual de todas as instâncias em execução do aplicativo."""

    try:
        processos = monitor.status()

        # Define os nomes das colunas
        colunas = ["PID", "Versão", "Porta", "Tempo de execução", "Memória", "CPU", "Tarefas"]

        # Junta cabeçalho e dados para calcular larguras
        dados = [
            [str(processo['PID']),
            str(processo['Version']),
            str(processo['Port']),
            str(processo['Uptime']),
            str(processo['Memory']),
            str(processo['CPU']),
            str(processo['Tasks'])]
            for processo in processos
        ]

        # Inclui o cabeçalho para calcular o tamanho máximo de cada coluna
        dados_com_cabecalho = [colunas] + dados

        # Calcula a largura de cada coluna
        larguras = [max(len(str(linha[i])) for linha in dados_com_cabecalho) for i in range(len(colunas))]

        # Função para formatar uma linha
        def formatar_linha(linha):
            return "  ".join(f"{texto:<{larguras[i]}}" for i, texto in enumerate(linha))

        # Imprime cabeçalho
        typer.echo(formatar_linha(colunas))

        # Imprime os dados
        for linha in dados:
            typer.echo(formatar_linha(linha))

    except Exception as e:
        typer.echo()
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

@app.command()
def logs(version: str = versionOptionHelp, 
         app_name: str = appNameHelp, 
         tail: int = tailHelp, 
         follow: bool = followHelp
         ):
    """Exibe os logs de uma instância em execução específica."""
    
    try:
        for linha in monitor.logs(app_name, version, tail, follow):
            typer.echo(linha)
    except Exception as e:
        typer.echo()
        typer.echo(typer.style(e, fg=typer.colors.RED, bold=True))

if __name__ == "__main__":
    app()
