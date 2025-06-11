from classes.versoes import Registro
from datetime import date

def test_registro():
   r = Registro(versao="1.0.0", data=date(2024, 6, 11), valor=42)
   assert r.versao == "1.0.0"
   assert r.data == date(2024, 6, 11)
   assert r.valor == 42 