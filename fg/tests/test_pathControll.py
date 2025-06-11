import pytest
import pathControll
from unittest import mock

def test_set_and_get_home_path():
   pathControll.set_home_path("/tmp/test_fg")
   assert pathControll.home_path().endswith("/tmp/test_fg/.fg") or pathControll.home_path().endswith("\\tmp\\test_fg\\.fg")

@mock.patch("os.path.exists", return_value=False)
@mock.patch("pathControll.procurarNovasVersoes")
def test_openJson_calls_procurarNovasVersoes(mock_procurar, mock_exists):
   with pytest.raises(RuntimeError):
      pathControll.openJson()
   assert mock_procurar.called 