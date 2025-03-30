from abc import ABC, abstractmethod

class Command(ABC):
   """
   
   """
   @abstractmethod
   def execute(self):
      """
      Executa o comando com os argumentos fornecidos.
      """
      pass