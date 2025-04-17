import tkinter as tk
from tkinter import messagebox
import appinstall

def instalar():
    resultado = appinstall.install()
    messagebox.showinfo("Instalação", resultado)

janela = tk.Tk()
janela.title("FHIR Guard GUI")

btn_instalar = tk.Button(janela, text="Instalar FHIR Guard", command=instalar)
btn_instalar.pack(pady=20)

janela.mainloop()
