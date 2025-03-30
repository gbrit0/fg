from interfaces.command import Command

class GUICommand(Command):
   """
   Lança a interface gráfica do aplicativo (GUI).

   A GUI fornece acesso a todas as funcionalidades do fg por meio de uma interface gráfica interativa.

   Sucesso (em verde): "GUI iniciada com sucesso."
   Erro (em vermelho): "Erro ao iniciar a GUI: [erro]".
   """

   def execute(self):
      print("Iniciando a GUI...")
      # Lógica para iniciar a GUI do aplicativo...