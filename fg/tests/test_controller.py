import pytest
import controller
from unittest import mock
import signal
import os
import sys
import types
import platform

if not hasattr(os, "setsid"):
    os.setsid = lambda: None  # mock simples

if not hasattr(os, "killpg"):
    os.killpg = lambda pgid, sig: None  # mock simples

if not hasattr(os, "getpgid"):
    os.getpgid = lambda pid: pid  # mock simples, retorna o próprio pid

@mock.patch("os.path.exists", return_value=True)
def test_montarComando_windows(mock_exists):
   with mock.patch("platform.system", return_value="Windows"):
      cmd = controller.montarComando("-jar app.jar", "1.0.0", "app")
      assert any("java.exe" in c or "java" in c for c in cmd)

@mock.patch("os.path.exists", return_value=False)
def test_montarComando_java_not_found(mock_exists):
   with pytest.raises(FileNotFoundError):
      controller.montarComando("-jar app.jar", "1.0.0", "app") 


# Teste: erro quando o JAR não é encontrado
@mock.patch("os.path.exists", side_effect=[True, False])  # java existe, jar não
def test_montarComando_jar_not_found(mock_exists):
   with pytest.raises(FileNotFoundError) as exc:
      controller.montarComando("-jar app.jar", "1.0.0", "app")
   assert "Jar file not found" in str(exc.value)


# Teste: sucesso no start em ambiente Linux
@mock.patch("controller.system", "Linux")
@mock.patch("controller.pathControll.getVersion")
@mock.patch("controller.montarComando")
@mock.patch("controller.subprocess.Popen")
@mock.patch("controller.monitor.save_pid")
def test_start_linux_success(mock_save_pid, mock_popen, mock_montar, mock_getVersion):
   mock_getVersion.return_value = {
      'apps': [{'nome': 'app', 'comando': '-jar app.jar'}]
   }
   mock_montar.return_value = ['/path/to/java', '-jar', '/path/to/app.jar']

   process_mock = mock.Mock()
   process_mock.pid = 12345
   mock_popen.return_value = process_mock

   pid = controller.start("1.0.0", "app")
   assert pid == 12345
   mock_save_pid.assert_called_once()


# Teste: erro quando versão não possui chave 'apps'
@mock.patch("controller.pathControll.getVersion", return_value={})
def test_start_missing_apps_key(mock_getVersion):
   with pytest.raises(KeyError) as exc:
      controller.start("1.0.0", "app")
   assert "Missing key" in str(exc.value)


# Teste: erro quando app não está na lista
@mock.patch("controller.pathControll.getVersion", return_value={'apps': []})
def test_start_app_not_found(mock_getVersion):
   with pytest.raises(RuntimeError) as exc:
      controller.start("1.0.0", "app")
   assert "Jar 'app' not found" in str(exc.value)

# Teste: erro de ao iniciar subprocesso
@mock.patch("controller.pathControll.getVersion", return_value={
    'apps': [{'nome': 'app', 'comando': '-jar app.jar'}]
})
@mock.patch("controller.montarComando", return_value=['java', '-jar', 'app.jar'])
@mock.patch("controller.subprocess.Popen", side_effect=Exception("Erro"))
def test_start_subprocess_exception(mock_popen, mock_montar, mock_getVersion):
   with pytest.raises(RuntimeError) as exc:
      controller.start("1.0.0", "app")
   assert "Unexpected error while starting application" in str(exc.value)


# Teste: parada bem-sucedida no Windows
@mock.patch("controller.system", "Windows")
@mock.patch("controller.subprocess.run")
def test_stop_windows_success(mock_run):
   result = controller.stop(12345)
   assert "stopped successfully" in result
   mock_run.assert_called_once()


# Teste: parada bem-sucedida no Linux
@pytest.mark.skipif(platform.system() == "Windows", reason="Só roda em Linux")
@mock.patch("os.getpgid", return_value=12345)
@mock.patch("os.killpg")
def test_stop_linux_success(mock_killpg, mock_getpgid):
   result = controller.stop(12345)
   assert "stopped successfully" in result
   mock_killpg.assert_called_once_with(12345, signal.SIGTERM)


# Teste: erro de permissão ao parar processo
@mock.patch("controller.system", "Linux")
@mock.patch("os.getpgid", return_value=12345)
@mock.patch("os.killpg", side_effect=PermissionError)
def test_stop_permission_error(mock_killpg, mock_getpgid):
   with pytest.raises(PermissionError):
      controller.stop(12345)

# Teste: PID inválido
def test_stop_invalid_pid():
   with pytest.raises(ValueError):
      controller.stop(-1)

