import pytest
from classes.message import Message, Status

def test_message_ok():
   msg = Message(status=Status.OK, mensagem="Sucesso", dado=[1, 2, 3])
   assert msg.status == Status.OK
   assert msg.mensagem == "Sucesso"
   assert msg.dado == [1, 2, 3]

def test_message_erro():
   msg = Message(status=Status.ERRO, mensagem="Erro", dado=None)
   assert msg.status == Status.ERRO
   assert msg.mensagem == "Erro"
   assert msg.dado is None 