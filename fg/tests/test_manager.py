import pytest
import manager


def test_get_file_extension():
   assert manager.get_file_extension("http://exemplo.com/arquivo.zip") == ".zip"
   assert manager.get_file_extension("http://exemplo.com/arquivo.tar.gz") == ".gz"
   assert manager.get_file_extension("http://exemplo.com/arquivo.txt?param=1") == ".txt" 