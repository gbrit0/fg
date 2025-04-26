from typing import List
import typer

app = typer.Typer()

@app.command(
         context_settings={"allow_extra_args": True, "ignore_unknown_options": True} #desse jeito ele vai ignorar os -
)
def hello(
    args: List[str] = typer.Argument(None, help="Additional arguments for the application"),
):
    # Verifica se args é None e substitui por uma lista vazia
    
    print(f"{args}")

@app.command(
    context_settings={
        "allow_extra_args": True, "ignore_unknown_options": True
    }
)
def install(
    version: str = typer.Argument(help="versao"),
    jar: str = typer.Option("ola","--jar","-j",help= "nome do jar file"),
    args : list[str] = typer.Argument(None, help="Additional arguments for the application"), #ctx: typer.Context = typer.Context() isso pega todos os argumentos de contexto,
):
    print(f"{version} {jar} {args}") 

if __name__ == "__main__":
    app()
