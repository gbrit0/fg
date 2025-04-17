import tkinter as tk
from tkinter import messagebox
import appinstall

def instalar():
    resultado = appinstall.install()
    messagebox.showinfo("Instalação", resultado)

def main():
    janela = tk.Tk()
    janela.title("FHIR Guard GUI")

    btn_instalar = tk.Button(janela, text="Instalar FHIR Guard", command=instalar)
    btn_instalar.pack(pady=20)

    janela.mainloop()

# Protege a execução automática ao importar:
if __name__ == "__main__":
    main()
