from typing import List
import typer

app = typer.Typer()

@app.command()
def hello(
    **args: str 
):
    # Verifica se args é None e substitui por uma lista vazia
    
    print(f"helo {args}")

if __name__ == "__main__":
    app()
