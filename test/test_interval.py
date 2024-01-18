import pytest

from trworkout import Interval

def test_create_empty_empty_interval():
  i = Interval()
  assert i is not None
