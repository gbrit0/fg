import typer
#import argparse

app = typer.Typer()

@app.command()
def update():
    """Instala a versão mais recente"""
    print("Instalando a versão mais recente")

@app.command()
def start(ver:str = "v1"):
    """Inicia a aplicação"""
    print("oi")

@app.command()
def status():
    """Mostra o status da aplicação"""
    print("Mostrando status")
    #outromodulo.status()

@app.command()
def available():
    """Mostra as versões disponivéis"""
    print("v1")
    print("v2")


if __name__ == "__main__":
    app()