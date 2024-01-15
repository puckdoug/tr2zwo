#!/usr/local/bin/python3
import IPython
import ujson
import pprint
from typing import List, Dict
import msgspec

#------------------------------------------------------------------------------
class WorkoutItem(msgspec.Struct):
  raw: Dict = None
  seconds: int = 0
  ftp: float = 0.0
  member_ftp: float = 0.0

  @classmethod
  def create(cls, **kwargs):
    instance = WorkoutItem()
    if 'raw' in kwargs:
      instance.raw = kwargs['raw']
      instance.seconds = instance.raw['seconds']
      instance.ftp = instance.raw['ftpPercent']
      instance.member_ftp = instance.raw['memberFtpPercent']
    return instance
  
#------------------------------------------------------------------------------
class Interval(msgspec.Struct):
  raw: Dict = None
  start: int = 0
  end: int = 0
  name: str = ""
  power: float = 0.0
  power_max: float = 0.0
  power_max_when: int = 0
  power_min: float = -1.0
  power_min_when: int = 0
  ramp_direction: str = ""
  is_fake: bool = False
  test_interval: bool = False
  wd: List[WorkoutItem] = []
  interval_type: str = ""
  xml: str = ""

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

  def include(self, workout_item):
    if self.start <= workout_item.seconds / 1000 and self.end > workout_item.seconds / 1000:
      self.wd.append(workout_item)

  def ramp_analysis(self):
    for w in self.wd:
      if self.power_max < w.ftp:
        self.power_max = w.ftp
        self.power_max_when = w.seconds / 1000
      if self.power_min > w.ftp or self.power_min < 0:
        self.power_min = w.ftp
        self.power_min_when = w.seconds / 1000
    if self.power_min_when < self.power_max_when:
      self.ramp_direction = "up"
    else:
       self.ramp_direction = "down"

  def find_type(self):
    if self.wd[0].ftp == self.wd[-1].ftp:
      self.interval_type = "SteadyState"
    else:
      self.interval_type = "Ramp"
      self.ramp_analysis()
    #print(f"{self.interval_type:<15} ({self.start}-{self.end}): {int(self.wd[0].seconds / 1000)} : {self.wd[0].ftp}, {int(self.wd[-1].seconds / 1000)} : {self.wd[-1].ftp}")

  def to_xml(self):
    match self.interval_type:
      case "SteadyState":
        self.xml = f'<SteadyState Duration="{self.end - self.start}" Power="{self.power}"></SteadyState>'
      case "Ramp":
        if self.ramp_direction == "up":
          self.xml = f'<Ramp Duration="{self.end - self.start}" PowerLow="{self.power_min}" PowerHigh="{float(round(self.power_max))}"></Ramp>'
        else:
          self.xml = f'<Ramp Duration="{self.end - self.start}" PowerLow="{self.power_max}" PowerHigh="{float(round(self.power_min))}"></Ramp>'
      case _:
        self.xml = f'<unknown></unknown>'
    
#------------------------------------------------------------------------------
def find_intervals(blob):
  il = []
  for row in blob:
    i = Interval.create(raw=row)
    il.append(i)
  return il
    
#------------------------------------------------------------------------------
def find_workout_items(blob):
  wl = []
  for row in blob:
    w = WorkoutItem.create(raw=row)
    wl.append(w)
  return wl

#------------------------------------------------------------------------------
def assign_workout_items_to_intervals(intervals, workout_items):
  for i in intervals:
    for w in workout_items:
      i.include(w)
  return intervals

#------------------------------------------------------------------------------
def main():
  data = {}

  with open('./191639.json', 'r') as f:
    x = f.read()
    data = ujson.loads(x)

  interval_list = find_intervals(data['Workout']['intervalData'])
  workout_item_list = find_workout_items(data['Workout']['workoutData'])

  print(f"{len(interval_list)} intervals and {len(workout_item_list)} workout_items")

  interval_list = assign_workout_items_to_intervals(interval_list, workout_item_list)

  for i in interval_list:
      #print(f"{i.name} has {len(i.wd)} workout_items")
    i.find_type()
    i.to_xml()
    print(i.xml)

  # for i in interval_list:
  #   print(i)

  # for item in workout_item_list:
  #   print(item.raw['seconds'], item.seconds)

main()
