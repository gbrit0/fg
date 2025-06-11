import pytest
import controller
from unittest import mock

@mock.patch("os.path.exists", return_value=True)
def test_montarComando_windows(mock_exists):
   with mock.patch("platform.system", return_value="Windows"):
      cmd = controller.montarComando("-jar app.jar", "1.0.0", "app")
      assert any("java.exe" in c or "java" in c for c in cmd)

@mock.patch("os.path.exists", return_value=False)
def test_montarComando_java_not_found(mock_exists):
   with pytest.raises(FileNotFoundError):
      controller.montarComando("-jar app.jar", "1.0.0", "app") 