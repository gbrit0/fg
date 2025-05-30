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
    
    typer.echo(typer.style("Mensagem vermelha!", fg=typer.colors.RED, bold=True))
    typer.echo("ola")


if __name__ == "__main__":
    app()
