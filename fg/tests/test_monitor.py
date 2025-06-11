import pytest
import monitor


def test_format_uptime_seconds():
   assert monitor.format_uptime(45) == "45s"
   assert monitor.format_uptime(75) == "1m 15s"
   assert monitor.format_uptime(3700) == "1h 1m 40s"
   assert monitor.format_uptime(90061) == "1d 1h 1m 1s" 