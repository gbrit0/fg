from interfaces.command import Command

class CommandInvoker:
   def __init__(self):
         self.commands = {}

   def register_command(self, name: str, command: Command):
      self.commands[name] = command

   def execute_command(self, name: str):
      command = self.commands.get(name)
      if command:
         command.execute()
      else:
         print(f"Comando '{name}' não reconhecido.")