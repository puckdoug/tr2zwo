import pytest

from tr2zwo.trworkout import WorkoutItem

def test_create_empty_workout_item():
  w = WorkoutItem 
  assert w is not None
