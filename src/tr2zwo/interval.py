import msgspec
from typing import List, Dict
from tr2zwo.workoutitem import WorkoutItem


# ------------------------------------------------------------------------------
class Interval(msgspec.Struct):
  verbose: bool = False
  raw: Dict = {}
  start: int = 0
  end: int = 0
  name: str = ''
  power: float = 0.0
  power_max: float = 0.0
  power_max_when: int = 0
  power_min: float = -1.0
  power_min_when: int = 0
  ramp_direction: str = ''
  is_fake: bool = False
  test_interval: bool = False
  item: List[WorkoutItem] = []
  interval_type: str = ''
  xml: str = ''

  # ------------------------------------------------------------------------------
  @classmethod
  def create(cls, **kwargs):
    instance = Interval()
    if 'raw' in kwargs:
      instance.raw = kwargs['raw']
      instance.start = instance.raw['Start']
      instance.end = instance.raw['End']
      instance.name = instance.raw['Name']
      instance.is_fake = instance.raw['IsFake']
      instance.test_interval = instance.raw['TestInterval']
      instance.power = instance.raw['StartTargetPowerPercent']
    return instance

  # ------------------------------------------------------------------------------
  def include(self, workout_item):
    if (
      self.start <= workout_item.seconds / 1000
      and self.end > workout_item.seconds / 1000
    ):
      self.item.append(workout_item)

  # ------------------------------------------------------------------------------
  def assign_workout_items(self, workout_items):
    for w in workout_items:
      self.include(w)
    self.find_type()
    self.to_xml()

  # ------------------------------------------------------------------------------
  def ramp_analysis(self):
    for w in self.item:
      if self.power_max < w.ftp:
        self.power_max = w.ftp
        self.power_max_when = int(w.seconds / 1000)
      if self.power_min > w.ftp or self.power_min < 0:
        self.power_min = w.ftp
        self.power_min_when = int(w.seconds / 1000)
    if self.power_min_when < self.power_max_when:
      self.ramp_direction = 'up'
    else:
      self.ramp_direction = 'down'

  # ------------------------------------------------------------------------------
  def find_type(self):
    if self.item[0].ftp == self.item[-1].ftp:
      self.interval_type = 'SteadyState'
    else:
      self.interval_type = 'Ramp'
      self.ramp_analysis()

  # ------------------------------------------------------------------------------
  def to_xml(self):
    match self.interval_type:
      case 'SteadyState':
        self.xml = (
          f'<SteadyState Duration="{self.end - self.start}"'
          + f' Power="{self.power / 100}"></SteadyState>'
        )
      case 'Ramp':
        if self.ramp_direction == 'up':
          self.xml = (
            f'<Ramp Duration="{self.end - self.start}"'
            + f' PowerLow="{self.power_min / 100}"'
            + f' PowerHigh="{float(round(self.power_max) / 100)}">'
            + '</Ramp>'
          )
        else:
          self.xml = (
            f'<Ramp Duration="{self.end - self.start}"'
            + f' PowerLow="{self.power_max / 100}"'
            + f' PowerHigh="{float(round(self.power_min) / 100)}">'
            + '</Ramp>'
          )
      case _:
        self.xml = '<unknown></unknown>'
