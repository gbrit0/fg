from abc import ABC, abstractmethod

class CommandInterface(ABC):
   """
   
   """
   @abstractmethod
   def execute(self, *args, **kwargs):
      """
      Executa o comando com os argumentos fornecidos.
      """
      pass