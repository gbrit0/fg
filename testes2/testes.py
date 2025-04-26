import typer
import start

app = typer.Typer()



@app.command()
def ola():
    print("ola")

@app.command(
    context_settings={
        "allow_extra_args": True, "ignore_unknown_options": True
    }
)
def install(
    args : list[str] = typer.Argument(None, help="Additional arguments for the application"), #ctx: typer.Context = typer.Context() isso pega todos os argumentos de contexto,
):
    start.start(args)

if __name__ == "__main__":
    app()