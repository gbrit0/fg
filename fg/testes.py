from typing import List
import typer
import os

nome = "fg/dependencias/config.log"
with open(nome, 'r') as file:
    for linha in file.readlines():
        print(linha)