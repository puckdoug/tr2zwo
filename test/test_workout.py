import pytest

from tr2zwo.trworkout import Workout

def test_create_empty_workout():
  w = Workout
  assert w is not None
