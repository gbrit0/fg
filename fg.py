import typer


app = typer.Typer()

@app.command()
def update():
    """Instala a versão mais recente"""
    print("Instalando a versão mais recente")

@app.command()
def start():
    """Inicia a aplicação"""
    print("Iniciando a aplicação")

@app.command()
def status():
    """Mostra o status da aplicação"""
    print("Mostrando status")


if __name__ == "__main__":
    app()